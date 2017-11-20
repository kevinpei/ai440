
# coding: utf-8

#Importing all necessary libraries
import tkinter as tk
import random as r
import math as m
import wx
import wx.grid

#Reads the start coordinates from the given file
def readStart(filename):
    data = open(filename)
    start = data.readline()
    data.close()
    coordinates = start.split("\n")[0].split(",")
    return (int(coordinates[0]), int(coordinates[1]))

#Reads the goal coordinates from the given file
def readGoal(filename):
    data = open(filename)
    data.readline()
    goal = data.readline()
    data.close()
    coordinates = goal.split("\n")[0].split(",")
    return (int(coordinates[0]), int(coordinates[1]))

#Reads the grid from the given file and returns an array of that grid
def createGrid(filename, rows):
    data = open(filename)
    for x in range(10):
        data.readline()
    grid = []
    for x in range(rows):
        grid.append(list(data.readline().split("\n")[0]))
    data.close()
    return grid

#A class to represent a node on the map. It has a variable to keep track of the type of terrain and whether it has a highway
class mapNode:
    def __init__(self, block, highway):
        self.block = block
        self.highway = highway

#A function to randomly choose 8 points to start rough patches
def createRoughTerrain(arr, width, height):
    pairs = []
    for x in range(8):
        pairs.append([r.randint(0,width),r.randint(0,height)])
    #For each center of each rough patch, randomly create rough terrain in a 31x31 area
    for pair in pairs:
        for x in range(31):
            if pair[0] + 15 - x >= 0 and pair[0] + 15 - x < width:
                for y in range(31):
                    if pair[1] + 15 - y >= 0 and pair[1] + 15 - y < height:
                        #50% chance to make it rough
                        if r.random() > 0.5:
                            arr[pair[0] + 15 - x][pair[1] + 15 - y].block = 1
    return pairs

#A function to create the start of highways randomly
def generateHighwayStart(width, height):
    start = [0,0]
    direction = [0,0]
    #Randomly choose a starting place for the highway from the edge and its direction
    if r.random() > 0.5:
        startx = r.randint(0, width - 1)
        if r.random() > 0.5:
            direction = [0,-1]
            start = [startx, height - 1]
        else:
            direction = [0,1]
            start = [startx, 0]
    else:
        starty = r.randint(0, height - 1)
        if r.random() > 0.5:
            direction = [1,0]
            start = [0, starty]
        else:
            direction = [-1,0]
            start = [width - 1, starty]
    return [start, direction]
 
#A function to create a highway given a grid and its size
def createHighway(arr, width, height):
    highwayNodes = []
    highwayStart = generateHighwayStart(width, height)
    highwayNodes.append(highwayStart[0])
    direction = highwayStart[1]
    invalids = 0
    invalid = 0
    #If invalids reaches 100, then assume no highways are possible
    while invalids < 100:
        #Go 20 segments forward
        for x in range(20):
            nextx = highwayNodes[len(highwayNodes) - 1][0] + direction[0]
            nexty = highwayNodes[len(highwayNodes) - 1][1] + direction[1]
            if nextx >= 0 and nexty >= 0 and nextx < width and nexty < height:
                #Only add the next segment if it's not part of the current highway and it's not part of another highway
                if [nextx, nexty] not in highwayNodes and arr[nextx][nexty].highway == 0:
                    highwayNodes.append([nextx, nexty])
                else:
                    invalids+=1
                    invalid = 1
                    break
            else:
                #Only return if the highway is at least 100 segments long
                if len(highwayNodes) >= 100:
                    return highwayNodes
                else:
                    invalids+=1
                    invalid = 1
                    break
        #If the highway was created invalidly, then create another highway
        if invalid == 1:
            highwayNodes = []
            highwayStart = generateHighwayStart(width, height)
            highwayNodes.append(highwayStart[0])
            direction = highwayStart[1]
            invalid = 0
        else:
            #20% chance to turn right, 20% chance to turn left, 60% chance to go straight
            randFloat = r.random()
            if randFloat < 0.2:
                if direction[0] == 0:
                    direction = [direction[1],direction[0]]
                else:
                    direction = [-direction[1],-direction[0]]
            elif randFloat < 0.4 and randFloat > 0.2:
                if direction[0] == 0:
                    direction = [-direction[1],-direction[0]]
                else:
                    direction = [direction[1],direction[0]]
    return [0]
   
