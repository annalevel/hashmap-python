# Name: Anna Level
# OSU Email: levela@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/3/2022
# Description: Implementation of hashmap using chaining for collision management.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the given key/value pair in the hash table.
        If the key is already in the hash table, the value is updated.
        If not, the key and value are inserted.

        Args:
            key (String): value's corresponding key
            value (object): value to insert or replace
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hashedKey = self._hash_function(key)
        bucketToPut = self._buckets[hashedKey % self._capacity]
        hashedKeyNode = bucketToPut.contains(key)

        if hashedKeyNode is not None:
            hashedKeyNode.value = value
        else:
            bucketToPut.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table.

        Returns:
            int: Number of empty buckets
        """
        emptyCount = 0

        for bucketIndex in range(self._capacity):
            if self._buckets[bucketIndex].length() == 0:
                emptyCount += 1

        return emptyCount

    def table_load(self) -> float:
        """
        Returns the hash table's current load factor.
        Load factor = number of elements / number of buckets

        Returns:
            float: load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hash table's contents but does not reset the capacity.
        """
        self._buckets = DynamicArray()
        for counter in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs are present in the updated
        table.

        Args:
            new_capacity (int): New capacity of the internal hash table
        """
        if new_capacity < 1:
            return

        if self._is_prime(new_capacity):
            primeCapacity = new_capacity
        else:
            primeCapacity = self._next_prime(new_capacity)

        newBuckets = DynamicArray()
        for counter in range(primeCapacity):
            newBuckets.append(LinkedList())

        oldCapacity = self._capacity
        oldBuckets = self._buckets
        self._buckets = newBuckets
        self._capacity = primeCapacity
        self._size = 0

        for oldBucketIndex in range(oldCapacity):
            for element in oldBuckets[oldBucketIndex]:
                self.put(element.key, element.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.

        Args:
            key (String): key to return the associated value of

        Returns:
            object: value associated with key; None if key is not in hash table
        """
        bucketIndexToSearch = self._hash_function(key) % self._capacity
        nodeWithKey = self._buckets[bucketIndexToSearch].contains(key)

        return None if nodeWithKey is None else nodeWithKey.value

    def contains_key(self, key: str) -> bool:
        """
        Returns whether the given key is in the hash table.

        Args:
            key (String): key to look for in hash table

        Returns:
            bool: True if key is in hash table; False otherwise
        """
        bucketIndexToSearch = self._hash_function(key) % self._capacity
        nodeWithKey = self._buckets[bucketIndexToSearch].contains(key)

        return False if nodeWithKey is None else True

    def remove(self, key: str) -> None:
        """
        Removes the key and corresponding value from the hash table.

        Args:
            key (String): key to remove from hash table
        """
        bucketIndexToSearch = self._hash_function(key) % self._capacity
        elementWasRemoved = self._buckets[bucketIndexToSearch].remove(key)
        if elementWasRemoved:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of tuples corresponding to each key and value pair.

        Returns:
            DynamicArray: consisting of tuples representing (key, value)
        """
        tupleArray = DynamicArray()

        for bucketIndex in range(self._capacity):
            for element in self._buckets[bucketIndex]:
                tupleElement = element.key, element.value
                tupleArray.append(tupleElement)

        return tupleArray

    def get_underlying_list(self):
        """
        Return the underlying Python list object.
        For unit testing only.
        """
        return self._buckets.get_underlying_list()


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing the mode(s) of the given array, and the number of times this occurs.
    Runtime: O(n)

    Args:
        da (DynamicArray): array of values, potentially unsorted

    Returns:
        (DynamicArray, int): (mode value(s), mode frequency)
    """
    frequencyMap = HashMap()
    modeValues = DynamicArray()

    # Populate frequency map
    for index in range(da.length()):
        keyToInsert = str(da[index])
        existingNode = frequencyMap.get(keyToInsert)
        valueToInsert = 1 if existingNode is None else existingNode + 1
        frequencyMap.put(keyToInsert, valueToInsert)

    arrayOfKeyValueTuples = frequencyMap.get_keys_and_values()  # format: (key, value)

    # Find highest frequency
    highFreq = 0
    for countingIndex in range(arrayOfKeyValueTuples.length()):
        curKey, curValue = arrayOfKeyValueTuples[countingIndex]
        if curValue > highFreq:
            highFreq = curValue

    # Collect the mode values
    for arrayIndex in range(arrayOfKeyValueTuples.length()):
        curKey, curValue = arrayOfKeyValueTuples[arrayIndex]
        if curValue == highFreq:
            modeValues.append(curKey)

    return modeValues, highFreq
