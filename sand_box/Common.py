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
	"""Find the codon in flag_InUse with the highest Frequency value that is
	not currently InUse. Add this Codon to best_list. Return the updated list.
	"""
	temp_dict = {'Codon' : '', 'Frequency' : 0}
	for key in InUse:
		for item in InUse[key]:
			if item['Frequency'] > temp_dict['Frequency'] and item['InUse'] != 1:
				temp_dict['Frequency'] = item['Frequency']
				temp_dict['Codon'] = item['Codon']
	best_list.append(temp_dict['Codon'])
	return temp_dict, best_list

def TestTempDict(temp_dict):
	"""Return 0 if temp_dict 'Codon' is empty string and return 1 if not an
	empty string
	"""
	for key in temp_dict:
		if temp_dict['Codon'] == '':
			return 0
		else:
			return 1


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
	InUse_dict = ReformatUsageDict(filtered_dict)
	#best_list = BestList(filtered_dict)
	#print('List (' + str(len(best_list)) + ')')
	#print best_list
	codon_list = BestList(filtered_dict)
	print('List (' + str(len(codon_list)) + ')')
	print codon_list
	
	#in_use = FlagInUse(best_list, InUse_dict)
	in_use = FlagInUse(codon_list, InUse_dict)
	
	#recursive = Recursive(best_list, rules_dict)
	#compressed_list = recursive.FindMinList(best_list)
	#print('Reduced List (' + str(len(compressed_list)) + ')')
	#print compressed_list

	recursive = Recursive(codon_list, rules_dict)
	compressed_list = recursive.FindMinList(codon_list)
	print('Reduced List (' + str(len(compressed_list)) + ')')
	print compressed_list
	
	#temp_dict, next_best_list = NextBestList(best_list, in_use) 
	#in_use = FlagInUse(next_best_list, in_use)
	#print('List (' + str(len(next_best_list)) + ')')
	#print next_best_list

	temp_dict, codon_list = NextBestList(codon_list, in_use) 
	in_use = FlagInUse(codon_list, in_use)
	print('List (' + str(len(codon_list)) + ')')
	print codon_list
	recursive = Recursive(codon_list, rules_dict)
	compressed_list = recursive.FindMinList(codon_list)
	print('Reduced List (' + str(len(compressed_list)) + ')')
	print compressed_list


	while TestTempDict(temp_dict) == 1:
		temp_dict, codon_list = NextBestList(codon_list, in_use) 
		in_use = FlagInUse(codon_list, in_use)
		print('List (' + str(len(codon_list)) + ')')
		print codon_list
		recursive = Recursive(codon_list, rules_dict)
		compressed_list = recursive.FindMinList(codon_list)
		print('Reduced List (' + str(len(compressed_list)) + ')')
		print compressed_list

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













