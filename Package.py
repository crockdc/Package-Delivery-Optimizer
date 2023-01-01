from datetime import *


# Package class allows for package objects to be instantiated manually or while reading in a CSV file automatically.
# The delivery time uses Python's datetime library to align with the rest of the program.
# The space and time complexity of instantiating the package object are each O(1).
class Package:
    def __init__(self, packageID, delivery_address, delivery_deadline,
                 delivery_city, delivery_zip, weight, delivery_status):
        self.packageID = int(packageID)
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.weight = weight
        self.delivery_status = delivery_status
        # All trucks are loaded at the hub at 08:00am
        self.delivery_time = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 8)

    # The accessors and mutators are all space and time complexities of 0(1).
    def getDeliveryStatus(self):
        return self.delivery_status

    def getDeliveryAddress(self):
        return self.delivery_address

    def setDeliveryStatus(self, status):
        self.delivery_status = status

    def setDeliveryTime(self, timestamp):
        self.delivery_time = timestamp

    def setDeliveryAddress(self, address):
        self.delivery_address = address

    def setZipCode(self, zipCode):
        self.delivery_zip = zipCode

