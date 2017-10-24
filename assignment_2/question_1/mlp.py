# mlp.py
# -------------

# mlp implementation
import util
import random as r
import math as m
PRINT = True
	  
class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.layer_weights = {}
    self.output_layer = {}
    for label in legalLabels:
      self.layer_weights[label] = util.Counter() # this is the data-structure you should use
      self.output_layer[label] = 0

  def softmax(self, value, sums):
    sum = 0
    for value in sums:
      sum += m.exp(value)
    return m.exp(value) / sum
		
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
  
    self.features = trainingData[0].keys() # could be useful later
    # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING
	
  # Initialize the weights for both layers of the perceptrons to be either 0 or 1 randomly
    for x in range(10):
      for y in self.features:
        self.layer_weights[x][y] = r.randint(0,1)
  
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
	  
      for i in range(len(trainingData)):
# 		Create a counter containing the sum of the weights times the value of the corresponding location on the graph
        sums = util.Counter()
#		Multiply for each label 0-9
        for j in range(10):
          self.output_layer[j] = trainingData[i] * self.layer_weights[j]
        for j in range(10):
          sums[j] = self.softmax(self.output_layer[j], self.output_layer)
        
#		If the label was incorrect, then decrease the weights of the obtained label and increase the weights of the correct label
        if sums.argMax() != trainingLabels[i]:
          


    
  def classify(self, data ):
    self.features = data[0].keys()
  
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        self.output_layer[l] = datum * self.layer_weights[l]
      for l in self.legalLabels:
        vectors[l] = self.softmax(self.output_layer[l], self.output_layer)
      guesses.append(vectors.argMax())
    return guesses