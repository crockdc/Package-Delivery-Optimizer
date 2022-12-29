# Daniel Crocker - Student ID: 010301135
# C950 - Data Structures and Algorithms II

from HashTable import *
from Truck import *

import datetime
import csv

# Today's date initialized.
currentDate = datetime.date.today()
# 1 = run entire route, 2 = pick a time and see all packages at given time
# 3 = pick a time and a package
# Variable initialized for keyboard selections in within the console interface.
userMenuChoices = 0
# Variable for which package the user wants to retrieve information on.
userPackageChoice = 0
# Variable initialized for the time that a user enters.
userTimeInput = datetime.datetime(2000, 1, 1)
# Variable for status check time stamp for second and third menu options.
userStatusCheckTime = datetime.datetime(2000, 1, 1)
# =====================================================================================================================
print("")
print("Welcome to the WGU UPS Package Delivery interface".center(100))
print("How would you like to proceed? Choose a number, then press ENTER:\n".center(100))
print("Option 1) Run through the entire delivery route and see all the packages at the end of the day.\n")
print("Option 2) To input a time and receive the status of all packages at the selected time.\n")
print("Option 3) To input a time followed by a package number to receive information about a specific package at the"
      " specified time.\n")
print("Option 4) EXIT the program.")
while userMenuChoices < 1 or userMenuChoices > 4:
    try:
        userMenuChoices = int(input())
        if userMenuChoices > 4 or userMenuChoices < 1:
            raise ValueError
    except (Exception,):
        print("Please enter a value between 1 and 4 then press ENTER:")
        pass
if userMenuChoices == 1:
    userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 17)
elif userMenuChoices == 2:
    print("What time would you like to specify? Enter time in format HH:MM then press ENTER:")
    userTimeInput = datetime.datetime(2000, 1, 1)
    while userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
        try:
            userTimeString = input()
            hr, minute = [int(i) for i in userTimeString.split(":")]
            userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, hr, minute)
            userStatusCheckTime = userTimeInput
            if userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
                raise ValueError
        except (Exception,):
            print("Please enter a time after 08:00am in the proper format HH:MM then press ENTER:")
elif userMenuChoices == 3:
    print("What time would you like to specify? Enter time in format HH:MM then press ENTER:")
    userTimeInput = datetime.datetime(2000, 1, 1)
    while userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
        try:
            userTimeString = input()
            hr, minute = [int(i) for i in userTimeString.split(":")]
            userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, hr, minute)
            userStatusCheckTime = userTimeInput
            if userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
                raise ValueError
        except (Exception,):
            print("Please enter a time after 08:00am in the proper format HH:MM then press ENTER:")
    userPackageChoice = 0
    print("Please enter a package ID number then press ENTER:")
    while userPackageChoice < 1 or userPackageChoice > 40:
        try:
            userPackageChoice = int(input())
            if userPackageChoice < 1 or userPackageChoice > 40:
                raise ValueError
        except (Exception,):
            print("Please enter a value between 1 and 40 then press ENTER:")
            pass
elif userMenuChoices == 4:
    quit()
