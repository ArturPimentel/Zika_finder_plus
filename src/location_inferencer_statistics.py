user_locations = []
matches = float(0)

with open("../data/loc_results/gt_cities2.txt") as infer_f:
	for line in infer_f:
		fields = line.strip('\n').split(',')
		
		user_loc = {}		
		user_loc['username'] = fields[0]
		user_loc['real_location'] = fields[1]
		user_loc['infer_location'] = fields[2]

		user_locations.append(user_loc)

		if user_loc['real_location'] == user_loc['infer_location']:
			matches += 1

print "%.2f" % (matches/len(user_locations))
