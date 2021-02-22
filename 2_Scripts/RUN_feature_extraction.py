# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:51:47 2017

@author: jsuter

Project: Language Level Analysis and Classification
Seminar "Educational Assessment for Language Technology" 
WS 2015/16, Magdalena Wolska

Julia Suter, January 2018

-----------------------------------------------------------------

processing_texts.py

- get input texts for each level (stored in nested directories)
- get parsed sentences
- get desired fragment of sentences, or all (depending on version)
- extract features (through module fe:language_level_feature_extraction)
- write results into output dir 

"""

# Import Statements
import os
import shutil
import language_level_feature_extraction as fe  # feature extraction module

# Settings
split_into_5_sents_fragments = True

truncated_to_5_sents = False
middle_part = False

if split_into_5_sents_fragments:
    middle_part = False

# default: False
# --> Language Level Classifications
literature_set = False
# use only 10 sentences
short = True

# From where to load data
data_dir = '../1_Text_collections/Language_Levels/'

# Set output directory based on version

if truncated_to_5_sents:
    if middle_part:
        output_dir = '../3_Text_features/Features_truncated_middle/'
    else:
        output_dir = '../3_Text_features/Features_truncated_beginning/'
else:
    output_dir = '../3_Text_features/Features/'
    
if split_into_5_sents_fragments:
    output_dir = '../3_Text_features/Features_5sents_chunks/'

if literature_set:
    data_dir = '../1_Text_collections/Literature/'

    if short:
        output_dir = '../3_Text_features/Literature_Features_short/'
    else:
        output_dir = '../3_Text_features/Literature_Features/'


print(output_dir)

# if output directory does not yet exist, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# whether or not to overwrite existing files
overwrite_existing_dirs = False

# for each directory in data dir ([A1, A2, B1, B2] or authors)
for i, directory in enumerate(os.listdir(data_dir)):
    
    print(directory)

    # check whether output dir already exists
    if os.path.exists(output_dir + directory):

        # if not overwriting mode, ask whether existing dir should be overwritten
        if not overwrite_existing_dirs:
            answer = input('Do you want to overwrite the existing folder? ' + output_dir + directory+'\n')

            # yes: enter overwriting mode
            if not answer.startswith('n'):
                overwrite_existing_dirs = True
            # no: skip this dir
            else:
                continue
    # if dir does not exist yet, create it
    else:
        os.makedirs(output_dir + directory)

    # in overwriting mode, always overwrite folders
    if overwrite_existing_dirs:
        shutil.rmtree(output_dir + directory)
        os.makedirs(output_dir + directory)

    # for file in each dir
    for file in os.listdir(data_dir+directory):       

            print(data_dir+directory+'/'+file)
            print(file)
          
            # set file path
            file_path = data_dir+directory+'/'+file
            
            if literature_set:
                sentences = fe.get_sentences(file_path, True)

                if short:
                    # Only 10 sentences each for "short"
                    sentences = sentences[:10]

            else:                
                # get parsed sentences
                sentences = fe.get_sentences(file_path, True)

            # if truncated version
            if truncated_to_5_sents:
                
                # get number of sents
                n_sents = len(sentences)
                
                # if middle part, text has to be longer than 5 sents
                if middle_part:                    
                    if len(sentences)<5:
                        continue                    
                    sentences = sentences[(n_sents//2)-2:(n_sents//2)+3]
                
                # if starting part, just take first 5 sents (could be less)
                else:
                    sentences = sentences[:5]
               
          
            # increase number of samples by taking 5 sent fragments
            if split_into_5_sents_fragments:

                # discard if fewer than 5 sents                                
                if len(sentences)<5:
                    continue
                            
                # get number of sents and possible splits
                n_sents = len(sentences)                       
                splits = int(n_sents/5)
                
                
                # get chunks of 5 sentences
                for j,i in enumerate(range(0,n_sents,5)):
                    
                    # relevant sentences
                    rel_sentences = sentences[i:i+5]    
                    
                    # discard if fewer than 5 sents
                    if len(rel_sentences)<5:
                        continue
                    
                    # parse texts and process them (feature extraction)
                    parsed_text =  fe.get_sentence_token_information(rel_sentences)                
                    fe.process_text(parsed_text, output_dir+directory+'/'+file[:-4]+'_'+str(j)+'.csv')
                    
            # default version       
            else:              
                      
                # parse and process texts (feature extraction)
                parsed_text =  fe.get_sentence_token_information(sentences)                
                fe.process_text(parsed_text, output_dir+directory+'/'+file[:-4]+'.csv')
            