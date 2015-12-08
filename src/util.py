"""
I/O utils (:mod:`skeng.io.util`)
================================

.. currentmodule:: skeng.io.util

This module provides utility functions to deal with files and I/O in
general.

Functions
---------

class FileHandlers
	methods = [
		search_directory,
		find_files,
		filter_files,
		clean,
		build_dict]
	
"""
import os
from collections import defaultdict

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

def BuildUsageDict(filename):
    """
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
	"""

    try:
        fhandle = open(os.path.join(os.getcwd(),'codon_tables',filename),'rU')
        lines = fhandle.readlines()
        fhandle.close()

    except:
        raise

    usage_dict = defaultdict(list)

    for line in lines[1:]:
        tokens = line.strip().split('\t')
        codon = tokens[0]
        frequency = float(tokens[2])
        residue = tokens[1]

        usage_dict[residue].append((codon, frequency))

    for residue in usage_dict:
        usage_dict[residue] = sorted(usage_dict[residue], key = lambda x: x[1], reverse=True)

    return usage_dict

def BuildCodonDict(usage_dict):
	"""
	-------
	codon_dict: dict
		Dictionary describing usage, rank, and aa for each codon. Dictionary has the
		following structure:
		{
			TTT: (1, 0.58, F), 
			TTC: (2, 0.42, F),
			TTA: (1, 0.14, L),
			TTG: (2, 0.13, L),
			CTT: (3, 0.12, L),
			CTC: (4, 0.1, L),
			...
			...
			...
			GGG: (4, 0.15, G)
		}
	--------
	"""
	codon_dict = {}
	
	for residue in usage_dict:
		for i in range(len(usage_dict[residue])):
			codon_dict[usage_dict[residue][i][0]] = (str(i + 1), usage_dict[residue][i][1], residue)
	return codon_dict

def BuildRulesDict(rule_file):
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

    """

    try:
        fhandle = open(os.path.join(os.getcwd(),'rules',rule_file),'rU')
        lines = fhandle.readlines()
        fhandle.close()
    except:
        raise

    rules_dict = {}
    inverse_dict = {}
    for line in lines[1:]:

        tokens = line.strip().split('\t')

        code = tokens[0]
        replacements = ''.join(tokens[1:len(tokens)])

        rules_dict[code] = replacements
        inverse_dict[replacements] = code

    return inverse_dict, rules_dict

class FileHandlers:
	def __init__(self):
		self.directory = os.getcwd()
		self.file_paths = []
		self.new_file_list = []
		self.filtered_list = []


	def search_directory(self):
		"""Search current working directory for files
		
		Useful for finding all files in the current directory of a particular 
		type

		Parameters
		----------
		none

		Returns
		-------
		list
			List of strings. Each string is the root path to each file in the 
			current working directory 

    	Examples
    	--------
    	>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> print file_paths
	
		"""
		for root, self.directory, file_list in os.walk(self.directory):
			for file_name in file_list:
				path = root + os.sep + file_name
				self.file_paths.append(path)
		return self.file_paths


	def find_files(self, file_list, extension):
		"""Find all files with a specified extension (.txt, .png, .py, etc)

		Useful for getting particular files before parsing

		Parameters
		----------
		file_list: list
			List of strings to loop through. Each string corresponds to a file
			path.
		extension: string
			String corresponding to the file extension to search for.

		Returns
		-------
		list
			List of strings. Each string is the root path to each file within
			the current working directory that also contains the specified
			file extension. 

		Examples
		--------
		>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> fasta_files = file_handlers.find_files(file_paths, 'fasta')
    	>>> print fasta_files
		"""
		self.new_file_list = []
		for file_path in file_list:
			new_list = file_path.split('.')
			if new_list[-1] == extension:
				self.new_file_list.append(file_path)
			else:
				pass
		return self.new_file_list

	def get_file_name(file_path):
		"""Retrieve the file name from a sting corresponding to the file path

		Useful for printing out file names

		Parameters
		----------
		file_path: string
			String corresponds to a file

		Returns
		-------
		string
			String corresponds to region of the input string following the 
			last backslash character 

		Examples
		--------
		>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> fasta_files = file_handlers.find_files(file_paths, 'fasta')
    	>>> for i in range(len(fasta_files)):
    	...    print get_file_name(fasta_files[i])
		"""
		path_as_list = file_path.split('/')
		return path_as_list[-1]


	def filter_files(self, file_list, character):
		"""Filter a list of files by excluding all files that contain a
		particular character.

		Useful if you know that a certain file will never contain a particular
		character on the first line. For example you may want to filter out
		all .txt files in a list that do not contain \t character on the first 
		line and keep all the .txt files that contain tab delimited format

		Parameters
		----------
		file_list: list
			List of strings. Each string is the root path to the files staged
			for filtering
		character: string
			String form of character that will be searched for. i.e. if you
			want to filter out all files that do not contain tab delimited
			format, then character = '\t'

		Returns
		-------
		list
			List of strings. Each string is the root path to each file within
			the current working directory that does not contain the specified
			character. 

		Examples
		--------
		>>> file_handlers = FileHandlers()
		>>> file_paths = file_handlers.search_directory()
		>>> txt_files = file_handlers.find_files(file_paths, 'txt')
		>>> files_to_annotate = file_handlers.filter_files(txt_files, '\t')
		"""
		for file in file_list:
			for line in open(file):
				if '\t' not in line:
					break
				else:
					self.filtered_list.append(file)
					break
		return self.filtered_list


	def clean(self, values):
		"""Removes whitespace (including \n) from front and back of items in a 
		list.

		Useful for parsing csv files

		Parameters
		----------
		values: list
			List of strings that need to be cleaned of whitespace on front and
			back

		Returns
		-------
		list
			List of strings with no whitespace at beginning or end of string.
			Will not contain \n characters at beginning or end of string.

		Examples
		--------
		>>> test_file = '/path/to/test.csv'
		>>> for line in open(test_file):
		... 	file_handlers = FileHandlers()
		... 	fields = line.split(",")
		... 	print fields
		... 	cleaned = file_handlers.clean(fields)
		... 	print cleaned
		"""
		cleaned = []
		for field in values:
			cleaned.append(field.strip())  # strip() takes out white space from front and back of line
		return(cleaned)
