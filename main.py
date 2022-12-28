from HashTable import *
from Package import *
from Truck import *

import datetime
import csv
import time

packagesDelivered1, packagesDelivered2, packagesDelivered3 = 0, 0, 0
# 3 empty lists to load the packages into for each of the trucks
truckLoad1, truckLoad2, truckLoad3 = [], [], []
# Create an empty dictionary for the distances between addresses
distanceDictionary = {}
# # Create an empty dictionary to reference each address to a numerical value
addressDictionary = {}
# # Initialize number of addresses
totalAddresses = 0
# addressRows = 0
# Initialize a selection variable for the user interface
userSelection = 0
# Initialize initial mileage to 0
totalMileage = 0
# Initialize today's date and the start time of 08:00 hours
currentDate = datetime.date.today()
currentTime = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 8)
# Instantiate a chaining hash table of 10 buckets
table = HashTable(41)

# Utilize CSV reader and iterate through each row of the distance table file.
with open('DistanceTable.csv', encoding='utf-8-sig') as csvfile:
    # Count the number of addresses in the first row to assist with assigning numerical values to them.
    firstRow = csvfile.readline()
    totalAddresses = firstRow.count(',')
    # Reset CSV reader to first row.
    csvfile.seek(0)
    readCSV = csv.reader(csvfile, delimiter=',')
    # J will be used as a variable to add to the address dictionary which matches the list index to an address.
    j = 0
    for row in readCSV:
        # New empty list for each new row to collect the list of distances from the current address.
        addressList = []
        # Iterate through the total number of addresses, append each item to the list for that row.
        for i in range(totalAddresses):
            addressList.append(row[i + 1])
        # Add the list to the address, address being the key and the list being the value.
        distanceDictionary.update({row[0]: addressList})
        # Add the address to the dictionary which holds addresses represented as numerical values.
        addressDictionary.update({j: row[0]})
        # Iterate j by 1.
        j += 1

# print(addressDictionary)
# tempList = distanceDictionary.get('4001 South 700 East')
# print(tempList)
# print(distanceDictionary)

# Utilize CSV reader and iterate through each row of the packages file.
with open('PackageFile.csv', encoding='utf-8-sig') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    # Using for loop, instantiate a new package object for each row.
    for row in readCSV:
        # print(row[0])
        csvPackageID = row[0]
        csvPackageAddress = row[1]
        csvPackageCity = row[2]
        csvPackageZip = row[4]
        csvPackageDeadline = row[5]
        csvPackageWeight = row[6]
        package = Package(csvPackageID, csvPackageAddress, csvPackageDeadline, csvPackageCity,
                          csvPackageZip, csvPackageWeight, "At the hub")
        # print(package.packageID)
        table.insert(package.packageID, package)

# Load each truck manually using a list for each truck.
truckLoad1.extend([table.getVal(1), table.getVal(4), table.getVal(13), table.getVal(14), table.getVal(15),
                   table.getVal(16), table.getVal(19), table.getVal(20), table.getVal(21), table.getVal(34),
                   table.getVal(39), table.getVal(40)])

truckLoad2.extend([table.getVal(2), table.getVal(6), table.getVal(17), table.getVal(22), table.getVal(25),
                   table.getVal(26), table.getVal(27), table.getVal(28), table.getVal(31), table.getVal(32),
                   table.getVal(33), table.getVal(35)])

# Instantiate Each truck
truck1 = Truck(1, truckLoad1, 0, 0, 0, "4001 South 700 East", None, False)
truck2 = Truck(2, truckLoad2, 0, 0, 0, "4001 South 700 East", None, False)
truck3 = Truck(3, truckLoad3, 0, 0, 0, "4001 South 700 East", None, False)

# Set status as En route after loading onto truck1.
for i in truckLoad1:
    i.setDeliveryStatus("En route")

for i in truckLoad2:
    i.setDeliveryStatus("En route")

# move this down into the algorithm once the exact time is figured out for pack#

# Set the first address for the route using the nearest neighbor algorithm.
truck1.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
truck2.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
truck3.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)

