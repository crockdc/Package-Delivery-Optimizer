# NAME/ID: Daniel Crocker 010301135
# COURSE: C950 - Data Structures and Algorithms II
# PROGRAM: NHP2 TASK 1 - WGUPS ROUTING PROGRAM
# OVERVIEW: A package file with 40 packages is provided as well as a distance table of 27 addresses. The parameters are
#   that there are 3 trucks and 2 drivers. Loading and delivering times are averaged into an overall speed of 18mph.
#   Trucks can't leave before 08:00 hours. Certain packages have requirements that must be met. Packages must be able
#   to be inserted and looked up via a manually created hash table. An algorith to deliver the packages must be
#   implemented with a time and space big O complexity of no worse than O(n^2) leading to a delivery mileage of less
#   than 140 total miles between the three trucks. This program uses the nearest neighbor algorithm for deliveries.
# Big O: The omega time complexity for the totality of the program is O(n^2), the space complexity is the same O(n^2).
# =====================================================================================================================
from HashTable import *
from Truck import *

import datetime
import csv

# Today's date initialized.
currentDate = datetime.date.today()
# Variable initialized for keyboard selections in within the console interface.
userMenuChoices = 0
# Variable for which package the user wants to retrieve information on.
userPackageChoice = 0
# Variable initialized for the time that a user enters.
userTimeInput = datetime.datetime(2000, 1, 1)
# Variable for status check time stamp for second and third menu options.
userStatusCheckTime = datetime.datetime(2000, 1, 1)
# =====================================================================================================================
# Console interface for user to choose from 4 options.
print("")
print("Welcome to the WGUPS Package Delivery interface".center(100))
print("How would you like to proceed? Choose a number, then press ENTER:\n".center(100))
print("Option 1) Run through the entire delivery route and see all the packages at the end of the day.\n")
print("Option 2) To input a time and receive the status of all packages at the selected time.\n")
print("Option 3) To input a time followed by a package number to receive information about a specific package at the"
      " specified time.\n")
print("Option 4) EXIT the program.")
# Force user to input proper numerical using while loop with nested error handler.
while userMenuChoices < 1 or userMenuChoices > 4:
    try:
        userMenuChoices = int(input())
        if userMenuChoices > 4 or userMenuChoices < 1:
            raise ValueError
    except (Exception,):
        print("Please enter a value between 1 and 4 then press ENTER:")
        pass
# If the user chooses 1 the user time input is set to the end of business day i.e. 17:00 hours.
if userMenuChoices == 1:
    userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 17)
# Else if user enters 2 then another nested try except handler is added to force proper input of time.
# The user time input is set to the user's specification.
elif userMenuChoices == 2:
    print("What time would you like to specify? Enter time in format HH:MM then press ENTER:")
    userTimeInput = datetime.datetime(2000, 1, 1)
    while userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
        try:
            userTimeString = input()
            # The input is split by the ":" into hour and minute then a datetime is assigned to the user time input.
            hr, minute = [int(i) for i in userTimeString.split(":")]
            userTimeInput = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, hr, minute)
            userStatusCheckTime = userTimeInput
            # If the time is before business hours then an error is thrown until a proper time is entered.
            if userTimeInput < datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 7, 59, 59):
                raise ValueError
        except (Exception,):
            print("Please enter a time after 08:00am in the proper format HH:MM then press ENTER:")
# Else if user enters 3 then another 2 nested exception handlers are added to force proper input of time and package #.
# The user time input is set to the user's specification.
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
# Exit the program with selection 4.
elif userMenuChoices == 4:
    quit()

