"""
Copyright (c) 2016, Andrea Halweg-Edwards, Gur Pines, Assaf Pines, James Winkler
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of DYNAMCC nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import itertools
from tornado.web import RequestHandler
from src.DYNAMCC_0 import *
from src.DYNAMCC_R import *
from src.DYNAMCC_4 import *

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
		rank = False
		usage = False
		if selection == 'rank':
			rank = True
			Selection = 'R'
			#threshold = 2
			threshold = int(self.get_argument("input_rank"))
			print threshold
			new_dict = RemoveCodonByRank(threshold, filtered_dict)
		else:
			usage = True
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

		print "best_result:", best_result

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

		self.render("dynamcc_0_results.html", rank=rank, usage=usage, threshold_value=str(threshold), codon_dict=codon_dict, organism=organism_name, remove_aa=remove_aa, best_result=best_result, exploded_codons=exploded_codons, sorted_dict=sorted_dict)


class DynamccRHandler(RequestHandler):
	def get(self):
		self.render("dynamcc_R.html")

	def post(self):
		if "table" in self.request.files:
			sorted_dict = util.BuildCustomUsageDict(self.request.files["table"][0])
			organism_name = "user uploaded usage table"
		else:
			seletect_organism = self.get_argument("usage_table")
			if seletect_organism in organism_mapping:
				sorted_dict = util.BuildUsageDict(organism_mapping[seletect_organism])
				organism_name = organism_names[seletect_organism]
			else:
				pass
		#organism_name = "E. coli"
		#sorted_dict = util.BuildUsageDict(organism_mapping["Ecoli"])
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

		print "best_compression:", best_compression
		
		## exploding codons
		exploded_codons = {}
		codon_list = []
		for codon in best_compression:
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

		self.render("dynamcc_R_results.html", codon_dict=codon_dict, organism=organism_name, remove_aa=remove_aa, best_compression=best_compression, length=len(best_compression), exploded_codons=exploded_codons, sorted_dict=sorted_dict)


class ExploderHandler(RequestHandler):
	def get(self):
		self.render("codon_exploder.html")

	def post(self):
		if "table" in self.request.files:
			sorted_dict = util.BuildCustomUsageDict(self.request.files["table"][0])
			organism_name = "user uploaded usage table"
		else:
			seletect_organism = self.get_argument("usage_table")
			if seletect_organism in organism_mapping:
				sorted_dict = util.BuildUsageDict(organism_mapping[seletect_organism])
				organism_name = organism_names[seletect_organism]
			else:
				pass

		codon_dict = util.BuildCodonDict(sorted_dict)

		compressed_codons = (str(self.get_argument("compressedCodons"))).upper()
		compressed_list = compressed_codons.split(',')
		compressed_list = [codon.strip() for codon in compressed_list]
		print compressed_list
		
		## exploding codons
		exploded_codons = {}
		codon_list = []
		for codon in compressed_list:
			exploded_codons[codon] = list(codon)
			codon_list.append(list(codon))
		exploded_codons_copy1 = {}
		for key in exploded_codons:
			exploded_codons_copy1[key] = []
		for codon in exploded_codons:
			print codon
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

		self.render("exploded_codon_results.html", codon_dict=codon_dict, organism=organism_name, exploded_codons=exploded_codons, sorted_dict=sorted_dict)

class Dynamcc4Handler(RequestHandler):
	def get(self):
		self.render("dynamcc_4.html", step=None)

	def post(self):
		hamming_distance = int(self.get_argument("hamming_distance"))
		target_codon = self.get_argument("target_codon")
		form_step = int(self.get_argument("step", 0))

		if form_step == 2:
			if "table" in self.request.files:
				usage_table = util.BuildCustomUsageDict(self.request.files["table"][0])
				organism_name = "user uploaded usage table"
			else:
				seletect_organism = self.get_argument("usage_table")
				if seletect_organism in organism_mapping:
					usage_table = util.BuildUsageDict(organism_mapping[seletect_organism])
					organism_name = organism_names[seletect_organism]
				else:
					pass

			print "target_codon: %s\nhamming distance: %d\norganism: %s" % (target_codon, hamming_distance, organism_name)

			rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')

			"""
			Finding hamming distance from the usage table
			"""
			new_usage_table = defaultdict(list)
			for amino_acid in usage_table:
				codons = usage_table[amino_acid]
				distance_in_range = False
				for codon in codons:
					if codon[0] == target_codon:
						continue

					if hamming_distance != 1:
						distance_in_range = TargetHammingDistance(codon[0], target_codon, 2)
						if distance_in_range == False:
							distance_in_range = TargetHammingDistance(codon[0], target_codon, 3)
					else:
						distance_in_range = TargetHammingDistance(codon[0], target_codon, 1)

					"""
					Filter out possible codons from the list and
					only preserve the highest usage value possible codon
					"""
					sibling_in_range = False
					if len(new_usage_table[amino_acid]):
						for _codon in new_usage_table[amino_acid]:
							if _codon[2] == True and distance_in_range == True:
								distance_in_range = False
								sibling_in_range = True

					new_usage_table[amino_acid].append((codon[0], codon[1], distance_in_range, sibling_in_range))

				print amino_acid, new_usage_table[amino_acid]

			return self.render("dynamcc_4.html", step=form_step, usage_table=new_usage_table)

		if self.get_argument("keep_or_remove") == 'remove':
			remove_aa = self.get_arguments('aa')
		else:
			selected_aa = self.get_arguments('aa')
			remove_aa = list(aa.difference(selected_aa))

		HammingDistance()

		filtered_dict = util.EditUsageDict(remove_aa, usage_table)
		InUse_dict = ReformatUsageDict(filtered_dict)
		codon_list = BestList(filtered_dict)
		in_use = FlagInUse(codon_list, InUse_dict)
		best_compression = execute_algorithm(codon_list,in_use,rules_dict,inverse_dict)

		print "best_compression:", best_compression
		
		## exploding codons
		exploded_codons = {}
		codon_list = []
		for codon in best_compression:
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

		codon_dict = util.BuildCodonDict(usage_table)
		print "codon_dict:", codon_dict

		self.render("dynamcc_R_results.html", codon_dict=codon_dict, organism=organism_name, remove_aa=remove_aa, best_compression=best_compression, length=len(best_compression), exploded_codons=exploded_codons, sorted_dict=usage_table)
