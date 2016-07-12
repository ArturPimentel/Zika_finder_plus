import json

if __name__ == '__main__':
	tweets_texts = []
	pos = 1
	with open("../../data/dataset_samples/zika_2000tweets.json") as tweets_src_f:
		with open("../../data/samples_texts/zika_2000sample_ml.txt", "w") as tweets_sample_f:
			for line in tweets_src_f:
				jtweet = json.loads(line)
				text = jtweet["text"].encode('utf-8') + "\n"
				resp = raw_input(str(pos) + text)

				pos += 1

				tweets_sample_f.write(resp + " ")
				tweets_sample_f.write(text)
				tweets_sample_f.write('\n==============================================================================================================================================\n')

	#print str(pos) + "/" + str(len(tweets_src_f))