# for the correct perl version use:: /perl5/perlbrew/perls/perl-5.22.0/bin/perl


#!/opt/local/bin/python2.7

from util import FileHandlers
from time import time
import multiprocessing

def get_file_name(file_path):
	"""Get the names of files in the current directory
	
	Useful when you only need the file name and not the entire path for the
	file

	Parameters
	----------
	file_path: string
		String corresponding to the file path (/path/to/file_name)

	Returns
	-------
	list
		List of strings resulting from spliting the input string at each 
		backslash character  

	Examples
	--------
	>>> for file_path in list_of_file_paths:
	... 	print get_file_name(file_path)
	"""

	path_as_list = file_path.split('/')
	return path_as_list[-1]

def LoadFiles(extention):
	"""Get the paths to the .txt files listed in the current directory
		
	Useful when you have a set of custom .txt files that need to be loaded and
	parsed prior to some calculation or data analysis

	Parameters
	----------
	none

	Returns
	-------
	list
		List of strings corresponding to the path/to/file.txt for each txt
		file found in the current directory  

	Examples
	--------
	>>> all_files = LoadFiles()
	"""
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	files = file_handlers.find_files(file_paths, extention)
	return files
	
def GetDataFile(files):
	"""Ask the user to select which data file (*.txt) to parse
		
	Useful when you have several versions of a data file (for example several
	codon usage tables) that the user must select from.

	Parameters
	----------
	files: list
		List of strings corresponding to the path/to/file.txt for each txt
		file found in the current directory

	Returns
	-------
	selection: int
		Integer corresponding to list[index + 1] of input list  
	files[selection - 1]: string
		String corresponding to path/to/file_name
	get_file_name(files[selection]): string 
		String corresponding to the file_name (everything after last backslash
		character) from string located in list[selection - 1]

	Examples
	--------
	>>> files = LoadFiles()
	>>> selection, file_name = PromptUser(files)
	"""
	print "Select data file: "
	for i in range(len(files)):
		print "[", i + 1, "]", " ", get_file_name(files[i])
	while True:
		try:
			selection = int(raw_input())
			if selection in range(len(files)):
				return(selection, files[selection - 1],
						get_file_name(files[selection - 1]))
			else: 
				raise ValueError()
		except ValueError:
			print("Invalid entry. You must enter an iteger value " +
			"corresponding to one of the listed data files.")

def BuildUsageDict():
	"""Build a codon usage dictionary based on the user selected codon usage
	file
		
	Useful for downstream calculations involving known codon usage frequencies
	in a given organism

	Parameters
	----------
	none

	Returns
	-------
	usage_dict: dict
		Dictionary of lists of dictionaries for codon usage. Dictionary has the
		following structure:
		{
			F : [{TTT: 0.58}, {TTC: 0.42}],
			L : [{TTA: 0.14}, {TTG: 0.13}, {CTT: 0.12}, {CTC: 0.1}, 
					{CTA: 0.04}, {CTG: 0.47}],
			I : [{ATT: 0.49}, {ATC: 0.39}, {ATA: 0.11}],
			...
			...
			...
			G : [{GGT: 0.35}, {GGC: 0.37}, {GGA: 0.13}, {GGG: 0.15}]
		}

	Examples
	--------
	>>> usage_dict = BuildUsageDict()
	"""
	file_handlers = FileHandlers()
	all_files = LoadFiles('txt')
	selection_int, file_path, file_name = GetDataFile(all_files)
	usage_dict = {}
	try:
		for line in open(file_path):
			fields = line.split("\t")
			cleaned = file_handlers.clean(fields)
			if ('Codon' and 'name' and 'prob') in line:
				pass
			else:
				if cleaned[1] in usage_dict:
					usage_dict[cleaned[1]].append({cleaned[0]: cleaned[2]})
				else:
					usage_dict[cleaned[1]] = [{cleaned[0]: cleaned[2]}]
		return usage_dict
	except IOError:
		print("An error occurred while trying to load the data file." +
		"Make sure the file is located in your current working directory.")