#A function to generate all 4 highways in the given grid
def generateHighways(arr, width, height):
    x = 0
    while x < 4:
        nodes = createHighway(arr, width, height)
        if len(nodes) >= 100:
            for node in nodes:
                arr[node[0]][node[1]].highway = 1
            x += 1
        else:
            for x in range(width):
                for y in range(height):
                    arr[x][y].highway = 0
            x = 0
    return
   
#A function to randomly create impassable blocks in the grid
def createBlocks(arr, width, height):
    for x in range(width):
        for y in range(height):
            if r.random() < 0.2:
                if arr[x][y].highway == 0:
                    arr[x][y].block = 2
    return

#A function to get euclidean distance between two tuples
def getEuclideanDistance(coordinate1, coordinate2):
    return m.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)

#A function to get coordinates for the start and goal nodes
def generateBorderCoordinates(width, height):
    if r.random() < 0.5:
        startx = r.randint(0, width - 1)
        if r.random() < 0.5:
            starty = r.randint(0, 19)
        else:
            starty = r.randint(height - 20, height - 1)
        return [startx, starty]
    else:
        starty = r.randint(0, height - 1)
        if r.random() < 0.5:
            startx = r.randint(0, 19)
        else:
            startx = r.randint(width - 20, width - 1)
        return [startx, starty]

    #A function to return start and end goals
def generateStartandFinish(arr, width, height):
    start = generateBorderCoordinates(width, height)
    while arr[start[0]][start[1]].block == 2:
        start = generateBorderCoordinates(width, height)
    return start               

#Create a grid with the given width and height and store it in the given file
def arrayGen(width, height, filename):
#Create an empty array 
    newArr = [[mapNode(0,0) for x in range(height)] for y in range(width)]
    roughCenters = createRoughTerrain(newArr, width, height)
    generateHighways(newArr, width, height)
    createBlocks(newArr, width, height)
    start = generateStartandFinish(newArr, width, height)
    goal = generateStartandFinish(newArr, width, height)
    #The start and goal must be at least 100 away from each other
    while getEuclideanDistance(start, goal) < 100:
        start = generateStartandFinish(newArr, width, height)
        goal = generateStartandFinish(newArr, width, height)
    file = open(filename, 'w')
    file.write('')
    file.close()
    file = open(filename, 'a')
    file.write(str(start[0]) + ',' + str(start[1]) + '\n')
    file.write(str(goal[0]) + ',' + str(goal[1]) + '\n')
    for coordinate in roughCenters:
        file.write(str(coordinate[0]) + ',' + str(coordinate[1]) + '\n')
    #Write a 0 for impassable, 1 for normal, 2 for rough, a for highway, and b for rough highway
    for x in range(width):
        for y in range(height):
            if newArr[x][y].block == 2:
                file.write('0')
            elif newArr[x][y].block == 1:
                if newArr[x][y].highway == 0:
                    file.write('2')
                else:
                    file.write('b')
            else:
                if newArr[x][y].highway == 0:
                    file.write('1')
                else:
                    file.write('a')
        file.write('\n')
    file.close()
    return newArr

class puzzleGrid:
    
    #A constructor for intializing a map. Accepts a master and 2D array as inputs. 
    #Produces a window displaying the values inside the input 2D Array
    def __init__(self, master, inArray):
        width = len(inArray)
        height = len(inArray[0])
        #Constructor loop iterates over all values in the input array and input their value in string form to a tkinter grid at an equivalent position
        for i in range(width):
            for j in range(height):
                tk.Label(master, text = (str(inArray[i][j].block) + ',' + str(inArray[i][j].highway)), padx = 0, pady = 0, relief = "sunken").grid(row=i, column=j)

