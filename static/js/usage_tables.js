var ecoli = {
	"F" : {"TTT": 0.58, "TTC": 0.42},
	"L" : {"CTG": 0.47, "TTA": 0.14, "TTG": 0.13, "CTT": 0.12, "CTC": 0.1, "CTA": 0.04},
	"I" : {"ATT": 0.49, "ATC": 0.39, "ATA": 0.11},
	"M" : {"ATG": 1},
	"V" : {"GTG": 0.35, "GTT": 0.28, "GTC": 0.2, "GTA": 0.17},
	"S" : {"AGC": 0.25, "TCT": 0.17, "AGT": 0.16, "TCC": 0.15, "TCA": 0.14, "TCG": 0.14},
	"P" : {"CCG": 0.49, "CCA": 0.2, "CCT": 0.18, "CCC": 0.13},
	"T": {"ACC": 0.4, "ACG": 0.25, "ACT": 0.19, "ACA": 0.17},
	"A": {"GCG": 0.33, "GCC": 0.26, "GCA": 0.23, "GCT": 0.18},
	"Y": {"TAT": 0.59, "TAC": 0.41},
	"X": {"TAA": 0.61, "TGA": 0.3, "TAG": 0.09},
	"H": {"CAT": 0.57, "CAC": 0.43},
	"Q": {"CAG": 0.66, "CAA": 0.34},
	"N": {"AAC": 0.51, "AAT": 0.49},
	"K": {"AAA": 0.74, "AAG": 0.26},
	"D": {"GAT": 0.63, "GAC": 0.37},
	"E": {"GAA": 0.68, "GAG": 0.32},
	"C": {"TGC": 0.54, "TGT": 0.46},
	"W": {"TGG": 1},
	"R": {"CGT": 0.36, "CGC": 0.36, "CGG": 0.11, "CGA": 0.07, "AGA": 0.07, "AGG": 0.04},
	"G": {"GGC": 0.37, "GGT": 0.35, "GGG": 0.15, "GGA": 0.13}
};

var ecoli_highest_usage = {
	"F" : {"TTT": 0.58},
	"L" : {"CTG": 0.47},
	"I" : {"ATT": 0.49},
	"M" : {"ATG": 1},
	"V" : {"GTG": 0.35},
	"S" : {"AGC": 0.25},
	"P" : {"CCG": 0.49},
	"T": {"ACC": 0.4},
	"A": {"GCG": 0.33},
	"Y": {"TAT": 0.59},
	"X": {"TAA": 0.61},
	"H": {"CAT": 0.57},
	"Q": {"CAG": 0.66},
	"N": {"AAC": 0.51},
	"K": {"AAA": 0.74},
	"D": {"GAT": 0.63},
	"E": {"GAA": 0.68},
	"C": {"TGC": 0.54},
	"W": {"TGG": 1},
	"R": {"CGT": 0.36},
	"G": {"GGC": 0.37}
};

var yeast = {
	"F": {"TTT": 0.59, "TTC": 0.41},
	"L": {"TTG": 0.29, "TTA": 0.28, "CTA": 0.14, "CTT": 0.13, "CTG": 0.11, "CTC": 0.06},
	"I": {"ATT": 0.46, "ATA": 0.27, "ATC": 0.26},
	"M": {"ATG": 1},
	"V": {"GTT": 0.39, "GTC": 0.21, "GTA": 0.21, "GTG": 0.19},
	"S": {"TCT": 0.26, "TCA": 0.21, "TCC": 0.16, "AGT": 0.16, "AGC": 0.11, "TCG": 0.1},
	"P": {"CCA": 0.41, "CCT": 0.31, "CCC": 0.15, "CCG": 0.12},
	"T": {"ACT": 0.35, "ACA": 0.3, "ACC": 0.22, "ACG": 0.13},
	"A": {"GCT": 0.38, "GCA": 0.29, "GCC": 0.22, "GCG": 0.11},
	"Y": {"TAT": 0.56, "TAC": 0.44},
	"X": {"TAA": 0.48, "TGA": 0.29, "TAG": 0.24},
	"H": {"CAT": 0.64, "CAC": 0.36},
	"Q": {"CAA": 0.69, "CAG": 0.31},
	"N": {"AAT": 0.59, "AAC": 0.41},
	"K": {"AAA": 0.58, "AAG": 0.42},
	"D": {"GAT": 0.65, "GAC": 0.35},
	"E": {"GAA": 0.71, "GAG": 0.29},
	"C": {"TGT": 0.63, "TGC": 0.37},
	"W": {"TGG": 1},
	"R": {"AGA": 0.48, "AGG": 0.21, "CGT": 0.15, "CGA": 0.07, "CGC": 0.06, "CGG": 0.04},
	"G": {"GGT": 0.47, "GGA": 0.22, "GGC": 0.19, "GGG": 0.12}
};

