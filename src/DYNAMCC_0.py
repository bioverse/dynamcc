# for the correct perl version use:: /perl5/perlbrew/perls/perl-5.22.0/bin/perl


# !/opt/local/bin/python2.7
import multiprocessing
from collections import defaultdict
import os
import itertools
from CodonWorker import CodonWorker
import util

def CalcCombinations(filtered_dict):
    """Calculates the total combinations of codons possible. This is n! for
    all combinations of codons in the filtered_dict.

    Parameters
    ----------
    filtered_dict : dict
        Dictionary formatted in the same way as EditUsageDict(). Dictionary of
        lists of dictionaries for codon usage. Technically, any
        dictionary that has single letter amino acid symbols as keys would
        work

    Returns
    -------
    total : int
        This is the total number of combinations of codons that are possible
        after the user has selected which codon(s) to remove.

    Examples
    --------
    >>> CalcCombinations(filtered_dict)
    """
    total = 1
    for key in filtered_dict:
        total *= len(filtered_dict[key])
    return total

def BuildCodonCount(new_dict, key_order):
    """Iterate through a codon usage dictionary, and build a list that contains
    the sum of number of codons for each key (amino acid) at the indices

    Parameters
    ----------
    new_dict : dict
        This is the dictionary returned by either RemoveCodonByRank or
        ByUsage. The dictionary formatted the same as EditUsageDict().
        Dictionary of lists of dictionaries except that the codons with
        usage frequency below user specified rank or usage have been removed

    Returns
    -------
    codon_count : list
        A list containing the number of codons for each amino acid (this is
        a list of integers)
    """
    codon_count = []
    for key in key_order:
        codon_count.append(len(new_dict[key]))
    return codon_count

def FindMinimumThreshold(filtered_dict):
    """Iterates through filtered_dict and builds a list of all the codons with
    the hightest usage (because the list of codons is ordered by usage,
    this script just grabs the first index of each value's list). Then the
    script returns the lowest number in the list. This number will be the
    minimum threshold (i.e. users should select a cut-off below this number
    otherwise they will be omitting codons that they did not intend to omit).

    Parameters
    ----------
    filtered_dict : dict
        Dictionary formatted in the same way as EditUsageDict(). Dictionary of
        lists of dictionaries for codon usage. Technically, any
        dictionary that has single letter amino acid symbols as keys would
        work

    Returns
    -------
    float(min(usage_list)) : float
        Among all the codons remaing (after the user has thrown out particular
        residues), this number represents the lowest usage frequency of all
        codons with the highest usage frequency. In other words, given a list
        of the highest usage frequency for each codon, return the minimum
        number.

    Examples
    --------
    >>> min_threshold = FindMinimumThreshold(filtered_dict)
    """
    usage_list = []
    for key in filtered_dict:
        highest_usage = filtered_dict[key][0]
        for codon in highest_usage:
            usage_list.append(highest_usage[codon])
    return float(min(usage_list))


def RemoveLowCodons(threshold, filtered_dict):
    """Given the user input for the codon usage threshold (i.e. the user
    would like to remove all codons with a usage frequency below the threshold)
    the script builds a new dictionary (in the same format as the input
    dictionary) that does not contain the codons with usage frequency below
    threshold.

    Parameters
    ----------
    threshold : float
        This is the codon usage frequency input by the user that specifies
        which codons to remove based on usage frequency.
    filtered_dict : dict
        Dictionary formatted in the same way as EditUsageDict(). Dictionary of
        lists of dictionaries for codon usage. Technically, any
        dictionary that has single letter amino acid symbols as keys would
        work

    Returns
    -------
    new_dict : dict
        Dictionary formatted the same as input except that the codons with
        usage frequency below user specified threshold have been removed

    Examples
    --------
    """
    new_dict = {}
    for key1 in filtered_dict:
        new_dict[key1] = filter(lambda x: x[1] > threshold, filtered_dict[key1])
        if(len(new_dict[key1]) == 0):
            raise SyntaxError('No codons avaliable for key: %s' % key1)
    return new_dict


