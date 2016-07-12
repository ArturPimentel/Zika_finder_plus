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

	for line in file_lines:
		if line == "==============================================================================================================================================\n":
			texts.append(text)
			text = ""
		else:
			text += line

	return texts

def pipeline_and_evaluate(data, labels, test_data, test_labels, clf_model, model_name):
	text_clf = Pipeline([('vect', CountVectorizer()),
							('tfidf', TfidfTransformer()),
							('clf', clf_model)])

	text_clf = text_clf.fit(data, labels)
	examples = ["To com dengue", "Tengo dengue", "I have dengue", "Descobri que tive dengue e passei para ele", "Second time admitted in hospital due to dengue fever. Its not cool.", "\"vamo sair\" \"nao da, to com dengue\" Que tipo de ser humano sou eu", "Learn more about dengue here at the VRP Medical Center Official Facebook Page. Also, before the month of June... http://fb.me/H89X6IVB"]
	probas_ = []
	fp_rates = []
	tp_rates = []

	if model_name == "SVM":
		probas_ = text_clf.decision_function(test_data)
		fp_rates, tp_rates, _ = metrics.roc_curve(test_labels, probas_)
	else:
		probas_ = text_clf.predict_proba(test_data)
		fp_rates, tp_rates, _ = metrics.roc_curve(test_labels, probas_[:, 1])

	predicted = text_clf.predict(test_data)
	predicted_examples = text_clf.predict(examples)
	print model_name
	print predicted_examples
	print np.mean(predicted == test_labels)
	print metrics.classification_report(test_labels, predicted,
										target_names = ['irrelevant', 'relevant'])
	print metrics.confusion_matrix(test_labels, predicted)
	print "-----------------------------------------------------------------------"
	
	roc_auc = metrics.auc(fp_rates, tp_rates)
	plt.plot(fp_rates, tp_rates, label=model_name + ("(AUC = %0.2f)" % roc_auc))

if __name__ == '__main__':
	ml_file = sys.argv[1]
	test_file = sys.argv[2]
	with open("../data/samples_texts/" + ml_file) as f, \
		 open("../data/samples_texts/" + test_file) as tf, \
		 open("textlocf.txt") as tlf:

		# read the files with the manually labeled tweets
		lines = f.readlines()
		labeled_texts = group_lines(lines)
		tweets_train = TweetsAndLabels([], [])

		tlines = tf.readlines()
		tlabeled_texts = group_lines(tlines)
		tweets_test = TweetsAndLabels([], [])

		tllines = tlf.readlines()
		tllines_texts = group_lines(tllines)

		n_pos = 0
		n_neg = 0
		for text in labeled_texts:
			label = text[0:1]
			if label == "y":
				tweets_train.labels.append(1)
				n_pos += 1
			elif label == "n":
				tweets_train.labels.append(0)
				n_neg += 1
			elif label == "u":
				tweets_train.labels.append(0)
				n_neg += 1
			tweets_train.data.append(text[2:])

		print n_pos, n_neg
		n_pos = 0
		n_neg = 0

		for text in tlabeled_texts:
			label = text[0:1]
			if label == "y":
				n_pos += 1
				tweets_test.labels.append(1)
			elif label == "n":
				n_neg += 1
				tweets_test.labels.append(0)
			elif label == "u":
				n_neg += 1
				tweets_test.labels.append(0)
			#tweets_test.data.append(text[2:])

		for text in tllines_texts:
			tweets_test.data.append(text)

		print n_pos, n_neg
		
		plt.figure(1)
		plt.plot([0, 1], [0, 1], 'k--')

		# Naive-Bayes baseline
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  tweets_test.data,
							  tweets_test.labels,
							  MultinomialNB(),
							  "Naive-Bayes")
		
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  tweets_test.data,
							  tweets_test.labels,
							  SGDClassifier(loss = 'hinge',
							  				penalty = 'l2',
											alpha = 1e-3,
											n_iter = 5,
											random_state = None),
							  "SVM")
		
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  tweets_test.data,
							  tweets_test.labels,
							  LogisticRegression(C=1,
							  					 penalty='l2',
							  					 tol=0.01),
							  "Logistic_Regression")
		pipeline_and_evaluate(tweets_train.data,
							  tweets_train.labels,
							  tweets_test.data,
							  tweets_test.labels,
							  DecisionTreeClassifier(max_depth=7),
							  "Decision_Tree")

		plt.xlabel('False positive rate')
		plt.ylabel('True positive rate')
		plt.title('ROC curve')
		plt.legend(loc='best')
		plt.savefig("roc_baselines_wl.png")