def SortUsageDict(usage_dict):
	"""An ugly implementation of bubble sort.

	Useful for sorting the values in a codon usage dictionary in descending
	order based on usage frequency. In this context the value is a list: a 
	list of dictionaries in which each key is a codon and each value is its 
	usage frequency. The list represents all codons/usage_freq for each amino 
	acid. 

	Parameters
	----------
	usage_dict: dict
		Dictionary of lists of dictionaries for codon usage. For example, the
		output of BuildUsageDict() would work as input

	Returns
	-------
	usage_dict: dict
		Dictionary of lists of dictionaries for codon usage. The same format
		as the input dictionary except that list item for each 
		sorted_usage_dict[key] is sorted in descending order based on the
		values of dictionary items in each list.

	Examples
	--------
	>>> usage_dict = BuildUsageDict()
	>>> sorted_dict = SortUsageDict(usage_dict)
	"""
	for key1 in usage_dict: 										# key1 is string corresponding to AA single letter code
		for i in range(len(usage_dict[key1]) - 1, -1, -1):			# iterate through dictionary in reverse order. prevents "list index out of range error" in subsquent step
			j = 0 													# non-pythonic list iteration. Again, preventing "list index out of range error". Allowing for bubble sort
			while j < i: 											# iterate through list. ignore last item, because it will already be sorted
				for key2a in usage_dict[key1][j]: 					# key2a is codon at index j
					for key2b in usage_dict[key1][j + 1]: 			# key2b is codon at index j + 1
						if(float(usage_dict[key1][j][key2a]) < 		# compare usage frequency for each codon, and swap positions if key2a is less then key2b
							float(usage_dict[key1][j + 1][key2b])):
							temp = usage_dict[key1][j + 1]
							usage_dict[key1][j + 1] = usage_dict[key1][j]
							usage_dict[key1][j] = temp
				j += 1
	return usage_dict # return sorted dictionary

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
			for key1 in item:
				new_dict[key].append({'Codon' : key1, 'Frequency' : item[key1], 
										'InUse' : 0})
	return new_dict

def BuildRulesDict():
	"""Construct a dictionary from the .rul file. Each key-value pair is 
	constructed from a single line of the .rul file The .rul file has the 
	following format:

	this	replace_this
	R	A	G
	Y	C	T
	M	A	C
	K	G	T
	S	C	G
	W	A	T
	H	A	C	T
	B	C	G	T
	V	A	C	G
	D	A	G	T
	N	A	C	G	T

	Parameters
	----------
	none

	Returns
	-------
	rules_dict: dict
		dictionary in which the key is a string resulting from joining the 
		nucleotides (A, G, C, T) in columns 2-5 of each line from the .rul
		file and the value corresponds to the string in the first column of
		each line of the .rul file

	Examples
	--------
	>>> rules_dict = BuildRulesDict()
	"""
	file_handlers = FileHandlers()
	rules_file = LoadFiles('rul')
	rules_dict = {}
	try:
		for line in open(rules_file[0]):
			fields = line.split("\t")
			cleaned = file_handlers.clean(fields)
			if ('this' and 'replace_this') in line:
				pass
			else:
				if ''.join((cleaned[1:])) not in rules_dict:
					rules_dict[''.join((cleaned[1:]))] = cleaned[0]
				else:
					pass
		return rules_dict
	except IOError:
		print("An error occurred while trying to load the rules file." +
		"Make sure the file is located in your current working directory.")			

def GetUserSelection(sorted_dict):
	"""Prompt user for selection of amino acids to remove from list

	Parameters
	----------
	sorted_dict: dict
		Dictionary of lists of dictionaries for codon usage. For example, the
		output of BuildUsageDict() would work as input. In this case, any 
		dictionary that has single letter amino acid symbols as keys would
		work

	Returns
	-------
	aa_list: list
		List of amino acids that the user has entered. Amino acid symbols are
		converted to uppercase and all white space is removed.
	
	Examples
	--------
	>>> selection = GetUserSelection()
	"""	
	file_handlers = FileHandlers()
	while True:
		selection = raw_input("Choose amino acids to remove (multiple amino " +
							"acids are indicated as a comma-separated list: ")
		aa_list = file_handlers.clean(selection.split(','))
		try:
			for i in range(len(aa_list)):
				if aa_list[i].upper() in sorted_dict:
					aa_list[i] = aa_list[i].upper()
				else:
					raise ValueError()
			return aa_list
		except ValueError:
				print("Invalid entry. You must enter a letter or series of " +
				"comma-separated letters corresponding to the amino acids " + 
				"you wish to omit.")