var yeast_highest_usage = {
	"F": {"TTT": 0.59},
	"L": {"TTG": 0.29},
	"I": {"ATT": 0.46},
	"M": {"ATG": 1},
	"V": {"GTT": 0.39},
	"S": {"TCT": 0.26},
	"P": {"CCA": 0.41},
	"T": {"ACT": 0.35},
	"A": {"GCT": 0.38},
	"Y": {"TAT": 0.56},
	"X": {"TAA": 0.48},
	"H": {"CAT": 0.64},
	"Q": {"CAA": 0.69},
	"N": {"AAT": 0.59},
	"K": {"AAA": 0.58},
	"D": {"GAT": 0.65},
	"E": {"GAA": 0.71},
	"C": {"TGT": 0.63},
	"W": {"TGG": 1},
	"R": {"AGA": 0.48},
	"G": {"GGT": 0.47}
};

var celegans = {
	"F": {"TTT": 0.5, "TTC": 0.5},
	"L": {"CTT": 0.24, "TTG": 0.23, "CTC": 0.17, "CTG": 0.14, "TTA": 0.12, "CTA": 0.09},
	"I": {"ATT": 0.53, "ATC": 0.31, "ATA": 0.16},
	"M": {"ATG": 1},
	"V": {"GTT": 0.39, "GTG": 0.23, "GTC": 0.22, "GTA": 0.16},
	"S": {"TCA": 0.25, "TCT": 0.21, "TCG": 0.15, "AGT": 0.15, "TCC": 0.13, "AGC": 0.1},
	"P": {"CCA": 0.53, "CCG": 0.2, "CCT": 0.18, "CCC": 0.09},
	"T": {"ACA": 0.34, "ACT": 0.33, "ACC": 0.18, "ACG": 0.15},
	"A": {"GCT": 0.36, "GCA": 0.31, "GCC": 0.2, "GCG": 0.13},
	"Y": {"TAT": 0.56, "TAC": 0.44},
	"X": {"TAA": 0.44, "TGA": 0.39, "TAG": 0.17},
	"H": {"CAT": 0.61, "CAC": 0.39},
	"Q": {"CAA": 0.66, "CAG": 0.34},
	"N": {"AAT": 0.62, "AAC": 0.38},
	"K": {"AAA": 0.59, "AAG": 0.41},
	"D": {"GAT": 0.68, "GAC": 0.33},
	"E": {"GAA": 0.62, "GAG": 0.38},
	"C": {"TGT": 0.55, "TGC": 0.45},
	"W": {"TGG": 1},
	"R": {"AGA": 0.29, "CGA": 0.23, "CGT": 0.21, "CGC": 0.1, "CGG": 0.09, "AGG": 0.08},
	"G": {"GGA": 0.59, "GGT": 0.2, "GGC": 0.12, "GGG": 0.08}
};

var celegans_highest_usage = {
	"F": {"TTT": 0.5},
	"L": {"CTT": 0.24},
	"I": {"ATT": 0.53},
	"M": {"ATG": 1},
	"V": {"GTT": 0.39},
	"S": {"TCA": 0.25},
	"P": {"CCA": 0.53},
	"T": {"ACA": 0.34},
	"A": {"GCT": 0.36},
	"Y": {"TAT": 0.56},
	"X": {"TAA": 0.44},
	"H": {"CAT": 0.61},
	"Q": {"CAA": 0.66},
	"N": {"AAT": 0.62},
	"K": {"AAA": 0.59},
	"D": {"GAT": 0.68},
	"E": {"GAA": 0.62},
	"C": {"TGT": 0.55},
	"W": {"TGG": 1},
	"R": {"AGA": 0.29},
	"G": {"GGA": 0.59}
};

