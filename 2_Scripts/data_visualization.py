"""
Created on Tue Oct 24 15:51:47 2017

@author: jsuter

Project: Language Level Analysis and Classification
Seminar "Educational Assessment for Language Technology" 
WS 2015/16, Magdalena Wolska

Julia Suter, January 2019

-----------------------------------------------------------------

data_visualization.py

- save matplotlib figures
- plot confusion matrix
- plot feature coefficients
- plot cluster components
- plot PCA
- set up feature set/n_cluster widgets
"""


# Import Statements
import os

import matplotlib.pyplot as plt
import numpy as np
import sklearn

from ipywidgets import Select, IntSlider, Layout
from IPython.display import display



def save_fig(fig_name, tight_layout=True, fig_extension="png", resolution=300):
	"""Save current matplotlib plot as image with given file name.
	
	Parameters:

		fig_name (string): figure name
	
	Keyword arguments:

		tight_layout (Boolean) -- set a tight layout for the figure (default = True)
		fig_extension (string) -- file format, e.g. "jpeg" will make the file end in .jpeg, default = "png"
		solution (int) -- resolution of saved figure (default = 300)

	Return: None"""
	
	# Set the file path 
	path = os.path.join("./figures/", fig_name + "." + fig_extension)

	# Get tight layout if necessary
	if tight_layout:
		plt.tight_layout()
		
	# Save the figure in the right format and resolution
	plt.savefig(path, format=fig_extension, dpi=resolution)


def plot_confusion_matrix(solutions, predictions, label_set, title):	
	"""Plot the confusion matrix for different classes given correct labels and predictions.
	
	Paramters:
	
		solutions (np.array) -- correct labels
		predictions (np.array) -- predicted labels
		label_set (list) -- labels/classes to predict
		title (string) -- plot title displayed above plot

	Return: None"""
	
	# Compute confusion matrix
	cm = sklearn.metrics.confusion_matrix(solutions, predictions, labels=range(len(label_set)))
	
	# Set figure size
	if len(label_set)>5:
		plt.figure(figsize=(10,10))
	else:
		plt.figure(figsize=(5,5))

	# Plot  confusion matrix with blue color map
	plt.imshow(cm, interpolation='none',cmap='Blues')

	# Write out the number of instances per cell
	for (i,j), z in np.ndenumerate(cm):
		plt.text(j, i, z, ha='center', va='center')
		
	# Assign labels and title
	plt.xlabel("Prediction")
	plt.ylabel("Ground truth")
	plt.title(title)

	# Set x ticks and labels
	plt.gca().set_xticks(range(len(label_set)))
	plt.gca().set_xticklabels(label_set, rotation=50)

	# Set y ticks and labels
	plt.gca().set_yticks(range(len(label_set)))
	plt.gca().set_yticklabels(label_set)
	plt.gca().invert_yaxis()
	
	# Show plot
	plt.show()
	

