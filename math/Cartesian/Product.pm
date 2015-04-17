=head1 Name

Math::Cartesian::Product - Generate the cartesian product of zero or more lists.

=head1 Synopsis

 use Math::Cartesian::Product;

 cartesian {print "@_\n"} [qw(a b c)], [1..2];

 #  a 1
 #  a 2
 #  b 1
 #  b 2
 #  c 1
 #  c 2

 cartesian {print "@_\n"} ([0..1]) x 8;

 #  0 0 0 0 0 0 0 0
 #  0 0 0 0 0 0 0 1
 #  0 0 0 0 0 0 1 0
 #  ...
 #  1 1 1 1 1 1 1 0
 #  1 1 1 1 1 1 1 1

=cut


package Math::Cartesian::Product;

use Carp;
use strict;

sub cartesian(&@)
 {my $s = shift;       # Subroutine to call to process each element of the product

  my @C = @_;          # Lists to be multiplied
  my @c = ();          # Current element of cartesian product
  my @P = ();          # Cartesian product
  my $n = 0;           # Number of elements in product

  return 0 if @C == 0; # Empty product

  @C == grep {ref eq 'ARRAY'} @C or croak("Arrays of things required by cartesian");

# Generate each cartesian product when there are no prior cartesian products.

  my $p; $p = sub  
   {if (@c < @C) 
     {for(@{$C[@c]})
       {push @c, $_;
        &$p();
        pop @c;
       }
     }
    else 
     {my $p = [@c];
      push @P, bless $p if &$s(@$p);
     }
   };

# Generate each cartesian product allowing for prior cartesian products.

  my $q; $q = sub  
   {if (@c < @C) 
     {for(@{$C[@c]})
       {push @c, $_;
        &$q();
        pop @c;
       }
     }
    else 
     {my $p = [map {ref eq __PACKAGE__ ? @$_ : $_} @c];
      push @P, bless $p if &$s(@$p);
     }
   };

# Determine optimal method of forming cartesian products for this call

  if (grep {grep {ref eq __PACKAGE__} @$_} @C)
   {&$q
   }
  else
   {&$p
   }

  @P
 }

# Export details
 
require 5;
require Exporter;

use vars qw(@ISA @EXPORT $VERSION);

@ISA     = qw(Exporter);
@EXPORT  = qw(cartesian);
$VERSION = '1.006'; # Saturday 18 April 2009

=head1 Description

Generate the cartesian product of zero or more lists.

Given two lists, say: [a,b] and [1,2,3], the cartesian product is the
set of all ordered pairs:

 (a,1), (a,2), (a,3), (b,1), (b,2), (b,3)

which select their first element from all the possibilities listed in
the first list, and select their second element from all the
possibilities in the second list.

The idea can be generalized to n-tuples selected from n lists. In
particular, the cartesian product of zero lists is the empty set, as is
the cartesian product of any set of lists which contain a list with no
elements.

C<cartesian()> takes the following parameters:

1. A block of code to process each n-tuple. this code should return true
if the current n-tuple should be included in the returned value of the
C<cartesian()> function, otherwise false.

2. Zero or more lists.

C<cartesian()> returns an array of references to all the n-tuples
selected by the code block supplied as parameter 1. 

C<cartesian()> croaks if you try to form the cartesian product of
something other than lists of things.

The cartesian product of lists A,B,C is associative, that is: 

  (A X B) X C = A X (B X C)

C<cartesian()> respects associativity by allowing you to include a
cartesian product produced by an earlier call to C<cartesian()> in the
set of lists whose cartesian product is to be formed, at the cost of a
performance penalty if this option is chosen.

  use Math::Cartesian::Product;
 
  my $a = [qw(a b)];
  my $b = [cartesian {1} $a, $a];
  cartesian {print "@_\n"} $b, $b;

  # a a a a
  # a a a b       
  # a a b a 
  # ...
 

C<cartesian()> is easy to use and fast. It is written in 100% Pure Perl.


=head1 Export

The C<cartesian()> function is exported.

=head1 Installation

Standard Module::Build process for building and installing modules:

  perl Build.PL
  ./Build
  ./Build test
  ./Build install

Or, if you're on a platform (like DOS or Windows) that doesn't require
the "./" notation, you can do this:

  perl Build.PL
  Build
  Build test
  Build install

=head1 Author

PhilipRBrenan@handybackup.com

http://www.handybackup.com

=head1 See Also

=over

=item L<Math::Disarrange::List>

=item L<Math::Permute::List>

=item L<Math::Subsets::List>

=item L<Math::Transform::List>

=back

=head1 Copyright

Copyright (c) 2009 Philip R Brenan.

This module is free software. It may be used, redistributed and/or
modified under the same terms as Perl itself.

=cut
