# -*- coding: utf-8 -*-
"""


@author: avery
"""

import re                                   # for regular expressions
import os                                   # to look up operating system-based info
import string                               # to do fancy things with strings
import glob                                 # to locate a specific file type
from pathlib import Path                    # to access files in other directories   
import pandas as pd                         # to sort and organize data
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

dirpath = r'C:\\Users\\avery\\Desktop\\text_corpora' # get file path (you can change this)
file_type = ".txt" # if your data is not in a plain text format, you can change this
filenames = []
data = []

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

# this for loop then goes through the list of files, reads them, and then adds the text to a list
for filename in filenames:
    with open(filename, encoding='utf-8') as afile:
        print(filename)
        data.append(afile.read()) # read the file and then add it to the list
        afile.close() # close the file when you're done
        
        

 
stop_words = set(stopwords.words('english'))
 

 
        
def clean_text(text):       
    # lower case
    tokens = text.split()
    tokens = [t.lower() for t in tokens]

    # remove punctuation
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    tokens = [re_punc.sub('', token) for token in tokens]

    # only include tokens that aren't numbers
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [w for w in tokens if not w in stop_words]
    
    for w in tokens:
        if w not in stop_words:
            return w
            
data_clean = []
for x in data:
    data_clean.append(clean_text(x))


counted_words = Counter(data_clean)
top_words = counted_words.most_common(30) # 30 most common
least_common = counted_words.most_common()[:-30-1:-1] # 30 least common