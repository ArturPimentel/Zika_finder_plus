import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics

class TweetsAndLabels():
	"""TweetsAndLabels is a struct-like class to store tweets and the labels that were given manually"""
	def __init__(self, data, labels):
		self.data = data
		self.labels = labels

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

def pipeline_and_evaluate(data, labels, clf_model, model_name):
	text_clf = Pipeline([('vect', CountVectorizer()),
							('tfidf', TfidfTransformer()),
							('clf', clf_model)])

	text_clf = text_clf.fit(data, labels)
	predicted = text_clf.predict(data)
	#y_pred = text_clf.predict_proba()

	print model_name
	print np.mean(predicted == labels)
	print metrics.classification_report(labels, predicted,
										target_names = ['irrelevant', 'relevant'])
	print metrics.confusion_matrix(labels, predicted)

	"""fp_rates, tp_rates, _ = metrics.roc_curve(data, predicted)
				plt.figure(1)
				plt.plot([0, 1], [0, 1], 'k--')
				plt.plot(fp_rates, tp_rates, label=model_name)
				plt.xlabel('False positive rate')
				plt.ylabel('True positive rate')
				plt.title('ROC curve')
				plt.legend(loc='best')
				plt.savefig("roc_" + model_name + ".png")"""

	print "-----------------------------------------------------------------------"


if __name__ == '__main__':
	ml_file = sys.argv[1]
	with open("../data/samples_texts/" + ml_file) as f:
		# make a directory with the file's name to contain the results
		directory = "../data/auto_label_stats/" + ml_file.split(".")[0]
		if not os.path.exists(directory):
			os.makedirs(directory)
		# open the five results files for this analysis

		# read the file with the manually labeled tweets
		lines = f.readlines()
		labeled_texts = group_lines(lines)
		tweets_train = TweetsAndLabels([], [])

		for text in labeled_texts:
			label = text[0:1]
			if label == "y":
				tweets_train.labels.append(1)
			elif label == "n":
				tweets_train.labels.append(0)
			elif label == "u":
				tweets_train.labels.append(0)
			tweets_train.data.append(text[2:])

		# Naive-Bayes baseline

		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  MultinomialNB(),
							  "Naive-Bayes")
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  SGDClassifier(loss = 'hinge',
							  				penalty = 'l2',
											alpha = 1e-3,
											n_iter = 5,
											random_state = 42),
							  "SVM")
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  LogisticRegression(C=10000,
							  					 penalty='l1',
							  					 tol=0.01),
							  "Logistic_Regression")
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  DecisionTreeClassifier(),
							  "Decision_Tree")
