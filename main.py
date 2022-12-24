from HashTable import *
from Package import *
import datetime
import csv

# Initialize a selection variable for the user interface
userSelection = 0
# Initialize initial mileage to 0
totalMileage = 0
# Initialize today's date and the start time of 08:00 hours
startDate = datetime.date.today()
startTime = datetime.datetime(startDate.year, startDate.month, startDate.day, 8)
# Instantiate hash table of 41 buckets
table = HashTable(10)

# Utilize CSV reader and iterate through each row of the file.
# Create a new package object for each row.
with open('PackageFile.csv', encoding='utf-8-sig') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row[0])
        csvPackageID = row[0]
        csvPackageAddress = row[1]
        csvPackageCity = row[2]
        csvPackageZip = row[4]
        csvPackageDeadline = row[5]
        csvPackageWeight = row[6]
        package = Package(csvPackageID, csvPackageAddress, csvPackageDeadline, csvPackageCity,
                          csvPackageZip, csvPackageWeight, "At the hub")
        print(package.packageID)
        table.insert(package.packageID, package)

print("Welcome to the WGU UPS Package Delivery interface.\n"
      "How would you like to proceed?\n\n"
      "Enter 1 to run the program from start to finish. You will receive information "
      "on each of the 40 packages and the total mileage to complete the deliveries for the day.\n\n"
      "Enter 2 to enter a specific time and receive all package and mileage information at the"
      " time that you specify\n\nEnter 3 to enter a specific package number followed by a specific"
      "time to receive information about your specified package at the specified time.")
userSelection = int(input("\nENTER A NUMBER:"))
if userSelection == 1:
    print("you typed 1")

# package1 = Package(1, "555 maple", "10:30", "Manassas", 32119, 22.1, "loaded")
# package2 = Package(2, "543 maple", "10:00", "Port", 32128, 22.1, "loaded")

# newCurrentTime = startTime + datetime.timedelta(0, 5)
# package1.setDeliveryTime(datetime.datetime.time(newCurrentTime))

# table.insert(package1.packageID, package1)
# table.insert(1, package2)

# print(table)
print(table.getVal(1))
package = table.getVal(1)
print(package.delivery_address)
# print(table.returnValues())

# if __name__ == '__main__':
