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
#say $Total;
#say %Aminolist;
#foreach my $key (keys %Aminolist) {
#	say 'key: ' . $key;
#	say 'value: ';
#	say @{$Aminolist{$key}};
#	say scalar @{$Aminolist{$key}};
#	#say scalar @{$Aminolist{$_}};
#	foreach my $hash (@{$Aminolist{$key}}) {
#		say 'index: ';
#		say %$hash;
#	}
#}

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

my (@z,@l); # instantiate two new lists
my $CodonCount = 0; # initiate CodonCount to 0
$Total = 1; # initiate Total to 1



#say $Total;
#say %Aminolist;
#foreach my $key (keys %Aminolist) {
#	say 'key: ' . $key;
#	say 'value: ';
#	say @{$Aminolist{$key}};
#	say scalar @{$Aminolist{$key}};
#	#say scalar @{$Aminolist{$_}};
#	foreach my $hash (@{$Aminolist{$key}}) {
#		say 'index: ';
#		say %$hash;
#	}
#}

$Total*=scalar @{$Aminolist{$_}}, # compute n! for remaining codons
	$CodonCount+=scalar @{$Aminolist{$_}}, # compute sum of remaining codons
	push(@z,0),
	push(@l,scalar @{$Aminolist{$_}})  foreach (keys %Aminolist);

#say $Total;
#say @z;
#say $CodonCount;
#say @l;


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

my @threads; # instantiate empty array 'threads'
for (my $i=0;$i<$NumOfThreads;$i++) { # iterate through the number of threads specified
	my $th = threads->new(\&DoWork,$i); # start a worker for each thread specified
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
		#say $t;
		#say $NumOfThreads;
		#say $idx;
		#say $t % $NumOfThreads;
		#say $idx;
		if (($t % $NumOfThreads ) == $idx) {
			#Create List , reduce and check agains the current best
			#say 'running';
			#say @z;
			my @x = CreateListFromIndex(@z); # this returns a list that contains two references. the first is a reference to the list that contains the codons and the second is a list that contains the frequencies
			#say @{@x[0]};
			#say @{@x[1]};

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
				#say @r;
				my $ratio=0;
				$ratio+= $_ for (@{$x[1]});
				#say $ratio;
				#say scalar @r;
				#say $BestReduceSize;
				#say $ratio;
				#say $BestRatio;
				if (((scalar @r) < $BestReduceSize) || ((scalar @r) == $BestReduceSize) && ($ratio > $BestRatio) ) {				
					#say 'true';
					$BestList = \@x;
					#say $BestList;
					$BestReduceSize = (scalar @r);
					#say $BestReduceSize;
					$BestIndex = $t;
					#say $BestIndex;
					$BestRatio = $ratio;
					#say $BestRatio;
					@BestZ = @z;
					#say @BestZ;
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
		#say $z[$i];
		#say @z;
		#say ($z[$i]+1);
		#say @z;
		#say 'here';
		#say (($z[$i] = ($z[$i]+1) % $l[$i]));
		#say 'first i is';
		#say $i;
		#say @z;
		while ((!$stop) && (($z[$i] = ($z[$i]+1) % $l[$i]))==0) {	# $l is reference to @l which is the array that holds the number of codons for each amino acid remaining after trimming	
			#say 'hello';
			#++$i;
			#say 'third i is';
			#say $i;
			$stop =1 if (++$i>$#z) # asking of the current index i is greater than the last index of the array
		}
		#say 'second i is';
		#say $i;
		#say @z;
		$t++;
		
	} while (!$stop);
	my %c = ("BestList" => $BestList, "ReduceSize" => $BestReduceSize,"Ratio" => $BestRatio);
	#say %c;

	return \%c;
}


sub CreateListFromIndex {
	#say 'from CreateListFromIndex';
	my @z = @_;
	#say @z;
	my (@codes,@Ratios);
	my $i=0;
	foreach my $key (keys %Aminolist) {
		#say $key;
		my @t = @{$Aminolist{$key}};
		#say @t; 
		#say %{$t[$z[$i]]};
		push (@codes, $t[$z[$i]]->{"Code"});
		#say @codes;
		push (@Ratios, $t[$z[$i]]->{"Ratio"});
		#say @Ratios;
		$i++;
	}
	#say scalar @codes;
	#say scalar @Ratios;
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
		#say \@{$Aminolist{$key}};
		#say @{$Aminolist{$key}};
		#say 'key is: ';
		#say $key;
		my $t = \@{$Aminolist{$key}}; # $t is the reference for the hash array (values in %Aminolist hash)
		my $y=0;
		foreach my $c (@$t) { # de-reference each array and iterate through the hashes
			#say 'y is: ' . $y;
			if ($c->{"Ratio"}> $y) { # de-reference eash hash and test if the value of 'Ratio' > current value of $y
				$y = $c->{"Ratio"};
				#say 'y is: ' . $y;
			}
		}
		push (@x,$y); # make a list of the highest 'Ratio' values for each codon
		
	}	
	#say @x;
	return min(@x);
}





















