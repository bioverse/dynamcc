#package Common;



use 5.010;
use strict;
use warnings;
use diagnostics;

our $VERSION = '0.01';

our %Aminolist;
our %Rules;
1;
# select data file from current directory
sub GetDataFile {
	my $Input;
	my @files = glob("*.txt");
	do {
		#print "Select Data File\n";
		#for (my $i=0;$i<@files;$i++) {
		#	print "[$i] $files[$i] \n";
		#}
		$Input = <STDIN>;	
	} while (! exists  $files[$Input]);
	return $files[$Input];

}

#Load Amino Database
sub LoadData {
	my $Fname = GetDataFile();	
	%Aminolist = ();
	open (DATA,$Fname) or die "Error: $!";
	my (@title) = split(/\t/,<DATA>);		
	for my $line (<DATA>) {		
		$line =~ s/\r?\n$//;
		my (@d) = split(/\t/,$line);
		my %c = ("Code" => $d[0],"Ratio" => $d[2],"InUse" => 0);		
		push(@{$Aminolist{$d[1]}}, \%c);
	} 
	close DATA;
	# sort Desending
	foreach my $key (keys %Aminolist) {
		@{$Aminolist{$key}} = sort {$$b{"Ratio"} <=> $$a{"Ratio"}}  @{$Aminolist{$key}};
	}	
	return $Fname;
}

#Load Replacment rules
sub LoadRules {
	%Rules =();
	open (RULES,"Rules.rul") or die "Can't Find Rules: $!";
	my (@title) = split(/\t/,<RULES>);	
	for my $line (<RULES>) {
		$line =~ s/\r?\n$//;		
		my @d = split(/\t/,$line);			
		$Rules{join ('',sort(@d[1.. @d-1]))} = $d[0];
	}
	close RULES;	
}

#group codon that only differ in the $GroupBy letter, return a hush 
sub Grouping {
	my ($list,$GroupBy) = @_;
	my %g=();
	for my $x (@{$list}) {		
		my $y = substr($x,$GroupBy,1,'');	
		my $InRules=0;
		foreach my $l (keys %Rules) {
			if ($Rules{$l} eq $y) {
				push (@{$g{$x}},split(//,$l));
				$InRules = 1;
			}
		}
		push(@{$g{$x}},$y) if (!$InRules);
		
	}
	for (keys %g) {
		$g{$_} = join('',sort(@{$g{$_}}));
	}	
	return %g;
	
	
}



#using the groups created by grouping construct a list using the replecment rules
sub ListFromGroup {
	my ($g,$index) = @_;
	my @list;	
	for my $x  (keys %{$g})  {
		my $v = $x;							
		if (length($g->{$x}) >1) {
			substr($v,$index,0)=$Rules{$g->{$x}};
		}
		else {
			 substr($v,$index,0)=$g->{$x} ;				
		}
		push(@list,$v);
	}
	return @list;	
}



# putting it togather: group by letter then make reduce list, then by the next letter...
sub Reduce {
	my @a = @_;
	for my $i (0..2) {		
		my %g = Grouping(\@a,$i);		
		@a = ListFromGroup(\%g,$i);		
	}
	return @a;
}

# recurse on the reduce funtion untill there is no change...
sub FindMinList {
	my @a = Reduce(@_);
	if (join('',@a) ne join('',@_)) {
		FindMinList(@a);
	}
	return @a;
		
}


sub ExpandCodon {	
	my $c = shift;
	my @letters  = split(//,$c);
	for (my $i=0;$i<scalar @letters;$i++) {
		foreach my $key  (keys %Rules) {
			if ($Rules{$key} eq $letters[$i]) {		
				my  @res;
				foreach my $x (split(//,$key)) {
					my $t = $c;
					substr($t,$i,1) = $x;
					push (@res,$t);
				}				
				return map (ExpandCodon($_),@res);
			}
		}
		
	}
	return ($c);
}


sub CodeToAcid {
	my $code = shift;
	foreach my $key (keys %Aminolist) {
		foreach my $x (@{$Aminolist{$key}}) {
			return $key if ($$x{"Code"} eq $code);
			
		}
		
	}
}

sub GetCodonData {
	my $c = shift;	
	foreach my $amino (keys %Aminolist) {
		my @x = @{$Aminolist{$amino}};
		for (my $i=0;$i<@x;$i++) {
			if (${$x[$i]}{"Code"} eq $c) {
				return ($amino,$c,${$x[$i]}{"Ratio"},$i+1);		
			}		
		}
	}
}


sub GetAllCodnos {
	my @res;	
	foreach my $a (keys %Aminolist) {
		foreach my $c (@{$Aminolist{$a}}) {
			push (@res,[$$c{"Code"},$$c{"Ratio"}]);			
		} 
	}
	return @res;
}