# While the truck route is incomplete, continue to iterate through time.
# Iterate through time via seconds. Distance traveled is approximately 0.005 miles per second(Based on 18mph).
while not truck1.routeComplete and not truck2.routeComplete:  # and not truck3.routeComplete
    # Iterate by seconds using timedelta.
    currentTime += timedelta(0, 1)
    truck1RouteComplete = truck1.getRouteComplete()
    if not truck1RouteComplete:
        truck1.setTempMiles(truck1.tempMileage + 0.005)
        truck1.setTotalMiles(truck1.totalMileage + 0.005)
    # ============================================================================================
    # Truck 1 begins at 08:00 hours
    # ============================================================================================
    if truck1.nextLocation == "4001 South 700 East" and truck1.neededMileage <= truck1.tempMileage and \
            not truck1RouteComplete:
        truck1.setRouteComplete(True)
        print(truck1.currentLocation)
        truck1.setCurrentLocation("4001 South 700 East")
        print(currentTime)
        print(truck1.totalMileage)
        print(truck1.nextLocation)
        package = table.getVal(15)
        print(package)
        totalMileage += truck1.totalMileage
    elif truck1.neededMileage <= truck1.tempMileage:
        packagesDelivered1 += 1
        for i in truck1.getUndeliveredLoad():
            if truck1.nextLocation == i.getDeliveryAddress():
                i.setDeliveryStatus("Delivered")
                i.setDeliveryTime(currentTime)
        if len(truck1.load) == packagesDelivered1:
            truck1.returnToHub(distanceDictionary, addressDictionary)
        else:
            truck1.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
    # ============================================================================================
    # Truck 2 begins at
    # ============================================================================================
    truck2RouteComplete = truck2.getRouteComplete()
    if not truck2RouteComplete:
        truck2.setTempMiles(truck2.tempMileage + 0.005)
        truck2.setTotalMiles(truck2.totalMileage + 0.005)
    if truck2.nextLocation == "4001 South 700 East" and truck2.neededMileage <= truck2.tempMileage and \
            not truck2RouteComplete:
        truck2.setRouteComplete(True)
        print(truck2.currentLocation)
        truck2.setCurrentLocation("4001 South 700 East")
        print(currentTime)
        print(truck2.totalMileage)
        print(truck2.nextLocation)
        # package = table.getVal(15)
        # print(package)
        totalMileage += truck2.totalMileage
    elif truck2.neededMileage <= truck2.tempMileage:
        packagesDelivered2 += 1
        for k in truck2.getUndeliveredLoad():
            if truck2.nextLocation == k.getDeliveryAddress():
                k.setDeliveryStatus("Delivered")
                k.setDeliveryTime(currentTime)
        if len(truck2.load) == packagesDelivered2:
            truck2.returnToHub(distanceDictionary, addressDictionary)
        else:
            truck2.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)


print(table.returnValues())

# print("Welcome to the WGU UPS Package Delivery interface.\n"
#       "How would you like to proceed?\n\n"
#       "Enter 1 to run the program from start to finish. You will receive information "
#       "on each of the 40 packages and the total mileage to complete the deliveries for the day.\n\n"
#       "Enter 2 to enter a specific time and receive all package and mileage information at the"
#       " time that you specify\n\nEnter 3 to enter a specific package number followed by a specific"
#       "time to receive information about your specified package at the specified time.")
# userSelection = int(input("\nENTER A NUMBER:"))
# if userSelection == 1:
#     print("you typed 1")

# package1 = Package(1, "555 maple", "10:30", "Manassas", 32119, 22.1, "loaded")
# package2 = Package(2, "543 maple", "10:00", "Port", 32128, 22.1, "loaded")
#
# newCurrentTime = startTime + datetime.timedelta(0, 5)
# package1.setDeliveryTime(datetime.datetime.time(newCurrentTime))

# table.insert(package1.packageID, package1)
# table.insert(1, package2)

# print(table)
# print(table.getVal(1))
# package = table.getVal(1)
# print(package.delivery_address)
# print(table.returnValues())

# if __name__ == '__main__':

# deliveryDate = datetime.date.today()
# deliveryTime = datetime.datetime(deliveryDate.year,deliveryDate.month,deliveryDate.day,21,24, 30)
# nowTime = datetime.datetime.now()
# print(str(nowTime))
# print(deliveryTime)
# while nowTime < deliveryTime:
#     print("not delivered, please wait")
#     nowTime = datetime.datetime.now()
#     time.sleep(2)
# print("delivered, it is now correct time")
