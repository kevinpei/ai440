import tkinter as tk
import random as r
import math as m

class mapNode:
    def __init__(self, block, highway):
        self.block = block
        self.highway = highway

def createRoughTerrain(arr, width, height):
    pairs = []
    for x in range(8):
        pairs.append([r.randint(0,width),r.randint(0,height)])
    for pair in pairs:
        for x in range(31):
            if pair[0] + 15 - x >= 0 and pair[0] + 15 - x < width:
                for y in range(31):
                    if pair[1] + 15 - y >= 0 and pair[1] + 15 - y < height:
                        if r.random() > 0.5:
                            arr[pair[0] + 15 - x][pair[1] + 15 - y].block = 1
    return pairs
    
def generateHighwayStart(width, height):
    start = [0,0]
    direction = [0,0]
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
    
def createHighway(arr, width, height):
    highwayNodes = []
    highwayStart = generateHighwayStart(width, height)
    highwayNodes.append(highwayStart[0])
    direction = highwayStart[1]
    invalids = 0
    invalid = 0
    while invalids < 100:
        for x in range(20):
            nextx = highwayNodes[len(highwayNodes) - 1][0] + direction[0]
            nexty = highwayNodes[len(highwayNodes) - 1][1] + direction[1]
            if nextx >= 0 and nexty >= 0 and nextx < width and nexty < height:
                if [nextx, nexty] not in highwayNodes and arr[nextx][nexty].highway == 0:
                    highwayNodes.append([nextx, nexty])
                else:
                    invalids+=1
                    invalid = 1
                    break
            else:
                if len(highwayNodes) >= 100:
                    return highwayNodes
                else:
                    invalids+=1
                    invalid = 1
                    break
        if invalid == 1:
            highwayNodes = []
            highwayStart = generateHighwayStart(width, height)
            highwayNodes.append(highwayStart[0])
            direction = highwayStart[1]
            invalid = 0
        else:
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
   
def createBlocks(arr, width, height):
    for x in range(width):
        for y in range(height):
            if r.random() < 0.2:
                if arr[x][y].highway == 0:
                    arr[x][y].block = 2
    return

def getEuclideanDistance(coordinate1, coordinate2):
    return m.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)

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

def generateStartandFinish(arr, width, height):
    start = generateBorderCoordinates(width, height)
    while arr[start[0]][start[1]].block != 2:
        start = generateBorderCoordinates(width, height)
    return start               

def arrayGen(width, height, filename):
    newArr = [[mapNode(0,0) for x in range(height)] for y in range(width)]
    roughCenters = createRoughTerrain(newArr, width, height)
    generateHighways(newArr, width, height)
    createBlocks(newArr, width, height)
    start = generateStartandFinish(newArr, width, height)
    goal = generateStartandFinish(newArr, width, height)
    while getEuclideanDistance(start, goal) < 100:
        start = generateStartandFinish(newArr, width, height)
        goal = generateStartandFinish(newArr, width, height)
    file = open(filename, 'a')
    file.write(str(start[0]) + ',' + str(start[1]) + '\n')
    file.write(str(goal[0]) + ',' + str(goal[1]) + '\n')
    for coordinate in roughCenters:
        file.write(str(coordinate[0]) + ',' + str(coordinate[1]) + '\n')
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
        
x = arrayGen(120, 160, 'test.txt')