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

###############################################################################
if __name__ == '__main__':
	with open("../data/texts/dengue_sample.txt") as f:
		lines = f.readlines()
		texts = group_lines(lines)
		pos = 0

		for text in texts:
			if text[0:2] == "y ":
				pos += 1

		print ("Total: " + str(len(texts)) + "positives: " + str(pos))