#Performs a binary insertion, placing a new vertex in sorted order.
def vertexInsert(vertexList, vertex, start, end):
    m = (start + end)//2
    if m == start:
        vertexList.insert(m, vertex)
        return
    if vertexList[m].fVal < vertex.fVal:
        vertexInsert(vertexList, vertex, m, end)
    else:
        vertexInsert(vertexList, vertex, start, m)
#Automatically performs a binary insertion on a list of vertices.
def vertexPush(vertexList, vertex):
    vertexInsert(vertexList, vertex, 0, len(vertexList))
#Removes and returns the first vertex in the list.
def vertexPop(vertexList):
    return vertexList.pop(0)
def vertexPeek(vertexList):
    return vertexList[0]

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
    
    #Euclidean distance heuristic, for use while prototyping A* search
    def getEuclideanDistance(self, coordinate1, coordinate2):
        return m.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)
    
    def getPath(self, current):
        totalPath = [current.coordinate]
        while current.parent != current:
            current = current.parent
            totalPath.append(current.coordinate)
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
                if (x != 0 and y != 0) or ((x != parentCoordinate[0]) and (y != parentCoordinate[1])):
                    try:
                        if (self.gridWorld[coordinate[0]+x][coordinate[1]+y] != '0'):
                            neighbors.append(vertex((coordinate[0]+x, coordinate[1]+y), None, self.gridWorld[coordinate[0]+x][coordinate[1]+y], 0, 0, 0))
                    except IndexError:
                        continue    
        return neighbors
    
    #Checks if the vertex is in the heap, priority queue fringe. Accepts a vertex class object and returns True or False
    def inFringe(self, vertex):
        for x in self.fringe:
            if vertex.coordinate == x.coordinate:
                return True
        return False
    
    #Identifies the cost of traveling between two vertices using the terrain and coordinate values
    def getCost(self, vertex1, vertex2):
        x_difference = vertex2.coordinate[0] - vertex1.coordinate[0]
        y_difference = vertex2.coordinate[1] - vertex1.coordinate[1]
        total_cost = 0.5 * costOf[self.gridWorld[vertex1.coordinate[0]][vertex1.coordinate[1]]] + 0.5 * costOf[self.gridWorld[vertex2.coordinate[0]][vertex2.coordinate[1]]]
        #If the x difference or y difference is 0, then the movement is horizontal/vertical
        #This means that cost is just 1/2 cost of vertex 1 + 1/2 cost vertex 2
        if x_difference == 0 or y_difference == 0:
            return total_cost
        #If both differences are not 0, then this means movement is diagonal
        #Cost is 1/2 * sqrt(2) * cost of the vertices
        else:
            return total_cost * m.sqrt(2)
        
    def updateVertex(self, current, successor):
        #If the successor is new (infinite g value)
        if current.gVal + self.getEuclideanDistance(current.coordinate, successor.coordinate) < successor.gVal:
            #Assigning f,g,h values and parent to successor
            successor.gVal = current.gVal + self.getCost(current, successor)
            successor.hVal = 0.25 * self.getEuclideanDistance(successor.coordinate, self.goalCoordinate)
            successor.fVal = successor.gVal + successor.hVal
            successor.parent = current
            
            #Updates priority of successor by removing and readding the successor to the fringe. Otherwise adds new successor to fringe
            if self.inFringe(successor):
                self.fringe.remove(successor)
            vertexPush(self.fringe, successor)

    #Will be using euclidean distance heuristic written by K. Pei, should make algorithm modular as we develop the project.        
    def aStarSearch(self):
    
        #Initializing start vertex
        #Must be an unblocked cell
        startVertex = vertex(self.startCoordinate, None, 1, 0, 0, 0)
        startVertex.parent = startVertex
        startVertex.hVal = self.getEuclideanDistance(startVertex.coordinate, self.goalCoordinate)
        startVertex.fVal = startVertex.gVal + startVertex.hVal
    
        #Adding the start vertice to the fringe
        vertexPush(self.fringe, startVertex)
    
        #Main searching loop
        while len(self.fringe)>0:
            search = vertexPop(self.fringe)
            #Checking if goal found
            if search.coordinate[0] == self.goalCoordinate[0] and search.coordinate[1] == self.goalCoordinate[1]:
                print("Path found")
                return self.getPath(search)
            #Setting current node to have been visited and checked
            self.closedList[search.coordinate] = search
        
            #Identifying successors
            newSuccessors = self.getSuccessors(search.coordinate, search.parent.coordinate)
            #Iterating through successors
            for successor in newSuccessors:
                #Checking if successor was already visited
                if (successor.coordinate in self.closedList) == False:
                    #Checking if successor is not in the fringe, it is a new successor. Assign g and parent
                    if not self.inFringe(successor):
                        successor.gVal = float('inf')
                        successor.parent = None
                    #Update the values of the fringe nodes based on the new current node (popped from fringe)
                    self.updateVertex(search, successor)
        return None

