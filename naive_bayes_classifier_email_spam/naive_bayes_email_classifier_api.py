from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

class Tuple:
	'''This is tuple class, whic holds the data in the format of
	doc_id,feature1,feature2,....,class
	'''
	cnt = 1

	def __init__(self):
		self.id = Tuple.cnt
		Tuple.cnt += 1
		self.features = []
		self.cls = ''

	def setId(self, id):
		self.id = id
	
	def getId(self):
		return self.id

	def setFeatures(self, txt):
		for w in txt:
			self.features.append(w)

	def getFeatures(self):
		return self.features

	def setClass(self, cls):
		self.cls = cls

	def getClass(self):
		return self.cls

	def show(self):
		print "id = ", self.id, "\nfeatures = ", self.features, "\nclass = ", self.cls

#------------------------------------------
def loadData(training_data):
	training_tuples = []
	for line in training_data:
		data = line.split(",")
		temp = Tuple()
		temp.setId(data[0])
		temp.setFeatures(data[1:-1])
		temp.setClass(data[-1].replace("\n",""))

		training_tuples.append(temp)

	return training_tuples


def filterClasses(training_tuples):
	'''This generates unique classes that are possible in the given dataset
	'''
	temp = {}
	for t in training_tuples:
		if t.getClass() not in temp:
			temp[t.getClass()] = 1

	return temp.keys()
			
def getVocab(training_tuples):
	'''This function generate unique words from the given text in all tuples
	'''
	vocab = []
	for t in training_tuples:
		vocab += list(set(t.getFeatures()))

	return vocab

def generatePrior(training_tuples, classes):
	'''This function returns prior
	'''
	prior = {}
	total_count = len(training_tuples)
	for cls in classes:
		temp = 0
		for t in training_tuples:
			if t.getClass() == cls:
				temp += 1

		prior[cls] = temp/float(total_count)

	return prior	


def generateLikelihood(training_tuples, vocab, classes):
	'''This function returns likelihood
	'''
	likelihood = {}
	vocab_count = len(vocab)
	for c in classes:
		txt = []
		#for every class, gather the data
		for t in training_tuples:
			if t.getClass() == c:
				txt += t.getFeatures()

		#iterate over the vocab, and calculate likelihood
		for w in vocab:
			N1 = txt.count(w)
			N2 = len(txt)	
			likelihood[w+'|'+c] = float(N1+1)/(N2+vocab_count)

	return likelihood


def predict(test_tuples, classes, prior, likelihood):
	'''This function calculates max a prior for every test record
	and returns hash of records as doc => prediction
	'''

	CMAP = {}
	for t in test_tuples:
		posterior = {}
		for c in classes:
			temp = prior[c]
			for f in t.getFeatures():
				if f+'|'+c in likelihood:
					temp *= likelihood[f+'|'+c]
			posterior[c] = temp

		max = 0.0
		cls = ''
		for c in posterior:
			if posterior[c] > max:
				max = posterior[c]
				cls = c
		CMAP[t.getId()] = cls

	return CMAP
		 
		
def showResults(training_data, test_data, posterior):
	'''This function shows the training data, test data and predictions
	'''
	print "Training Data:"
	print training_data
	print "Test Data:"
	print test_data
	print "Predictions..."
	print posterior

				
def evaluateAccuracy(test_tuples, posterior):
	'''This function calculates accuracy'''
	flag = 0
	for t in test_tuples:
		print t.getId(), " | ", t.getClass(), " | ", posterior[t.getId()]
		if t.getClass() == posterior[t.getId()]:
			flag += 1	
				
	print "accuracy = ", flag/float(10)


def make_api_tuples(tuples):
	l1 = []
	for t in tuples:
		temp = (" ".join(t.getFeatures()), t.getClass())
		l1.append(temp)

	return l1

#------------MAIN------------
def main():
	print "This is Naive Bayes' Classifier..."

	#read training data
	#training_data = open("training_data").readlines()
	training_data = open("training_data_final").readlines()
	#load training data
	training_tuples = loadData(training_data)

	training_tuples_api = make_api_tuples(training_tuples)
	print training_tuples_api

	#display tuples
	#for t in training_tuples:
	#	t.show()

	#gather classes
	classes = filterClasses(training_tuples)
	#print "classes = ", classes

	#gather vocab
	vocab = getVocab(training_tuples)
	#print vocab

	#generate prior
	prior = generatePrior(training_tuples, classes)
	#print prior

	#generate likelihood
	likelihood = generateLikelihood(training_tuples, vocab, classes)
	#print likelihood

	#read test data
        #test_data = open("test_data").readlines()
        test_data = open("test_data_final").readlines()
        #load test data
        test_tuples = loadData(test_data)

	test_tuples_api = make_api_tuples(test_tuples)
	#calculate C-MAP
	posterior = predict(test_tuples, classes, prior, likelihood)
	showResults(training_data, test_data, posterior)

	#calculate accuracy
	evaluateAccuracy(test_tuples, posterior)

	#Naive Bayes API
	cl = NaiveBayesClassifier(training_tuples_api)
	# Compute accuracy
	print("Accuracy: {0}".format(cl.accuracy(test_tuples_api)))

if __name__ == "__main__":
	main()
	
