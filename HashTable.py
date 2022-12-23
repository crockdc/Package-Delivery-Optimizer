class HashTable:
    def __init__(self, size):
        self.size = size
        self.hashTable = self.createBuckets()

    def createBuckets(self):
        return [[] for _ in range(self.size)]

    def insert(self, key, val):
        hashedKey = hash(key) % self.size

        bucket = self.hashTable[hashedKey]

        foundKey = False
        for index, record in enumerate(bucket):
            recordKey, recordVal = record

            if recordKey == key:
                foundKey = True
                break

        if foundKey:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    def getVal(self, key):
        hashedKey = hash(key) % self.size
        bucket = self.hashTable[hashedKey]

        foundKey = False
        for index, record in enumerate(bucket):
            recordKey, recordVal = record

            if recordKey == key:
                foundKey = True
                break
        if foundKey:
            return recordVal
        else:
            return "No record found"

    def __str__(self):
        return "".join(str(item) for item in self.hashTable)

    def returnValues(self):
        for i in range(self.size):
            print(self.hashTable[i])
