import json

if __name__ == '__main__':
	tweets_texts = []
	pos = 0
	with open("../data/dengue_tweets3.json") as tweets_src_f:
		with open("../data/texts/dengue_sample.txt", "w") as tweets_sample_f:
			for line in tweets_src_f:
				jtweet = json.loads(line)
				text = jtweet["text"].encode('utf-8') + "\n"
				resp = raw_input(text)

				if resp == "y":
					pos += 1

				tweets_sample_f.write(resp + " ")
				tweets_sample_f.write(text)
				tweets_sample_f.write('\n==============================================================================================================================================\n')

	print str(pos) + "/" + str(len(tweets_src_f))