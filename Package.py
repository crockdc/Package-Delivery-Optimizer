from datetime import *


class Package:
    def __init__(self, packageID, delivery_address, delivery_deadline,
                 delivery_city, delivery_zip, weight, delivery_status):
        self.packageID = int(packageID)
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.weight = weight
        self.delivery_status = "At the hub"
        self.delivery_time = None

    def __str__(self):
        return str(self.packageID) + " " + self.delivery_address + " " + self.delivery_deadline + " " + \
            self.delivery_city + " " + str(self.delivery_zip) + " " + str(self.weight) + " " + self.delivery_status \
            + " " + str(self.delivery_time)

    def getDeliveryStatus(self):
        return self.delivery_status

    def getDeliveryAddress(self):
        return self.delivery_address

    def setDeliveryStatus(self, status):
        self.delivery_status = status

    def setDeliveryTime(self, timestamp):
        self.delivery_time = timestamp

