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

def main():
	usage_dict = BuildUsageDict()
	sorted_dict = SortUsageDict(usage_dict)
	#print sorted_dict
	rules_dict = BuildRulesDict()
	#print rules_dict
	print("Available amino acids (count: " + str(len(sorted_dict)) + 
		"; X represents stop codons)")
	AA_list = []
	for key in sorted_dict:
		AA_list.append(key)
	print ','.join(AA_list)
	selection = GetUserSelection(sorted_dict)
	print selection

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

"""













