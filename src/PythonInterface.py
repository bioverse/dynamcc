import subprocess
import Queue
import os
import time

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

TEMP_DIR = os.path.join(os.getcwd(),'temp')

AAlist = set(['V','N','S','K','G','C','H','I','L','W','F','R','A','Y','P','Q','X','E','M','D','T'])

removal_methods = set(['R','U'])

location = os.path.realpath(__file__)

path, filename = os.path.split(location)


AAtables = ['Data C.elegans GeneScript.txt',
            'Data D.melanogaster GeneScript.txt',
            'Data ecoli GeneScript.txt',
            'Data human GeneScript.txt',
            'Data mouse GeneScript.txt',
            'Data yeast GeneScript.txt']

AAtable_dict = {'celegans': 0,
                'dmelanogaster':1,
                'ecoli': 2,
                'hsapiens':3,
                'mmusculus':4,
                'scerevisiae':5}

AAfreq = {}

for i in range(0,len(AAtables)):

    fhandle = open(os.path.join(path,AAtables[i]), 'rU')
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

    if(data_file.lower() not in AAtable_dict):
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
            if(data_file in AAtable_dict and aa in AAfreq[AAtable_dict[data_file]]):
                frequency.append(AAfreq[AAtable_dict[data_file]][aa])

        if(threshold > min(frequency)):

            error_dict['Threshold Selection'] = 'Threshold input: %f is not allowed with removal method %s, maximum allowed is %f' % (threshold,removal_method, min(frequency))

    if(redundancy < 0):

        error_dict['Redundancy Selection'] = 'Invalid redundancy threshold selection: %i' % redundancy

    return (len(error_dict.keys()) == 0, error_dict)

def output(pipe):

    outputList = []

    with pipe.stdout:
        for line in iter(pipe.stdout.readline,b''):
            outputList.append(line)

    return outputList

def generate_command_line_args(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads):

    string = output_file_name + ' ' + str(data_file) + ' ' + ','.join(removeAAs) + ' ' + removal_method + ' ' + str(threshold) + ' ' + str(redundancy) + ' ' + str(threads)
    return string

def run_codon_compression_CLI(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads = 4):

    import time

    dynamcc0 = '\"' + os.path.join(os.getcwd(), 'DYNAMCC_0.pl') + '\"'

    libraries = '-I ' + '\"' + path + '\"'

    print libraries

    print dynamcc0

    (correct, error_dict) = input_validator(data_file, removeAAs, removal_method, threshold, redundancy)

    if(not correct):

        error_list = []
        
        for key in error_dict:
            error_list.append(error_dict[key])
            print (key, error_dict[key])

        return error_list

    command_line = generate_command_line_args(output_file_name, AAtable_dict[data_file], removeAAs, removal_method, threshold, redundancy, threads)

    print command_line
    
    p = subprocess.Popen('perl' + ' ' + libraries + ' ' + dynamcc0 + ' ' + command_line)

    print 'started process'
    
    p.wait()

    #read output into list

    try:

        print 'I got here!'

        fhandle = open(output_file_name,'rU')
        lines = fhandle.readlines()
        fhandle.close()

        fhandle = open(os.path.join(os.getcwd(),'temp',output_file_name),'w')

        for line in lines:
            fhandle.write(line)
        fhandle.close()

        return lines

    except:

        print 'died?'

        #raise

        return ['DYNAMCC 0 did not return any input!']
        


#data file is a number 0-5
#AA is a list of amino acids
def run_codon_compression_PIPE(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads = 4):

    import time

    dynamcc0 = os.path.join(path, 'DYNAMCC_0.pl')

    (correct, error_dict) = input_validator(data_file, removeAAs, removal_method, threshold, redundancy)

    if(not correct):

        error_list = []
        
        for key in error_dict:
            error_list.append((key, error_dict[key]))
            print (key, error_dict[key])

        return error_list
    
    p = subprocess.Popen(['perl', '-I \"' +  path + '\"', dynamcc0], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    

    p.stdin.write(str(AAtable_dict[data_file]) + '\n')

    print 'communicated file choice %s ' % str(AAtable_dict[data_file])

    p.stdin.write(','.join(removeAAs) + '\n')

    print 'communicated AAs to remove'

    p.stdin.write(removal_method + '\n')

    print 'communicated removal method'

    p.stdin.write(str(threshold) + '\n')

    print 'communicated %s threshold' % removal_method

    p.stdin.write(str(redundancy) + '\n')

    print 'communicated desired level of redundancy'

    p.stdin.write(str(threads) +'\n')


    

    print 'communicated number of threads'

    outputList = output(p)

    #for line in outputList:
    #    print line.strip()


    '''
    #fhandle = open(os.path.join(TEMP_DIR,output_file_name),'w')

    for line in outputList:
        fhandle.write(line.strip() + '\n')
    fhandle.close()
    '''

    return outputList

    #doneQueue.add(output_file_name)
    #notify server or user of completion here, depends on server structure
    #can email the user a link to the web-page generate from CC output
    #can notify the server that the analysis is complete and to generate the page from outputList

def start_cc_thread(output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads=2):

    import threading

    t = threading.Thread(target = run_codon_compression, args = (output_file_name, data_file, removeAAs, removal_method, threshold, redundancy, threads))
    t.start()



#output_file_name = 'test.txt'
#run_codon_compression_CLI(output_file_name,'ecoli', ['A','N','W','G','V','T','K'], 'U', 0.1, 0, 4)

