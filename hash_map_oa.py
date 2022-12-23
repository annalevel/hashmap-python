# Name: Anna Level
# OSU Email: levela@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/3/2022
# Description: Implementation of hashmap using open addressing for collision management.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hashedKey = self._hash_function(key)
        initialIndex = hashedKey % self._capacity
        index = initialIndex
        collisionCheckCounter = 0

        while self._buckets[index] is not None and self._buckets[index].key != key and \
                not self._buckets[index].is_tombstone:
            collisionCheckCounter += 1
            index = (initialIndex + (collisionCheckCounter ** 2 + collisionCheckCounter)//2) % self._capacity

        if self._buckets[index] is None or self._buckets[index].is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        else:
            self._buckets[index].value = value

    def table_load(self) -> float:
        """
        Returns the hash table's current load factor.
        Load factor = number of elements / number of buckets

        Returns:
            float: load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table.

        Returns:
            int: Number of empty buckets
        """
        emptyCount = 0

        for bucketIndex in range(self._capacity):
            if self._buckets[bucketIndex] is None:
                emptyCount += 1

        return emptyCount

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs are present in the updated
        table.

        Args:
            new_capacity (int): New capacity of the internal hash table
        """
        if new_capacity < 1 or new_capacity < self._size:
            return

        if self._is_prime(new_capacity):
            primeCapacity = new_capacity
        else:
            primeCapacity = self._next_prime(new_capacity)

        newBuckets = DynamicArray()
        for counter in range(primeCapacity):
            newBuckets.append(None)

        oldCapacity = self._capacity
        oldBuckets = self._buckets
        self._buckets = newBuckets
        self._capacity = primeCapacity
        self._size = 0

        for oldBucketIndex in range(oldCapacity):
            if oldBuckets[oldBucketIndex] is not None and not oldBuckets[oldBucketIndex].is_tombstone:
                self.put(oldBuckets[oldBucketIndex].key, oldBuckets[oldBucketIndex].value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.

        Args:
            key (String): key to return the associated value of

        Returns:
            object: value associated with key; None if key is not in hash table
        """
        hashedKey = self._hash_function(key)
        initialIndex = hashedKey % self._capacity
        index = initialIndex
        collisionCheckCounter = 0

        while self._buckets[index] is not None and self._buckets[index].key != key:
            collisionCheckCounter += 1
            index = (initialIndex + (collisionCheckCounter ** 2 + collisionCheckCounter)//2) % self._capacity

        return None if self._buckets[index] is None or self._buckets[index].is_tombstone \
            else self._buckets[index].value

    def contains_key(self, key: str) -> bool:
        """
        Returns whether the given key is in the hash table.

        Args:
            key (String): key to look for in hash table

        Returns:
            bool: True if key is in hash table; False otherwise
        """
        hashedKey = self._hash_function(key)
        initialIndex = hashedKey % self._capacity
        index = initialIndex
        collisionCheckCounter = 0

        while self._buckets[index] is not None and \
                (self._buckets[index].is_tombstone or self._buckets[index].key != key):
            collisionCheckCounter += 1
            index = (initialIndex + (collisionCheckCounter ** 2 + collisionCheckCounter)//2) % self._capacity

        return False if self._buckets[index] is None else True

    def remove(self, key: str) -> None:
        """
        Removes the key and corresponding value from the hash table.

        Args:
            key (String): key to remove from hash table
        """
        hashedKey = self._hash_function(key)
        initialIndex = hashedKey % self._capacity
        index = initialIndex
        collisionCheckCounter = 0

        while self._buckets[index] is not None and self._buckets[index].key != key:
            collisionCheckCounter += 1
            index = (initialIndex + (collisionCheckCounter ** 2 + collisionCheckCounter)//2) % self._capacity  # Quadratic probing

        if self._buckets[index] is not None:
            if not self._buckets[index].is_tombstone:
                self._buckets[index].is_tombstone = True
                self._size -= 1

    def clear(self) -> None:
        """
        Clears the hash table's contents but does not reset the capacity.
        """

        self._buckets = DynamicArray()
        for counter in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of tuples corresponding to each key and value pair.

        Returns:
            DynamicArray: consisting of tuples representing (key, value)
        """
        tupleArray = DynamicArray()

        for bucketIndex in range(self._capacity):
            if self._buckets[bucketIndex] is not None and not self._buckets[bucketIndex].is_tombstone:
                tupleEntry = self._buckets[bucketIndex].key, self._buckets[bucketIndex].value
                tupleArray.append(tupleEntry)

        return tupleArray

    def __iter__(self) -> object:
        """
        Allows the hashmap to iterate across itself by initializing its built-in index to 0.

        Returns:
            object: self
        """
        self._index = 0

        return self

    def __next__(self) -> object:
        """
        Returns the next value in the hash table.

        Returns:
            object: next value, unless the end of the hash table has been reached
        """
        try:
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone:
                self._index += 1
            value = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_underlying_list(self):
        """
        Return the underlying Python list object.
        For unit testing only.
        """
        return self._buckets.get_underlying_list()