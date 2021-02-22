# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:51:47 2017

@author: jsuter

Project: Language Level Analysis and Classification
Seminar "Educational Assessment for Language Technology" 
WS 2015/16, Magdalena Wolska

Julia Suter, January 2019

-----------------------------------------------------------------

language_level_features.py

- load the linguistic features for language level texts
- load the baseline features for language level texts
"""

# Import statements
import os
import glob

import pandas as pd
import numpy as np

# Author dictionary for matching abbreviating with author name
author_dict = {'KA':'Kafka',
				   'KL':'Kleist',
				   'SCHN':'Schnitzler',
				   'ZW':'Zweig',
				   'HOFF':'Hoffmann',
				   
				   'TWA':'Twain', 
				   'TCK':'Tieck', 
				   'GTTH':'Gotthelf',
				   'EICH':'Eichendorff',
				   'KEL':'Keller',
				   
				   'SPY':'Spyri', 
				   'BIE':'Bierbaum',
				   'DAUT':'Dauthendey',
				   'FON':'Fontane',
				   'GANG':'Ganghofer', 
				   
				   'GER':'Gerstäcker',
				   'GRI':'Grimm',
				   'HALT':'Haltrich',
				   'HEB':'Hebbel', 
				   'JEA':'Jean Paul',
				   
				   'MAY':'May',
				   'POE':'Poe',
				   'RAA':'Raabe',
				   'SCHE':'Scheerbart',
				   'SCHW':'Schwab',
				   
				   'STI':'Stifter',
				   'STO':'Storm',
				   'THO':'Thoma'}


def load_data(dataset_name="lang_levels", baseline=False):
	"""Load dataset with language level features and return respective features and solutions.
	
	Keyword arguments:
		dataset_name (string) -- which dataset to use ("lang_levels" or "classical_lit")
		baseline (Boolean) -- whether or not to return baseline features
		
	Return:
		dataset (np.array) -- feature array with linguistic/baseline features
		labels (np.array) -- solutions/labels for samples
		label_set (list) -- list of strings representing labels/classes"""
	
	# Set the data path
	data_dir = '../3_Text_features/'

	# If "language levels" data set is used
	if dataset_name == "lang_levels":
		
		# Set data path and label set
		data_dir = data_dir + "Features/"
		label_set = ["A1", "A2", "B1", "B2"]
		
	# If "classical literature"
	else:
		
		# Set data path and label set
		data_dir = data_dir + "Literature_Features/"
		label_set = os.listdir(data_dir)

	# Get sample file
	sample_file = os.listdir(data_dir+"/"+label_set[0])[0]

	# Get feature names
	feature_names = pd.read_csv(data_dir+label_set[0]+"/"+sample_file, usecols = ["Feature"])
	feature_names = [elem[0] for elem in feature_names.values]

	# Initalize lists
	labels = []
	frames = []

	# For each label, retrieve data from csv files
	for i, label in enumerate(label_set):

		# Get all csv files
		all_files = glob.glob(os.path.join(data_dir+label, "*.csv"))

		# Get and concatenate dataframe structure from all files
		df_from_each_file = (pd.read_csv(f, usecols = ['Value']) for f in all_files)
		concatenated_df = pd.concat(df_from_each_file, axis=1, ignore_index=True).T
		
		# Save concatenated dataframes
		frames.append(concatenated_df)

		# Save correct labels (number of samples in this class times index)
		labels += concatenated_df.shape[0] * [i]
	
	# Cenerate complete dataset (along sample axis)
	dataset = pd.concat(frames, axis=0)
	
	# Set feature names
	dataset.columns = feature_names
	
	# If classical literature, fix class labels
	if dataset_name != "lang_levels":
		label_set = [author_dict[l] for l in label_set]

	# For baseline, use baseline features
	if baseline:
		dataset = dataset.loc[:, ["LIX", "words per sent"]]
		
	# Otherwise use linguistic features only
	else:
		dataset = dataset.drop(['# sents', "# words", "LIX", "words per sent"], axis=1)
		
	# Transform label list into array
	labels = np.array(labels)

	# Return dataset with labels and label set
	return dataset, labels, label_set