def plot_feature_coefficients(classifier, feature_names, label_set):
	"""Plot the feature coefficients for each label given an SVM classifier. 
	
	Paramters:
		
		classifier (sklearn.svm._classes.LinearSVC) -- linear SVM classifier (has to be fitted!)
		feature_names (list) -- feature names as list of strings
		label_set (list) -- label set as a list of strings

	Return: None
	"""
	
	# Layout settings depending un number of labels
	if len(label_set)>4:
		FIGSIZE = (80,30)
		ROTATION = 35
		RIGHT = 0.81
	else:
		FIGSIZE = (40,12)
		ROTATION = 45
		RIGHT = 0.58

	# Sort the feature indices according coefficients (highest coefficient first)
	sort_idx = np.argsort(-abs(classifier.coef_).max(axis=0))

	# Get sorted coefficients and feature names
	sorted_coef = classifier.coef_[:,sort_idx]
	sorted_fnames = feature_names[sort_idx]

	# Make subplots
	x_fig, x_axis = plt.subplots(2,1,figsize=FIGSIZE)

	# Plot coefficients on two different lines
	im_0 = x_axis[0].imshow(sorted_coef[:,:sorted_coef.shape[1]//2], interpolation='none', cmap='seismic',vmin=-2.5, vmax=2.5)
	im_1 = x_axis[1].imshow(sorted_coef[:,sorted_coef.shape[1]//2:], interpolation='none', cmap='seismic',vmin=-2.5, vmax=2.5)

	# Set y ticks (number of classes)
	x_axis[0].set_yticks(range(len(label_set)))
	x_axis[1].set_yticks(range(len(label_set)))

	# Set the y labels (classes/labels)
	x_axis[0].set_yticklabels(label_set, fontsize=24)
	x_axis[1].set_yticklabels(label_set, fontsize=24)

	# Set x ticks (half the number of features) and labels
	x_axis[0].set_xticks(range(len(feature_names)//2))
	x_axis[1].set_xticks(range(len(feature_names)//2))

	# Set the x labels (feature names)
	x_axis[0].set_xticklabels(sorted_fnames[:len(feature_names)//2], rotation=ROTATION, ha='right', fontsize=20)
	x_axis[1].set_xticklabels(sorted_fnames[len(feature_names)//2:], rotation=ROTATION, ha='right', fontsize=20)

	# Move plot to the right
	x_fig.subplots_adjust(right=RIGHT)

	# Set color bar
	cbar_ax = x_fig.add_axes([0.605, 0.15, 0.02, 0.7])
	cbar = x_fig.colorbar(im_0, cax=cbar_ax)
	cbar.ax.tick_params(labelsize=24) 
	
	# Show
	plt.show()



def plot_cluster_components(clusters, names):
	"""Visualize cluster components.
	
	Parameters:

		clusters (np.array) -- array representing to which cluster each feature belongs
		names (list) -- cluster components as list of strings

	Return: None
	"""

	# Initialize figure
	fig = plt.figure(figsize=(20, 0.5))

	# Plot lines of appropriate length
	cluster_sizes = np.bincount(clusters)
	
	# Set color list
	colors = ["b","g","r","c","m"]*100	
	colors = colors[:len(cluster_sizes)]
	
	# Transform names into list
	names = names.tolist()

	# Plot a bar representing number of components for each cluster
	pos = 0.0
	for clust_size, color in zip(cluster_sizes, colors):
		plt.plot([pos-0.9, pos+clust_size-1+0.1], [0, 0], lw=7, c=color)
		pos += clust_size+1

		# Add feature names
		names.insert(int(pos-1),"")

	# Get axis
	ax = fig.gca()

	# Remove all the frame stuff
	ax.set_frame_on(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_visible(False)
	
	# Set the labels
	ax.set_xticks(range(len(names)))
	ax.xaxis.set_ticklabels(names, rotation=55, ha="right", fontsize=11)
	
	# Set limitation of frame
	ax.set_xlim((-0.9, pos+clust_size-1+0.1))

	# Show
	plt.show()
	
	
def plot_PCA(pca, transformed_data, features, solutions):
	"""Plot Principal Component Analysis.
	
	Parameters:

		pca (sklearn._pca.PCA) -- PCA for features
		transformed_data (np.array) -- PCA-transformed data
		features (np.array) -- feature array
		solutions (np.array) -- solution/label array  

	Return: None"""

	# Get first and second principal components
	first_pc  =  pca.components_[0]
	second_pc =  pca.components_[1]
	
	# Axis of pc1, pc2
	for i,j in zip(transformed_data, features):
		plt.scatter(first_pc[0]*i[0], first_pc[1]*i[0], color='r')
		plt.scatter(second_pc[0]*i[1], second_pc[1]*i[1], color='c')
		plt.scatter(j[0],j[1], color='b')
		
	# Plot
	#plt.show()

	# Prinicipal component space (pc1, pc2)
	target_colors = {0:'blue', 1:'green', 2:'orange', 3:'red'}
	plt.scatter(transformed_data[:,0],transformed_data[:,1], 
				c=[target_colors[key] for key in solutions],
				alpha=0.5, edgecolor='none')

	# Assign labels and title
	plt.xlabel("PC 1")
	plt.ylabel("PC 2")
	plt.title("PCA transformed data space")

	plt.show()


	# Explained variance ratio (how much is covered by how many components)

	# Per component
	plt.plot(pca.explained_variance_ratio_)
	# Cumulative
	plt.plot(np.cumsum(pca.explained_variance_ratio_))

	# Assign labels and title
	plt.xlabel("Dimensions")
	plt.ylabel("Explained variance")
	plt.title("Explained Variance Ratio by Dimensions")

	plt.show()
	
	
# Widgets

# Set box layout
box_layout = Layout(display='flex',
					flex_flow='column',
					align_items='stretch',
					border='solid',
					width='40%')
	
# Set feature set widget
feature_set_widi = Select(
		 options=['original features','original agglomerated features', 'baseline features',
		          "PCA components (explained variance of 95%)", 
				  'only non-sparse features', 'only relevant features', 
				  'only sparse features', 'only less relevant features',
				  'only agglomerated sparse features','only agglomerated less relevant features',
				  'agglomerated sparse features + non-sprase features', 
				  'agglomerated less relevant features + relevant features'],
		 
		value='agglomerated less relevant features + relevant features',                                
		description='Feature set',
		layout=box_layout)

# Set cluster widget
n_cluster_widi = IntSlider(
	value=5,
	min=1,
	max=80,
	step=1,
	max_width = 300,
	description='# clusters')
