with open("param/cities15000.tsv") as tsv_f:
	with open("param/cities15000.csv", "w") as csv_f:
		for line in tsv_f:
			csv_f.write(line.replace("\t", "|"))