class weightedAStarSearcher(aStarSearcher):
    def __init__(self, gridWorld, startCoordinate, goalCoordinate, weight, algoType):
        #Initializing search variables
        self.gridWorld = gridWorld
        self.startCoordinate = startCoordinate
        self.goalCoordinate = goalCoordinate
        if(algoType == "dijkstra"):
            self.weight = 0
        else:
            self.weight = weight
        
        self.fringe = []
        self.closedList = {}
    
    #Will be using euclidean distance heuristic written by K. Pei, should make algorithm modular as we develop the project.        
    def weightedSearch(self):
        #Initializing start vertex
        #Must be an unblocked cell
        startVertex = vertex(self.startCoordinate, None, 1, 0, 0, 0)
        startVertex.parent = startVertex
        startVertex.hVal = 0.25 * self.getEuclideanDistance(startVertex.coordinate, self.goalCoordinate)
        startVertex.fVal = startVertex.gVal + (self.weight * startVertex.hVal)
    
        #Adding the start vertice to the fringe
        vertexPush(self.fringe, startVertex)
    
        #Main searching loop
        while len(self.fringe)>0:
            search = vertexPop(self.fringe)
            #Checking if goal found
            if search.coordinate[0] == self.goalCoordinate[0] and search.coordinate[1] == self.goalCoordinate[1]:
                print("Path found")
                return self.getPath(search)
            #Setting current node to have been visited and checked. OH WAIT ARRAYS CAN'T BE FUCKING DICTIONARY KEYS
            self.closedList[search.coordinate] = search
        
            #Identifying successors
            newSuccessors = self.getSuccessors(search.coordinate, search.parent.coordinate)
        
            #Iterating through successors
            for successor in newSuccessors:
                #Checking if successor was already visited
                if (successor.coordinate in self.closedList) == False:
                    #Checking if successor is not in the fringe, it is a new successor. Assign g and parent
                    if self.inFringe(successor) is not True:
                        successor.gVal = float('inf')
                        successor.parent = None
                    #Update the values of the fringe nodes based on the new current node (popped from fringe)
                    self.updateVertex(search, successor)
        return None

