#!/opt/local/bin/python2.7

import util
from Recursive import Recursive
from collections import defaultdict
import os

def ReformatUsageDict(usage_dict):
    """Reformat the usage dict such that the output will

    Parameters
    ----------

    Returns
    -------
    usage_dict : dict
        dictionary with the following format:
        {
            F : [{Codon: TTT, Frequency : 0.58, InUse : 0},
                    {Codon: TTC, Frequency : 0.42, InUse : 0}],
            L : [{Codon : TTA, Frequency : 0.14, InUse : 0},
                    {Codon : TTG, Frequency : 0.13, InUse : 0},
                    {Codon : CTT, Frequency : 0.12, InUse : 0},
                    {Codon : CTC, Frequency : 0.1, InUse : 0},
                    {CTA: 0.04}, {CTG: 0.47}],
            I : [{Codon : ATT, Frequency : 0.49, InUse : 0},
                    {Codon : ATC, Frequency : 0.39, InUse : 0},
                    {Codon : ATA, Frequency : 0.11, InUse : 0}],
            ...
            ...
            ...
            G : [{Codon : GGT, Frequency : 0.35, InUse : 0},
                    {Codon : GGC, Frequency : 0.37, InUse : 0},
                    {Codon : GGA, Frequency : 0.13, InUse : 0},
                    {Codon : GGG, Frequency : 0.15, InUse : 0}]
        }


    """
    new_dict = {}
    for key in usage_dict:
        new_dict[key] = []
        for item in usage_dict[key]:
            new_dict[key].append({'Codon': item[0], 'Frequency': item[1], 'InUse': 0})
    return new_dict

def BestList(filtered_dict):
    """Returns a list of codons with highest usage frequency given a usage
    dictionary

    Parameters
    ----------
    filtered_dict: dict
        Dictionary of lists of dictionaries for codon usage. The keys are
        single letter amino acid symbols, and the values are a sorted list of
        dicts (these dicts have keys corresponsing to codons and values
        corresponsing to usage freuqency). This list must be sorted in
        descending order of usage frequency!

    Returns
    -------
    best_list: list
        A list of codons that are most frequently used

    Examples
    --------
    >>> usage_dict = BuildUsageDict()
    >>> sorted_dict = SortUsageDict(usage_dict)
    >>> selection = GetUserSelection(sorted_dict)
    >>> filtered_dict = EditUsageDict(selection, sorted_dict)
    >>> BestList(filtered_dict)
    """
    best_list = []
    for key1 in filtered_dict:

        print filtered_dict[key1]
        best_tuple = filtered_dict[key1][0]
        best_list.append(best_tuple[0])
    return best_list


def FlagInUse(best_list, formatted_dict):
    """For all codons in best_list, set InUse flag to 1 in InUse dict
    """
    for key in formatted_dict:
        for item in formatted_dict[key]:
            if item['Codon'] in best_list:
                item['InUse'] = 1
    return formatted_dict

def NextBestList(best_list, InUse):
    """Find the codon in InUse with the highest Frequency value that is
    not currently 'InUse'. Add this Codon to best_list. Return the updated
    list.

    Parameters
    ----------
    best_list : list
        The current codon list (this changes as the program runs and will
        eventually include all the degenerate codons for amino acids that the
        user has specified they want to include)
    InUse : dict
        This is the dictionary that results from running
        ReformatUsageDict(usage_dict)

    Returns
    -------
    temp_dict : dict

    best_list : list
    """
    temp_dict = {'Codon': '', 'Frequency': 0}
    for key in InUse:
        for item in InUse[key]:
            if item['Frequency'] > temp_dict['Frequency'] and item['InUse'] != 1:
                temp_dict['Frequency'] = item['Frequency']
                temp_dict['Codon'] = item['Codon']
    if temp_dict['Codon'] != '':
        best_list.append(temp_dict['Codon'])
    else:
        pass
    return temp_dict, best_list


def TestTempDict(temp_dict):
    """Return 0 if temp_dict 'Codon' is empty string and return 1 if not an
    empty string
    """
    for key in temp_dict:
        if temp_dict['Codon'] == '':
            return False
        else:
            return True

def execute_algorithm(codon_list, in_use, rules_dict, inverse_dict):

    results = []

    while True:

        recursive = Recursive(codon_list, rules_dict, inverse_dict)
        compressed_list = recursive.FindMinList(codon_list, None)
        #print('Reduced List (' + str(len(compressed_list)) + ')')
        #print compressed_list

        results.append(compressed_list)

        temp_dict, codon_list = NextBestList(codon_list, in_use)
        in_use = FlagInUse(codon_list, in_use)
        #print('List (' + str(len(codon_list)) + ')')
        #print codon_list

        if(TestTempDict(temp_dict) == False):
            break

    return results[-1]


def main():


    sorted_dict = util.BuildUsageDict('ecoli.txt')
    rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')

    selection = ['A','C','G','F','I','X','Y','V','W','T','S','P','L','M']

    filtered_dict = util.EditUsageDict(selection, sorted_dict)

    InUse_dict = ReformatUsageDict(filtered_dict)

    codon_list = BestList(filtered_dict)
    in_use = FlagInUse(codon_list, InUse_dict)

    best_compression = execute_algorithm(codon_list,in_use,rules_dict,inverse_dict)

    print 'Maximally compressed list,', best_compression, ', Length: %i' % len(best_compression)

main()