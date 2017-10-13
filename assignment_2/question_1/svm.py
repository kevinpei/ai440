# svm.py
# -------------

# svm implementation
import util
#Import statement for scikit learn
from sklearn import svm
PRINT = True

class SVMClassifier:
  """
  svm classifier
  """
  def __init__( self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "svm"
    self.newMachine = svm.LinearSVC()
  
  def flatten_array(self, inArray):
    outArray=[]
    
    for x in range(len(inArray)):
        outArray.extend(inArray[x])
        
    return outArray

  #Accepts a trainingData dictionary. Returns a 2D array containing a reconstruction of the initial binary (0,1) image. This is inelegant but I want a solution NOW
  def reformatTrain(self, inputDic):
    #Initializing output VECTOR
    imageArr = [[0 for x in range(28)] for y in range(28)]

    #Itemizing dictionary & ripping data
    temp = inputDic.items()
    coordinates = [list(y) for y in [x[0] for x in temp]]
    features = [x[1] for x in temp]
    
    #Reforming 28x28 image
    for i in range(len(coordinates)):
      imageArr[coordinates[i][0]][coordinates[i][1]] = features[i]

    #Flattening...
    output = self.flatten_array(imageArr)

    #Returning output
    return output

  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    #print "Starting iteration ", iteration, "..."
    rebuiltImages= []
    for i in range(len(trainingData)):
      #Calling helper to format training Data dictionary.
      rebuiltImages.append(self.reformatTrain(trainingData[i]))
    self.newMachine.fit(rebuiltImages, trainingLabels)



    
  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
      guesses.append(self.reformatTrain(datum))
    return self.newMachine.predict(guesses).tolist()

