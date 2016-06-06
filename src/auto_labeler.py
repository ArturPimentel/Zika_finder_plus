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

def get_bad_terms(file_path):
	with open(file_path) as bad_terms_f:
		bad_terms = bad_terms_f.readlines()
		bad_terms = [x.strip('\n') for x in bad_terms]
		return bad_terms

def there_is_bad_term(bad_terms, text):
	for bad_term in bad_terms:
		if bad_term in text:
			return True
	return False

def write_to(textfile, text):
	textfile.write(text)
	textfile.write("====================================================\n")

###############################################################################
if __name__ == '__main__':
	with open("../data/texts/out_label.txt") as f, \
		 open("../data/texts/auto_label/auto_label_fn.txt", "w") as o_fn, \
		 open("../data/texts/auto_label/auto_label_fp.txt", "w") as o_fp, \
		 open("../data/texts/auto_label/auto_label_pm.txt", "w") as o_pm, \
		 open("../data/texts/auto_label/auto_label_nm.txt", "w") as o_nm:
		lines = f.readlines()
		texts = group_lines(lines)
		bad_terms = get_bad_terms("param/bad_terms.txt")

		matches = 0
		fp = 0
		fn = 0

		for text in texts:
			if there_is_bad_term(bad_terms, text):
				text = "n " + text
			else:
				text = "y " + text

			label_end = 3
			if text[0:label_end] == "y y":
				write_to(o_pm, text)
				matches += 1
			elif text[0:label_end] == "n n":
				write_to(o_nm, text)
				matches += 1
			elif text[0:label_end] == "n y":
				write_to(o_fn, text)
				fn += 1
			elif text[0:label_end] == "y n":
				write_to(o_fp, text)
				fp += 1

		print ("Total: " + str(len(texts)) + ", matches: " + str(matches) + 
			   ", fn: " + str(fn) + ", fp: " + str(fp))
		print ("Acc: %.2f" % (float(matches)/len(texts)))

