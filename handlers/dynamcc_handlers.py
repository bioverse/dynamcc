from tornado.web import RequestHandler
from src.DYNAMCC_0 import *
from src.DYNAMCC_R import *


organism_mapping = {
	"Ecoli" : "ecoli.txt",
	"yeast" : "yeast.txt",
	"human" : "hsapiens.txt",
	"mouse" : "mmusculus.txt",
	"Dmel"	: "dmelanogaster.txt",
	"Cele"	: "celegans.txt"
	}

organism_names = {
	"Ecoli" : "E. coli",
	"yeast" : "yeast",
	"human" : "human",
	"mouse" : "mouse",
	"Dmel"	: "D. melanogaster",
	"Cele"	: "C. elegans"
}

aa = set(['A', 'R', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'N', 'X'])

class Dynamcc0Handler(RequestHandler):
    def get(self):
        self.render("dynamcc_0.html")

    def post(self):
    	seletect_organism = self.get_argument("usage_table")
    	if seletect_organism in organism_mapping:
    		sorted_dict = util.BuildUsageDict(organism_mapping[seletect_organism])
    		organism_name = organism_names[seletect_organism]
    	else:
    		pass
    	rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')
    	if self.get_argument("keep_or_remove") == 'remove':
            remove_aa = self.get_arguments('aa')
        else:
            selected_aa = self.get_arguments('aa')
            remove_aa = list(aa.difference(selected_aa))
    	filtered_dict = util.EditUsageDict(remove_aa, sorted_dict)
    	selection = self.get_argument("compression_method")
    	if selection == 'rank':
    	    print selection
    	    threshold = 2
    	    new_dict = RemoveCodonByRank(threshold, filtered_dict)
    	else:
    	    print selection
    	    threshold = 0.04
    	    new_dict = RemoveCodonByUsage(threshold, filtered_dict)

    	codon_order = new_dict.keys()

    	codon_count = BuildCodonCount(new_dict, codon_order)

    	redundancy = 0

    	best_result = start_multiprocessing(new_dict,rules_dict,codon_count, redundancy, processes = 3)
    	self.render("dynamcc_0_results.html", best_result=best_result)


class DynamccRHandler(RequestHandler):
    def get(self):
        self.render("dynamcc_R.html")

    def post(self):
    	seletect_organism = self.get_argument("usage_table")
        if seletect_organism in organism_mapping:
    		sorted_dict = util.BuildUsageDict(organism_mapping[seletect_organism])
    		organism_name = organism_names[seletect_organism]
    	else:
    		pass
    	rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')
    	if self.get_argument("keep_or_remove") == 'remove':
            remove_aa = self.get_arguments('aa')
        else:
            selected_aa = self.get_arguments('aa')
            remove_aa = list(aa.difference(selected_aa))
    	filtered_dict = util.EditUsageDict(remove_aa, sorted_dict)
    	InUse_dict = ReformatUsageDict(filtered_dict)
    	codon_list = BestList(filtered_dict)
    	in_use = FlagInUse(codon_list, InUse_dict)
    	best_compression = execute_algorithm(codon_list,in_use,rules_dict,inverse_dict)
    	#print 'Maximally compressed list,', best_compression, ', Length: %i' % len(best_compression)
    	self.render("dynamcc_R_results.html", organism=organism_name, remove_aa=remove_aa, best_compression=best_compression, length=len(best_compression))










