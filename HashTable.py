# The HashTable class allows for instantiation of an object that holds buckets of key:value pairs.
# To instantiate the hash table, O(n) space and time complexity is used due to the for loop in the createTable function.
# This hash table uses chaining to avoid collisions.
class HashTable:
    # Constructor uses size parameter to allocate desired memory space.
    def __init__(self, size):
        self.size = size
        # Uses the createTable function to create a list of lists.
        self.hashTable = self.createTable()

    # Create and return a list of lists of the size allocated during construction.
    # Space and time complexity O(n)
    def createTable(self):
        return [[] for i in range(self.size)]

    # In this case we use the unique package ID as the key, and it's corresponding package object as the value.
    # The time complexity to insert into the hash table is O(n).
    # The space complexity to insert into the hash table is O(1).
    def insert(self, key, value):
        # Using modulus based on the size, create a numerical key using the key parameter from the constructor.
        # Hash function not needed here due to using unique package ID's, but would be useful for other data types.
        hashedKey = key % self.size
        # The bucket that is chosen is the value of the hashedKey.
        bucket = self.hashTable[hashedKey]
        # Set the foundKey variable to false until the parameter key is matched within one of the pairs within bucket.
        foundKey = False
        # Iterate through each of the items within the specified bucket list using enumerate.
        for i in range(len(bucket)):
            # Assign each of the pairs of items within the bucket list key value variable names.
            recordKey, recordVal = bucket[i]
            # If the found key equals the parameter key then update found key to True and break the loop.
            if recordKey == key:
                foundKey = True
                break
        # If the key was found then update the information for that key, else append the new key value pair.
        if foundKey:
            bucket[i] = [key, value]
        else:
            bucket.append([key, value])

    # The lookup method uses the unique package ID as an argument.
    # The time complexity is O(n).
    # The space complexity is O(1).
    def lookup(self, key):
        # Hash function not needed here due to using unique package ID's, but would be useful for other data types.
        hashedKey = key % self.size
        # Use the hashed key to find the bucket within the hash table and assign to variable name bucket.
        bucket = self.hashTable[hashedKey]
        # Set a boolean variable to check if a matching key is found within the bucket list.
        foundKey = False
        # Iterate through the bucket list splitting each list into a key value pair named index and record.
        for i in range(len(bucket)):
            # Assign each of the pairs of items within the bucket list key value variable names.
            recordKey, recordVal = bucket[i]
            # If the key equals the recordKey then change boolean to true and break out of the loop.
            if recordKey == key:
                foundKey = True
                break
        # Return the value(Package) if the key was found, otherwise return no package found.
        if foundKey:
            return recordVal
        else:
            return "No package found"