var dmelanogaster = {
	"F": {"TTC": 0.63, "TTT": 0.37},
	"L": {"CTG": 0.43, "TTG": 0.18, "CTC": 0.15, "CTT": 0.1, "CTA": 0.09, "TTA": 0.05},
	"I": {"ATC": 0.47, "ATT": 0.34, "ATA": 0.19},
	"M": {"ATG": 1},
	"V": {"GTG": 0.47, "GTC": 0.24, "GTT": 0.18, "GTA": 0.11},
	"S": {"AGC": 0.25, "TCC": 0.24, "TCG": 0.2, "AGT": 0.14, "TCA": 0.09, "TCT": 0.08},
	"P": {"CCC": 0.33, "CCG": 0.29, "CCA": 0.25, "CCT": 0.13},
	"T": {"ACC": 0.38, "ACG": 0.26, "ACA": 0.19, "ACT": 0.17},
	"A": {"GCC": 0.45, "GCT": 0.19, "GCG": 0.19, "GCA": 0.17},
	"Y": {"TAC": 0.63, "TAT": 0.37},
	"X": {"TAA": 0.42, "TAG": 0.32, "TGA": 0.26},
	"H": {"CAC": 0.6, "CAT": 0.4},
	"Q": {"CAG": 0.7, "CAA": 0.3},
	"N": {"AAC": 0.56, "AAT": 0.44},
	"K": {"AAG": 0.71, "AAA": 0.29},
	"D": {"GAT": 0.53, "GAC": 0.47},
	"E": {"GAG": 0.67, "GAA": 0.33},
	"C": {"TGC": 0.71, "TGT": 0.29},
	"W": {"TGG": 1},
	"R": {"CGC": 0.33, "CGT": 0.16, "CGA": 0.15, "CGG": 0.15, "AGG": 0.11, "AGA": 0.09},
	"G": {"GGC": 0.43, "GGA": 0.29, "GGT": 0.21, "GGG": 0.07}
};

var dmelanogaster_highest_usage = {
	"F": {"TTC": 0.63},
	"L": {"CTG": 0.43},
	"I": {"ATC": 0.47},
	"M": {"ATG": 1},
	"V": {"GTG": 0.47},
	"S": {"AGC": 0.25},
	"P": {"CCC": 0.33},
	"T": {"ACC": 0.38},
	"A": {"GCC": 0.45},
	"Y": {"TAC": 0.63},
	"X": {"TAA": 0.42},
	"H": {"CAC": 0.6},
	"Q": {"CAG": 0.7},
	"N": {"AAC": 0.56},
	"K": {"AAG": 0.71},
	"D": {"GAT": 0.53},
	"E": {"GAG": 0.67},
	"C": {"TGC": 0.71},
	"W": {"TGG": 1},
	"R": {"CGC": 0.33},
	"G": {"GGC": 0.43}
};

var hsapiens = {
	"F": {"TTC": 0.55, "TTT": 0.45},
	"L": {"CTG": 0.41, "CTC": 0.2, "TTG": 0.13, "CTT": 0.13, "CTA": 0.07, "TTA": 0.07},
	"I": {"ATC": 0.48, "ATT": 0.36, "ATA": 0.16},
	"M": {"ATG": 1},
	"V": {"GTG": 0.47, "GTC": 0.24, "GTT": 0.18, "GTA": 0.11},
	"S": {"AGC": 0.24, "TCC": 0.22, "TCT": 0.18, "TCA": 0.15, "AGT": 0.15, "TCG": 0.06},
	"P": {"CCC": 0.33, "CCT": 0.28, "CCA": 0.27, "CCG": 0.11},
	"T": {"ACC": 0.36, "ACA": 0.28, "ACT": 0.24, "ACG": 0.12},
	"A": {"GCC": 0.4, "GCT": 0.26, "GCA": 0.23, "GCG": 0.11},
	"Y": {"TAC": 0.57, "TAT": 0.43},
	"X": {"TGA": 0.52, "TAA": 0.28, "TAG": 0.2},
	"H": {"CAC": 0.59, "CAT": 0.41},
	"Q": {"CAG": 0.75, "CAA": 0.25},
	"N": {"AAC": 0.54, "AAT": 0.46},
	"K": {"AAG": 0.58, "AAA": 0.42},
	"D": {"GAC": 0.54, "GAT": 0.46},
	"E": {"GAG": 0.58, "GAA": 0.42},
	"C": {"TGC": 0.55, "TGT": 0.45},
	"W": {"TGG": 1},
	"R": {"CGG": 0.21, "AGA": 0.2, "AGG": 0.2, "CGC": 0.19, "CGA": 0.11, "CGT": 0.08},
	"G": {"GGC": 0.34, "GGA": 0.25, "GGG": 0.25, "GGT": 0.16}
};

