__author__ = 'jdwinkler'
from time import time
from Recursive import Recursive
from collections import defaultdict
import multiprocessing


class CodonWorker(multiprocessing.Process):

    def __init__(self, input_queue, output_queue, new_dict, rules_dict, redundancy):

        super(CodonWorker, self).__init__()

        self.input_queue = input_queue
        self.output_queue = output_queue
        self.position_cache = defaultdict(dict)

        self.new_dict = new_dict
        self.rules_dict = rules_dict
        self.redundancy = redundancy

    def push(self, combination):

        self.input_queue.put(combination)

    def kill_worker(self):

        self.input_queue.put(None)

    def run(self):

        new_dict = self.new_dict
        rules_dict = self.rules_dict
        redundancy = self.redundancy

        BestReduceSize = 20
        BestRatio = 0
        BestList = []
        BestReducedList = []
        t = 0

        inverse_rule_dict = {}

        for key in rules_dict:
            inverse_rule_dict[rules_dict[key]] = key

        combo = []

        while(True):

            combo = self.input_queue.get(block=True)

            if(combo == None):
                print 'Worker terminated'
                break

            codons, ratios = CodonWorker.CreateListFromIndex(combo, new_dict)

            t += 1

            if redundancy != 0:
                pass
            else:
                recursive = Recursive(codons, rules_dict, inverse_rule_dict)
                reduced_list = recursive.Reduce(self.position_cache)
                total_usage_frequency = 0
                for frequency in ratios:
                    total_usage_frequency += frequency
                if len(reduced_list) < BestReduceSize or (len(reduced_list) == BestReduceSize and total_usage_frequency > BestRatio):
                    BestList = [codons, ratios]
                    BestReduceSize = len(reduced_list)
                    BestRatio = total_usage_frequency
                    BestReducedList = reduced_list

            if(t % 10000 == 0):
                print 'Current best reduced list is',BestReducedList
                print t

        information_dict = {
            "BestReducedList":BestReducedList,
            "BestList": BestList,
            "ReduceSize": BestReduceSize,
            "Ratio": BestRatio
        }
        self.output_queue.put(information_dict)

    @staticmethod
    def CreateListFromIndex(empty_list, new_dict):
        codons = []
        ratios = []

        counter = 0

        for aa in new_dict:
            #print aa,empty_list[i],empty_list,i
            (codon, ratio) = new_dict[aa][empty_list[counter]]
            codons.append(codon)
            ratios.append(ratio)
            counter+=1

        return codons, ratios