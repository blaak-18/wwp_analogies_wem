# -*- coding: utf-8 -*-
"""
This code successfully runs as of 8/22/2023 using Python 3.9.13


@author: Avery Blankenship
"""

# =============================================================================
# LIBRARY AND PACKAGE IMPORTS 
# =============================================================================

import re                                   # for regular expressions
import os                                   # to look up operating system-based info
import string                               # to do fancy things with strings
import glob                                 # to locate a specific file type
from pathlib import Path                    # to access files in other directories   
import pandas as pd                         # to sort and organize data
import nltk                                 # to access stop words
from collections import Counter             # for word counts
from nltk.corpus import stopwords           # import set of stop words
from nltk.tokenize import word_tokenize     # lets us tokenize
import csv                                  # lets us read and write CSVs


# =============================================================================
# # COMMENT OUT THE LINES BELOW IF YOU ALREADY HAVE THESE INSTALLED
# =============================================================================
nltk.download('stopwords')                  
nltk.download('punkt')

 

# =============================================================================
# LOOP THROUGH FOLDER OF CORPORA TO GET LIST OF FILENAMES AND PATHS
# =============================================================================

dirpath = r'FILE PATH TO FOLDER OF CORPORA' # get file path for corpora (you can change this)


file_type = ".txt" # if your data is not in a plain text format, you can change this
filenames = []  # this variable will hold the locations of each file

 # this for loop will run through folders and subfolders looking for a specific file type
for root, dirs, files in os.walk(dirpath, topdown=False):
   # look through all the files in the given directory
   for name in files:
       if (root + os.sep + name).endswith(file_type):
           filenames.append(os.path.join(root, name))
   # look through all the directories
   for name in dirs:
       if (root + os.sep + name).endswith(file_type):
           filenames.append(os.path.join(root, name))


# =============================================================================
# LOOP TO OPEN ONE FILE AT A TIME, CLEAN TEXT, AND COUNT WORDS
# =============================================================================

temp_count = ["test_word"]   # initiate a list to aggregate word counts in
counted_words = Counter(temp_count) # count this iniital list



# this for loop then goes through the list of files, reads them, cleans those words and removes stop words, and then counts frequencies
# crawls through the data one file at a time to preserve memory
for filename in filenames:
    
    with open(filename, encoding='utf-8') as afile: # open the first file in the set of corpora
        data = afile.read()
    
        print("opening " + filename) # print statement to let you know the file was successfully opened
        stop_words = set(stopwords.words('english')) # setting the stopwords we want to remove
        
        # this function cleans the text and removes stop words
        def clean_text(text):       
            # lower case
            tokens = text.split()
            tokens = [t.lower() for t in tokens]
    
            # remove punctuation
            re_punc = re.compile('[%s]' % re.escape(string.punctuation))
            tokens = [re_punc.sub('', token) for token in tokens]
    
            # only include tokens that aren't numbers
            tokens = [token for token in tokens if token.isalpha()]
            
            # remove stop words
            tokens = [w for w in tokens if not w in stop_words]
            
            # return the cleaned text
            return tokens
        
        
        # run the function on our current file
        data_clean = clean_text(data)
        print(filename + " has been cleaned")  # print statement letting you know that the file was successfully cleaned
        
        new_count = Counter(data_clean) # count the word frequencies in the current file
        counted_words.update(new_count) # update our aggregated count with the new file
        
        # get the top thirty most common words in the aggregated set
        top_words = counted_words.most_common(30)
        
        # get the least common thirty words in the aggregated set
        least_common = counted_words.most_common()[:-30-1:-1]
        
        # open a csv file where we can save our word counts
        # the csv file will update every time the code loops through a new file in case python runs into memory issues
        with open(r'~FILE PATH TO PUT CSV FILE IN~/CSV_FILE_NAME.CSV', 'w', encoding='utf-8') as counted_file:
            c = csv.writer(counted_file)
            # write the word counts to the csv with the headers Top 30 Words and 30 Least Common
            c.writerows([['Top 30 Words', '30 Least Common'], [top_words, least_common]])
                        
            print("CSV File Updated") # print statement to let you know that the csv file was successfully updated
       
        # we want to also save the cleaned text to a text file for later
        text_file = open("all_text_clean.txt", "a", encoding="utf-8")
        n = text_file.write(str(data_clean))
        print(filename + " saved to .txt file") # print statement to let you know that the text has been saved to a .txt file
        text_file.close() # close the text file
            
        # close the file we have open currently
        # this is important for saving memory
        afile.close()

# =============================================================================
# 
#  TO OPEN TEXT FILE OF CLEANED TEXT AND CSV FILE OF COUNTS
# =============================================================================

# open the file with the cleaned text saved to it
# filename = r"FILE PATH TO TEXT FILE OF CLEANED TEXT"
# with open(filename, encoding ='utf-8') as afile:
#     cleaned_text = afile.read()


# filename = r"FILE PATH TO CSV FILE"
# with open(filename, newline='') as csvfile:
#     word_counts = csv.reader(csvfile, delimiter=',')


# counted_words = Counter(data_file)
# top_words = counted_words.most_common(30) # 30 most common
# least_common = counted_words.most_common()[:-30-1:-1] # 30 least common