while userMenuChoices == 1 or userMenuChoices == 2 or userMenuChoices == 3:
    # Counters initialized for loading the trucks once their conditions are met.
    truck1LoadCounter, truck2LoadCounter, truck3LoadCounter = 0, 0, 0
    # Counter initialized for package #9 address change notification at 10:20am.
    addressChangeCounter = 0
    # Packages delivered counters initialized.
    packagesDelivered1, packagesDelivered2, packagesDelivered3 = 0, 0, 0
    # 3 empty lists to load the packages into for each of the trucks.
    truckLoad1, truckLoad2, truckLoad3 = [], [], []
    # Create an empty dictionary for the distances between addresses.
    distanceDictionary = {}
    # # Create an empty dictionary to reference each address to a numerical value.
    addressDictionary = {}
    # # Initialize number of addresses.
    totalAddresses = 0
    # Initialize initial mileage to 0.
    totalMileage = 0
    # Initialize today's date and the start time of 08:00 hours.
    currentTime = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 8)
    # Instantiate a chaining hash table of 41 buckets.
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

    # Utilize CSV reader and iterate through each row of the packages file.
    with open('PackageFile.csv', encoding='utf-8-sig') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Using for loop, instantiate a new package object for each row.
        for row in readCSV:
            csvPackageID = row[0]
            csvPackageAddress = row[1]
            csvPackageCity = row[2]
            csvPackageZip = row[4]
            csvPackageDeadline = row[5]
            csvPackageWeight = row[6]
            package = Package(csvPackageID, csvPackageAddress, csvPackageDeadline, csvPackageCity,
                              csvPackageZip, csvPackageWeight, "At the hub")
            table.insert(package.packageID, package)

    # Load each truck manually using a list of package objects for each truck.
    truckLoad1.extend([table.getVal(1), table.getVal(4), table.getVal(13), table.getVal(14), table.getVal(15),
                       table.getVal(16), table.getVal(19), table.getVal(20), table.getVal(21), table.getVal(29),
                       table.getVal(30), table.getVal(34), table.getVal(37), table.getVal(39), table.getVal(40)])

    truckLoad2.extend([table.getVal(2), table.getVal(3), table.getVal(5), table.getVal(7), table.getVal(8), table.getVal(9),
                       table.getVal(10), table.getVal(11), table.getVal(12), table.getVal(18), table.getVal(23),
                       table.getVal(24), table.getVal(33), table.getVal(36), table.getVal(38)])

    truckLoad3.extend([table.getVal(6), table.getVal(17), table.getVal(22), table.getVal(25),
                       table.getVal(26), table.getVal(27), table.getVal(28), table.getVal(31), table.getVal(32),
                       table.getVal(35)])

    # Instantiate each truck and add to a list to be used to find the status of a package later.
    trucksList = []
    truck1 = Truck(1, truckLoad1, 0, 0, 0, "4001 South 700 East", None, False)
    truck2 = Truck(2, truckLoad2, 0, 0, 0, "4001 South 700 East", None, False)
    truck3 = Truck(3, truckLoad3, 0, 0, 0, "4001 South 700 East", None, False)
    trucksList.extend([truck1, truck2, truck3])

    # move this down into the algorithm once the exact time is figured out for pack#

    # Set the first address for the route using the nearest neighbor algorithm.
    truck1.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
    truck2.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
    truck3.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)

    # While the truck route is incomplete, continue to iterate through time.
    # Iterate through time via seconds. Distance traveled is approximately 0.005 miles per second(Based on 18mph).
    # while not truck1.routeComplete and not truck2.routeComplete:  # and not truck3.routeComplete
    while currentTime < userTimeInput:
        if truck1LoadCounter == 0:
            truck1LoadCounter = 1
            # Set status as En route after loading onto truck1 at start of the day 08:00am.
            for i in truckLoad1:
                i.setDeliveryStatus("En route")
                i.setDeliveryTime(currentTime)
        # Iterate by seconds using timedelta.
        currentTime += timedelta(0, 1)
        # Check to see if current time is 10:20 to change package address of package #9.
        if addressChangeCounter == 0 and \
                currentTime > datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 10, 19):
            addressChangeCounter = 1
            package9 = table.getVal(9)
            package9.setDeliveryAddress("410 S State St")
            package9.setZipCode("84111")
        # =================================================================================================================
        # Truck 1 begins at 08:00 hours
        # =================================================================================================================
        truck1RouteComplete = truck1.getRouteComplete()
        if not truck1RouteComplete:
            truck1.setTempMiles(truck1.tempMileage + 0.005)
            truck1.setTotalMiles(truck1.totalMileage + 0.005)
        if truck1.nextLocation == "4001 South 700 East" and truck1.neededMileage <= truck1.tempMileage and \
                not truck1RouteComplete:
            truck1.setRouteComplete(True)
            truck1.setCurrentLocation("4001 South 700 East")
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

        # =================================================================================================================
        # Truck 2 begins at 10:20 at the earliest, but must wait for Truck1 to return due to needing a driver.
        # =================================================================================================================
        if currentTime > datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 10, 20) and \
                truck1.routeComplete:
            if truck2LoadCounter == 0:
                truck2LoadCounter = 1
                # Truck is now en route, change all loaded packages to "En route" status.
                for i in truckLoad2:
                    i.setDeliveryStatus("En route")
                    i.setDeliveryTime(currentTime)
            truck2RouteComplete = truck2.getRouteComplete()
            if not truck2RouteComplete:
                truck2.setTempMiles(truck2.tempMileage + 0.005)
                truck2.setTotalMiles(truck2.totalMileage + 0.005)
            if truck2.nextLocation == "4001 South 700 East" and truck2.neededMileage <= truck2.tempMileage and \
                    not truck2RouteComplete:
                truck2.setRouteComplete(True)
                truck2.setCurrentLocation("4001 South 700 East")
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

        # =================================================================================================================
        # Truck 3 begins at 9:05am.
        # =================================================================================================================
        if currentTime > datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 9, 5):
            truck3RouteComplete = truck3.getRouteComplete()
            if truck3LoadCounter == 0:
                truck3LoadCounter = 1
                # Truck is now en route, change all loaded packages to "En route" status.
                for i in truckLoad3:
                    i.setDeliveryStatus("En route")
                    i.setDeliveryTime(currentTime)
            if not truck3RouteComplete:
                truck3.setTempMiles(truck3.tempMileage + 0.005)
                truck3.setTotalMiles(truck3.totalMileage + 0.005)
            if truck3.nextLocation == "4001 South 700 East" and truck3.neededMileage <= truck3.tempMileage and \
                    not truck3RouteComplete:
                truck3.setRouteComplete(True)
                truck3.setCurrentLocation("4001 South 700 East")
            elif truck3.neededMileage <= truck3.tempMileage:
                packagesDelivered3 += 1
                for m in truck3.getUndeliveredLoad():
                    if truck3.nextLocation == m.getDeliveryAddress():
                        m.setDeliveryStatus("Delivered")
                        m.setDeliveryTime(currentTime)
                if len(truck3.load) == packagesDelivered3:
                    truck3.returnToHub(distanceDictionary, addressDictionary)
                else:
                    truck3.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
        # End the day if all 3 trucks' routes are complete. This will change the while loop variable and timestamp it.
        if truck1RouteComplete and truck2.getRouteComplete() and truck3.getRouteComplete():
            userTimeInput = currentTime
    if userMenuChoices == 1:
        # Display all packages either at the end of day.
        print("Truck 1 delivered the following packages:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Delivery Information")
        for i in truck1.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status + " to " + i.delivery_address + ", " + i.delivery_city + " " +
                  i.delivery_zip + " at " + str(i.delivery_time))

        print("\nTruck 2 delivered the following packages:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Delivery Information")
        for i in truck2.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status + " to " + i.delivery_address + ", " + i.delivery_city + " " +
                  i.delivery_zip + " at " + str(i.delivery_time))

        print("\nTruck 3 delivered the following packages:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Delivery Information")
        for i in truck3.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status + " to " + i.delivery_address + ", " + i.delivery_city + " " +
                  i.delivery_zip + " at " + str(i.delivery_time))
        print("\nAll packages delivered on time and all trucks returned to the hub at: " + str(currentTime) + ".\n")
        # Display the total mileage traveled by all the trucks.
        totalMileage = truck1.totalMileage + truck2.totalMileage + truck3.totalMileage
        print("Truck 1 mileage: " + str("{0:.3f}".format(truck1.totalMileage)))
        print("Truck 2 mileage: " + str("{0:.3f}".format(truck2.totalMileage)))
        print("Truck 3 mileage: " + str("{0:.3f}".format(truck3.totalMileage)))
        print("\nTotal mileage traveled by all trucks after returning to the hub: " + str("{0:.3f}".format(totalMileage)))
    elif userMenuChoices == 2:
        # Display all packages either at the specified time.
        print("Truck 1 load status:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Status".ljust(11) +
              "Status Timestamp".ljust(20) + "Delivery Address")
        for i in truck1.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status.ljust(11) + str(i.delivery_time).ljust(20) + i.delivery_address +
                  ", " + i.delivery_city + " " + i.delivery_zip)

        print("\nTruck 2 load status:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Status".ljust(11) +
              "Status Timestamp".ljust(20) + "Delivery Address")
        for i in truck2.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status.ljust(11) + str(i.delivery_time).ljust(20) + i.delivery_address +
                  ", " + i.delivery_city + " " + i.delivery_zip)

        print("\nTruck 3 load status:\n")
        print("ID".ljust(3) + "Kg".ljust(3) + "Deadline".ljust(9) + "Status".ljust(11) +
              "Status Timestamp".ljust(20) + "Delivery Address")
        for i in truck3.load:
            print(str(i.packageID).ljust(3) + i.weight.ljust(3) + i.delivery_deadline.ljust(9) +
                  i.delivery_status.ljust(11) + str(i.delivery_time).ljust(20) + i.delivery_address +
                  ", " + i.delivery_city + " " + i.delivery_zip)
        print("\nTime of this status check: " + str(userStatusCheckTime) + ".\n")
        if currentTime < userStatusCheckTime:
            print("All packages delivered on time and all trucks returned to the hub at: " + str(currentTime) + ".")
        else:
            # Truck 1 status.
            atHubCounter = 0
            enRouteCounter = 0
            for i in truck1.load:
                if i.delivery_status == "At the hub":
                    atHubCounter += 1
                elif i.delivery_status == "En route":
                    enRouteCounter += 1
            if atHubCounter > 0:
                print("Truck 1 is at the hub awaiting dispatch.")
            elif enRouteCounter > 0:
                print("Truck 1 is currently at " + truck1.currentLocation + " and is en route to " +
                      truck1.nextLocation + ".")
            else:
                print("Truck 1 has completed the route.")
            # Truck 2 status.
            atHubCounter = 0
            enRouteCounter = 0
            for i in truck2.load:
                if i.delivery_status == "At the hub":
                    atHubCounter += 1
                elif i.delivery_status == "En route":
                    enRouteCounter += 1
            if atHubCounter > 0:
                print("Truck 2 is at the hub awaiting dispatch.")
            elif enRouteCounter > 0:
                print("Truck 2 is currently at " + truck2.currentLocation + " and is en route to " +
                      truck2.nextLocation + ".")
            else:
                print("Truck 2 has completed the route.")
            # Truck 3 status.
            atHubCounter = 0
            enRouteCounter = 0
            for i in truck3.load:
                if i.delivery_status == "At the hub":
                    atHubCounter += 1
                elif i.delivery_status == "En route":
                    enRouteCounter += 1
            if atHubCounter > 0:
                print("Truck 3 is at the hub awaiting dispatch.")
            elif enRouteCounter > 0:
                print("Truck 3 is currently at " + truck3.currentLocation + " and is en route to " +
                      truck3.nextLocation + ".")
            else:
                print("Truck 3 has completed the route.")

        # Display the total mileage traveled by all the trucks.
        totalMileage = truck1.totalMileage + truck2.totalMileage + truck3.totalMileage
        print("\nTruck 1 mileage: " + str("{0:.3f}".format(truck1.totalMileage)))
        print("Truck 2 mileage: " + str("{0:.3f}".format(truck2.totalMileage)))
        print("Truck 3 mileage: " + str("{0:.3f}".format(truck3.totalMileage)))
        print("\nTotal mileage traveled by all trucks at specified time: " + str("{0:.3f}".format(totalMileage)))
    elif userMenuChoices == 3:
        package = table.getVal(userPackageChoice)
        print("\nTime of this status check: " + str(userStatusCheckTime))
        if currentTime < userStatusCheckTime:
            print("All packages delivered on time and all trucks returned to the hub at: " + str(currentTime))
        for i in trucksList:
            for j in i.load:
                if j.packageID == int(userPackageChoice):
                    if j.getDeliveryStatus() == "Delivered":
                        print("\nPackage #" + str(userPackageChoice) + " weighs " + j.weight +
                              "kg and was delivered to " + j.delivery_address + ", " +
                              j.delivery_city + " " + j.delivery_zip + " by Truck #" + str(i.truckID) +
                              " at " + str(j.delivery_time) + ".")
                        print("\nThe deadline of this package is " + j.delivery_deadline + ".\n")
                    elif j.getDeliveryStatus() == "En route":
                        print("\nPackage #" + str(userPackageChoice) + " weighs " + j.weight +
                              "kg, is currently at " + str(i.currentLocation) + " on Truck #" + str(i.truckID) +
                              " and is en route to " + str(i.nextLocation) + ".")
                        print("\nThe final destination for this package is " + j.delivery_address + ", " +
                              j.delivery_city + " " + j.delivery_zip + " with a deadline of " +
                              j.delivery_deadline + ".")
                        print("The package was placed en route at " + str(j.delivery_time) + ".\n")
                    elif j.getDeliveryStatus() == "At the hub":
                        print("\nPackage #" + str(userPackageChoice) + " weighs " + j.weight +
                              "kg and is at the hub on Truck #" + str(i.truckID) + ".")
                        print("\nThe final destination for this package is " + j.delivery_address + ", " +
                              j.delivery_city + " " + j.delivery_zip + " with a deadline of " +
                              j.delivery_deadline + ".\n")

    print("\nHow would you like to proceed? Choose a number, then press ENTER:\n".center(100))
    print("Option 1) Run through the entire delivery route and see all the packages at the end of the day.\n")
    print("Option 2) To input a time and receive the status of all packages at the selected time.\n")
    print("Option 3) To input a time followed by a package to receive information about a specific package at the"
          " specified time.\n")
    print("Option 4) EXIT the program.\n")
    userMenuChoices = 0
    while userMenuChoices < 1 or userMenuChoices > 4:
        try:
            userMenuChoices = int(input())
            if userMenuChoices > 4 or userMenuChoices < 1:
                raise ValueError
        except (Exception,):
            print("Please enter a value between 1 and 4 then press ENTER")
            pass
    if userMenuChoices == 1:
        userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 17)
    elif userMenuChoices == 2:
        print("What time would you like to specify? Enter time in format HH:MM then press ENTER:")
        userTimeInput = datetime.datetime(2000, 1, 1)
        while userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
            try:
                userTimeString = input()
                hr, minute = [int(i) for i in userTimeString.split(":")]
                userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, hr, minute)
                userStatusCheckTime = userTimeInput
                if userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
                    raise ValueError
            except (Exception,):
                print("Please enter a time after 08:00am in the proper format HH:MM then press ENTER:")
    elif userMenuChoices == 3:
        print("What time would you like to specify? Enter time in format HH:MM then press ENTER:")
        userTimeInput = datetime.datetime(2000, 1, 1)
        while userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
            try:
                userTimeString = input()
                hr, minute = [int(i) for i in userTimeString.split(":")]
                userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, hr, minute)
                userStatusCheckTime = userTimeInput
                if userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
                    raise ValueError
            except (Exception,):
                print("Please enter a time after 08:00am in the proper format HH:MM then press ENTER:")
        userPackageChoice = 0
        print("Please enter a package ID number then press ENTER:")
        while userPackageChoice < 1 or userPackageChoice > 40:
            try:
                userPackageChoice = int(input())
                if userPackageChoice < 1 or userPackageChoice > 40:
                    raise ValueError
            except (Exception,):
                print("Please enter a value between 1 and 40 then press ENTER:")
                pass
    elif userMenuChoices == 4:
        quit()



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


# print(totalMileage)
