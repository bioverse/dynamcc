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

def GetDataFiles():
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
	>>> all_files = GetDataFiles()
	"""
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	files = file_handlers.find_files(file_paths, 'txt')
	return files
	
def GetUserSelection(files):
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
	>>> files = GetDataFiles()
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

def LoadData():
	file_handlers = FileHandlers()
	all_files = GetDataFiles()
	selection_int, file_path, file_name = GetUserSelection(all_files)
	amino_dict = {}
	try:
		for line in open(file_path):
			fields = line.split("\t")
			print fields
			cleaned = file_handlers.clean(fields)
			print cleaned
	except IOError:
		print("An error occurred while trying to load the data file." +
		"Make sure the file is located in your current working directory.")



"""
Next steps...
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


"""

def main():
	LoadData()

main()















