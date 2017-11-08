def readStart(filename):
    data = open(filename)
    start = data.readline()
    data.close()
    coordinates = start.split("\n")[0].split(",")
    return (float(coordinates[0]), float(coordinates[1]))

def readGoal(filename):
    data = open(filename)
    data.readline()
    goal = data.readline()
    data.close()
    coordinates = goal.split("\n")[0].split(",")
    return (float(coordinates[0]), float(coordinates[1]))

def createGrid(filename, rows):
    data = open(filename)
    for x in range(10):
        data.readline()
    grid = []
    for x in range(rows):
        grid.append(list(data.readline().split("\n")[0]))
    data.close()
    return grid
    