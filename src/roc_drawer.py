import sys
import os
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

def num_there(s):
	return any(i.isdigit() for i in s)

def group_lines(file_lines):
	texts = []
	text = ""

	for line in lines:
		if line == "==============================================================================================================================================\n":
			texts.append(text)
			text = ""
		else:
			text += line

	return texts

def parse(line):
	l = line.split(",")
	return (l[0], int(l[1].strip("\n")))

def get_terms(file_path):
	with open(file_path) as f:
		w_terms = []
		for line in f:
			if line[0] != "#":
				w_terms.append(parse(line))
	return w_terms

def score(w_terms, text):
	s = []
	text = text.lower()
	for w_term in w_terms:
		if w_term[0] in text:
			s.append(w_term[1])
	return s

###############################################################################
if __name__ == '__main__':
	ml_file = sys.argv[1]
	with open("../data/samples_texts/" + ml_file) as f:
		# make a directory with the file's name to contain the results
		directory = "../data/auto_label_stats/" + ml_file.split(".")[0]
		if not os.path.exists(directory):
			os.makedirs(directory)
		
		# read the file with the manually labeled tweets
		lines = f.readlines()
		labeled_texts = group_lines(lines)
		w_terms = get_terms("param/" + ml_file.split(".")[0] + "_terms.txt")

		# Counters for analysis
		yy_matches = 0
		nn_matches = 0
		fp = 0
		fn = 0

		# Vectors for analysis
		fprates = []
		tprates = []
		fps = []

		b_score = -1000
		l_score = 1000

		# Make a list of texts with separeted label
		texts = [[text[0:1], text[2:]] for text in labeled_texts]

		for ythreshold in xrange(-420, 240):
			for l_text in texts:
				label = l_text[0]
				text = l_text[1]
				t_scores = score(w_terms, text)
				t_score = sum(t_scores)

				# Record automatic label together with manual label for analysis
				if t_score < ythreshold:
					label = "n " + label
				else:
					label = "y " + label

				if t_score > b_score:
					b_score = t_score
				if t_score < l_score:
					l_score = t_score
				# Update stats
				if label == "y y":
					yy_matches += 1
				elif label == "n n" or label == "n u":
					nn_matches += 1
				elif label == "n y" or label == "u y":
					fn += 1
				elif label == "y n" or label == "y u":
					fp += 1

			# Calculate stats
			fprates.append(float(fp)/(fp + nn_matches))
			tprates.append(float(yy_matches)/(yy_matches + fn))
			fp = 0; fn = 0; yy_matches = 0; nn_matches = 0

		#print fps
		# This is the ROC curve
		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.plot(fprates, tprates)
		plt.plot([0,1], [0,1], 'r')
		plt.xlabel('False positive rate (1-specificity)', fontsize=16)
		plt.ylabel('True positive rate (sensitivity)', fontsize=16)
		axes = plt.gca()
		axes.set_xlim([0,1])
		axes.set_ylim([0,1])

		score = -420
		for i, j in zip(fprates, tprates):
			if score % 40 == 0:
				ax.annotate('%d' % score, xy = (i, j), textcoords = 'data')
			score += 1

		#print b_score
		#print l_score

		# This is the AUC
		auc = np.trapz(list(reversed(tprates)), list(reversed(fprates)))

		fig.suptitle(('ROC dengue 2000 filter 1 (AUC = %.3f' % auc) + ')', fontsize=20)
		plt.savefig("plot_roc_dengue2000.png")