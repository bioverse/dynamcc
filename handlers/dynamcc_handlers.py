import itertools
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

rules = {   'R' : ['A', 'G'],
			'Y' : ['C', 'T'],
			'M' : ['A', 'C'],
			'K' : ['G', 'T'],
			'S' : ['C', 'G'],
			'W' : ['A', 'T'],
			'H' : ['A', 'C', 'T'],
			'B' : ['C', 'G', 'T'],
			'V' : ['A', 'C', 'G'],
			'D' : ['A', 'G', 'T'],
			'N' : ['A', 'C', 'G', 'T'],
			'A' : ['A'],
			'C' : ['C'],
			'G' : ['G'],
			'T' : ['T']
		}

class Dynamcc0Handler(RequestHandler):
	def get(self):
		self.render("dynamcc_0.html", usage_array = [])

	def post(self):
		if "table" in self.request.files:
			sorted_dict = util.BuildCustomUsageDict(self.request.files["table"][0])
			organism_name = "user uploaded usage table"
		else:
			seletect_organism = self.get_argument("usage_table")
			if seletect_organism in organism_mapping:
				sorted_dict = util.BuildUsageDict(organism_mapping[seletect_organism])
				organism_name = organism_names[seletect_organism]
				print "sorted_dict", sorted_dict
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
		#print selection
		if selection == 'rank':
			Selection = 'R'
			#threshold = 2
			threshold = int(self.get_argument("input_rank"))
			print threshold
			new_dict = RemoveCodonByRank(threshold, filtered_dict)
		else:
			Selection = 'U'
			print Selection
			#threshold = 0.04
			threshold = float(self.get_argument("input_usage"))
			new_dict = RemoveLowCodons(threshold, filtered_dict)

		print "new_dict: ", new_dict
		
		codon_order = new_dict.keys()

		codon_count = BuildCodonCount(new_dict, codon_order)

		redundancy = 0

		best_result = start_multiprocessing(new_dict,rules_dict, Selection, codon_count, redundancy, processes = 3)

		## exploding codons
		exploded_codons = {}
		codon_list = []
		for codon in best_result['BestReducedList']:
			exploded_codons[codon] = list(codon)
			codon_list.append(list(codon))
		exploded_codons_copy1 = {}
		for key in exploded_codons:
			exploded_codons_copy1[key] = []
		for codon in exploded_codons:
			for j in range(len(exploded_codons[codon])):
				exploded_codons_copy1[codon].append(rules[exploded_codons[codon][j]])

		exploded_codons_copy2 = {}
		for key in exploded_codons:
			exploded_codons_copy2[key] = []
		for codon in exploded_codons_copy1:
			combos = list(itertools.product(*exploded_codons_copy1[codon]))
			for combo in combos:
				exploded_codons_copy2[codon].append(combo)

		exploded_codons = {}
		for key in exploded_codons_copy2:
			exploded_codons[key] = []
			for value in exploded_codons_copy2[key]:
				joined_codon = ''.join(list(value))
				exploded_codons[key].append(joined_codon)
		print "exploded_codons:", exploded_codons

		codon_dict = util.BuildCodonDict(sorted_dict)
		print "codon_dict:", codon_dict

	#	# getting rank and usage of exploded codons
	#	exploded_codon_list = []
	#	for key in exploded_codons:
	#		exploded_codon_list.append(exploded_codons[key])
	#	for key in sorted_dict:
	#		tmp = []
	#		for i in range(len(sorted_dict[key])):
	#			tmp.append((sorted_dict[key][i][0], sorted_dict[key][i][1], i + 1))
	#		print tmp 

		self.render("dynamcc_0_results.html", codon_dict=codon_dict, organism=organism_name, remove_aa=remove_aa, best_result=best_result, exploded_codons=exploded_codons, sorted_dict=sorted_dict)


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










