# svm.py
# -------------

# svm implementation
import util
PRINT = True

class SVMClassifier:
  """
  svm classifier
  """
  def __init__( self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "svm"
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    print "Starting iteration ", iteration, "..."
    for i in range(len(trainingData)):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
    
  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
      "*** YOUR CODE HERE ***"
      util.raiseNotDefined()
      
    return guesses

