'''
coordinates.txt is for latitude and longitude of each city.

map.txt has the distance from one city to another

Program has to:
    - parse the .txt files
    - take a departing city and an arriving city as input arguments
    - output an optimal route from the departing city to the arriving city

Example Output:

python a-star.py SanFrancisco LongBeach
From city: SanFrancisco
To city: LongBeach
Best Route: SanFrancisco - SanJose - Fresno - LosAngeles - LongBeach
Total distance: 442 mi

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
import math
from haversine import haversine, Unit

'''
Evalulation Function: f(n) = g(n) + h(n)
    - g(n) = cost so far to reach n
    - h(n) = estimated cost to goal from n
    - f(n) = estimated total cost of path through n to goal

A* Algorithm is a combination of Dijkstra's algorithm and greedy search
'''
def a_star(initialCity, arrivingCity):
    # Base conditions
    traversal_path = [initialCity]
    
    # Cities that have been traversed
    seenCities = [initialCity]

    # Queue to keep track of distances of other cities so that we can go to it immediately
    distanceQueue = []
    print(initialCity)
    # Loop until initialCity is equal to arrivedCity and end loop
    while initialCity != arrivingCity:
        # nested loop through all nearestCities of currentCity to find SLD (straight line distance)
        for city in mapDict[initialCity]:
            if city[0] in seenCities:
                continue
            else:
                seenCities.append(city[0])

            # Check SLD amount from initialcity to all city neighbors
            SLD = haversineFormulaConversion(coordinateDict[initialCity], coordinateDict[city[0]])
            
            # Add distance with SLD
            # Evalulation Function: f(n) = g(n) + h(n)
            
            distance = SLD + float(city[1])

            distanceQueue.append([distance, city[0]])

        element = min(distanceQueue)
        distanceQueue.pop(distanceQueue.index(element))

        initialCity = element[1]         
        traversal_path.append(initialCity)

    return traversal_path      

# Convert latitude and longitude to be the straight line distance between
# two connected cities
def haversineFormulaConversion(city1Coordinate, city2Coordinate):
    p1 = city1Coordinate[0] * (math.pi / 180)
    p2 = city2Coordinate[0] * (math.pi / 180)
    a1 = city1Coordinate[1] * (math.pi / 180)
    a2 = city2Coordinate[1] * (math.pi / 180)

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


startingCity = "Yosemite"
arrivingCity = "LongBeach"

'''
for city in mapDict[startingCity]:
    arrivingCity = city[0]

    print(startingCity, "to", arrivingCity)
    print(haversineFormulaConversion(coordinateDict[startingCity], coordinateDict[arrivingCity]) + city[1])
    print(haversine(coordinateDict[startingCity], coordinateDict[arrivingCity], unit="mi") + city[1])
    print()
'''

optimal_route = a_star(startingCity, arrivingCity)

print(optimal_route)