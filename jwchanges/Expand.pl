#!/usr/bin/perl

use 5.010;
use strict;
use warnings;

use Common;

our %Aminolist;
our %Rules;

LoadData();
LoadRules();

print "Enter Codons to expand:\n";
my $Input = <STDIN>;
chomp $Input;
my @list = map {uc($_)}  split(/,/,$Input);
my @codons;
foreach my $c (@list) {
	my @x = ExpandCodon($c);
	print "$c -> ". join(',',@x) ."\n";
	push(@codons,@x);
}

print "Acid\tCode\tUsage\tRank\n";print join("\t" ,GetCodonData($_) ),"\n" foreach (@codons);



