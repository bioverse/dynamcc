use feature ':5.16';
say "Hello, world!";
print "This is a single statement";
print "Look" , "a", "list";

# Two basic data types in perl. numbers and strings
# numbers are as expected
# strings are interpretted if enclosed with double quotes ("\n" will give
# return character) or literal if enclosed with single quotes ('\n' will give 
# backslash and n characters)

# There are three variable types in perl. scalars, arrays, and hashes.
# scalars analogous to things
# arrays analogous to lists
# hashes analogous to dictionaries
# all variable names consist of a punctuation character, a letter or
# underscore, and one or more alphanumeric characters or underscores.

# Scalars are single things
# Importantly you don't need to specify whether a scalar is a number or a
# string. Perl automatically converts between the two data types.
# keyword "my" declares a new variable. scalars begin with $ symbol
my $i = 5;
my $pie_flavor = 'apple';
my $constitution1776 = "We the People, etc.";

# If you use a double-quoted string, perl will insert the value of any scalar
# variables you name in the string. Useful for filling in strings on the fly
my $count_report = "There are $i apples.";
print "The report is: $count_report\n";

# can use standard mathematical operators
my $a = 5;
my $b = $a + 10;
my $c = $b * 10;
$a = $a - 1;
$a++;
$a += 10;
$a /= 2;
my $d = "4";
my $e = $d + "5";
my $f = $d . "5";
print $a . "\n";
print $e . "\n";
print $f . "\n";

# Arrays are lists of scalars. Array names begin with @ symbol
# arrays are defined by listing their contents in parentheses separated 
# by commas.
my @lotto_numbers = (1, 2, 3, 4, 5, 6);
my @months = ("July", "August", "September", "October");
say @months;

# To retrieve the elements of an array by index, replace the @ sign with a 
# $ sign followed by the index position of the element you want.
print $months[1] . "\n";

# Arrays are mutable
$months[1] = "December";
print $months[1] . "\n";

# appending to an array is automatic
$months[4] = "November";
$months[6] = "January";
print $months[4] . " " . $months[5] . "\n";

#you can find the length of an array by assigning it to a scalar
my $length = @months;
say $length

# hashes are dictionaries. They contain key, value pairs. Keys can have 
# only one value. Name of a hash begins with % sign and are specified as
# comma separated key and value
my %hash = ("July" => 31, "August" => 31, "September" => 30);
say %hash;
print %hash;

# any value can be retrieved from a hash by referring to is as a scalar
say $hash{July};

# and key value pairs can be added to a hash using
$hash{February} = 28;
say $hash{February};

# to see what keys are in a hash, use the keys function with the name of the 
# hash. The keys will not be printed out in any particular order. 
say keys %hash;
















