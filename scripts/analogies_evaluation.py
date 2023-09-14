# -*- coding: utf-8 -*-
"""
  Copyright [2021] [Stofnun Árna Magnússonar í íslenskum fræðum]
  
  Github located at: https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/blob/main/README.md

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
   *******************************
   Changes to the code were made to remove the b and c variables and their accompanying dependencies
   The current version of the code accepts analogies formatted with a root word and multiple answers
   to the analogy question
   *******************************
   
   
"""

import itertools as it
from gensim.models import KeyedVectors
from progress.bar import IncrementalBar
import sys

vectors = r"C:\Users\avery\Documents\GitHub\wwp_analogies_wem\models\all_texts.wordvectors"
analogies = r"C:\Users\avery\Documents\GitHub\wwp_analogies_wem\data\analogies_test.txt"



def evaluate_word_analogies_mod(analogies, vectors):
    """
    analogies = the txt file containing the analogy questions of one of the four
    top categories of IceBATS. 
    vectors = the kv file containing the vectors of the trained language model
    to be evaluated. 

    This function is heavily inspired by the function evaluate_word_analogies
    from Gensim's KeyedVectors. It starts by loading the vectors of the model to
    be used (either w2v, fastText or GloVe (GloVe vectors need to be converted 
    to w2v format)) and then evaluates the analogy questions of one of the four
    top categories of the Icelandic Bigger Analogy Test Set, IceBATS, using the
    vector offset method provided by Gensim. Each of the 10 subcategories is 
    evaluated individually as well as the category as a whole. The function 
    prints the evaluations for each subcategory to the console. It returns the 
    total evaluation score of the category. It also keeps track of the proportion 
    of questions that contain out-of-vocabulary (OOV) words and prints it to 
    the console.
    
    The biggest deviation from the original Gensim function is that this modified
    version allows for multiple possible answers to an analogy question. For example,
    in the question 'snow is for white is like grass is for what?', the answer could
    be green, yellow or brown, depending on the condition of the grass. This function
    therefore iterates through every possible quadruple combination from multiple
    options (when provided) and if the predicted outcome is the same as one of the
    options, the question is considered to be correctly answered. Likewise, when
    checking for OOV words within the question, the OOV count is only raised if 
    all of the possible combinations include OOV words. We also drop the condition
    that the answer d to a question a:b::c:d cannot be one of the a, b and c words
    as it can be the case that the most correct answer is to be found within that
    group of words (e.g. 'USA is to English is like Britain is to what?')."""

    print('Starting analogy evaluations using %s. Loading model...' % analogies)
    language_model = KeyedVectors.load(vectors)

    ok_keys = language_model.index_to_key 

    ok_vocab = {k.upper(): language_model.get_index(k) for k in reversed(ok_keys)} # the vocabulary of the model
    oov = 0
    quadruplets_no = 0

    sections, section = [], None

    with open(analogies, encoding='utf8') as analogs:
        filebar = IncrementalBar('Performing analogy evaluations', max = 24510)
        for line in analogs:
            if line.startswith(': '): # the subcategories are seperated here
                name_section = line.split(':')[1]
                if section:
                    sections.append(section)
                section = {'section': line.lstrip(': ').strip(), 'correct': [], 'incorrect': []}
            
            else:    
                a, expected = [word.upper() for word in line.split()] # convert all words to uppercase to avoid case variations

                a = [a]
                
                expected = expected.split('/')

                combo = list(it.product(a, expected)) # all possible quadruple combinations 
                quadruplets_no += 1 
                filebar.next()
                sys.stdout.flush()
                not_ok = 0 # the quadruple contains an OOV word
                right = False
                for i in combo:
                    a, expected = i
                    if len(a) > 0 and len(expected) > 0: # don't include quadruples containing an empty string
                        if a not in ok_vocab or expected not in ok_vocab:
                            not_ok += 1
                        else:
                            original_key_to_index = language_model.key_to_index
                            language_model.key_to_index = ok_vocab
                            predicted = None

                            sims = language_model.most_similar(positive=[a], topn=15, restrict_vocab=3000000000) # the restrict_vocab is an aribtrary high number
                            language_model.key_to_index = original_key_to_index
                            for element in sims:
                                predicted = element[0].upper() 
                                if predicted in ok_vocab:
                                    if predicted == expected:
                                        right = True
                
                    if right:
                        break
                if len(combo) == not_ok: # if the number of possible combinations is the same as the quadruples containing OOV words, the question is void
                    oov += 1   
                    # print(line.rstrip()) # if desired, print out the analogy questions containing OOV words
                if right:
                    section['correct'].append((a, expected))
                else:
                    section['incorrect'].append((a, expected))
        
        if section:
            sections.append(section)
            
    total = 0
    total_correct = 0
    filebar.finish()
    for section in sections:
        correct, incorrect = len(section['correct']), len(section['incorrect'])
        if correct + incorrect == 0: # avoid dividing by zero
            score = 0
        else:
            score = correct / (correct + incorrect)
        
        subcat_score = list(section.items())[0], score, correct,"/",(correct + incorrect)
        print(subcat_score)
        
        total += (correct+incorrect)
        total_correct += correct    
    
    oov_ratio = oov/ quadruplets_no         
    print('Out Of Vocabulary rate: ', oov_ratio)

    total_score = total_correct/total
    print('Total category score: ', total_score)

    return total_score


if __name__ == "__main__":
    pass