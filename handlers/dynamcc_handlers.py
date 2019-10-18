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
	"Ecoli": "ecoli.txt",
	"yeast": "yeast.txt",
	"human": "hsapiens.txt",
	"mouse": "mmusculus.txt",
	"Dmel"	: "dmelanogaster.txt",
	"Cele"	: "celegans.txt"
	}

organism_names = {
	"Ecoli": "E. coli",
	"yeast": "yeast",
	"human": "human",
	"mouse": "mouse",
	"Dmel"	: "D. melanogaster",
	"Cele"	: "C. elegans"
}

aa = set(['A', 'R', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L',
         'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'N', 'X'])

rules = {'R': ['A', 'G'],
			'Y': ['C', 'T'],
			'M': ['A', 'C'],
			'K': ['G', 'T'],
			'S': ['C', 'G'],
			'W': ['A', 'T'],
			'H': ['A', 'C', 'T'],
			'B': ['C', 'G', 'T'],
			'V': ['A', 'C', 'G'],
			'D': ['A', 'G', 'T'],
			'N': ['A', 'C', 'G', 'T'],
			'A': ['A'],
			'C': ['C'],
			'G': ['G'],
			'T': ['T']
		}

ALLOWED_NEUCLOTIDES = ['A', 'C', 'G', 'T']
ACCESS_CODE = "af12d5f5c349b38b3be6ca40ca4b0d79"

class Dynamcc0Handler(RequestHandler):
	def get(self):
		self.render("dynamcc_0.html", usage_array=[])

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
		# print selection
		rank = False
		usage = False
		if selection == 'rank':
			rank = True
			Selection = 'R'
			# threshold = 2
			threshold = int(self.get_argument("input_rank"))
			print threshold
			new_dict = RemoveCodonByRank(threshold, filtered_dict)
		else:
			usage = True
			Selection = 'U'
			print Selection
			# threshold = 0.04
			threshold = float(self.get_argument("input_usage"))
			new_dict = RemoveLowCodons(threshold, filtered_dict)

		print "new_dict: ", new_dict

		codon_order = new_dict.keys()

		codon_count = BuildCodonCount(new_dict, codon_order)

		redundancy = 0

		best_result = start_multiprocessing(
		    new_dict, rules_dict, Selection, codon_count, redundancy, processes=3)

		print "best_result:", best_result

		# exploding codons
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

		self.render("dynamcc_0_results.html", rank=rank, usage=usage, threshold_value=str(threshold), codon_dict=codon_dict,
		            organism=organism_name, remove_aa=remove_aa, best_result=best_result, exploded_codons=exploded_codons, sorted_dict=sorted_dict)


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
		# organism_name = "E. coli"
		# sorted_dict = util.BuildUsageDict(organism_mapping["Ecoli"])
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
		best_compression = execute_algorithm(
		    codon_list, in_use, rules_dict, inverse_dict)

		print "best_compression:", best_compression

		# exploding codons
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

		self.render("dynamcc_R_results.html", codon_dict=codon_dict, organism=organism_name, remove_aa=remove_aa,
		            best_compression=best_compression, length=len(best_compression), exploded_codons=exploded_codons, sorted_dict=sorted_dict)


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

		# exploding codons
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

		self.render("exploded_codon_results.html", codon_dict=codon_dict,
		            organism=organism_name, exploded_codons=exploded_codons, sorted_dict=sorted_dict)


class Dynamcc4Handler(RequestHandler):
	def get(self):
		access_code = self.get_argument("access_code", False)
		if access_code == ACCESS_CODE:
			self.render("dynamcc_4.html", step=None, error=None, access_code=ACCESS_CODE)

	def post(self):
		access_code = self.get_argument("access_code", False)
		if access_code != ACCESS_CODE:
			return

		hamming_distance_label = self.get_argument("hamming_distance")
		hamming_distance = 1 if hamming_distance_label == '1' else 2
		target_codon = self.get_argument("target_codon")
		form_step = int(self.get_argument("step", 0))
		target_codon = target_codon.upper()

		verified_ncltds = [c in ALLOWED_NEUCLOTIDES for c in list(target_codon)];
		verified_ncltd = all(verified_ncltds)

		if not verified_ncltd or len(verified_ncltds) != 3:
			return self.render("dynamcc_4.html", step=None, error="Invalid Codon", access_code=ACCESS_CODE)

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

			"""
			Finding hamming distance from the usage table
			"""
			new_usage_table = defaultdict(list)
			amino_acids = {}
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
					only preserve the possible highest usage value codon
					"""
					sibling_in_range = False
					if len(new_usage_table[amino_acid]):
						for _codon in new_usage_table[amino_acid]:
							if _codon[2] == True and distance_in_range == True:
								distance_in_range = False
								sibling_in_range = True

					new_usage_table[amino_acid].append((codon[0], codon[1], distance_in_range, sibling_in_range))

				amino_acids[amino_acid] = any([_codon[2] for _codon in new_usage_table[amino_acid]])
				print amino_acid, new_usage_table[amino_acid], amino_acids[amino_acid]

			return self.render("dynamcc_4.html", error=None, amino_acids=amino_acids, step=form_step, target_codon=target_codon, hamming_distance=hamming_distance_label, organism_name=organism_name, usage_table=new_usage_table, access_code=ACCESS_CODE)

		codons = self.get_arguments("codons")

		sorted_dict_codons = defaultdict(list)
		for codon in codons:
			inline_codon = str.split(str(codon), '_')

			sorted_dict_codons[ inline_codon[0] ].append((inline_codon[1],inline_codon[2]))
		
		print sorted_dict_codons

		rules_dict, inverse_dict = util.BuildRulesDict('rules.txt')
		organism_name = self.get_argument("organism_name")

		InUse_dict = ReformatUsageDict(sorted_dict_codons)
		codon_list = BestList(sorted_dict_codons)
		in_use = FlagInUse(codon_list, InUse_dict)
		best_compression = execute_algorithm(codon_list,in_use,rules_dict,inverse_dict)

		print "best_compression:", best_compression

		inline_codon_list = codon_list

		# exploding codons
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

		codon_dict = util.BuildCodonDict(sorted_dict_codons)
		print "codon_dict:", codon_dict

		self.render("dynamcc_4_results.html", hamming_distance=hamming_distance_label, target_codon=target_codon, inline_codon_list=inline_codon_list, codon_dict=codon_dict, organism=organism_name, best_compression=best_compression, length=len(best_compression), exploded_codons=exploded_codons, sorted_dict=sorted_dict_codons, access_code=ACCESS_CODE)