def EditUsageDict(selection, sorted_dict):
	"""Remove selected key-value pairs from a codon usage dictionary

	Parameters
	----------
	selection: list
		list of single letter amino acids (such as that returned from 
		GetUserSelection)
	sorted_dict: dict
		Dictionary of lists of dictionaries for codon usage. For example, the
		output of BuildUsageDict() would work as input. In this case, any 
		dictionary that has single letter amino acid symbols as keys would
		work

	Returns
	-------
	sorted_dict: dict
		The same dictionary as input except that all key-value pairs with keys
		that match the user selection are deleted.
	
	Examples
	--------
	>>> usage_dict = BuildUsageDict()
	>>> sorted_dict = SortUsageDict(usage_dict)
	>>> selection = GetUserSelection(sorted_dict)
	>>> EditUsageDict(selection, sorted_dict)
	"""	
	for i in range(len(selection)):
		if selection[i] in sorted_dict:
			del sorted_dict[selection[i]]
	return sorted_dict

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
		for key2 in filtered_dict[key1][0]:
			best_list.append(key2)
	return best_list


def FlagInUse(best_list, formatted_dict):
	"""For all codons in best_list, set InUse flag to 1 in InUse dict
	"""
	for key in formatted_dict:
		for item in formatted_dict[key]:
			if item['Codon'] in best_list:
				item['InUse'] = 1
	return formatted_dict


