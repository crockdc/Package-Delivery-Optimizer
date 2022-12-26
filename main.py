from HashTable import *
from Package import *
from Truck import *

import datetime
import csv

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
startDate = datetime.date.today()
startTime = datetime.datetime(startDate.year, startDate.month, startDate.day, 8)
# Instantiate a chaining hash table of 10 buckets
table = HashTable(2)

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
            addressList.append(row[i+1])
        # Add the list to the address which is the key to the dictionary.
        distanceDictionary.update({row[0]: addressList})
        # Add the address to the dictionary which holds addresses represented as numerical values.
        addressDictionary.update({j: row[0]})
        # Iterate j by 1.
        j += 1

# print(addressDictionary)
# tempList = distanceDictionary.get('1060 Dalton Ave S')
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

# Manually load the trucks
truckLoad1.append(table.getVal(11))
truck1 = Truck(1, truckLoad1, 0, 0, "321 gfds", None, False)
print(truck1)