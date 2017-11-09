#Importing all necessary libraries
import heapq as h
import math as m

#Dictionary containing inferred costs for each terrain type. Use to calculate cost for traveling between cells.
costOf = {"1": 1, "2": 2, "a":.25, "b":.5}

#Initializing fringe and closed list
#Might be better to initialize these separately and have this as its own method
#Pass it a map, and start node have it return a list of the path with [0] being start and [n] being the goal.

#Vertices are used to track A*'s progress across the grid. Each vertex has coordinate values for its position, a parent, and f, g, and h values which can be udpated.
class vertex:
    def __init__(self, coordinate, parent, terrain, fVal, gVal, hVal):
        self.coordinate = coordinate
        self.parent = parent
        self.terrain = terrain
        #Possible to initialize this last and set it equal to sum of gVal and hVal?
        self.fVal = fVal
        self.gVal = gVal
        self.hVal = hVal

class aStarSearcher:
    def __init__(self, gridWorld, startCoordinate, goalCoordinate):
        #Initializing search variables
        self.gridWorld = gridWorld
        self.startCoordinate = startCoordinate
        self.goalCoordinate = goalCoordinate
        
        self.fringe = []
        self.closedList = {}
        self.searchPath = []
    
    #Euclidean distance heuristic, for use while prototyping A* search
    def getEuclideanDistance(self, coordinate1, coordinate2):
        return m.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)
    
    def getPath(self, current, path):
        totalPath = [current]
        while current.parent in path:
            current = path[current.parent]
            totalPath.append(current)
        return totalPath

    #Identifies the valid (nothing off grid) neighboring cells of the 8 adjacent cells to a coordinate and returns a list containing these neighbors initialized to vertices
    #Ignorant of parents and impassable terrain on purpose
    def getSuccessors(self, coordinate, parentCoordinate):
    #Utilizes 2D array based calculations to identify 8 adjacent cells. Assigns terrain values to each.
    
        #Return list of adjacent cells
        neighbors = []
    
        #Iterating over x values
        for x in range (-1, 2):
            for y in range(-1, 2):
                #Skipping the coordinate itself to avoid having 9 coordiantes
                if (x != 0 and y != 0) or (x != parentCoordinate[0] and y != parentCoordinate[1]):
                    try:
                        print(self.gridWorld[coordinate[0]+x][coordinate[1]+y])
                        neighbors.append(vertex((coordinate[0]+x, coordinate[1]+y), None, self.gridWorld[coordinate[0]+x][coordinate[1]+y], 0, 0, 0))
                    except IndexError:
                        continue    
        return neighbors
    
    #Checks if the vertex is in the heap, priority queue fringe. Accepts a vertex class object and returns True or False
    def inFringe(self, vertex):
        for x in self.fringe:
            if vertex.coordinate == x[1].coordinate:
                return True
        return False
    
    #Identifies the cost of traveling between two vertices using the terrain and coordinate values
    def getCost(self, vertex1, vertex2):
        x_difference = vertex2.coordinate[0] - vertex1.coordinate[0]
        y_difference = vertex2.coordinate[1] - vertex1.coordinate[0]
        #If the x difference or y difference is 0, then the movement is horizontal/vertical
        #This means that cost is just 1/2 cost of vertex 1 + 1/2 cost vertex 2
        if x_difference == 0 or y_difference == 0:
            return 0.5 * costOf[self.gridWorld[vertex1.coordinate[0]][vertex1.coordinate[1]]] + 0.5 * costOf[self.gridWorld[vertex2.coordinate[0]][vertex2.coordinate[1]]]
        #If both differences are not 0, then this means movement is diagonal
        #Cost is 1/2 * sqrt(2) * cost of the vertices
        else:
            diagonal_1 = 0.5 * costOf[self.gridWorld[vertex1.coordinate[0]][vertex1.coordinate[1]]] * m.sqrt(2)
            diagonal_2 = 0.5 * costOf[self.gridWorld[vertex2.coordinate[0]][vertex2.coordinate[1]]] * m.sqrt(2)
            return diagonal_1 + diagonal_2
        
    def updateVertex(self, current, successor):
        #If the successor is new (infinite g value)
        if current.gVal + self.getEuclideanDistance(current.coordinate, successor.coordinate) < successor.gVal:
            #Assigning f,g,h values and parent to successor
            successor.gVal = current.gVal + self.getCost(current, successor)
            successor.hVal = self.getEuclideanDistance(successor.coordinate, self.goalCoordinate)
            successor.fVal = successor.gVal + successor.hVal
            successor.parent = current.coordinate
            
            #Updates priority of successor by removing and readding the successor to the fringe. Otherwise adds new successor to fringe
            if self.inFringe(successor):
                self.fringe.remove((successor.fVal, successor))
                h.heapify(self.fringe)
            h.heappush(self.fringe, (successor.fVal, successor))

    #Will be using euclidean distance heuristic written by K. Pei, should make algorithm modular as we develop the project.        
    def aStarSearch(self):
    
        #Initializing start vertex
        #Must be an unblocked cell
        startVertex = vertex(self.startCoordinate, None, 1, 0, 0, 0)
        startVertex.parent = startVertex.coordinate
        startVertex.hVal = self.getEuclideanDistance(startVertex.coordinate, self.goalCoordinate)
        startVertex.fVal = startVertex.gVal + startVertex.hVal
    
        #Adding the start vertice to the fringe
        h.heappush(self.fringe, (startVertex.fVal, startVertex))
    
        #Main searching loop
        while len(self.fringe)>0:
            search = h.heappop(self.fringe)[1]
            #Checking if goal found
            if search.coordinate[0] == self.goalCoordinate[0] and search.coordinate[1] == self.goalCoordinate[1]:
                print("Path found")
                return self.getPath(search, self.searchPath)
            #Setting current node to have been visited and checked
            self.closedList[search.coordinate] = True
        
            #Identifying successors
            print(search.parent)
            newSuccessors = self.getSuccessors(search.coordinate, search.parent)
        
            #Iterating through successors
            for successor in newSuccessors:
                #Checking if successor was already visited
                if successor.coordinate in self.closedList == False:
                    #Checking if successor is not in the fringe, it is a new successor. Assign g and parent
                    if not self.inFringe(successor):
                        successor.gVal = m.inf
                        successor.parent = None
                    #Update the values of the fringe nodes based on the new current node (popped from fringe)
                    self.updateVertex(search, successor)
        return None