class Recursive:
	def __init__(self, codon_list, rules_dict):
		"""Initialize the Recursive object with two parameters.

		Parameters
		----------
		codon_list: list
			list of codons that are most frequently used after removing codons 
			corresponding to amino acids (or stop codon) that the user has 
			specified they want left out. This list can be the result of 
			running BestList
		rules_dict: dict
			dictionary in which the key is a string resulting from joining the 
			nucleotides (A, G, C, T) in columns 2-5 of each line from the .rul
			file and the value corresponds to the string in the first column of
			each line of the .rul file

		Returns
		-------
		none
		
		Examples
		--------
		>>> recursive = Recursive(best_list, rules_dict)
		"""			
		self.codon_list = codon_list
		self.rules_dict = rules_dict
		self.reduced = []
		self.my_dict = {}

	def FindMinList(self, list):
		"""Recursive algorithm in which the self.codon_list is a list of the
		most frequently used codons for amino acids that the user wants to 
		include for compression. self.codon is initially the list passed in
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
		reduced_list = self.Reduce()
		if temp != reduced_list:
			self.FindMinList(reduced_list)
		return self.codon_list

	def Reduce(self):
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
			self.my_dict = self.Grouping(i)
			self.codon_list = self.ListFromGroup(self.my_dict, i)
		return self.codon_list

	def Grouping(self, int):
		"""This function initializes an empty dict. Then iterates through each
		codon in self.codon_list. The code then branches depending on which 
		codon position was passed in (0, 1, or 2). If int == 0, InRules == 0 
		and the codon is split into two variables ('position' == the first 
		position and 'remainder' == the rest of the codon). Then it iterates 
		through the keys in self.rules_dict and checks if the value is equal to
		the position. If so, then it adds a new key-value pair to the local 
		my_dict variable. The key corresponds to the "remainder" and the value 
		is a set that contains the split key from self.rules_dict and the 
		InRules variable is set to 1. If the value in self.rules_dict is not
		equivalent to the position, then nothing happens. After exiting the
		if branch, the script checks whether InRules is 1 or 0. If 0, then
		my_dict is extended. If a key already exists in this dict with the 
		same value as the remainder, then the value of that key is (which is 
		a set) is extended to include the new value of the position variable.
		If not, then a new key-value pair is added. The logic is the same for 
		int == 1 and int == 2. The script then iterates through the keys in 
		my_dict and joins the value's strings.

		Parameters
		----------
		int : int
			This should be a 0, 1, or 2 (depending on what is being passed
			from Reduce()). Because we are interested in positions in the
			codons, it does not make sense to have numbers other than 0, 1, 
			or 2. There should be error handling here.

		Returns
		-------
		self.my_dict : dict 
			A dictionary in which the keys are strings of nucleotides that fall
			at particular positions in the codon (1,2 or 0,2 or 0,1) and the 
			values are all the nucleotides that can exist at the remaining 
			position. Here the key-value pairs represent compressed codons. 
	
			For example, the first iteration through looks like:
			{'AA': 'AGT', 'AC': 'A', 'GT': 'C', 'AG': 'C', 'CC': 'A', 
			'TT': 'AT', 'CG': 'CG', 'GG': 'T', 'GC': 'AG', 'AT': 'CGT', 
			'TG': 'ACG'}

			And the last iteration through looks like:
			{'BA': 'T', 'CG': 'T', 'CA': 'G', 'AM': 'C', 'DA': 'A', 
			'RG': 'C', 'WT': 'T', 'VT': 'G', 'SC': 'G', 'TG': 'G'}

		Examples
		--------
		>>> self.my_dict = self.Grouping(i)
		"""
		my_dict = {}
		for codon in self.codon_list:
			if int == 0:
				position = codon[int]
				remainder = codon[int+1:]
				InRules = 0
				for key in self.rules_dict:
					if self.rules_dict[key] == position:
						if remainder in my_dict:
							my_dict[remainder].add(key.split())
						else:
							my_dict[remainder] = set(key.split())
						InRules = 1
			elif int == 1:
				position = codon[int]
				remainder = codon[0] + codon[2]
				InRules = 0
				for key in self.rules_dict:
					if self.rules_dict[key] == position:
						if remainder in my_dict:
							my_dict[remainder].add(key.split())
						else:
							my_dict[remainder] = set(key.split())
						InRules = 1
			else:
				position = codon[int]
				remainder = codon[:2]
				InRules = 0
				for key in self.rules_dict:
					if self.rules_dict[key] == position:
						if remainder in my_dict:
							my_dict[remainder].add(key.split())
						else:
							my_dict[remainder] = set(key.split())
						InRules = 1
			if InRules == 0:
				if remainder in my_dict:
					my_dict[remainder].add(position)
				else:
					my_dict[remainder] = set(position)
		for key in my_dict:
			my_dict[key] = ''.join(sorted(my_dict[key]))
		self.my_dict = my_dict
		return self.my_dict

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
			if int == 0:
				if len(self.my_dict[key]) > 1:
					new_codon = self.rules_dict[temp] + key
					new_list.append(new_codon)
				else:
					new_codon = self.my_dict[key] + key
					new_list.append(new_codon)
			elif int == 1:
				if len(self.my_dict[key]) > 1:
					nt = self.my_dict[key]
					new_codon = key[0] + self.rules_dict[temp] + key[1]
					new_list.append(new_codon)
				else:
					nt = self.my_dict[key]
					new_codon = key[0] + self.my_dict[key] + key[1]
					new_list.append(new_codon)
			else:
				if len(self.my_dict[key]) > 1:
					new_codon =  key + self.rules_dict[temp]
					new_list.append(new_codon)
				else:
					new_codon = key + self.my_dict[key]
					new_list.append(new_codon)
		return new_list

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
	temp_dict = {'Codon' : '', 'Frequency' : 0}
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

def CalcSum(filtered_dict):
	"""Calculates the total number of codons Available
	
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
		The sum total of all codons left after user specified filters are
		applied

	Examples
	--------
	CalcSum(filtered_dict)
	"""
	total = 0
	for key in filtered_dict:
		total += len(filtered_dict[key])
	return total

def BuildCodonCount(new_dict):
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
	codon_count : int
		The sum of the number of codons for each amino acid (remaining after
		user specified codons have been removed)
	"""
	codon_count = []
	for key in new_dict:
		codon_count.append(len(new_dict[key]))
	return codon_count

def BuildEmptyList(new_dict):
	"""Builds a list containing a 0 at each index for each amino acid that the
	user wants to keep.

	Parameters
	----------
	new_dict : dict 
		This is the dictionary returned by either RemoveCodonByRank or 
		ByUsage. The dictionary formatted the same as EditUsageDict(). 
		Dictionary of lists of dictionaries except that the codons with 
		usage frequency below user specified rank or usage have been removed

	Returns
	-------
	empty_list : list
		List that is the same length as the input dictionary. Every index 
		contains a 0.
	"""
	empty_list = []
	for i in range(len(new_dict)):
		empty_list.append(0)
	return empty_list

