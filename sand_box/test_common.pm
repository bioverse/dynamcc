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
	my $Input; # declare new scalar 'Input'
	my @files = glob("*.txt"); # declare new array glob("*.txt") double quotes means interpretted string
	# glob(EXPR_1 EXPR_2) returns an array of filename expansions on the value of EXPR just as the standard
	# Unix shell /bin/csh would do. In scalar context, glob iterates through such filename expansions, 
	# returning undef when the list is exhausted.
	do {
		print "Select Data File\n"; # prints instructions to the user
		for (my $i=0;$i<@files;$i++) { # iterates through all the files in the array
			print "[$i] $files[$i] \n"; # prints the files along with the index
		}
		$Input = <STDIN>;	# takes input from user
	} while (! exists  $files[$Input]); # if the the stated index not a member of the list, loop back to beginning
	return $files[$Input]; # otherwise return the scalar (string) corresponding to the filename
}

#Load Amino Database
sub LoadData {
	my $Fname = GetDataFile(); # scalar = GetDataFile() output (path to user selected file)
	%Aminolist = (); # initialize hash 
	open (DATA,$Fname) or die "Error: $!"; # open file with DATA handler
	my (@title) = split(/\t/,<DATA>); # split first line of specified file and set as array 'title'
	for my $line (<DATA>) {		# iterate over each line (as scalar) in specified file
		$line =~ s/\r?\n$//; # line (scalar) is equivalent each line in file separated by \n or \r carriage return characters
		my (@d) = split(/\t/,$line); # split scalar (line) at tab and store resulting substrings in the array d
		my %c = ("Code" => $d[0],"Ratio" => $d[2],"InUse" => 0); # create a new hash c with key "Code" matched to value aa_code, "Ratio" matched to frequency, and "InUse" to null value		
		#say %c; # This prints the hash
		# say $Aminolist{$d[1]}; # This prints the memory address to the array (the value of each key in the hash table Aminolist)
		#say %Aminolist; # This prints the hash table Aminolist
		push(@{$Aminolist{$d[1]}}, \%c); # A lot of functionality in this line. 1) sets the key equal to $d[1] 2) Create an array and appends all hash tables as items in the array that match the key
	} # populating the aminolist (hash table) with keys = aa ($d[1]) and values are hash %c
	#Aminolist is a hash of arrays. Each array is also a hash. The keys are strings (scalars). The array is stored as a pointer? when you print, you get memory address of first variable 
	close DATA;
	# sort Desending
	foreach my $key (keys %Aminolist) { # iterate through all keys (aa) in aminolist (hash)
		#say "\n";
		@{$Aminolist{$key}} = sort {$$b{"Ratio"} <=> $$a{"Ratio"}}  @{$Aminolist{$key}}; # build an ordered array of aa. sort numerically descending
	}
	return $Fname;
}

#Load Replacment rules
sub LoadRules {
	%Rules =(); # instantiate empty hash
	say %Rules;
	open (RULES,"Rules.rul") or die "Can't Find Rules: $!"; 
	my (@title) = split(/\t/,<RULES>);	
	say @title;
	for my $line (<RULES>) {
		$line =~ s/\r?\n$//;		
		say $line;
		my @d = split(/\t/,$line);			
		say @d;
		say @d[1.. @d-1];
		say $d[0];
		say sort(@d[1.. @d-1]);
		$Rules{join ('',sort(@d[1.. @d-1]))} = $d[0]; #join takes an array and joins them together with a specified string between each element
		# Binary ".." is the range operator, which is really two different operators depending on the context. Here, it returns a list of values counting (up by ones) from the left to the right value. If the left value is greater than the right value, then it returns an empty list
	}
	say %Rules;
	say keys %Rules;
	say "\n\n\n";
	close RULES;	
}

