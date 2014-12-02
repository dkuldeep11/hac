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
		vocab += t.getFeatures()

	return list(set(vocab))

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
			print w,c, "=>", N1+1,N2,vocab_count
			likelihood[w+'|'+c] = float(N1+1)/(N2+vocab_count)

	return likelihood


def predict(test_tuples, classes, prior, likelihood):
	'''This function calculates max a prior for every test record
	and returns hash of records as doc => prediction
	'''

	CMAP = {}
	for t in test_tuples:
		print "For ", t.getFeatures(), " posterior is ...\n"
		posterior = {}
		for c in classes:
			temp = prior[c]
			print "for class", c, " prior is ", temp
			
			for f in t.getFeatures():
				if f+'|'+c in likelihood:
					temp *= likelihood[f+'|'+c]
			posterior[c] = temp

		max = 0.0
		cls = ''
		for c in posterior:
			print "P(",c,"|test_data)", " => ", '%.6f' % posterior[c]
			if posterior[c] > max:
				max = posterior[c]
				cls = c
		CMAP[t.getId()] = cls

	return CMAP
		 
		
def showResults(training_data, test_data, posterior):
	'''This function shows the training data, test data and predictions
	'''
	print "Predictions..."
	print posterior, "\n\n"

				
def evaluateAccuracy(test_tuples, posterior):
	'''This function calculates accuracy'''
	print "Accuracy...\n"
	print "ID | actual | predicted"
	flag = 0
	total = 0
	for t in test_tuples:
		print t.getId(), " | ", t.getClass(), " | ", posterior[t.getId()]
		if t.getClass() == posterior[t.getId()]:
			flag += 1	
		total += 1
				
	print "accuracy = ", flag/float(total)
#------------MAIN------------
def main():
	print "This is Naive Bayes' Classifier..."



	#read training data
	#training_data = open("training_data").readlines()
	training_data = open("training_data_final").readlines()
	#training_data = open("wiki_train").readlines()
	#load training data
	training_tuples = loadData(training_data)

	print "Training Data:"
        print training_data

	#display tuples
	'''
	for t in training_tuples:
		t.show()
	'''

	#gather classes
	classes = filterClasses(training_tuples)
	#print "classes = ", classes

	#gather vocab
	vocab = getVocab(training_tuples)
	#print vocab

	#generate prior
	prior = generatePrior(training_tuples, classes)
	print "prior..."
	print prior, "\n\n"

	#generate likelihood
	likelihood = generateLikelihood(training_tuples, vocab, classes)
	print "likelihood..."
	print likelihood, "\n\n"

	#read test data
        #test_data = open("test_data").readlines()
        test_data = open("test_data_final").readlines()
        #test_data = open("wiki_test").readlines()
        #load test data
        test_tuples = loadData(test_data)


        print "Test Data:"
        print test_data

	#calculate C-MAP
	posterior = predict(test_tuples, classes, prior, likelihood)
	showResults(training_data, test_data, posterior)

	#calculate accuracy
	evaluateAccuracy(test_tuples, posterior)

if __name__ == "__main__":
	main()
	
