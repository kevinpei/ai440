# mlp.py
# -------------

# mlp implementation
import util
PRINT = True

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
	self.layer_one_weights = {}
	self.layer_two_weights = {}
    for label in legalLabels:
      self.layer_one_weights[label] = util.Counter() # this is the data-structure you should use
	  self.layer_two_weights[label] = util.Counter()
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
  
  self.features = trainingData[0].keys() # could be useful later
    # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING
	
# Initialize the weights for both layers of the perceptrons to be either 0 or 1 randomly
  for x in range(10):
	for y in self.features:
	  self.layer_one_weights[x][y] = r.randint(0,1)
	  self.layer_two_weights[x][y] = r.randint(0,1)
  
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
	  
      for i in range(len(trainingData)):
# 		Create a counter containing the sum of the weights times the value of the corresponding location on the graph
        sums = util.Counter()
#		Multiply for each label 0-9
	    for j in range(10):
          layer_one = trainingData[i] * self.layer_one_weights[j]
		  sums[j] = layer_one * self.layer_two_weights[j]
#		If the label was incorrect, then decrease the weights of the obtained label and increase the weights of the correct label
        if sums.argMax() != trainingLabels[i]:
          self.layer_one_weights[sums.argMax()] -= trainingData[i]
          self.layer_one_weights[trainingLabels[i]] += trainingData[i]
		  
		  #EDIT THIS PART IT'S PROBABLY WRONG
		  wrong_label_error = self.layer_two_weights[sums.argMax()] - self.layer_one_weights[sums.argMax()]
		  right_label_error = self.layer_two_weights[trainingLabels[i]] - self.layer_one_weights[trainingLabels[i]]
		  #END EDITING PART
		  
		  self.layer_two_weights[sums.argMax()] -= trainingData[i] + wrong_label_error * self.layer_two_weights[sums.argMax()]
          self.layer_two_weights[trainingLabels[i]] += trainingData[i] + right_label_error * self.layer_two_weights[trainingLabels[i]]
    
  def classify(self, data ):
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
	    layer_one = datum * self.layer_one_weights[j]
        vectors[l] = layer_one * self.layer_two_weights[j]
      guesses.append(vectors.argMax())
    return guesses