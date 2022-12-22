from HashTable import *
from Package import *
import datetime

totalMileage = 0
startDate = datetime.date.today()
startTime = datetime.datetime(startDate.year, startDate.month, startDate.day, 8)
package1 = Package(1, "555 maple", "10:30", "Manassas", 32119, 22.1, "loaded")
package2 = Package(2, "543 maple", "10:00", "Port", 32128, 22.1, "loaded")

newCurrentTime = startTime + datetime.timedelta(0, 5)
package1.setDeliveryTime(datetime.datetime.time(newCurrentTime))
table = HashTable(41)

table.setVal(package1.packageID, package1)
table.setVal(1, package2)

print(table.getVal(1))
print(table)

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
