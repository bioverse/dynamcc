#!/opt/local/bin/python2.7

"""
Copyright (c) 2019, Rahil Wazir, Gur Pines, Assaf Pines
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


def HammingDistance(codonA, codonB):
    """Find hamming distance between two Codons

    Parameters
    ----------
    codonA (str): Codon to compare from

    codonB (str): Codon to compare with

    Returns
    -------
    int: hamming distance

    """

    codonALen = len(codonA)
    codonBLen = len(codonB)

    if codonALen != codonBLen:
        raise ValueError("Codons must be of equal length")

    outerCount = 0

    for i in range(codonALen):
        if codonA[i] != codonB[i]:
            outerCount += 1

    return outerCount


def TargetHammingDistance(codonA, codonB, distance):
    """Check if targetted hamming distance is in range between two Codons

    Parameters
    ----------
    codonA (str): Codon to compare from

    codonB (str): Codon to compare with

    distance (int): Base distance to be expected between the two Codons

    Returns
    -------
    bool: Is hamming distance in range

    """

    distance = int(distance)
    proton_engineering_bases = [2, 3]
    natural_mutation_base = 1
    hamming_distance = HammingDistance(codonA, codonB)

    if hamming_distance in proton_engineering_bases and distance in proton_engineering_bases:
        return True

    if distance == natural_mutation_base and hamming_distance == natural_mutation_base:
        return True

    return False
