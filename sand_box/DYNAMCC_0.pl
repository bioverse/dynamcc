#!/usr/bin/perl

use 5.010;
use strict;
use warnings;

use Data::Dumper;
use Time::HiRes qw/ time/;
use List::Util 'min';
use Common;
use diagnostics;
use threads;
use Math::Combinatorics;

$|++;

our %Aminolist;
our %Rules;

LoadData();
LoadRules();


my @whirley=("-", "\\", "|", "/");

print "Available amino acids (count: ". scalar (keys %Aminolist).")\n";
print join( ',', keys %Aminolist )."\n";
print "Choose amino acids to remove\n";
my  $Input =  <STDIN>;
chomp $Input ;
my @input =map {uc($_)}  split(/,/,$Input);
delete @Aminolist {@input};
my $Total = 1;
$Total*=scalar @{$Aminolist{$_}} foreach (keys %Aminolist);
print "Total Combinations: $Total\n";


do {
	print "Remove codon by [R]ank or [U]sage? ";
	$Input = <STDIN>;
	chomp $Input;
} while ($Input !~ /^[RU]$/i);

if (uc($Input) eq 'U') {
	
	# Remove codont by usage
	print "Set usage ratio threshold: (must be below: " . FindMinimumThreshold() ." )\n";
	$Input = <STDIN>;
	chomp $Input;
	RemoveLowCodons($Input);
}
else {

	#Remove Codons By Rank

	print "Set codon rank threshold:  ";
	$Input = <STDIN>;
	chomp $Input;
	RemoveCodonsByRank($Input);
}


my $NumOfThreads =3;
my $Redun=0;

my (@z,@l);
my $CodonCount = 0;
$Total = 1;
$Total*=scalar @{$Aminolist{$_}},
	$CodonCount+=scalar @{$Aminolist{$_}},
	push(@z,0),
	push(@l,scalar @{$Aminolist{$_}})  foreach (keys %Aminolist);

print "Total combinations after removing low usage codons = $Total\n";

print "Set redundency (0 for no redundency at all):  ";
$Input = <STDIN>;
chomp $Input;
$Redun = $Input;


print "Total Combinations including redundency = ". $Total * ($CodonCount - (scalar keys %Aminolist))**$Redun ."\n";


print "Number of thread to run (default 1):";
$Input = <STDIN>;
chomp $Input;
$NumOfThreads = $Input if ($Input ne "");


my $GlobalStart = time;

#Start Thread

my @threads;
for (my $i=0;$i<$NumOfThreads;$i++) {
	my $th = threads->new(\&DoWork,$i);
	push( @threads,$th);
}



#collect resouts from threads

my @res;
push(@res,$_->join())  foreach (@threads);


#find the best list from all threads

my $best;
foreach my $x (@res) {
	if (! defined $best) {
		$best = $x;
	} else {
		if (($$x{"ReduceSize"}<$$best{"ReduceSize"}) || ($$x{"ReduceSize"}==$$best{"ReduceSize"} && $$x{"Ratio"} > $$best{"Ratio"})) {
			$best = $x;
		}
	}
}


#Extract final Codon List

my @Final = @{${$$best{"BestList"}}[0]};

print "\nChoosen List:\n";
print "AA\tCodon\tUsage\tRank\n";


print join("\t",GetCodonData($_)) ."\n" foreach (@Final);

print "Compressed codons:\n";
print "$_  -> " . join(',',ExpandCodon($_)) . "\n" foreach (Reduce(@Final)) ;


print "Finished! Total time: ". int(time-$GlobalStart)  . " sec \n";









##*********************Subs************************

