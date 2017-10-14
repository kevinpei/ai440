# mlp.py
# -------------

# mlp implementation
import util
import random as r
PRINT = True

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.layer_number = 5
    self.layer_weights = {}
    for layer in range(self.layer_number):
      self.layer_weights[layer] = {}
      for label in legalLabels:
        self.layer_weights[layer][label] = util.Counter() # this is the data-structure you should use
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
  
    self.features = trainingData[0].keys() # could be useful later
    # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING
	
  # Initialize the weights for both layers of the perceptrons to be either 0 or 1 randomly
    for layer in range(self.layer_number):
      for x in range(10):
        for y in self.features:
          self.layer_weights[layer][x][y] = r.randint(0,1)
  
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
	  
      for i in range(len(trainingData)):
# 		Create a counter containing the sum of the weights times the value of the corresponding location on the graph
        sums = util.Counter()
#		Multiply for each label 0-9
        for j in range(10):
		      value = trainingData[i] * self.layer_weights[0][j]
		      for x in range(1, self.layer_number):
		        value *= self.layer_weights[x][j]
		        sums[j] = value
#		If the label was incorrect, then decrease the weights of the obtained label and increase the weights of the correct label
        if sums.argMax() != trainingLabels[i]:
		      self.layer_weights[0][sums.argMax()] -= trainingData[i]
		      self.layer_weights[0][trainingLabels[i]] += trainingData[i]
		  
		  #EDIT THIS PART IT'S PROBABLY WRONG
        for x in range(1, self.layer_number):
          wrong_label_error = self.layer_weights[x][sums.argMax()] - self.layer_weights[x-1][sums.argMax()]
          right_label_error = self.layer_weights[x][trainingLabels[i]] - self.layer_weights[x-1][trainingLabels[i]]
          self.layer_weights[x][sums.argMax()] -= trainingData[i] + wrong_label_error * self.layer_weights[x][sums.argMax()]
          self.layer_weights[x][trainingLabels[i]] += trainingData[i] + right_label_error * self.layer_weights[x][trainingLabels[i]]
		  #END EDITING PART

    
  def classify(self, data ):
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        layer_one = datum * self.layer_one_weights[j]
        vectors[l] = layer_one * self.layer_two_weights[j]
      guesses.append(vectors.argMax())
    return guesses