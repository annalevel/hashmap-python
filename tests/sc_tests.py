import unittest
from a6_include import hash_function_1, HashEntry, hash_function_2, LinkedList, DynamicArray
from hash_map_sc import HashMap, find_mode


class TestOAHashMap(unittest.TestCase):
    def test_put_1(self):
        """
        Test the put method with hash function 1.
        """
        testMap = HashMap(5, hash_function_1)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)

        expectedData = []
        for i in range(11):
            expectedData.append(LinkedList())
        expectedData[8].insert('str0', 0)
        expectedData[9].insert('str1', 100)
        expectedData[10].insert('str2', 200)
        expectedData[0].insert('str3', 300)
        expectedData[1].insert('str4', 400)
        expectedData[2].insert('str5', 500)
        expectedData[3].insert('str6', 600)
        expectedData[4].insert('str7', 700)
        expectedData[5].insert('str8', 800)
        expectedData[6].insert('str9', 900)
        expectedData[2].insert('str10', 1000)

        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

    def test_put_2(self):
        """
        Test the put method with hash function 2.
        """
        testMap = HashMap(5, hash_function_2)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)

        expectedData = []
        for i in range(11):
            expectedData.append(LinkedList())
        expectedData[1].insert('str0', 0)
        expectedData[5].insert('str1', 100)
        expectedData[9].insert('str2', 200)
        expectedData[2].insert('str3', 300)
        expectedData[6].insert('str4', 400)
        expectedData[10].insert('str5', 500)
        expectedData[3].insert('str6', 600)
        expectedData[7].insert('str7', 700)
        expectedData[0].insert('str8', 800)
        expectedData[4].insert('str9', 900)
        expectedData[3].insert('str10', 1000)

        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

    def test_put_same_key(self):
        """
        Test the put method when several calls use the same key.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        expectedData = []
        for i in range(7):
            expectedData.append(LinkedList())
        expectedData[1].insert('str0', 600)
        expectedData[2].insert('str1', 700)
        expectedData[3].insert('str2', 500)
        expectedData[1].insert('stra', 'a')

        self.assertEqual(4, testMap.get_size())
        self.assertEqual(7, testMap.get_capacity())

        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

    def test_table_load(self):
        """
        Test the table_load method that determines the current load.
        """
        testMap = HashMap(5, hash_function_1)
        for i in range(11):
            testMap.put('key' + str(i), i * 100)
        self.assertAlmostEqual(1, testMap.table_load())

        testMap.put('newVal', 999)
        self.assertAlmostEqual(12/23, testMap.table_load())

    def test_empty_buckets(self):
        """
        Tests the function that counts the number of empty buckets.
        """
        testMap = HashMap(67, hash_function_1)
        for i in range(10):
            testMap.put('key' + str(i), i * 100)

        self.assertEqual(67-10, testMap.empty_buckets())

        testMap.put('newValue', 1111)
        self.assertEqual(67-11, testMap.empty_buckets())

    def test_resize_table(self):
        """
        Tests resizing hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        self.assertEqual(4, testMap.get_size())
        self.assertEqual(7, testMap.get_capacity())

        testMap.resize_table(25)

        expectedData = []
        for i in range(29):
            expectedData.append(LinkedList())
        expectedData[16].insert('str0', 600)
        expectedData[17].insert('str1', 700)
        expectedData[18].insert('str2', 500)
        expectedData[7].insert('stra', 'a')

        self.assertEqual(4, testMap.get_size())
        self.assertEqual(29, testMap.get_capacity())
        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

        testMap.resize_table(7)

        expectedData = []
        for i in range(7):
            expectedData.append(LinkedList())
        expectedData[1].insert('stra', 'a')
        expectedData[1].insert('str0', 600)
        expectedData[2].insert('str1', 700)
        expectedData[3].insert('str2', 500)

        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

    def test_get(self):
        """
        Tests retrieving existent and nonexistent values from hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(10):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        testGetTrue = testMap.get('stra')
        testGetFalse = testMap.get('str01')

        self.assertEqual('a', testGetTrue)
        self.assertFalse(testGetFalse)

    def test_contains_key(self):
        """
        Tests the function that tests whether the given key is in the hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(10):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        testTrue = testMap.contains_key('str1')
        testFalse = testMap.contains_key('aaa')

        testMap.remove('str1')
        testFalse2 = testMap.contains_key('str1')

        self.assertTrue(testTrue)
        self.assertFalse(testFalse)
        self.assertFalse(testFalse2)

    def test_remove(self):
        """
        Tests removing an entry from the hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        expectedData = []
        for i in range(7):
            expectedData.append(LinkedList())
        expectedData[1].insert('str0', 600)
        expectedData[2].insert('str1', 700)
        expectedData[3].insert('str2', 500)
        expectedData[1].insert('stra', 'a')

        testMap.remove('x')     # Removing non-existent key shouldn't do anything
        self.assertEqual(4, testMap.get_size())

        testMap.remove('stra')
        expectedData[1].remove('stra')     # Update expected data
        self.assertEqual(3, testMap.get_size())

        for idx in range(len(expectedData)):
            expectedElement = expectedData[idx].get_head()
            actualElement = testMap.get_underlying_list()[idx].get_head()

            if actualElement is not None or expectedElement is not None:
                self.assertEqual(expectedElement.key, actualElement.key)
                self.assertEqual(expectedElement.value, actualElement.value)

                actualElement = actualElement.next
                expectedElement = expectedElement.next

                while actualElement is not None or expectedElement is not None:
                    self.assertEqual(expectedElement.key, actualElement.key)
                    self.assertEqual(expectedElement.value, actualElement.value)

                    actualElement = actualElement.next
                    expectedElement = expectedElement.next

    def test_clear(self):
        """
        Tests clearing the hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)
        testMap.clear()

        self.assertEqual(0, testMap.get_size())
        self.assertEqual(17, testMap.get_capacity())

    def test_get_keys_and_values(self):
        """
        Tests the get_keys_and_values method that returns a DynamicArray of tuples corresponding to each key and value.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        expectedTupleArray = [
            ('stra', 'a'),
            ('str0', 600),
            ('str1', 700),
            ('str2', 500),
        ]

        actualTupleArray = testMap.get_keys_and_values().get_underlying_list()
        self.assertListEqual(expectedTupleArray, actualTupleArray)

        del expectedTupleArray[1]
        testMap.remove('str0')
        actualTupleArray = testMap.get_keys_and_values().get_underlying_list()
        self.assertListEqual(expectedTupleArray, actualTupleArray)

    def test_find_mode(self):
        """
        Tests the find_mode method, which returns a tuple of the mode(s) of a DynamicArray and how many occurrences.
        """
        testArray = DynamicArray(['a', 'a', 'a1', 'a1'])
        modeTuple = find_mode(testArray)
        actualTuple = modeTuple[0].get_underlying_list(), modeTuple[1]
        expectedTuple = (
            ['a1', 'a'],
            2
        )

        self.assertEqual(expectedTuple, actualTuple)

        testArray = DynamicArray([1, 200, 200, 2, 200, 2, 1, 200, 300])
        modeTuple = find_mode(testArray)
        actualTuple = modeTuple[0].get_underlying_list(), modeTuple[1]
        expectedTuple = (
            ['200'],
            4
        )

        self.assertEqual(expectedTuple, actualTuple)


if __name__ == '__main__':
    unittest.main()
