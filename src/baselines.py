import sys
import os
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import tree
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
		text_nb_clf = Pipeline([('vect', CountVectorizer()),
							 ('tfidf', TfidfTransformer()),
							 ('clf', MultinomialNB())])

		text_nb_clf = text_nb_clf.fit(tweets_train.data, tweets_train.labels)
		tweets_test = tweets_train.data

		predicted = text_nb_clf.predict(tweets_test)
		print "Naive-Bayes"
		print np.mean(predicted == tweets_train.labels)

		print metrics.classification_report(tweets_train.labels, predicted,
    										target_names = ['irrelevant', 'relevant'])

		print metrics.confusion_matrix(tweets_train.labels, predicted)
		print "-----------------------------------------------------------------------"

		# SVM baseline
		text_svm_clf = Pipeline([('vect', CountVectorizer()),
								 ('tfidf', TfidfTransformer()),
								 ('clf', SGDClassifier(loss = 'hinge', penalty = 'l2',
													   alpha = 1e-3, n_iter = 5, random_state = 42))])

		text_svm_clf = text_svm_clf.fit(tweets_train.data, tweets_train.labels)
		predicted = text_svm_clf.predict(tweets_test)
		print "SVM"
		print np.mean(predicted == tweets_train.labels)
		print metrics.classification_report(tweets_train.labels, predicted,
    										target_names = ['irrelevant', 'relevant'])
		print metrics.confusion_matrix(tweets_train.labels, predicted)

		print "-----------------------------------------------------------------------"

		# Logistic Regression baseline
		text_lr_clf = Pipeline([('vect', CountVectorizer()),
								 ('tfidf', TfidfTransformer()),
								 ('clf', LogisticRegression(C=1, penalty='l1', tol=0.01))])


		text_lr_clf = text_lr_clf.fit(tweets_train.data, tweets_train.labels)
		predicted = text_lr_clf.predict(tweets_test)
		print "Logistic Regression"
		print np.mean(predicted == tweets_train.labels)
		print metrics.classification_report(tweets_train.labels, predicted,
    										target_names = ['irrelevant', 'relevant'])
		print metrics.confusion_matrix(tweets_train.labels, predicted)

		print "-----------------------------------------------------------------------"

		# Decision Tree baseline
		text_tree_clf = Pipeline([('vect', CountVectorizer()),
								 ('tfidf', TfidfTransformer()),
								 ('clf', tree.DecisionTreeClassifier())])


		text_tree_clf = text_tree_clf.fit(tweets_train.data, tweets_train.labels)
		predicted = text_tree_clf.predict(tweets_test)
		print "Decision Tree"
		print np.mean(predicted == tweets_train.labels)
		print metrics.classification_report(tweets_train.labels, predicted,
    										target_names = ['irrelevant', 'relevant'])
		print metrics.confusion_matrix(tweets_train.labels, predicted)