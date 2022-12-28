from Package import *


class Truck:
    def __init__(self, truckID, load, tempMileage, neededMileage, totalMileage, currentLocation, nextLocation,
                 routeComplete):
        self.truckID = int(truckID)
        self.load = load
        self.tempMileage = tempMileage
        self.neededMileage = neededMileage
        self.totalMileage = totalMileage
        self.currentLocation = currentLocation
        self.nextLocation = nextLocation
        self.routeComplete = routeComplete

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

    def nearestNeighborSearch(self, totalAddresses, distanceDictionary, addressDictionary):
        nextAddressDistance = 20
        nextAddressIndex = 0
        # previousLocation = self.currentLocation
        routeComplete = True
        undeliveredLoad = self.getUndeliveredLoad()
        if self.nextLocation is not None:
            self.setCurrentLocation(self.nextLocation)
        for i in range(totalAddresses):
            distancesList = distanceDictionary.get(self.currentLocation)
            if float(distancesList[i]) < nextAddressDistance:
                for j in undeliveredLoad:
                    if j.getDeliveryAddress() == addressDictionary.get(i):
                        nextAddressDistance = float(distancesList[i])
                        nextAddressIndex = i
                        routeComplete = False
        if not routeComplete:
            self.setNextLocation(addressDictionary.get(nextAddressIndex))
            self.setTempMiles(0)
            self.setNeededMiles(nextAddressDistance)

    def returnToHub(self, distanceDictionary, addressDictionary):
        distanceList = distanceDictionary.get(self.currentLocation)
        self.setCurrentLocation(self.nextLocation)
        self.setNeededMiles(float(distanceList[0]))
        self.setTempMiles(0)
        self.setNextLocation("4001 South 700 East")

    def loadContains(self, address):
        for i in self.load:
            if address == i.delivery_address:
                return True
            else:
                return False

    def getUndeliveredLoad(self):
        undeliveredPackagesList = []
        for i in self.load:
            if i.getDeliveryStatus() == "En route":
                undeliveredPackagesList.append(i)
        return undeliveredPackagesList

    def packageUndelivered(self, address):
        for i in self.load:
            if address == i.delivery_address and i.getDeliveryStatus() == "En route":
                return True

    def __str__(self):
        return str(self.truckID) + " " + str(len(self.load)) + " " + str(self.tempMileage) + str(self.totalMileage) + \
            self.currentLocation + str(self.nextLocation) + str(self.routeComplete)