sub BestList {
	my @list; # instantiate array structure
	for my $key (keys %Aminolist) { # iterate through keys in %Aminolist (with deleted aa's selected by user)
		if ((scalar @{$Aminolist{$key}})>1) { # if there are more than one codon for the amino acid (list length > 1)
			my $c = {"Ratio"=>0,"Code"=>""}; # new scalar (pointer to 'empty' hash).  
			#say %$c;
			for my $x (@{$Aminolist{$key}}) { # iterate through the hash items in the list
				#say %$x;
				#say $$x{"Ratio"};
				#say $$c{"Ratio"};
				if ($$x{"Ratio"}>$$c{"Ratio"} && $$x{"InUse"}==0) { # assign hash c key 'ratio' to highest value codon usage frequency
					$c=$x; # set the c hash equal to the x hash (the one with highest frequency usage)
				}
				#say $$x{"Ratio"};
				#say $$c{"Ratio"};
			}
			#say $$c{"Code"};
			#say %$c;
			#say "\n\n\n";
			if ($$c{"Code"} ne "") { # ne is perl string inequality (equivalent to != for numeric inequality).
				$$c{"InUse"}=1; # assign InUse key to 1
				push (@list,$$c{"Code"}); # append this codon to the array 'list'
			}
		}
		else { # if there are not more than one entry in the list (i.e. only one codon for that aa)
			my $c = ${$Aminolist{$key}}[0]; # new scalar (pointer) to hash 'c' that contains key-value pair identical to the single codon.
			if ($$c{"InUse"}==0) {
				$$c{"InUse"}=1; # set InUser to 1
				push(@list,$$c{"Code"}); # append this codon to the array 'list'
			}
		}
	}
	return @list; # retun the list of highest frequency usage codons.
}