var hsapiens_highest_usage = {
	"F": {"TTC": 0.55},
	"L": {"CTG": 0.41},
	"I": {"ATC": 0.48},
	"M": {"ATG": 1},
	"V": {"GTG": 0.47},
	"S": {"AGC": 0.24},
	"P": {"CCC": 0.33},
	"T": {"ACC": 0.36},
	"A": {"GCC": 0.4},
	"Y": {"TAC": 0.57},
	"X": {"TGA": 0.52},
	"H": {"CAC": 0.59},
	"Q": {"CAG": 0.75},
	"N": {"AAC": 0.54},
	"K": {"AAG": 0.58},
	"D": {"GAC": 0.54},
	"E": {"GAG": 0.58},
	"C": {"TGC": 0.55},
	"W": {"TGG": 1},
	"R": {"CGG": 0.21},
	"G": {"GGC": 0.34}
};

var mmusculus = {
	"F": {"TTC": 0.57, "TTT": 0.43},
	"L": {"CTG": 0.39, "CTC": 0.2, "TTG": 0.13, "CTT": 0.13, "CTA": 0.08, "TTA": 0.06},
	"I": {"ATC": 0.5, "ATT": 0.34, "ATA": 0.16},
	"M": {"ATG": 1},
	"V": {"GTG": 0.46, "GTC": 0.25, "GTT": 0.17, "GTA": 0.12},
	"S": {"AGC": 0.24, "TCC": 0.22, "TCT": 0.19, "AGT": 0.15, "TCA": 0.14, "TCG": 0.05},
	"P": {"CCC": 0.31, "CCT": 0.3, "CCA": 0.28, "CCG": 0.1},
	"T": {"ACC": 0.35, "ACA": 0.29, "ACT": 0.25, "ACG": 0.11},
	"A": {"GCC": 0.38, "GCT": 0.29, "GCA": 0.23, "GCG": 0.1},
	"Y": {"TAC": 0.58, "TAT": 0.43},
	"X": {"TGA": 0.52, "TAA": 0.26, "TAG": 0.22},
	"H": {"CAC": 0.6, "CAT": 0.4},
	"Q": {"CAG": 0.75, "CAA": 0.25},
	"N": {"AAC": 0.57, "AAT": 0.43},
	"K": {"AAG": 0.61, "AAA": 0.39},
	"D": {"GAC": 0.56, "GAT": 0.44},
	"E": {"GAG": 0.6, "GAA": 0.4},
	"C": {"TGC": 0.52, "TGT": 0.48},
	"W": {"TGG": 1},
	"R": {"AGG": 0.22, "AGA": 0.21, "CGG": 0.19, "CGC": 0.18, "CGA": 0.12, "CGT": 0.09},
	"G": {"GGC": 0.33, "GGA": 0.26, "GGG": 0.23, "GGT": 0.18}
};

var mmusculus_highest_usage = {
	"F": {"TTC": 0.57},
	"L": {"CTG": 0.39},
	"I": {"ATC": 0.5},
	"M": {"ATG": 1},
	"V": {"GTG": 0.46},
	"S": {"AGC": 0.24},
	"P": {"CCC": 0.31},
	"T": {"ACC": 0.35},
	"A": {"GCC": 0.38},
	"Y": {"TAC": 0.58},
	"X": {"TGA": 0.52},
	"H": {"CAC": 0.6},
	"Q": {"CAG": 0.75},
	"N": {"AAC": 0.57},
	"K": {"AAG": 0.61},
	"D": {"GAC": 0.56},
	"E": {"GAG": 0.6},
	"C": {"TGC": 0.52},
	"W": {"TGG": 1},
	"R": {"AGG": 0.22},
	"G": {"GGC": 0.33}
};

var organism_mapping = {
	"Ecoli": ecoli, 
	"yeast": yeast, 
	"human": hsapiens, 
	"mouse": mmusculus, 
	"Dmel": dmelanogaster, 
	"Cele": celegans
};

var highest_usage_mapping = {
	"Ecoli": ecoli_highest_usage, 
	"yeast": yeast_highest_usage, 
	"human": hsapiens_highest_usage, 
	"mouse": mmusculus_highest_usage, 
	"Dmel": dmelanogaster_highest_usage, 
	"Cele": celegans_highest_usage
};



