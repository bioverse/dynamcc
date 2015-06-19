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
say $|++;
say $|++;
say $|++;

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





















