#!/opt/local/bin/python2.7

from util import FileHandlers

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

		print "from FindMinList: "
		print "best_list is: ", self.codon_list
		temp = self.codon_list
		print "temp is: ", temp
		reduced_list = self.Reduce()
		print "reduced is: ", reduced_list
		if temp != reduced_list:
			self.FindMinList(reduced_list)
		return self.codon_list

	def Reduce(self):
		"""Iterate through each position in the codon. At each position,
		capture the result of Grouping(int) in self.my_dict. Pass this dict to
		ListFromGroup(dict, int) and capture the result in self.codon_list. Return
		self.codon_list after interating through each position in the codon.
		
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
		print "from reduce: ", self.codon_list
		return self.codon_list

	def Grouping(self, int):
		"""Grouping initializes an empty dict
		"""
		my_dict = {}
		print "From Grouping: "
		#print best_list
		#print int
		##print "first: ", my_dict
		print "best list: ", self.codon_list
		print "int is: ", int
		for codon in self.codon_list:
			##print "second: ", my_dict
			#print "From Grouping loop 1: "
			##print "codon is: ", codon
			if int == 0:
				position = codon[int]
				remainder = codon[int+1:]
				##print "x is: ", first_position
				##print "y is: ", end_of_codon
				##print "third: ", my_dict
				InRules = 0
				##print "forth: ", my_dict
				#print rules_dict
				for key in self.rules_dict:
					##print "fifth: ", my_dict
					##print "l is: ", key
					#print "From Grouping loop 2: "
					#print key
					#print rules_dict[key]
					if self.rules_dict[key] == position:
						##print "sixth: ", my_dict
						##print "rules_dict[key] is: ", rules_dict[key]
						#my_dict[codon]
						##print "seventh: ", my_dict
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
						if remainder in self.my_dict:
							my_dict[remainder].add(key.split())
						else:
							my_dict[remainder] = set(key.split())
						InRules = 1
			else:
				position = codon[int]
				#print "position: ", position
				remainder = codon[:2]
				#print "remainder: ", remainder
				InRules = 0
				for key in self.rules_dict:
					#print "key in rules_dict: ", key
					if self.rules_dict[key] == position:
						#print "value in rules_dict", self.rules_dict[key]
						if remainder in my_dict:
							#print remainder, my_dict[remainder]
							my_dict[remainder].add(key.split())
						else:
							my_dict[remainder] = set(key.split())
						InRules = 1
			if InRules == 0:
				if remainder in my_dict:
					#print "remainder in self.my_dict"
					my_dict[remainder].add(position)
					#print my_dict[remainder]
					#print my_dict
				else:
					my_dict[remainder] = set(position)
			#print "eigth: ", my_dict
		#print my_dict
		for key in my_dict:
			my_dict[key] = ''.join(sorted(my_dict[key]))
		for key, value in my_dict.iteritems():
			print key, ":", value
		self.my_dict = my_dict
		print self.my_dict
		return self.my_dict

	def ListFromGroup(self, my_dict, int):
		print "from ListFromGroup: "
		new_list = []
		print self.my_dict
		for key in self.my_dict:
			print "key is: ", key
			print "value is: ", my_dict[key]
			temp = self.my_dict[key]
			if int == 0:
				if len(self.my_dict[key]) > 1:
					new_codon = self.rules_dict[temp] + key
					print new_codon
					new_list.append(new_codon)
				else:
					new_codon = self.my_dict[key] + key
					new_list.append(new_codon)
			elif int == 1:
				if len(self.my_dict[key]) > 1:
					nt = self.my_dict[key]
					print nt
					print self.rules_dict[temp]
					new_codon = key[0] + self.rules_dict[temp] + key[1]
					print new_codon
					new_list.append(new_codon)
				else:
					nt = self.my_dict[key]
					print nt
					new_codon = key[0] + self.my_dict[key] + key[1]
					new_list.append(new_codon)
			else:
				if len(self.my_dict[key]) > 1:
					new_codon =  key + self.rules_dict[temp]
					print new_codon
					new_list.append(new_codon)
				else:
					new_codon = key + self.my_dict[key]
					new_list.append(new_codon)
		print new_list
		return new_list

def main():
	usage_dict = BuildUsageDict()
	sorted_dict = SortUsageDict(usage_dict)
	rules_dict = BuildRulesDict()
	print rules_dict
	print("Available amino acids (count: " + str(len(sorted_dict)) + 
		"; X represents stop codons)")
	AA_list = []
	for key in sorted_dict:
		AA_list.append(key)
	print ','.join(AA_list)
	selection = GetUserSelection(sorted_dict)
	filtered_dict = EditUsageDict(selection, sorted_dict)
	best_list = BestList(filtered_dict)
	print best_list
	recursive = Recursive(best_list, rules_dict)
	recursive.FindMinList(best_list)

main()

"""
Key steps...
1. Need to create a dictionary of lists of dictionaries.
{
	F : [{TTT: 0.58}, {TTC: 0.42}],
	L : [{TTA: 0.14}, {TTG: 0.13}, {CTT: 0.12}, {CTC: 0.1}, {CTA: 0.04}, {CTG: 0.47}],
	I : [{ATT: 0.49}, {ATC: 0.39}, {ATA: 0.11}],
	...
	G : [{GGT: 0.35}, {GGC: 0.37}, {GGA: 0.13}, {GGG: 0.15}]
}

2. Then sort the lists in descending order of the values in the contained dictionaries.
For example, G would look like

	G : [{GGC: 0.37}, {GGT: 0.35}, {GGG: 0.15}, {GGA: 0.13}]

3. Build a dictionary for the "Rules.rul" file. This dictionary will have the following
format:
{
	AG 	: 	R,
	CT 	: 	Y,
	AC 	: 	M,
	GT 	: 	K,
	CG 	: 	S,
	AT 	: 	W,
	ACT : 	H,
	CGT : 	B,
	ACG : 	V
	AGT :  	D
	ACGT: 	N
}

4. Ask user which amino acids to delete, and remove these from the sorted
codon usage dictionary

5. Generate list of codons with highest frequency (using dict with deleted aa).
def BestList 

6. Pass BestList to FindMinList

"""