sub Grouping {
	my ($list,$GroupBy) = @_; # $list is the pointer to array passed to Reduce. $GroupBy is an integer 0, 1, 2
	#say "From Grouping: ";
	#say "best list: ", @{$_[0]}; # $_[0] == $list
	#say "int is: ", $_[1]; # $_[1] == $GroupBy
	my %g=(); # instantiate empty hash
	##say "first: ", %g;
	for my $x (@{$list}) {	# dereference the array and iterate through it
		##say "second: ",  %g;
		#say "From Grouping loop 1: ";
		say "Codon is: ", $x; # each element in array
		my $y = substr($x,$GroupBy,1,''); # substr EXPR, OFFSET, LENGTH, REPLACEMENT. Extracts a substring out of EXPR and returns it. First character is at offset zero. If OFFSET is negative, starts that far back from the end of the string.
		#say "x is: ", $x;
		#say "y is: ", $y;
		##say "third: ", %g;
		#say "Position is: ", $y; # new string (depending on the value of $GroupBy, this gives the first, middle, or last character of string $x)
		my $InRules=0; # instantiate new scalar
		##say "forth: ", %g;
		#say "Rules hash is: ", %Rules;
		foreach my $l (keys %Rules) { # iterate over keys in %Rules
			##say "fifth: ", %g;
			#say "l is: ", $l;
			#say "From Grouping loop 2: ";
			#say "Rules key is: ", $l; # keys from %Rules
			#say "Rules value is: ", $Rules{$l}; # values from %Rules
			if ($Rules{$l} eq $y) { # if key == $y (sliced string)
				##say "sixth: ", %g;
				##say "Rules{l} is: ", $Rules{$l};
				#say "REALLY WEIRD EXPR: ";
				#say "split rules key: ", split(//,$l);
				push (@{$g{$x}},split(//,$l)); # the key of the rules dict is being pushed to an array of 
				#say "seventh: ", %g;
				#say "unknown hash is: ", %g;
				foreach my $k (keys %g) {
					print "$k:  @{$g{$k}}\n";
				}
				$InRules = 1;
			}
		}
		#say "InRules: ", $InRules;
		#say !$InRules;
		push(@{$g{$x}},$y) if (!$InRules); # 1 is true. g = {x: [y]}. If the key is already in hash, then append the new y to the array
		##say "eigth: ", %g;
		foreach my $k (keys %g) {
			print "$k:  @{$g{$k}}\n";	
		}
		#say @{$g{$x}};
		#say "End Grouping loop 1: ";
		#say @{$g{$x}};
		#say $y;
		
	}
	#say %g;
	for (keys %g) {
		#say "new for loop";
		#say @{$g{$_}};
		$g{$_} = join('',sort(@{$g{$_}})); # sort the values of g = {x: [y]} alphabetically and join them into one string at the same time. now saved as scalar
	}
	for my $k (keys %g) {
		print "$k:  $g{$k}\n";	
	}	
	#say %g;
	return %g;	
}

sub ListFromGroup {
	#say "from ListFromGroup: ";
	my ($g,$index) = @_;
	my @list;	
	#say %{$g};
	for my $x  (keys %{$g})  { # iterate through dereferenced hash. keys are x
		my $v = $x;		# v is now equal to x (the hash key)					
		#say $g;
		#say $x;
		#say $g->{$x};
		#say length($g->{$x}); # "->" is an infix dereference operator, just as in C and C++. in this case, fetching the $x member (getting the value for the key x) of the $g object
		if (length($g->{$x}) >1) { # if the value of each key is > 1
			#say substr($v,$index,0);
			#say $Rules{$g->{$x}};
			substr($v,$index,0)=$Rules{$g->{$x}}; # take a substring of the original v and save it in v. In the case that this is the first_position, delete the first position and replace with the corresponding letter from the rules hash
		}
		else {
			 substr($v,$index,0)=$g->{$x} ;				
		}
		push(@list,$v); # populate this list with the single letter code (either the original single letter or the single letter from the rules)
	}
	#say @list;
	return @list;	
}

sub Reduce {
	my @a = @_; # @_ is the list that was passed as argument. capturing this as @a (local array) ## @_: within a subroutine the array @_ contains the parameters passed to that subroutine
	#say "from Reduce: ";
	#say $_[0]; # the first index item in the array (which was passed to this function)
	#say @a;
	#print "\n";
	for my $i (0..2) {	# iterate through integers 0, 1, 2	
		my %g = Grouping(\@a,$i); # pass @a by reference along with integers 0-2 to the Grouping sub-routine. Capture result in hash %g
		@a = ListFromGroup(\%g,$i);	#pass %g by reference along with integers 0-2 to the ListFromGroup subroutine. Capture result in array @a	
	}
	return @a;
}

sub FindMinList {
	#say "from FindMinList: ";
	#say "best_list is: ", @_;
	my @a = Reduce(@_); # Pass the list that was passed to FindMinList to Reduce (BestList). capture result in @a 
	#say "reduced is: ", @a;
	if (join('',@a) ne join('',@_)) { # if the list passed to FindMinList (BestList) is != to the result of Reduce
		FindMinList(@a); # then pass the list back to itself (i.e. back to Reduce for another trial)
	}
	return @a;	# when the two lists are equal then return the final list
}

sub NextBestList { # The best list (@wlist) was passed by reference to this script
	say 'input list: ';
	say @{ $_[0] };
	my $list = shift; # here @wlist is dereferenced by shift, and the reference to the resulting array is captured in $list	
	say 'shift output reference: ';
	say $list;
	say 'shift output dereferenced: ';
	say @$list;
	my $c = {"Ratio"=>0,"Code"=>""};
	say %$c; 
	for my $amino (keys %Aminolist) {
		say $amino;
		#say @{$Aminolist{$amino}};
		for my $x (@{$Aminolist{$amino}}) {
			say %$x;
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


LoadData();
LoadRules();

my @wlist = BestList();
print @wlist;
print "\n";
print "List (" .(scalar @wlist) .")\n";
print join(", ",@wlist)."\n";
my @s = FindMinList(@wlist); # pass best list to FindMinList. Capture result in @a
print @s;
print "\n";

say 'best list: ';
say @wlist;

print "NextBestList: " . NextBestList(\@wlist) # 0 is false and 1 is true


#print "Available amino acids (count: ". scalar (keys %Aminolist)." ,X represents stop codons)\n";
#print join( ',', keys %Aminolist )."\n";
#print "Choose amino acids to remove:\n";
#my  $a =  <STDIN>;
#print $a;
#chomp $a; # chomp removes any trailing string that corresponds to the current value of $/. It returns the total number of characters removed from all its arguments. By default $/ is set to newline character
#print $a;

#foreach my $key (keys %Aminolist) {
#	say "The key is: " . $key;
#	say "The value is: " . $Aminolist{$key};
#	my $array_ref = $Aminolist{$key};
#	print "The de-referenced value is: ";
#	say @$array_ref;
#	print "The de-referenced hashes are: ";
#	foreach (@$array_ref) {
#		my $hash_ref = $_;
#		print %$hash_ref;
#		print " ";
#	}
#	print "\n";
#	say @{$Aminolist{$key}};
#}

#say %Aminolist;

#LoadRules();














