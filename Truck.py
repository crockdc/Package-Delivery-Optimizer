class Truck:
    def __init__(self, truckID, load, tempMileage, totalMileage, currentLocation,
            nextLocation, routeComplete):
        self.truckID = int(truckID)
        self.load = load
        self.tempMileage = tempMileage
        self.totalMileage = totalMileage
        self.currentLocation = currentLocation
        self.nextLocation = nextLocation
        self.routeComplete = routeComplete

    def loadTruck(self, load):
        self.load = load

    def setTempMiles(self, mileage):
        self.tempMileage = mileage

    def setTotalMiles(self, mileage):
        self.totalMileage = mileage

    def setCurrentLocation(self, currentLoc):
        self.currentLocation = currentLoc

    def setNextLocation(self, nextLoc):
        self.nextLocation = nextLoc

    def setRouteComplete(self, boolean):
        self.routeComplete = boolean

    def __str__(self):
        return str(self.truckID) + " " + str(self.load[0]) + str(self.tempMileage) + str(self.totalMileage) + self.currentLocation + \
            str(self.nextLocation) + str(self.routeComplete)