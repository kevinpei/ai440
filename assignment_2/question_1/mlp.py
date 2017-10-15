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
          intermediate_value = util.Counter();
          for feature in self.features:
            intermediate_value[feature] = trainingData[i][feature] * self.layer_weights[0][j][feature]
          for x in range(1, self.layer_number - 1):
            for feature in self.features:
              intermediate_value[feature] = intermediate_value[feature] * self.layer_weights[x][j][feature]
          value = intermediate_value * self.layer_weights[self.layer_number - 1][j]
          sums[j] = value
#		If the label was incorrect, then decrease the weights of the obtained label and increase the weights of the correct label
        if sums.argMax() != trainingLabels[i]:
          self.layer_weights[0][sums.argMax()] -= trainingData[i]
          self.layer_weights[0][trainingLabels[i]] += trainingData[i]
		  
		  #EDIT THIS PART IT'S PROBABLY WRONG
          for x in range(1, self.layer_number):
            wrong_label_error = self.layer_weights[x][sums.argMax()] - self.layer_weights[x-1][sums.argMax()]
            right_label_error = self.layer_weights[x][trainingLabels[i]] - self.layer_weights[x-1][trainingLabels[i]]
            wrong_data = util.Counter()
            right_data = util.Counter()
            for feature in self.features:
              wrong_data[feature] = wrong_label_error[feature] * self.layer_weights[x][sums.argMax()][feature]
              right_data[feature] = right_label_error[feature] * self.layer_weights[x][trainingLabels[i]][feature]
            self.layer_weights[x][sums.argMax()] -= wrong_data
            self.layer_weights[x][trainingLabels[i]] += right_data
		  #END EDITING PART

    
  def classify(self, data ):
    self.features = data[0].keys()
  
    guesses = []
    for datum in data:
      vectors = util.Counter()
      intermediate_value = util.Counter()
      for l in self.legalLabels:
        for feature in self.features:
          intermediate_value[feature] = datum[feature] * self.layer_weights[0][l][feature]
        for x in range(1, self.layer_number - 1):
          for feature in self.features:
            intermediate_value[feature] = intermediate_value[feature] * self.layer_weights[x][l][feature]
        vectors[l] = intermediate_value * self.layer_weights[self.layer_number - 1][l]
      guesses.append(vectors.argMax())
    return guesses