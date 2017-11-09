import aStar as aStar
import FileReader as filereader
import mapMaker as mapMaker
import weighted_aStar as weighted

filename = 'test.txt'

startCoordinate = filereader.readStart(filename)
goalCoordinate = filereader.readGoal(filename)

print(goalCoordinate)

gridWorld = filereader.createGrid(filename,120)

pathFinder = aStar.aStarSearcher(gridWorld, startCoordinate, goalCoordinate)
output = pathFinder.aStarSearch()
print(output)