sub DoWork {	
	my $idx = shift;
	print "Thread $idx starting \n";
	my ($BestList,$BestReduceSize,$BestIndex,$BestRatio,@BestZ);
	$BestReduceSize=20;
	$BestRatio=0;
	$BestIndex=0;
	my $StartTime = time;
	my $t=0;
	my $stop=0;
	do {
		if (($t % $NumOfThreads ) == $idx) {
			#Create List , reduce and check agains the current best
			
			my @x = CreateListFromIndex(@z);	
			
			if ($Redun!=0) {
				my @RedunIndeces = GetRestOfIndeces(@z);				
				my $comb = Math::Combinatorics->new(count => $Redun ,data=>[@RedunIndeces]);
				while (my @rz = $comb->next_combination) {
					my @y = CreateListFromIndex(@z);
					foreach (@rz) {
						my @tt = split(//,$_);						
						my @cl = @{$Aminolist{$tt[0]}};
						my $c = $cl[$tt[1]];
						push (@{$y[0]},$$c{"Code"});
						push (@{$y[1]},$$c{"Ratio"});
					}								
					my @r = Reduce(@{$y[0]});
					my $ratio=0;
					$ratio+= $_ for (@{$y[1]});
					if (((scalar @r) < $BestReduceSize) || ((scalar @r) == $BestReduceSize) && ($ratio > $BestRatio) ) {				
						$BestList = \@y;
						$BestReduceSize = (scalar @r);
						$BestIndex = $t;
						$BestRatio = $ratio;
						@BestZ = @z;
					}						
				}
			}	else {		
				my @r = Reduce(@{$x[0]});
				my $ratio=0;
				$ratio+= $_ for (@{$x[1]});
				if (((scalar @r) < $BestReduceSize) || ((scalar @r) == $BestReduceSize) && ($ratio > $BestRatio) ) {				
					$BestList = \@x;
					$BestReduceSize = (scalar @r);
					$BestIndex = $t;
					$BestRatio = $ratio;
					@BestZ = @z;
				}	
			}
		}
		

		#print a report evey 1000 iter
		
		if (($t % 10000)==0) {
			my $EndTime = time;
			print "thread $idx finished " .int(100* $t/$Total) ." % @ " . int((time -  $GlobalStart)* 1000) . " ms Best Size: $BestReduceSize , Best Index: $BestIndex, Best Ratio: $BestRatio\n";
			$StartTime = $EndTime;
			#print "Working: " . $whirley[$Spinner];
		}		
							

		
		# advance the index
		
		my $i=0;
		while ((!$stop) && (($z[$i] = ($z[$i]+1) % $l[$i]))==0) {		
			$stop =1 if (++$i>$#z)
		}
		
		$t++;
		
	} while (!$stop);
	my %c = ("BestList" => $BestList, "ReduceSize" => $BestReduceSize,"Ratio" => $BestRatio);
	return \%c;
}






sub CreateListFromIndex {
	my @z = @_;
	my (@codes,@Ratios);
	my $i=0;
	foreach my $key (keys %Aminolist) {
		my @t = @{$Aminolist{$key}};
		push (@codes, $t[$z[$i]]->{"Code"});
		push (@Ratios, $t[$z[$i]]->{"Ratio"});
		$i++;
	}
	my @res =  (\@codes,\@Ratios);
		
	
	
	return  @res;
	
}


sub GetRestOfIndeces {
	my @z = @_;
	my $i=0;
	my @res;
	foreach my $a (keys %Aminolist) {
		my @t = @{$Aminolist{$a}};
		if (@t>1) {
			my @k = (0..$#t);			
			splice @k,$z[$i],1;		
			push (@res, map {$a.$_} @k);
		}
		$i++;
	}
	return @res;
}


sub RemoveLowCodons {
	my $Threshold = shift;
	foreach my $key (keys %Aminolist) {
		my $t = \@{$Aminolist{$key}};
		my $index=0;
		while ($index < (scalar @$t)) {
			if (${$t}[$index]->{"Ratio"} <=$Threshold) {				
				splice @{$t},$index,1;
			} else {
				$index++;
			}
		}
	}
}

sub RemoveCodonsByRank {
	my $Rank = shift;
	foreach my $key (keys %Aminolist) {
		if (@{$Aminolist{$key}} > $Rank) {
			splice(@{$Aminolist{$key}} ,$Rank);
		}
	}
}

sub FindMinimumThreshold {
	my @x;
	foreach my $key (keys %Aminolist) {
		my $t = \@{$Aminolist{$key}};
		my $y=0;
		foreach my $c (@$t) {
			if ($c->{"Ratio"}> $y) {
				$y = $c->{"Ratio"};
			}
		}
		push (@x,$y);
		
	}	
	return min(@x);
}


