from Package import *


# The truck class is used to store the load of packages in the form of lists.
# The truck keeps track of current location and next location, as well as whether they completed the route.
# Mileage is all tracked to help keep track of how far the trucks are traveling and how far they need to travel.
# The space and time complexities for instantiating the truck are each O(1).
class Truck:
    def __init__(self, truckID, load, tempMileage, neededMileage, totalMileage, currentLocation, nextLocation,
                 routeComplete):
        self.truckID = int(truckID)
        # A list of package objects is used as the load.
        self.load = load
        # This helps keep track between current location and next location and is reset after each location.
        self.tempMileage = tempMileage
        # This is the distance that is needed to reach the next location from current location.
        self.neededMileage = neededMileage
        self.totalMileage = totalMileage
        # All trucks start at the hub then the nearest neighbor algorithm chooses the next location.
        self.currentLocation = currentLocation
        self.nextLocation = nextLocation
        # Once the truck has reached the hub after starting the route, the route is labeled complete.
        self.routeComplete = routeComplete

    # The time complexity O(n^2) and space complexity is O(n).
    # In this usage a list is pulled from the distance dictionary created within the main.py that aligns with the
    # address of the truck's current location. Each float within the list is compared to the previous float to see
    # which has the smallest distance. Once the list of length n(total addresses) is iterated through, the shortest
    # path is chosen. Although, the chosen address must match a package currently within the truck's load AND must
    # be currently not "Delivered".
    def nearestNeighborSearch(self, totalAddresses, distanceDictionary, addressDictionary):
        # Set the initial distance to a number greater than any of the distances from the distance table.
        nextAddressDistance = 20
        nextAddressIndex = 0
        routeComplete = True
        # Get the undelivered load specifically to filter what's left to deliver.
        undeliveredLoad = self.getUndeliveredLoad()
        # Initially set to None, first iteration needs to skip this, otherwise it would set it's new current location
        # to None which would stop the truck's progress and likely cause a future error.
        if self.nextLocation is not None:
            self.setCurrentLocation(self.nextLocation)
        # Retrieve the list of all distances from the current location from the distance dictionary created in main.
        distancesList = distanceDictionary.get(self.currentLocation)
        # Loop through the total number of addresses(27), compare each to the next finding the shortest.
        for i in range(totalAddresses):
            if float(distancesList[i]) < nextAddressDistance:
                # Iterates through the maximum load of 16(negligible impact on overall time and space complexity).
                for j in undeliveredLoad:
                    # If the needed address for the package equals the corresponding address found in the address
                    # dictionary created in main.py, then save the route complete to false and the next address
                    # index to the current index to use after this for loop. Save the distance until the shortest
                    # is found then use that as the needed miles.
                    if j.getDeliveryAddress() == addressDictionary.get(i):
                        nextAddressDistance = float(distancesList[i])
                        nextAddressIndex = i
                        routeComplete = False
        # If routeComplete is true then the following will not get executed, which means there are no more
        # undelivered packages left in the load. Otherwise, the temp miles get reset to 0 and the needed miles
        # get set to the needed miles to reach the next address.
        if not routeComplete:
            self.setNextLocation(addressDictionary.get(nextAddressIndex))
            self.setTempMiles(0)
            self.setNeededMiles(nextAddressDistance)

    # Used in the main.py after all packages are delivered by a truck. It retrieves the distances from the distance
    # dictionary from the current location, sets the current location to the previous next location, resets the temp
    # miles to 0, sets the needed miles to the index 0(which is the hub) from the current location, and sets the
    # next location to the hub.
    # The time and space complexity are each O(1).
    def returnToHub(self, distanceDictionary):
        distanceList = distanceDictionary.get(self.currentLocation)
        self.setCurrentLocation(self.nextLocation)
        self.setNeededMiles(float(distanceList[0]))
        self.setTempMiles(0)
        self.setNextLocation("4001 South 700 East")

    # Iterate through the load to check which packages are not delivered then add them to a new list.
    # Time and space complexity are each 0(n).
    def getUndeliveredLoad(self):
        undeliveredPackagesList = []
        for i in self.load:
            if i.getDeliveryStatus() == "En route":
                undeliveredPackagesList.append(i)
        return undeliveredPackagesList

    # All accessors and mutators are space and time complexity of 0(1).
    def getRouteComplete(self):
        return self.routeComplete

    def loadTruck(self, load):
        self.load = load

    def setTempMiles(self, mileage):
        self.tempMileage = mileage

    def setNeededMiles(self, mileage):
        self.neededMileage = mileage

    def setTotalMiles(self, mileage):
        self.totalMileage = mileage

    def setCurrentLocation(self, currentLoc):
        self.currentLocation = currentLoc

    def setNextLocation(self, nextLoc):
        self.nextLocation = nextLoc

    def setRouteComplete(self, boolean):
        self.routeComplete = boolean
