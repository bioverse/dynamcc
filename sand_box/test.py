def test4(empty_list, codon_count):
	# the best so far.
	stop = 0
	filled_codons = []
	for zero in empty_list:
		filled_codons.append(0)
	while stop == 0:
		for i in range(len(empty_list)):
			for j in range(len(empty_list[:i + 1])):
				print 'i: ', i, 'j: ', j
				while (empty_list[j] + 1) % codon_count[j] != 0:
					empty_list[j] += 1
					print empty_list
				for index, codons, k in zip(empty_list[:i + 1], codon_count[:i + 1], range(len(filled_codons[:i + 1]))):
					if index == codons - 1:
						filled_codons[k] = 1
				#print 'filled_codon tracker: ', filled_codons
				if i < len(empty_list) and all(items != 0 for items in filled_codons[:i + 1]):
					#print 'true'
					for number in range(len(empty_list[:i + 1])):
						empty_list[number] = 0
					empty_list[i + 1] = 1
				elif i == len(empty_list):
					stop = 1

				print empty_list


def test3(empty_list, codon_count):
	# the best so far.
	stop = 0
	filled_codons = []
	for zero in empty_list:
		filled_codons.append(0)
	while stop == 0:
		for i in range(len(empty_list)):
			for j in range(len(empty_list[:i + 1])):
				print 'i: ', i, 'j: ', j
				while (empty_list[j] + 1) % codon_count[j] != 0:
					empty_list[j] += 1
					print empty_list
				for index, codons, k in zip(empty_list[:i + 1], codon_count[:i + 1], range(len(filled_codons[:i + 1]))):
					if index == codons - 1:
						filled_codons[k] = 1
				#print 'filled_codon tracker: ', filled_codons
				if i < len(empty_list) and all(items != 0 for items in filled_codons[:i + 1]):
					#print 'true'
					for number in range(len(empty_list[:i + 1])):
						empty_list[number] = 0
					empty_list[i + 1] = 1
				elif i == len(empty_list):
					stop = 1

				print empty_list


def test2(empty_list, codon_count):
	stop = 0
	filled_codons = []
	for zero in empty_list:
		filled_codons.append(0)
	while stop == 0:
		for i in range(len(empty_list)):
			for j in range(len(empty_list[:i])):
				#print 'i: ', i, 'j: ', j
				while (empty_list[j] + 1) % codon_count[j] != 0:
					empty_list[j] += 1
					print empty_list
				for index, codons, k in zip(empty_list[:i + 1], codon_count[:i + 1], range(len(filled_codons[:i + 1]))):
					if index == codons - 1:
						filled_codons[k] = 1		
				if i < len(empty_list) and all(items != 0 for items in filled_codons[:i]):
					#print 'filled_codon tracker: ', filled_codons
					for number in range(len(empty_list[:i])):
						empty_list[number] = 0
					#empty_list[i] = 1			
				elif i == len(empty_list):
					empty_list[i] = 1
			print 'end'
			print empty_list

			if i == len(empty_list):
				stop = 1




def test(empty_list, codon_count):
	stop = 0
	while stop == 0:
		for i in range(len(empty_list)):
			print 'increment i:', i
			print 'codon_count[i]:', codon_count[i]
			j = 0
			print 'reset j = 0'
			while j < i + 1:
			#for j in range(0, i + 1):
				print 'it is true: j < i + 1'
				print 'codon_count[j]', codon_count[j]
				if (empty_list[j] + 1) % codon_count[j] != 0:
					print 'before iteration: '
					print 'i: ', i, 'j: ', j
					print 'empty_list', empty_list
					
					empty_list[j] += 1
					
					print 'after empty_list[j] += 1: '
					print 'i: ', i, 'j: ', j
					print 'empty_list', empty_list
				else:
					print 'false:'
					#print 'reset empty_list[j] = 0'
					#empty_list[j] = 0
					print 'increment j += 1'
					j += 1
					if i < len(empty_list):
						print 'i < len(empty_list)'
						print 'set i + 1 = 1 and all other numbers in list = 0'
						empty_list[i + 1] = 1
						for number in range(len(empty_list[:i + 1])):
							empty_list[number] = 0
					elif i == len(empty_list):
						empty_list[i] = 1
					print 'after iteration: '
					print 'i: ', i, 'j: ', j
					print 'empty_list', empty_list
				
				if i == len(empty_list):
					stop = 1




def main():
	empty_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	codon_count = [3, 2, 2, 3, 2, 3, 2, 2, 1, 3, 2, 2, 3, 3, 3, 3, 1, 3, 2, 3]
	test4(empty_list, codon_count)

main()