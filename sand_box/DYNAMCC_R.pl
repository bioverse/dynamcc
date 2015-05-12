#!/usr/bin/perl -w

use 5.010;
use strict;
use warnings;
use Data::Dumper;
use Common;
use diagnostics;

our  %Aminolist;
our %Rules;

LoadData();
LoadRules();



print "Available amino acids (count: ". scalar (keys %Aminolist)." ,X represents stop codons)\n";
print join( ',', keys %Aminolist )."\n";
print "Choose amino acids to remove:\n";
my  $a =  <STDIN>; # collect user input
chomp $a ; # remove carriage return at end (\n)
my @input =map {uc($_)}  split(/,/,$a); # split comma-separated values of user input into list. then iterate through the list and convert entries to upper case. save result in array @input
delete @Aminolist {@input}; # delete all key-value pairs corresponding to the amino acids the user selected for exclusion

my @wlist = BestList();


do {
	print "List (" .(scalar @wlist) .")\n";
	print join(", ",@wlist)."\n";
	my @s = FindMinList(@wlist);
	print "Reduce List (" .(scalar @s) .")\n";
	print join(", ",@s)."\n";	
	
}	while (NextBestList(\@wlist));




sub BestList {
	my @list;
	for my $key (keys %Aminolist) {
		if ((scalar @{$Aminolist{$key}})>1) {
			my $c = {"Ratio"=>0,"Code"=>""};
			for my $x (@{$Aminolist{$key}}) {
				if ($$x{"Ratio"}>$$c{"Ratio"} && $$x{"InUse"}==0) {
					$c=$x;
				}
			}
			if ($$c{"Code"} ne "") {
				$$c{"InUse"}=1;
				push (@list,$$c{"Code"});
			}
		}
		else {
			my $c = ${$Aminolist{$key}}[0];
			if ($$c{"InUse"}==0) {
				$$c{"InUse"}=1;
				push(@list,$$c{"Code"});
			}
		}
	}
	return @list;
}


#return the next best list,adding the more highly runked codon that isnt used yet
sub NextBestList {
	my $list = shift;	
	my $c = {"Ratio"=>0,"Code"=>""};
	for my $amino (keys %Aminolist) {
		for my $x (@{$Aminolist{$amino}}) {
			if ($x->{"Ratio"}>$c->{"Ratio"} && $x->{"InUse"}==0) {
				$c=$x;
			}
		}
	}
	if ($c->{"Code"} ne "") {
		$c->{"InUse"}=1;
		push (@$list,$c->{"Code"});
		
		return 1;
	}
	else {
		return 0;
	}	
	
}



