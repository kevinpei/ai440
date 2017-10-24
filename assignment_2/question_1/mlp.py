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
    self.intermediate_value = util.Counter();
    for layer in range(2):
      self.layer_weights[layer] = {}
      for label in legalLabels:
        self.layer_weights[layer][label] = util.Counter() # this is the data-structure you should use
      
  def softmax(self, value, hidden_layer, trainingdata):
    sum = 0
    for feature in self.features:
	  sum += m.exp(hidden_layer[feature] * trainingdata[feature])
    return m.exp(value)/(m.exp(sum))
	
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
  
    self.features = trainingData[0].keys() # could be useful later
    # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING
	
  # Initialize the weights for both layers of the perceptrons to be either 0 or 1 randomly
    for layer in range(2):
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
          for feature in self.features:
            intermediate_value[feature] = self.softmax(trainingData[i][feature] * self.layer_weights[0][j][feature], self.layer_weights[0][j], trainingData[i])
          value = intermediate_value * self.layer_weights[1][j]
          sums[j] = value
#		If the label was incorrect, then decrease the weights of the obtained label and increase the weights of the correct label
        if sums.argMax() != trainingLabels[i]:
          for feature in self.features:
            self.layer_weights[1][sums.argMax()] -= (trainingData[i][feature] * self.intermediate_value[feature])
            self.layer_weights[1][trainingLabels[i]] += (trainingData[i][feature] * self.intermediate_value[feature])
		  
		  #EDIT THIS PART IT'S PROBABLY WRONG
          for weight in self.features:
            wrong_output = 0
            for feature in self.features:
              hj = self.softmax(trainingData[i][feature] * self.layer_weights[0][sums.argMax()][feature], self.layer_weights[0][sums.argMax()], trainingData[i])
              wrong_output += ((self.softmax(trainingData[i][feature] * self.layer_weights[1][sums.argMax()][feature], self.layer_weights[1][sums.argMax()], trainingData[i]) - trainingData[i][feature]) * self.layer_weights[0][sums.argMax()][feature] * hj * (1 - hj))
            self.layer_weights[0][sums.argMax()][weight] -= wrong_output
            for feature in self.features:
              hj = self.softmax(trainingData[i][feature] * self.layer_weights[0][trainingLabels[i]][feature], self.layer_weights[0][trainingLabels[i]], trainingData[i])
              correct_output += ((self.softmax(trainingData[i][feature] * self.layer_weights[1][trainingLabels[i]][feature], self.layer_weights[1][trainingLabels[i]], trainingData[i]) - trainingData[i][feature]) * self.layer_weights[0][trainingLabels[i]][feature] * hj * (1 - hj))
            self.layer_weights[0][trainingLabels[i]][feature] += trainingData[i][feature] * correct_output * (1 - correct_output)
		  #END EDITING PART

    
  def classify(self, data ):
    self.features = data[0].keys()
  
    guesses = []
    for datum in data:
      vectors = util.Counter()
      intermediate_value = util.Counter()
      for l in self.legalLabels:
        for feature in self.features:
          intermediate_value[feature] = self.sigmoid(datum[feature] * self.layer_weights[0][l][feature])
        vectors[l] = intermediate_value * self.layer_weights[1][l]
      guesses.append(vectors.argMax())
    return guesses