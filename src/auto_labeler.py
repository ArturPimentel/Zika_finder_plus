import sys
import os

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

def write_to(textfile, text):
	textfile.write(text)
	textfile.write("====================================================\n")

###############################################################################
if __name__ == '__main__':
	ml_file = sys.argv[1]
	with open("../data/samples_texts/" + ml_file) as f:
		# make a directory with the file's name to contain the results
		directory = "../data/auto_label_stats/" + ml_file.split(".")[0]
		if not os.path.exists(directory):
			os.makedirs(directory)
		# open the five results files for this analysis
		with open(directory + "/auto_label_fn.txt", "w") as o_fn, \
			 open(directory + "/auto_label_fp.txt", "w") as o_fp, \
			 open(directory + "/auto_label_tp.txt", "w") as o_pm, \
			 open(directory + "/auto_label_tu.txt", "w") as o_um, \
			 open(directory + "/auto_label_tn.txt", "w") as o_nm:
			# read the file with the manually labeled tweets
			lines = f.readlines()
			labeled_texts = group_lines(lines)
			w_terms = get_terms("param/" + ml_file.split(".")[0] + "_terms.txt")

			# Thresholds for auto-labeler
			ythreshold = 80
			uthreshold = 60

			# Counters for analysis
			yy_matches = 0
			nn_matches = 0
			uu_matches = 0
			fp = 0
			fn = 0
			n_y = 0
			n_n = 0
			n_u = 0

			# Make a list of texts with separeted label
			texts = [[text[0:1], text[2:]] for text in labeled_texts]

			for l_text in texts:
				label = l_text[0]
				text = l_text[1]
				t_scores = score(w_terms, text)
				t_score = sum(t_scores)

				# Record automatic label together with manual label for analysis
				if t_score < uthreshold:
					label = "n " + label
				elif t_score < ythreshold:
					label = "u " + label
				else:
					label = "y " + label

				# Update stats
				if label == "y y":
					write_to(o_pm, label + " " + str(t_score) + " " + str(t_scores) + " "+ text)
					yy_matches += 1
					n_y += 1
				elif label == "n n":
					write_to(o_nm, label + " " + str(t_score) + " " + str(t_scores) + " "+ text)
					nn_matches += 1
					n_n += 1
				elif label == "u u":
					write_to(o_um, label + " " + str(t_score) + " " + str(t_scores) + " "+ text)
					uu_matches += 1
					n_u += 1
				elif label == "n y" or label == "u y":
					write_to(o_fn, label + " " + str(t_score) + " " + str(t_scores) + " "+ text)
					fn += 1
					n_y += 1
				elif label == "y n" or label == "y u":
					write_to(o_fp, label + " " + str(t_score) + " " + str(t_scores) + " "+ text)
					fp += 1
					if label == "y n":
						n_n += 1
					elif label == "y u":
						n_u += 1

			# Calculate stats
			matches = yy_matches + nn_matches + uu_matches
			non_matches = len(texts) - matches
			with open(directory + "/auto_label_log.txt", "a") as log:
				log.write("\n---------------------------------------------------------")
				log.write('\nTimestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.now()))
				log.write("\nTotal: " + str(len(texts)) + "\nMatches: " + str(matches) +
						  "\n\tyy: " + str(yy_matches) + "\n\tnn: " + str(nn_matches) +
						  "\n\tuu: " + str(uu_matches) + "\nNon-matches: " + str(non_matches) +
						  "\n\tfn: " + str(fn) + "\n\tfp: " + str(fp) + "\nThresholds:\n\ty: " +
						  str(ythreshold) + "\n\tu: " + str(uthreshold))
				log.write(("\nAccuracy: %.2f" % (float(matches)/len(texts))))
				log.write(("\nAccuracy w/o undefined: %.2f" % (float(len(texts) - fp - fn)/len(texts))))
				log.write("\nFalse positive rate: %.3f" % (float(fp)/(n_n + n_u)))
				log.write("\nTrue positive rate: %.3f" % (float(yy_matches)/n_y))