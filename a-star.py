import math

'''
Graph Traversal Algorithm that goes from the initialCity to the arrivingCity in the least optimal amount of distance in miles.
It's a combination of Dijkstra's Algorithm + Greedy Search Algorithm.
'''
def a_star(initialCity, arrivingCity):
    # Path from initialCity to arrivingCity
    traversal_path = [initialCity]
    
    # Cities that have been traversed
    seenCities = [initialCity]

    # List of cities to be compared to for least distance travelled and that haven't been traversed through 
    distanceQueue = []

    # List of all paths taken with backtracking
    allPaths = []

    # Minimum distance it takes to get to a city
    minimumDistance = None
    minimumCity = ""

    # Loop until initialCity is equal to arrivedCity and end loop
    while initialCity != arrivingCity:
        # nested loop through all nearest cities of currentCity to find SLD (straight line distance) 
        for city in mapDict[initialCity]:
            # Add city to list of seen cities if not visited, skip the city if it has been visited
            if city[0] in seenCities:
                continue
            else:
                seenCities.append(city[0])

            # Check SLD amount from initialcity to all city neighbors
            SLD = haversineFormulaConversion(coordinateDict[city[0]], coordinateDict[arrivingCity])
            
            # Add distance with SLD
            distance = SLD + float(city[1])

            # Add distance to list of cities visited
            distanceQueue.append([distance, city[0]])

            # Find minimum distance out of all neighbors of the current city
            if minimumDistance is None or distance < minimumDistance:
                minimumDistance = distance
                minimumCity = city[0]

        # Find the city with the minimum distance in queue currently
        element = min(distanceQueue)

        # If the element is less than the neighboring minimum distance found, that means the element is found elsewhere in the graph and is not a neighbor of the current city.
        if not minimumDistance or element[0] < minimumDistance:
            minimumCity = element[1]

            # Add path to list of paths traversed
            allPaths.append(traversal_path)

            # Find a path to that minimum city
            traversal_path = correction_path(allPaths, minimumCity)

        else:
            element = [minimumDistance, minimumCity]

        # Remove minimum element from the queue
        distanceQueue.pop(distanceQueue.index(element))
        
        # Set minimumCity as new initialCity and reset minimumDistance
        initialCity = minimumCity  
        minimumDistance = None

        traversal_path.append(initialCity)

    return traversal_path

'''
This function works by how it checks a given path in allPaths, checks to see if a given 
city in the path has the startingPoint as its neighbor and appends the city until startingPoint is found.
Returns the path taken to that startingPoint.
'''
def correction_path(allPaths, startingPoint):
    newPath = []
    
    for path in allPaths:
        for city in path:
            newPath.append(city)

            for neighbor in mapDict[city]:
                if neighbor[0] == startingPoint:
                    return newPath

        # Clear the list only if the path taken doesn't have the startingPoint as a neighbor in any of the cities in the path.
        newPath.clear()
            
    return newPath

'''
Distance calculator for the path taken 
from starting point to the destination.
'''
def distance_calculator(traversal_path):
    distance = 0
    
    for i in range(len(traversal_path) - 1):
        startingCity = traversal_path[i]

        for city in mapDict[startingCity]:
            if traversal_path[i + 1] == city[0]:
                distance += city[1]
    
    return distance

'''
Convert latitude and longitude to be the straight line distance between
two connected cities
'''
def haversineFormulaConversion(city1Coordinate, city2Coordinate):
    [p1, p2] = [city1Coordinate[0] * (math.pi / 180), city2Coordinate[0] * (math.pi / 180)]
    [a1, a2] = [city1Coordinate[1] * (math.pi / 180), city2Coordinate[1] * (math.pi / 180)]

    # Radius of Earth
    r = 3958.8

    distance = 2 * r * math.asin(math.sqrt( (math.sin((p2 - p1) / 2) ** 2) + (math.cos(p1) * math.cos(p2)) * (math.sin((a2 - a1) / 2) ** 2)))
    return distance

# Reading from coordinates.txt and putting the city name in 
# the dictionary as a key with the coordinate as a value
coordinateFile = open('coordinates.txt', 'r')
coordinateDict = {}

for line in coordinateFile:
    # Slice line to stop at the ":"
    cityName = line[:line.index(":")]

    # Remove any parentheses 
    coordinate = line[line.index("(") + 1: line.index(")")]
    coordinate = coordinate.split(",")
    
    # Assign the cityName to that coordinate as a key-value pair
    coordinateDict[cityName] = [float(coordinate[0]), float(coordinate[1])]

'''
for x, y in coordinateDict.items():
    print(x, ":", y)
'''

# Reading from map.txt
mapFile = open('map.txt', 'r')
mapDict = {}

# Dictionary will store the cityName as the key and the value will be an array of [city, distance] elements
# that are connected to the key
for line in mapFile:
    cityName = line[:line.index("-")]
    
    # Slice the line to include just connected cities and distance
    connectedCities = line[line.index("-") + 1:]

    # Split at the comma to just have it be "city(number)"
    cityNameDistanceList = connectedCities.split(",")

    arr = []
    for i in range(len(cityNameDistanceList)):
        # Remove any parentheses
        city = cityNameDistanceList[i][:cityNameDistanceList[i].index("(")]
        distance = cityNameDistanceList[i][cityNameDistanceList[i].index("(") + 1: cityNameDistanceList[i].index(")")]
        
        arr.append([city, float(distance)])
    
    mapDict[cityName] = arr


# Test Case Code
pairs = [["SanFrancisco", "LongBeach"], ["Eureka", "Monterey"], ["Monterey", "SanDiego"], ["Yosemite", "LongBeach"], ["LongBeach", "SanFrancisco"], ["Eureka", "SouthLakeTahoe"]]

for pair in pairs:
    
    print("From city:", pair[0])
    print("To city:", pair[1])

    optimal_route = a_star(pair[0], pair[1])
    route = ""
    for i in range(len(optimal_route)):
        if i == len(optimal_route) - 1:
            route += optimal_route[i]
            break

        route += optimal_route[i] + " - "

    print("Best Route:", route)
    print("Total distance:", "{0:.2f}".format(distance_calculator(optimal_route)), "mi")

    print()

'''
Actual output for assignment:

print("From city:", startingCity)
print("To city:", arrivingCity)

route = ""
for i in range(len(optimal_route)):
    if i == len(optimal_route) - 1:
        route += optimal_route[i]
        break

    route += optimal_route[i] + " - "

print("Best Route:", route)
print("Total distance:", distance_calculator(optimal_route), "mi")
'''

'''
Example Output:

python a-star.py SanFrancisco LongBeach
From city: SanFrancisco
To city: LongBeach
Best Route: SanFrancisco - SanJose - Fresno - LosAngeles - LongBeach
Total distance: 442.50 mi

From city: Eureka
To city: Monterey
Best Route: Eureka - SanFrancisco - SanJose - Monterey
Total distance: 391.10 mi

From city: Monterey
To city: SanDiego
Best Route: Monterey - SantaBarbara - SantaMonica - SanDiego
Total distance: 416.70 mi

From city: Yosemite
To city: LongBeach
Best Route: Yosemite - Fresno - LosAngeles - LongBeach
Total distance: 306.80 mi

From city: LongBeach
To city: SanFrancisco
Best Route: LongBeach - LosAngeles - Fresno - SanJose - SanFrancisco
Total distance: 442.50 mi

From city: Eureka
To city: SouthLakeTahoe
Best Route: Eureka - Sacramento - SouthLakeTahoe
Total distance: 392.00 mi
'''
