import subprocess
import Queue
import os
import time

TEMP_DIR = os.path.join(os.getcwd(),'temp')

AAlist = set(['V','N','S','K','G','C','H','I','L','W','F','R','A','Y','P','Q','X','E','M','D','T'])

removal_methods = set(['R','U'])

AAtables = ['Data C.elegans GeneScript.txt',
            'Data D.melanogaster GeneScript.txt',
            'Data ecoli GeneScript.txt',
            'Data human GeneScript.txt',
            'Data mouse GeneScript.txt',
            'Data yeast GeneScript.txt']

AAfreq = {}

for i in range(0,len(AAtables)):

    fhandle = open(AAtables[i], 'rU')
    lines = fhandle.readlines()
    fhandle.close()

    freqdict = {}

    for line in lines [1:]:

        tokens = line.strip().split('\t')

        codon = tokens[0]
        AA = tokens[1]
        freq = tokens[2]

        freqdict[AA] = float(freq)

    AAfreq[i] = freqdict

def input_validator(data_file, removeAAs, removal_method, threshold, redundancy):

    error_dict = {}

    correct = True

    if(data_file < 0 or data_file > len(AAtables)):
        error_dict['Data Input'] = 'Invalid organism data table selected'
    #if the provided list of AAs to remove is not a subset of the list of AAs
    if(not (set(removeAAs) <= AAlist)):

        invalid = []
        for aa in removeAAs:
            if(aa not in AAlist):
                invalid.append(aa)

        error_dict['AA Input'] = 'Invalid amino acids selected for removal: ' + ','.join(invalid)

    if(removal_method not in removal_methods):

        error_dict['Removal Method Selection'] = 'Provided removal method is not recognized: %s' % removal_method

    if(removal_method == 'R' and threshold < 0):

        error_dict['Threshold Selection'] = 'Threshold input: %i is not allowed with removal method %s' % (threshold,removal_method)

    if(removal_method == 'U'):

        frequency = []

        for aa in removeAAs:
            if(data_file in AAfreq and aa in AAfreq[data_file]):
                frequency.append(AAfreq[data_file][aa])

        if(threshold > min(frequency)):

            error_dict['Threshold Selection'] = 'Threshold input: %f is not allowed with removal method %s, maximum allowed is %f' % (threshold,removal_method, min(frequency))

    if(redundancy < 0):

        error_dict['Redundancy Selection'] = 'Invalid redundancy threshold selection: %i' % redundancy

    return (error_dict == {}, error_dict)

def output(pipe):

    outputList = []

    with pipe.stdout:
        for line in iter(pipe.stdout.readline,b''):
            outputList.append(line)

    return outputList

#data file is a number 0-5
#AA is a list of amino acids
def run_codon_compression(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads):

    path = os.getcwd()
    dynamcc0 = os.path.join(path, 'DYNAMCC_0.pl')

    

    (has_errors, error_dict) = input_validator(data_file, removeAAs, removal_method, threshold, redundancy)

    if(has_errors):
        
        for key in error_dict:
            print key, error_dict[key]

        return None
    
    p = subprocess.Popen(['perl', dynamcc0], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    p.stdin.write(str(data_file) + '\n')

    #print 'communicated file choice'

    p.stdin.write(','.join(removeAAs) + '\n')

    #print 'communicated AAs to remove'

    p.stdin.write(removal_method + '\n')

    #print 'communicated removal method'

    p.stdin.write(str(threshold) + '\n')

    #print 'communicated %s threshold' % removal_method

    p.stdin.write(str(redundancy) + '\n')

    #print 'communicated desired level of redundancy'

    p.stdin.write(str(threads) +'\n')

    #print 'communicated number of threads'

    outputList = output(p)

    #for line in outputList:
    #    print line.strip()

    fhandle = open(os.path.join(TEMP_DIR,output_file_name),'w')

    for line in outputList:
        fhandle.write(line.strip() + '\n')
    fhandle.close()

    #doneQueue.add(output_file_name)
    #notify server or user of completion here, depends on server structure
    #can email the user a link to the web-page generate from CC output
    #can notify the server that the analysis is complete and to generate the page from outputList

def start_cc_thread(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads=2):

    import threading

    t = threading.Thread(target = run_codon_compression, args = (output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads))
    t.start()



#output_file_name = 'test.txt'
#start_cc_thread(output_file_name,1, ['A','X','N','W','G','V'], 'U', 0.1, 0)

