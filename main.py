from HashTable import *
from Package import *
import datetime
import csv

# Instantiate hash table of 41 buckets
table = HashTable(41)

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



# Initialize initial mileage to 0
totalMileage = 0
# Initialize today's date and the start time of 08:00 hours
startDate = datetime.date.today()
startTime = datetime.datetime(startDate.year, startDate.month, startDate.day, 8)
#package1 = Package(1, "555 maple", "10:30", "Manassas", 32119, 22.1, "loaded")
#package2 = Package(2, "543 maple", "10:00", "Port", 32128, 22.1, "loaded")

# newCurrentTime = startTime + datetime.timedelta(0, 5)
# package1.setDeliveryTime(datetime.datetime.time(newCurrentTime))
#
# table.insert(package1.packageID, package1)
# table.insert(1, package2)

print(table)
print(table.getVal(1))
print(table.returnValues())

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