#The panel that contains the grid
class gridPanel(wx.Panel):
    def __init__(self, parent, gridWorld, closedList, textPanel, nodes, seq=0):
        wx.Panel.__init__(self, parent=parent)
        self.closedList = closedList
        self.textPanel = textPanel
        self.grid = self.showGrid(gridWorld, nodes)
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onSelect)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.seq = seq

        
    #A method to show the grid given as input
    def showGrid(self, gridWorld, nodes):
        grid = wx.grid.Grid(self, size=(1200, 600))
        grid.CreateGrid(120, 160)
        grid.SetLabelFont(wx.Font(1, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #Color the grid depending on the terrain
        for x in range(120):
            for y in range(160):
                attr = self.cellAttr = wx.grid.GridCellAttr()
                color = (0, 0, 0)
                if gridWorld[x][y] == '0':
                    color = (255,0,0)
                elif gridWorld[x][y] == '1':
                    color = (0, 255, 0)
                elif gridWorld[x][y] == '2':
                    color = (255, 255, 0)
                elif gridWorld[x][y] == 'a':
                    color = (0, 125, 0)
                elif gridWorld[x][y] == 'b':
                    color = (125, 125, 0)
                if nodes[0][0] == x and nodes[0][1] == y:
                    color = (255, 255, 255)
                elif nodes[1][0] == x and nodes[1][1] == y:
                    color = (0, 0, 255)
                attr.SetBackgroundColour(color)
                grid.SetAttr(x, y, attr)
        for x in range(120):
            grid.SetRowLabelValue(x, "")
        grid.SetDefaultRowSize(5, True)
        for y in range(160):
            grid.SetColLabelValue(y, "")
        grid.SetDefaultColSize(5, True)
        grid.SetColLabelSize(0) 
        grid.SetRowLabelSize(0) 
        return grid

    #Change the values of each of the heuristics when a grid cell is selected
    def onSelect(self, event):
        if self.seq == 0:
            try:
                self.textPanel.gVal.SetLabel("g Value:" + str(self.closedList[event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal.SetLabel("h Value:" + str(self.closedList[event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal.SetLabel("f Value:" + str(self.closedList[event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal.SetLabel("g value: Infinity")
                self.textPanel.hVal.SetLabel("h value: Infinity")
                self.textPanel.fVal.SetLabel("f value: Infinity")
        else:
            try:
                self.textPanel.gVal.SetLabel("g Value:" + str(self.closedList[0][event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal.SetLabel("h Value:" + str(self.closedList[0][event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal.SetLabel("f Value:" + str(self.closedList[0][event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal.SetLabel("g value: Infinity")
                self.textPanel.hVal.SetLabel("h value: Infinity")
                self.textPanel.fVal.SetLabel("f value: Infinity")
            try:
                self.textPanel.gVal2.SetLabel("g Value:" + str(self.closedList[1][event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal2.SetLabel("h Value:" + str(self.closedList[1][event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal2.SetLabel("f Value:" + str(self.closedList[1][event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal2.SetLabel("g value: Infinity")
                self.textPanel.hVal2.SetLabel("h value: Infinity")
                self.textPanel.fVal2.SetLabel("f value: Infinity")
            try:
                self.textPanel.gVal3.SetLabel("g Value:" + str(self.closedList[2][event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal3.SetLabel("h Value:" + str(self.closedList[2][event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal3.SetLabel("f Value:" + str(self.closedList[2][event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal3.SetLabel("g value: Infinity")
                self.textPanel.hVal3.SetLabel("h value: Infinity")
                self.textPanel.fVal3.SetLabel("f value: Infinity")
            try:
                self.textPanel.gVal4.SetLabel("g Value:" + str(self.closedList[3][event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal4.SetLabel("h Value:" + str(self.closedList[3][event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal4.SetLabel("f Value:" + str(self.closedList[3][event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal4.SetLabel("g value: Infinity")
                self.textPanel.hVal4.SetLabel("h value: Infinity")
                self.textPanel.fVal4.SetLabel("f value: Infinity")
            try:
                self.textPanel.gVal5.SetLabel("g Value:" + str(self.closedList[4][event.GetRow(), event.GetCol()].gVal))
                self.textPanel.hVal5.SetLabel("h Value:" + str(self.closedList[4][event.GetRow(), event.GetCol()].hVal))
                self.textPanel.fVal5.SetLabel("f Value:" + str(self.closedList[4][event.GetRow(), event.GetCol()].fVal))
            except KeyError or IndexError:
                self.textPanel.gVal5.SetLabel("g value: Infinity")
                self.textPanel.hVal5.SetLabel("h value: Infinity")
                self.textPanel.fVal5.SetLabel("f value: Infinity")

#The panel that contains the text for f value, g value, and h value
class textPanel(wx.Panel):
    def __init__(self, parent, seq=0):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        ypos = 80
        if seq != 0:
            ypos = 0
        self.gVal = wx.StaticText(self, 10, "g Value: 0", size=(200,40), pos=(225, ypos))
        self.hVal = wx.StaticText(self, 10, "h Value: 0", size=(200,40), pos=(475, ypos))
        self.fVal = wx.StaticText(self, 10, "f Value: 0", size=(200,40), pos=(725, ypos))
        if seq != 0:
            self.heuristic = wx.StaticText(self, 10, "Anchor Heuristic", size=(200,40), pos=(25, 0))
            self.heuristic2 = wx.StaticText(self, 10, "Manhattan Distance", size=(200,40), pos=(25, 40))
            self.gVal2 = wx.StaticText(self, 10, "g Value: 0", size=(200,40), pos=(225, 40))
            self.hVal2 = wx.StaticText(self, 10, "h Value: 0", size=(200,40), pos=(475, 40))
            self.fVal2 = wx.StaticText(self, 10, "f Value: 0", size=(200,40), pos=(725, 40))
            self.heuristic3 = wx.StaticText(self, 10, "Diagonal Favorer", size=(100,25), pos=(25, 80))
            self.gVal3 = wx.StaticText(self, 10, "g Value: 0", size=(200,40), pos=(225, 80))
            self.hVal3 = wx.StaticText(self, 10, "h Value: 0", size=(200,40), pos=(475, 80))
            self.fVal3 = wx.StaticText(self, 10, "f Value: 0", size=(200,40), pos=(725, 80))
            self.heuristic4 = wx.StaticText(self, 10, "Highway Favorer", size=(100,25), pos=(25, 120))
            self.gVal4 = wx.StaticText(self, 10, "g Value: 0", size=(200,40), pos=(225, 120))
            self.hVal4 = wx.StaticText(self, 10, "h Value: 0", size=(200,40), pos=(475, 120))
            self.fVal4 = wx.StaticText(self, 10, "f Value: 0", size=(200,40), pos=(725, 120))
            self.heuristic5 = wx.StaticText(self, 10, "Diagonal Distance", size=(100,25), pos=(25, 160))
            self.gVal5 = wx.StaticText(self, 10, "g Value: 0", size=(200,40), pos=(225, 160))
            self.hVal5 = wx.StaticText(self, 10, "h Value: 0", size=(200,40), pos=(475, 160))
            self.fVal5 = wx.StaticText(self, 10, "f Value: 0", size=(200,40), pos=(725, 160))
    
#The application that will be shown to the user
class aStar(wx.Frame):
    
    #Constructor for the application is the same as the constructor for wx.Frame
    def __init__(self, parent, title, gridWorld, closedList, nodes, seq=0):
        super(aStar, self).__init__(parent, title=title, size=(1200, 850))
        self.seq = seq
        self.initUI(gridWorld, closedList, nodes)
        self.Centre()
        self.Show()
    
    #A function to initialize the UI with the grid
    def initUI(self, gridWorld, closedList, nodes):
        vbox = wx.BoxSizer(wx.VERTICAL)
        splitter = wx.SplitterWindow(self)
        text = textPanel(splitter, self.seq)
        grid = gridPanel(splitter, gridWorld, closedList, text, nodes, self.seq)
        splitter.SplitHorizontally(grid, text)
        splitter.SetMinimumPaneSize(600)
        vbox.Add(splitter, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)

class seqAStarSearcher(aStarSearcher):
    def __init__(self, gridWorld, startCoordinate, goalCoordinate):
        #Initializing search variables
        self.gridWorld = gridWorld
        self.startCoordinate = startCoordinate
        self.goalCoordinate = goalCoordinate
        
        #Initializing sequential search weights
        self.w1 = 1.25
        self.w2 = 2.00
        
        #Initialzing sequential search fringes
        #Using 4 additional heuristics (Anchor(0), ManhattanTransfer(1), NotoriousBIG(2), HighWayStar(3), Whitesnake(4))
        # 0 - Manhattan Distance
        # 1 - Euclidean squared, greedy
        # 2 - Favors highways
        # 3 - Diagonal distance * 1/4, admissible

        self.seqFringe = [[] for i in range(5)]
        self.seqClosed = [{} for i in range(5)]
        
    def getHeuristic(self, vertex, hIndex):
        # 0 - ANCHOR HEURISTIC, EUCLIDEAN DISTANCE
        if hIndex == 0:
            return .25 * m.sqrt((self.goalCoordinate[0] - vertex.coordinate[0]) ** 2 + (self.goalCoordinate[1] - vertex.coordinate[1]) ** 2)
        # 1 - MANHANTTAN TRANSFER
        elif hIndex == 1:
            xDistance = m.fabs(self.goalCoordinate[0]-vertex.coordinate[0])
            yDistance = m.fabs(self.goalCoordinate[1]-vertex.coordinate[1])
            return xDistance+yDistance
        # 2 - NOTORIOUS B.I.G. EUCLIDEAN SQUARED
        elif hIndex == 2:
            return (self.goalCoordinate[0] - vertex.coordinate[0]) ** 2 + (self.goalCoordinate[1] - vertex.coordinate[1]) ** 2
        # 3 - HIGHWAYSTAR
        elif hIndex == 3:
            if vertex.terrain == 'a':
                return 0
            elif vertex.terrain == 'b':
                return 1
            elif vertex.terrain == '1':
                return 5
            else:
                return 10
        # 4 - WHITESNAKE DIAGONAL DISTANCE
        elif hIndex == 4:
            xDistance = m.fabs(self.goalCoordinate[0]-vertex.coordinate[0])
            yDistance = m.fabs(self.goalCoordinate[1]-vertex.coordinate[1])
            #m.sqrt(2) - 2 * min(xDistance, yDistance) is how much is saved by going diagonally instead of Manhattan
            return 0.25 * (xDistance + yDistance + (m.sqrt(2) - 2) * min(xDistance, yDistance))
        # SOMETHING ELSE - SHIT
        else:
            return None
        
    def seqInFringe(self, vertex, heuristicID):
        for x in self.seqFringe[heuristicID]:
            if vertex.coordinate == x.coordinate:
                return True
        return False
    
    def updateVertex(self, current, successor, heuristicID):
        #If the successor is new (infinite g value)
        if current.gVal + self.getEuclideanDistance(current.coordinate, successor.coordinate) < successor.gVal:
            #Assigning f,g,h values and parent to successor
            successor.gVal = current.gVal + self.getCost(current, successor)
            successor.hVal = self.getHeuristic(successor, heuristicID)
            successor.fVal = successor.gVal + successor.hVal
            successor.parent = current
            
            #Updates priority of successor by removing and readding the successor to the fringe. Otherwise adds new successor to fringe
            if self.seqInFringe(successor, heuristicID):
                self.seqFringe[heuristicID].remove(successor)
            vertexPush(self.seqFringe[heuristicID], successor)
    
    def expandState(self, search, heuristicID):
        #Identifying successors
        newSuccessors = self.getSuccessors(search.coordinate, search.parent.coordinate)
        #Iterating through successors
        for successor in newSuccessors:
        #Checking if successor was already visited
            if (successor.coordinate in self.seqClosed[heuristicID]) == False:
            #Checking if successor is not in the fringe, it is a new successor. Assign g and parent
                if not self.seqInFringe(successor, heuristicID):
                    successor.gVal = float('inf')
                    successor.parent = None
            #Update the values of the fringe nodes based on the new current node (popped from fringe)
            self.updateVertex(search, successor, heuristicID)
    
    def seqAStarSearch(self):
        #Initialzing start vertex
        for i in range(5):
            startVertex = vertex(self.startCoordinate, None, 1, 0, 0, 0)
            startVertex.parent = startVertex
            startVertex.hVal = self.getHeuristic(startVertex, i)
            #print(startVertex.hVal)
            startVertex.fVal = startVertex.gVal + startVertex.hVal
            #Pushing new start vertex to corresponding fringe
            vertexPush(self.seqFringe[i], startVertex)
        
        #BEGINNING MAIN LOOP
        while len(self.seqFringe[0]) > 0:
            for i in range(1,5):
                #print("Iteration number: " + str(i))
                #set_trace()
                if vertexPeek(self.seqFringe[i]).fVal <= self.w2 * vertexPeek(self.seqFringe[0]).fVal:
                    search = vertexPeek(self.seqFringe[i])
                    if search.coordinate[0] == self.goalCoordinate[0] and search.coordinate[1] == self.goalCoordinate[1]:
                        print("Path found")
                        return self.getPath(search)
                    else:
                        search = vertexPop(self.seqFringe[i])
                        self.expandState(search, i)
                        self.seqClosed[i][search.coordinate] = search
                else:
                    search = vertexPeek(self.seqFringe[0])
                    if search.coordinate[0] == self.goalCoordinate[0] and search.coordinate[1] == self.goalCoordinate[1]:
                        print("Path found")
                        return self.getPath(search)
                    else:
                        search = vertexPop(self.seqFringe[0])
                        self.expandState(search,0)
                        self.seqClosed[0][search.coordinate] = search
        return None

def runAStar(which_star):
    filename = 'test.txt'
    arrayGen(120, 160, filename)
    startCoordinate = readStart(filename)
    goalCoordinate = readGoal(filename)
    gridWorld = createGrid('test.txt', 120)
    nodes = [startCoordinate, goalCoordinate]
    output = None
    if which_star == 1:
        pathFinder = aStarSearcher(gridWorld, startCoordinate, goalCoordinate)
        output = pathFinder.aStarSearch()
        if output != None:
            for point in output:
                gridWorld[point[0]][point[1]] = 'X'
        aStar(None, title="A*", gridWorld=gridWorld, closedList = pathFinder.closedList, nodes=nodes)
    elif which_star == 2:
        weight = input("Enter the weight. Please enter a decimal number. Enter 0 for Dijkstra's.")
        while not (isinstance(float(weight), float)):
            weight = input("Invalid input.\nEnter the weight. Please enter a decimal number.Enter 0 for Dijkstra's.")
        pathFinder = weightedAStarSearcher(gridWorld, startCoordinate, goalCoordinate, float(weight), 'Whof Caress')
        output = pathFinder.weightedSearch()
        if output != None:
            for point in output:
                gridWorld[point[0]][point[1]] = 'X'
        aStar(None, title="Weighted A*", gridWorld=gridWorld, closedList = pathFinder.closedList, nodes=nodes)
    elif which_star == 3:
        pathFinder = seqAStarSearcher(gridWorld, startCoordinate, goalCoordinate)
        output = pathFinder.seqAStarSearch()
        if output != None:
            for point in output:
                gridWorld[point[0]][point[1]] = 'X'
        aStar(None, title="Sequential A*", gridWorld=gridWorld, closedList = pathFinder.seqClosed, nodes=nodes, seq=1)
    test.MainLoop()

def main(bad):
    AType = input(bad + "Please choose which A Star you want to use. Would you like to use:\n1) A Star\n2) Weighted A Star\n3) Sequential A Star\n")
    if (not isinstance(int(AType), int)):
        return -1
    if int(AType) <= 0 or int(AType) >= 4:
        return -1
    runAStar(int(AType))
    return 1

test = None
test = wx.App()
AStarType = main("")
while aStar == -1:
    AStarType = main("Invalid input. ")
i = 0