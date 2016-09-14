#!/usr/bin/env python3.4
# distance.py - Calculates the distance between two text files provided as command-line arguments
# usage - ./distance.py file1 file2
# Leo Gladkov, CMSC 162, Lab 2 Exercise 2

import sys
import re

def freq_count(wordlist):

    '''
    takes list of words, wordlist
    returns dictionary of word-frequency pairs based on the list
    '''

    freqs = dict.fromkeys(wordlist, 0)
    for word in wordlist:
        freqs[word] += 1
    
    return freqs

def normalize(freqs):

    '''
    takes a dictionary of word-frequency pairs, freqs
    returns the dictionary with the frequencies normalized
    '''

    s = 0
    for word in freqs:
        s += freqs[word]**2 # sum up squares of frequencies for each file

    for word in freqs:
        freqs[word] /= s**(1/2) # normalize each word's frequency

    return freqs

def distance(file_freqs):

    '''
    takes list containig normalized word-frequency dictionaries for file1 and file2, file_freqs
    file_freqs[0] is dictionary for file1, file_freqs[1] for file2
    returns text distance between file1 and file2 based these dictionaries
    '''

    # patch frequency dictionaries with 0's for words that do not appear in both files
    for i in (0,1):
        for word in file_freqs[i]:
            if word not in file_freqs[i-1]:
                file_freqs[i-1][word] = 0

    s = 0 # sum of squares of normalized frequency differencies between the files
    for word in file_freqs[0]:
        s += (file_freqs[0][word] - file_freqs[1][word])**2

    return s**(1/2)


# process the text from each argument file

words = []
for i in (1,2):
    with open(str(sys.argv[i])) as text:

        # read in the text from each file and extract the words into lists
        # sys.argv[1] is file1 and sys.argv[2] is file2
        # words[0] is word list for file1, and words[1] is word list for file2

        # split words at non-alphabetic characters
        # capitals and digits are ignored
        words.append(re.split("[^a-z]*", text.read().rstrip().lower()))


file_freqs = []
for wordlist in words:

    # file_freqs[0] is dict of normalized frequencies for file1
    # file_freqs[1] is dict of normalized frequencies for file2

    file_freqs.append(normalize(freq_count(wordlist)))
    
d = distance(file_freqs)

print("\nDistance between {0} and {1}: {2:f}\n".format(sys.argv[1], sys.argv[2], d))