def RemoveCodonByRank(rank, sorted_dict):
    """This script builds a new dictionary with the same format as the input
    dictionary except that is will not contain codons below the 'rank'
    specified by the user. In this case, rank is an integer that corresponds
    to 1 + the index of a list of codons ordered by usage frequency. In other
    words, given a list of codon, the codon with the highest usage frequency
    will be given rank 1 and the codon with the lowest usage frequency will be
    given the highest number (depending on how many codons code for the
    particular amino acid).

    Parameters
    ----------
    rank : int
        the user specified codon rank that has been chosen as a cutoff value
        (i.e. codons with a rank below the specified rank will not be
        included)
    sorted_dict : dict
        Dictionary formatted in the same way as EditUsageDict(). Dictionary of
        lists of dictionaries for codon usage. Technically, any
        dictionary that has single letter amino acid symbols as keys would
        work

    Returns
    -------
    new_dict : dict
        Dictionary formatted the same as input except that the codons with
        usage frequency below user specified rank have been removed

    Examples
    --------
    >>> rank = int(raw_input("Set codon rank threshold: "))
    >>> RemoveCodonByRank(rank, filtered_dict)
    """
    new_dict = {}
    for key in sorted_dict:
        if len(sorted_dict[key]) > rank:
            new_dict[key] = sorted_dict[key][0:rank]
        else:
            new_dict[key] = sorted_dict[key]

    return new_dict

def SetRedundancy():
    """
    Parameters
    ----------
    none

    Returns
    -------
    redundancy : int
        Return the integer entered by the user
    """
    redundancy = int(raw_input("Set redundancy" +
                               " (0 for no redundancy at all): "))
    return redundancy


def CalcTotCombinations(combinations, codon_count, new_dict, redundancy):
    """
    Parameters
    ----------
    combinations : int
    codon_count : int
    new_dict : dict
    redundancy : int

    Returns
    -------
    tot_combinations : int
    """
    tot_combinations = (combinations *
                        (codon_count - len(new_dict)) ** redundancy)
    return tot_combinations

def codon_exploder(codon_count):

    temp_list = []

    for item in codon_count:
        temp_list.append(range(0, item))

    combinations = itertools.product(*temp_list)
    return combinations

def start_multiprocessing(new_dict, rules_dict, codon_count, redundancy, processes = 3):

    worker_array = []
    output_queue = multiprocessing.Queue(maxsize=3)
    for thread in range(0,processes):
        input_queue = multiprocessing.Queue()
        w = CodonWorker(input_queue, output_queue, new_dict, rules_dict, redundancy)
        worker_array.append(w)

    for w in worker_array:
        w.start()

    cyclical_adder = itertools.cycle(range(0,processes))

    combinations = codon_exploder(codon_count)

    for combo in combinations:
        worker_array[cyclical_adder.next()].push(combo)

    for worker in worker_array:
        worker.kill_worker()

    output = []
    while(len(output) != len(worker_array)):
        output.append(output_queue.get(block = True))

    BestReduceSize = 22
    BestRatio = 0

    best_result = None

    for result in output:

        reduced_list = result['BestReducedList']
        total_usage_frequency = result['Ratio']

        if len(reduced_list) < BestReduceSize or (len(reduced_list) == BestReduceSize and total_usage_frequency > BestRatio):
            best_result = result

    for key in best_result:

        print key, best_result[key]

    return best_result

def main():

    sorted_dict = util.BuildUsageDict('ecoli.txt')
    rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')
    #print("Available amino acids (count: " + str(len(sorted_dict)) +"; X represents stop codons)")

    #selection = GetUserSelection(sorted_dict)

    selection = ['A','C','E']

    filtered_dict = util.EditUsageDict(selection, sorted_dict)

    selection = 'R'

    if selection == 'R':
        threshold = 2
        new_dict = RemoveCodonByRank(threshold, filtered_dict)
    else:
        threshold = 0.04
        new_dict = RemoveCodonByRank(threshold, filtered_dict)

    codon_order = new_dict.keys()

    codon_count = BuildCodonCount(new_dict, codon_order)

    redundancy = 0

    start_multiprocessing(new_dict,rules_dict,codon_count, redundancy, processes = 3)

if(__name__ == '__main__'):
    main()