def RemoveCodonBy():
	"""Ask user whether they want to remove codons by rank or by usage. 
	The script checks for errors in user input (only r, R, u, or U are allowed)

	Parameters
	----------
	none

	Returns
	-------
	selection.upper() : str
		The string corresponding to the user input. This will always output 
		an 'R' or 'U'

	Examples
	--------
	>>> selection = RemoveCodonBy()
	"""
	while True:
		try:
			selection = raw_input("Remove codon by [R]ank or [U]sage?")
			if selection.upper() == 'U' or selection.upper() == 'R':
				return selection.upper()
			else: 
				raise ValueError()
		except ValueError:
			print("Invalid entry. You must enter either 'R' or 'U'.")

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
	>>> RemoveLowCodons(threshold, filtered_dict)
	"""
	new_dict = {}
	for key1 in filtered_dict:
		temp_list = []
		for item in filtered_dict[key1]:
			for key2 in item:
				if float(item[key2]) > threshold:
					temp_list.append(item)
				else:
					pass
		new_dict[key1] = temp_list
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
		temp_list = []
		if len(sorted_dict[key]) > rank:
			for i in range(rank):
				temp_list.append(sorted_dict[key][i])
			new_dict[key] = temp_list
		else:
			new_dict[key] = sorted_dict[key]
	return new_dict

def ByUsage(filtered_dict):
	"""This script is called when the user decides to remove codons by usage
	frequency. To determine the minimum usage frequency that can be accepted
	as input without inadvertently omitting codons, the script calls 
	FindMinimumThreshold. Then, the script prompts the user for a cutoff 
	threshold. If the entry passes error checking, the threshold is passed
	to RemoveLowCodons.

	Parameters
	----------
	filtered_dict : dict
		Dictionary formatted in the same way as EditUsageDict(). Dictionary of 
		lists of dictionaries for codon usage. Technically, any 
		dictionary that has single letter amino acid symbols as keys would
		work

	Returns
	-------
	new_dict : dict
		The script accepts user input, checks for an acceptable entry (must
		be below a stated max as determined in FindMinimumThreshold), and 
		funnels the entry to RemoveLowCodons, and returns the new_dict from 
		RemoveLowCodons

	Examples
	--------
	>>> selection = RemoveCodonBy()
	>>> if selection == 'R':
	>>> 	ByRank(filtered_dict)
	>>> else:
	>>> 	ByUsage(filtered_dict)
	"""
	min_threshold = FindMinimumThreshold(filtered_dict)
	while True:
		try:
			threshold = float(raw_input("Set usage frequency threshold: " +
								" (must be below: " +
								str(min_threshold) + ")"))
			if threshold < min_threshold:
				return RemoveLowCodons(threshold, filtered_dict)
				break
			else:
				raise ValueError()
		except ValueError:
			print("Invalid entry. Set usage frequency threshold: (must be "
					+ "below: " + str(min_threshold) + ")")

def ByRank(sorted_dict):
	"""This script is called when the user decides to remove codons by rank. 
	User selection is then passed to RemoveCodonByRank.

	Parameters
	----------
	sorted_dict : dict
		Dictionary formatted in the same way as EditUsageDict(). Dictionary of 
		lists of dictionaries for codon usage. Technically, any 
		dictionary that has single letter amino acid symbols as keys would
		work

	Returns
	-------
	new_dict : dict
		The script accepts user input, funnels the entry to RemoveCodonByRank,
		and returns the new_dict from RemoveCodonByRank

	Examples
	--------
	>>> selection = RemoveCodonBy()
	>>> if selection == 'R':
	>>> 	ByRank(filtered_dict)
	>>> else:
	>>> 	ByUsage(filtered_dict)
	"""
	rank = int(raw_input("Set codon rank threshold: "))
	return RemoveCodonByRank(rank, sorted_dict)

def SetRedundancy():
	redundancy = int(raw_input("Set redundancy" + 
									" (0 for no redundancy at all): "))
	return redundancy

def CalcTotCombinations(combinations, codon_count, new_dict, redundancy):
	tot_combinations = (combinations * 
						(codon_count - len(new_dict))**redundancy)
	return tot_combinations

def SetProcesses():
	processes = int(raw_input("Number of thread to run (default 1): "))
	return processes

def DoWork(idx, processes, empty_list, new_dict, redundancy, rules_dict, tot_combinations, GlobalStart):
	"""
	Parameters
	----------
	idx : int
		probably short for index. this is the process number we are on
	"""
	print("Thread " + str(processes) + " starting")
	BestReduceSize = 20
	BestRatio = 0
	BestIndex = 0
	StartTime = time()
	t = 0
	stop = 0
	while stop == 0:
		if t % processes == idx:
			codons, ratios = CreateListFromIndex(empty_list, new_dict)
			if redundancy != 0:
				pass
			else:
				recursive = Recursive(codons, rules_dict)
				reduced_list = recursive.Reduce()
				total_usage_frequency = 0
				for frequency in ratios:
					total_usage_frequency += float(frequency)
				if len(reduced_list) <= BestReduceSize and total_usage_frequency > BestRatio:
					BestList = [codons, ratios]
					BestReduceSize = len(reduced_list)
					BestIndex = t 
					BestRatio = total_usage_frequency
					BestZ = empty_list
		#print report every 1000 iter
		if t % 1000 == 0:
			EndTime = time()
			print("thread " + str(processes) + 
					" finished " + 
					str(int(100 * t/tot_combinations)) + 
					" % @ " + 
					str(int((time()- GlobalStart) * 1000)) +
					" ms Best Size: " +
					str(BestReduceSize) +
					", Best Index: " +
					str(BestIndex) +
					", Best Ratio: " +
					str(BestRatio))
			stop = 1
		#advance the index


def CreateListFromIndex(empty_list, new_dict):
	codons = []
	ratios = []
	i = 0
	for key1 in new_dict:
		for key2 in new_dict[key1][i]:
			codons.append(key2)
			ratios.append(new_dict[key1][empty_list[i]][key2])
	return codons, ratios

def main():
	usage_dict = BuildUsageDict()
	sorted_dict = SortUsageDict(usage_dict)
	rules_dict = BuildRulesDict()
	print("Available amino acids (count: " + str(len(sorted_dict)) + 
		"; X represents stop codons)")
	AA_list = []
	for key in sorted_dict:
		AA_list.append(key)
	print ','.join(AA_list)
	
	selection = GetUserSelection(sorted_dict)
	filtered_dict = EditUsageDict(selection, sorted_dict)

	combinations = CalcCombinations(sorted_dict)
	print 'Total combinations: ', combinations
	selection = RemoveCodonBy()
	if selection == 'R':
		new_dict = ByRank(sorted_dict)
	else:
		new_dict = ByUsage(sorted_dict)

	#NumOfThreads = 3

	combinations = CalcCombinations(new_dict)

	print("Total combinations after removing low usage codons = " +
			str(combinations))
	codon_sum = CalcSum(new_dict)
	codon_count = BuildCodonCount(new_dict)
	empty_list = BuildEmptyList(new_dict)

	redundancy = SetRedundancy()
	tot_combinations = CalcTotCombinations(combinations, 
											codon_sum, 
											new_dict, 
											redundancy)

	print("Total combinations including redundancy = " + str(tot_combinations))

	#codon_list = BestList(new_dict)
	#temp_dict, codon_list = NextBestList(codon_list, in_use)
	#recursive = Recursive(codon_list, rules_dict)

	processes = SetProcesses()
	idx = 0 # this will change to index loop when multiprocessing is added
	GlobalStart = time()
	DoWork(idx, processes, empty_list, new_dict, redundancy, rules_dict, tot_combinations, GlobalStart)
	#codes, ratios = CreateListFromIndex(empty_list, new_dict)
	

		






	#InUse_dict = ReformatUsageDict(filtered_dict)
	#codon_list = BestList(filtered_dict)
	#print('List (' + str(len(codon_list)) + ')')
	#print codon_list
	
	#in_use = FlagInUse(codon_list, InUse_dict)


main()







