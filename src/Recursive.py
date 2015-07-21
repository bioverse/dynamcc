__author__ = 'jdwinkler'

class Recursive:

    def __init__(self, codon_list, rules_dict, inverse_rule_dict):

        self.codon_list = codon_list
        self.rules_dict = rules_dict
        self.inverse_dict = inverse_rule_dict
        self.reduced = []
        self.my_dict = {}

    def FindMinList(self, list, pos_cache):
        """Recursive algorithm in which the self.codon_list is a list of the
        most frequently used codons for amino acids that the user wants to
        include for compression. self.codon is initi1ally the list passed in
        when instantiating the Recursive class. This list is copied to the
        variable temp for downstream comparison. Then, Reduce() is called and
        the resulting list is captured in the variable reduced_list. The two
        lists are compared and if not equal, FindMinList recurses by calling
        itself and passing the new list (captured from Reduce()) in as the
        argument. When temp and reduced_list are equal, the method returns the
        updated self.codon_list (this member variable is modified in Reduce())

        Parameters
        ----------
        list: list
            This is a codon list, it can correspond to any codon list such as
            the most frequently used codons staged for compression or the
            semi-compressed list resulting from Reduce()

        Returns
        -------
        self.codon_list: list
            The updated codon list. This list represents the most compressed
            set of codons remaining after running the recursive algorithm once
            through. (need better description of this)

        Examples
        --------
        >>> recursive = Recursive(best_list, rules_dict)
        >>> recursive.FindMinList(best_list)
        """

        temp = self.codon_list
        reduced_list = self.Reduce(pos_cache)
        if temp != reduced_list:
            self.FindMinList(reduced_list, pos_cache)
        return self.codon_list

    def Reduce(self, pos_cache):
        """Iterate through each position in the codon. At each position,
        capture the result of Grouping(int) in self.my_dict. Pass this dict to
        ListFromGroup(dict, int) and capture the result in self.codon_list. Return
        self.codon_list after iterating through each position in the codon.

        Parameters
        ----------
        none

        Returns
        -------
        self.codon_list: list
            The updated codon list. This list represents the most compressed
            set of codons remaining after running Grouping(int) and
            ListFromGroup(dict, int) for all three codon positions

        Examples
        --------
        reduced_list = self.Reduce()

        """
        for i in range(3):
            self.my_dict = self.Grouping(i, self.codon_list, pos_cache)
            self.codon_list = self.ListFromGroup(self.my_dict, i)
        return self.codon_list

    def Grouping(self, int, codon_list, position_cache):

        array_slice = {0, 1, 2}
        idx = list(array_slice - {int})

        temp_dict = {}
        my_dict = {}

        for codon in codon_list:

            position = codon[int]

            if(position_cache != None):

                try:

                    remainder = position_cache[codon][int]

                except KeyError:
                    remainder = ''
                    for p in idx:
                        remainder = remainder + codon[p]
                    position_cache[codon][int] = remainder
            else:
                remainder = ''
                for p in idx:
                    remainder = remainder + codon[p]

            if (remainder not in temp_dict):
                temp_dict[remainder] = set()

            if (position in self.inverse_dict):
                # print remainder, position, self.inverse_dict[position].split(), 'split'
                # for nuc_pos in list(self.inverse_dict[position]):
                temp_dict[remainder].update(self.inverse_dict[position])
            else:
                temp_dict[remainder].add(position)

        for key in temp_dict:

            if (len(temp_dict[key]) > 1):
                my_dict[''.join(key)] = ''.join(sorted(temp_dict[key]))
            else:
                my_dict[''.join(key)] = temp_dict[key].pop()

                # self.my_dict = my_dict
        return my_dict

    def ListFromGroup(self, my_dict, int):
        """This function initializes an empty list. Then iterates through the
        keys in the member variable self.my_dict (which was modified in
        Grouping(int)) and captures the value in the variable temp. The code
        then branches depending on what integer was passed in (0, 1, or 2).
        If 0, it checks whether the value (a string) is longer than 1. If it
        is, then it finds the value from the member variable self.rules_dict
        and concatenates it with the key from self.my_dict. The concatenated
        product is then captured in the variable 'new_codon'. If it is not
        longer than one (i.e. only one nucleotide will work at that particular
        position in the compressed codon), then the value at self.my_dict[key]
        is concatenated with the key from self.my_dict and this concatenated
        product is captured in the variable 'new_codon'. new_codon is then
        added to the new_list. Logic is similar for int values of 1 or 2.

        Parameters
        ----------
        my_dict : dict
            This dictionary has a string as the key and string as value. The
            dictionary should be the same format as the output from Grouping()
        int : int
            This should be a 0, 1, or 2. Because we are interested in positions
            in the codons, it does not make sense to have numbers other than
            0, 1, or 2. There should be error handling here.

        Returns
        -------
        new_list : list
            A list of compressed codons

        Examples
        --------
        >>> self.codon_list = self.ListFromGroup(self.my_dict, i)
        """
        new_list = []

        for key in self.my_dict:
            temp = self.my_dict[key]

            if len(temp) > 1:
                if int == 0:
                    new_codon = self.rules_dict[temp] + key
                elif int == 1:
                    new_codon = key[0] + self.rules_dict[temp] + key[1]
                else:
                    new_codon = key + self.rules_dict[temp]
            else:
                if int == 0:
                    new_codon = temp + key
                elif int == 1:
                    new_codon = key[0] + temp + key[1]
                else:
                    new_codon = key + temp

            new_list.append(new_codon)

            # print new_codon, key, self.my_dict[key]

        return new_list