# =====================================================================================================================
# This while loop gets repeated until the user decides to press 4 and exit the program.
# The time complexity until the end of the program is O(n^2), the space complexity is O(n^2).
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
    # Initialize initial mileage to 0.
    totalMileage = 0
    # Initialize today's date and the start time of 08:00 hours.
    currentTime = datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 8)
    # Instantiate a chaining hash table of 41 buckets.
    table = HashTable(41)

    # Utilize CSV reader and iterate through each row of the distance table file.
    # The time complexity is O(n^2) and space complexity is O(n^2).
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
    # The time complexity is O(n) and space complexity is O(1)
    with open('PackageFile.csv', encoding='utf-8-sig') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Using for loop, instantiate a new package object for each row.
        for row in readCSV:
            csvPackageID = row[0]
            csvPackageAddress = row[1]
            csvPackageCity = row[2]
            # State is skipped due to not being required, but would be useful if crossing state lines in the future.
            csvPackageZip = row[4]
            csvPackageDeadline = row[5]
            csvPackageWeight = row[6]
            # Constructor uses delivery status as at the hub for all packages initially.
            package = Package(csvPackageID, csvPackageAddress, csvPackageDeadline, csvPackageCity,
                              csvPackageZip, csvPackageWeight, "At the hub")
            # Insert into the hash table using the package ID as the key and the package object as the value.
            table.insert(package.packageID, package)

    # Load each truck manually using a list of package objects for each truck.
    # Time complexity for creating the loads is O(n) n being the number of packages. The space complexity is the same.
    truckLoad1.extend([table.lookup(1), table.lookup(4), table.lookup(13), table.lookup(14), table.lookup(15),
                       table.lookup(16), table.lookup(19), table.lookup(20), table.lookup(21), table.lookup(29),
                       table.lookup(30), table.lookup(34), table.lookup(37), table.lookup(39), table.lookup(40)])

    truckLoad2.extend([table.lookup(2), table.lookup(3), table.lookup(5), table.lookup(7), table.lookup(8),
                       table.lookup(9), table.lookup(10), table.lookup(11), table.lookup(12), table.lookup(18),
                       table.lookup(23), table.lookup(24), table.lookup(33), table.lookup(36), table.lookup(38)])

    truckLoad3.extend([table.lookup(6), table.lookup(17), table.lookup(22), table.lookup(25),
                       table.lookup(26), table.lookup(27), table.lookup(28), table.lookup(31), table.lookup(32),
                       table.lookup(35)])

    # Instantiate each truck and add to a list to be used to find the status of a package later.
    trucksList = []
    truck1 = Truck(1, truckLoad1, 0, 0, 0, "4001 South 700 East", None, False)
    truck2 = Truck(2, truckLoad2, 0, 0, 0, "4001 South 700 East", None, False)
    truck3 = Truck(3, truckLoad3, 0, 0, 0, "4001 South 700 East", None, False)
    trucksList.extend([truck1, truck2, truck3])

    # Set the first address for the route using the nearest neighbor algorithm.
    # Each of these is time complexity O(n^2) and space complexity of O(1).
    truck1.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
    truck2.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
    truck3.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)

    # =================================================================================================================
    # While the truck route is incomplete, continue to iterate through time.
    # Iterate through time via seconds. Distance traveled is approximately 0.005 miles per second(Based on 18mph).
    # At the end of this loop, if all three trucks routes are complete then the userTimeInput will equal the
    # currentTime causing the loop to break.
    # Space and time complexity for the totality of the rest of the program is O(n^2) for both time and space.
    while currentTime < userTimeInput:
        # This just loads the truck one time by iterating through all packages in the load.
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
            package9 = table.lookup(9)
            package9.setDeliveryAddress("410 S State St")
            package9.setZipCode("84111")
        # =============================================================================================================
        # Truck 1 begins at 08:00 hours.
        # Check truck route completion status, if it's not back at the hub then move it forward the corresponding
        # distance. Since we are using minutes then the value is 0.005 based off of the stated 18mph.
        # Time complexity for each of the trucks is O(n^2) and space complexity of the same.
        truck1RouteComplete = truck1.getRouteComplete()
        if not truck1RouteComplete:
            truck1.setTempMiles(truck1.tempMileage + 0.005)
            truck1.setTotalMiles(truck1.totalMileage + 0.005)
        # This sets the route complete once the conditions are met(being back at the hub based on mileage needed).
        if truck1.nextLocation == "4001 South 700 East" and truck1.neededMileage <= truck1.tempMileage and \
                not truck1RouteComplete:
            truck1.setRouteComplete(True)
            # Set the truck currently at the hub due to route being complete.
            truck1.setCurrentLocation("4001 South 700 East")
        # Otherwise, the truck is still en route to it's next location. Once the needed mileage is less than the
        # currently tracked temp mileage, a package is added to the counter and the status is changed to delivered.
        elif truck1.neededMileage <= truck1.tempMileage:
            packagesDelivered1 += 1
            for i in truck1.getUndeliveredLoad():
                if truck1.nextLocation == i.getDeliveryAddress():
                    i.setDeliveryStatus("Delivered")
                    i.setDeliveryTime(currentTime)
            # If the packages delivered equals the load size then the truck must return to hub.
            if len(truck1.load) == packagesDelivered1:
                truck1.returnToHub(distanceDictionary)
            # Otherwise, perform nearest neighbor algorithm function to obtain next address, adjust current address,
            # and update mileages on the truck object.
            else:
                truck1.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)

        # =============================================================================================================
        # Truck 2 must wait for Truck 1 to return due to needing a driver, leaves at 10:20 at the earliest.
        if currentTime > datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 10, 20) and \
                truck1.routeComplete:
            # This just loads the truck one time by iterating through all packages in the load.
            if truck2LoadCounter == 0:
                truck2LoadCounter = 1
                # Truck is now en route, change all loaded packages to "En route" status.
                for i in truckLoad2:
                    i.setDeliveryStatus("En route")
                    i.setDeliveryTime(currentTime)
            # Check truck route completion status, if it's not back at the hub then move it forward the corresponding
            # distance. Since we are using minutes then the value is 0.005 based off of the stated 18mph.
            truck2RouteComplete = truck2.getRouteComplete()
            if not truck2RouteComplete:
                truck2.setTempMiles(truck2.tempMileage + 0.005)
                truck2.setTotalMiles(truck2.totalMileage + 0.005)
            # This sets the route complete once the conditions are met(being back at the hub based on mileage needed).
            if truck2.nextLocation == "4001 South 700 East" and truck2.neededMileage <= truck2.tempMileage and \
                    not truck2RouteComplete:
                truck2.setRouteComplete(True)
                # Set the truck currently at the hub due to route being complete.
                truck2.setCurrentLocation("4001 South 700 East")
            # Otherwise, the truck is still en route to it's next location. Once the needed mileage is less than the
            # currently tracked temp mileage, a package is added to the counter and the status is changed to delivered.
            elif truck2.neededMileage <= truck2.tempMileage:
                packagesDelivered2 += 1
                for k in truck2.getUndeliveredLoad():
                    if truck2.nextLocation == k.getDeliveryAddress():
                        k.setDeliveryStatus("Delivered")
                        k.setDeliveryTime(currentTime)
                # If the packages delivered equals the load size then the truck must return to hub.
                if len(truck2.load) == packagesDelivered2:
                    truck2.returnToHub(distanceDictionary)
                # Otherwise, perform nearest neighbor algorithm function to obtain next address, adjust current address,
                # and update mileages on the truck object.
                else:
                    truck2.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)

        # =============================================================================================================
        # Truck 3 begins at 9:05am.
        if currentTime > datetime.datetime(currentDate.year, currentDate.month, currentDate.day, 9, 5):
            # Check truck route completion status, if it's not back at the hub then move it forward the corresponding
            # distance. Since we are using minutes then the value is 0.005 based off of the stated 18mph.
            truck3RouteComplete = truck3.getRouteComplete()
            # This just loads the truck one time by iterating through all packages in the load.
            if truck3LoadCounter == 0:
                truck3LoadCounter = 1
                # Truck is now en route, change all loaded packages to "En route" status.
                for i in truckLoad3:
                    i.setDeliveryStatus("En route")
                    i.setDeliveryTime(currentTime)
            if not truck3RouteComplete:
                truck3.setTempMiles(truck3.tempMileage + 0.005)
                truck3.setTotalMiles(truck3.totalMileage + 0.005)
            # This sets the route complete once the conditions are met(being back at the hub based on mileage needed).
            if truck3.nextLocation == "4001 South 700 East" and truck3.neededMileage <= truck3.tempMileage and \
                    not truck3RouteComplete:
                truck3.setRouteComplete(True)
                # Set the truck currently at the hub due to route being complete.
                truck3.setCurrentLocation("4001 South 700 East")
            # Otherwise, the truck is still en route to it's next location. Once the needed mileage is less than the
            # currently tracked temp mileage, a package is added to the counter and the status is changed to delivered.
            elif truck3.neededMileage <= truck3.tempMileage:
                packagesDelivered3 += 1
                for m in truck3.getUndeliveredLoad():
                    if truck3.nextLocation == m.getDeliveryAddress():
                        m.setDeliveryStatus("Delivered")
                        m.setDeliveryTime(currentTime)
                # If the packages delivered equals the load size then the truck must return to hub.
                if len(truck3.load) == packagesDelivered3:
                    truck3.returnToHub(distanceDictionary)
                # Otherwise, perform nearest neighbor algorithm function to obtain next address, adjust current address,
                # and update mileages on the truck object.
                else:
                    truck3.nearestNeighborSearch(totalAddresses, distanceDictionary, addressDictionary)
        # End the day if all 3 trucks' routes are complete the userTimeInput will get set to the currentTime, then
        # used later as a timestamp of when all the packages were delivered for the print to screen.
        if truck1RouteComplete and truck2.getRouteComplete() and truck3.getRouteComplete():
            userTimeInput = currentTime

    # =================================================================================================================
    # Conditional statements for each of the menu choices will decide which information to output to the screen.
    # Choice 1 time complexity is O(n) and space of O(n).
    if userMenuChoices == 1:
        # Display all packages at the end of day.
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
        print("\nTotal mileage traveled by all trucks after returning to the hub: " +
              str("{0:.3f}".format(totalMileage)))

    # Choice 2 displays slightly different due to varying locations of the trucks depending on user time input.
    # Total time and space complexity for choice 2 is O(n) for each.
    elif userMenuChoices == 2:
        # Display all packages at the specified time.
        # Time complexity for this display is O(n) and space complexity is the same for choice 2.
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
        # The currentTime variable is timestamped once all packages are delivered, if the initial user input is greater
        # than the current time then the trucks must be complete with routes.
        if currentTime < userStatusCheckTime:
            print("All packages delivered on time and all trucks returned to the hub at: " + str(currentTime) + ".")
        else:
            # Truck 1 status.
            # Initialize counters to keep track of load status.
            # Time complexity is O(n) and space complexity is O(n) due to the input load size of n.
            atHubCounter = 0
            enRouteCounter = 0
            # Iterate through the load to track the status of the packages via the counters to determine print output.
            for i in truck1.load:
                if i.delivery_status == "At the hub":
                    atHubCounter += 1
                elif i.delivery_status == "En route":
                    enRouteCounter += 1
            # If any of the packages are at the hub then the truck is at the hub.
            if atHubCounter > 0:
                print("Truck 1 is at the hub awaiting dispatch.")
            # If any packages are en route then the truck is currently en route to a delivery.
            elif enRouteCounter > 0:
                print("Truck 1 is currently at " + truck1.currentLocation + " and is en route to " +
                      truck1.nextLocation + ".")
            # If the route is complete and the packages are delivered then print completed route.
            elif truck1.routeComplete and enRouteCounter == 0:
                print("Truck 1 has completed the route.")
            # If the route is not complete but the packages are delivered then it must be on the way back to hub.
            else:
                print("Truck 1 is en route to the hub from " + truck1.currentLocation + ".")
            # Truck 2 status.
            # Truck 2 and 3 status code is identical to truck 1.
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
            elif truck2.routeComplete and enRouteCounter == 0:
                print("Truck 2 has completed the route.")
            else:
                print("Truck 2 is en route to the hub from " + truck2.currentLocation + ".")
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
            elif truck3.routeComplete and enRouteCounter == 0:
                print("Truck 3 has completed the route.")
            else:
                print("Truck 3 is en route to the hub from " + truck3.currentLocation + ".")

        # Display the total mileage traveled by all the trucks. Add each of the individual trucks mileage together.
        totalMileage = truck1.totalMileage + truck2.totalMileage + truck3.totalMileage
        print("\nTruck 1 mileage: " + str("{0:.3f}".format(truck1.totalMileage)))
        print("Truck 2 mileage: " + str("{0:.3f}".format(truck2.totalMileage)))
        print("Truck 3 mileage: " + str("{0:.3f}".format(truck3.totalMileage)))
        print("\nTotal mileage traveled by all trucks at specified time: " + str("{0:.3f}".format(totalMileage)))
    elif userMenuChoices == 3:
        # Find the package within the hash table that the user specified.
        # Time complexity is O(n^2) and space complexity is O(n^2) for choice 3.
        package = table.lookup(userPackageChoice)
        print("\nTime of this status check: " + str(userStatusCheckTime) + ".")
        # The currentTime variable is timestamped once all packages are delivered, if the initial user input is greater
        # than the current time then the trucks must be complete with routes.
        if currentTime < userStatusCheckTime:
            print("All packages delivered on time and all trucks returned to the hub at: " + str(currentTime))
        # Iterate through the truck list then through each of their loads and adjust the output accordingly.
        # Time complexity is O(n^2) and space complexity is O(n^2).
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
                              j.delivery_deadline + ".\n")
                        print("The package was placed en route at " + str(j.delivery_time) + ".\n")
                    elif j.getDeliveryStatus() == "At the hub":
                        print("\nPackage #" + str(userPackageChoice) + " weighs " + j.weight +
                              "kg and is at the hub on Truck #" + str(i.truckID) + ".")
                        print("\nThe final destination for this package is " + j.delivery_address + ", " +
                              j.delivery_city + " " + j.delivery_zip + " with a deadline of " +
                              j.delivery_deadline + ".\n")

# =====================================================================================================================
# This block is a clone of the menu and code above. This allows a pause and a new menu choice to be made.
# All previous comments apply identically.
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
# Program continues iterating through the main while loop until selection 4 is made to exit the program.
# =====================================================================================================================
# If 4 is chosen then program exits loop and finishes.
# END OF PROGRAM.
