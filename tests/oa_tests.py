import unittest
from a6_include import hash_function_1, HashEntry, hash_function_2
from hash_map_oa import HashMap


class TestOAHashMap(unittest.TestCase):
    def test_put_1(self):
        """
        Test the put method with hash function 1.
        """
        testMap = HashMap(5, hash_function_1)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)

        expectedData = [
            None,
            None,
            HashEntry('str0', 0),
            HashEntry('str1', 100),
            HashEntry('str2', 200),
            HashEntry('str3', 300),
            HashEntry('str4', 400),
            HashEntry('str5', 500),
            HashEntry('str6', 600),
            HashEntry('str7', 700),
            HashEntry('str8', 800),
            HashEntry('str9', 900),
            None,
            None,
            None,
            HashEntry('str10', 1000),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        for idx in range(len(expectedData)):
            if expectedData[idx] is None:
                self.assertEqual(expectedData[idx], testMap.get_underlying_list()[idx])
            else:
                self.assertEqual(expectedData[idx].key, testMap.get_underlying_list()[idx].key)
                self.assertEqual(expectedData[idx].value, testMap.get_underlying_list()[idx].value)

    def test_put_2(self):
        """
        Test the put method with hash function 2.
        """
        testMap = HashMap(5, hash_function_2)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)

        expectedData = [
            HashEntry('str4', 400),
            None,
            None,
            None,
            HashEntry('str5', 500),
            None,
            None,
            HashEntry('str0', 0),
            HashEntry('str6', 600),
            None,
            None,
            HashEntry('str1', 100),
            HashEntry('str7', 700),
            None,
            None,
            HashEntry('str2', 200),
            HashEntry('str8', 800),
            None,
            None,
            HashEntry('str3', 300),
            HashEntry('str9', 900),
            HashEntry('str10', 1000),
            None,
        ]

        for idx in range(len(expectedData)):
            if expectedData[idx] is None:
                self.assertEqual(expectedData[idx], testMap.get_underlying_list()[idx])
            else:
                self.assertEqual(expectedData[idx].key, testMap.get_underlying_list()[idx].key)
                self.assertEqual(expectedData[idx].value, testMap.get_underlying_list()[idx].value)

    def test_put_same_key(self):
        """
        Test the put method when several calls use the same key.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        expectedData = [
            None,
            HashEntry('str0', 600),
            HashEntry('str1', 700),
            HashEntry('str2', 500),
            HashEntry('stra', 'a'),
            None,
            None,
        ]

        self.assertEqual(4, testMap.get_size())
        self.assertEqual(7, testMap.get_capacity())

        for idx in range(len(expectedData)):
            if expectedData[idx] is None:
                self.assertEqual(expectedData[idx], testMap.get_underlying_list()[idx])
            else:
                self.assertEqual(expectedData[idx].key, testMap.get_underlying_list()[idx].key)
                self.assertEqual(expectedData[idx].value, testMap.get_underlying_list()[idx].value)

    def test_table_load(self):
        """
        Test the table_load method that determines the current load.
        """
        testMap = HashMap(5, hash_function_1)
        for i in range(12):
            testMap.put('key' + str(i), i * 100)
        self.assertAlmostEqual(12/23, testMap.table_load())

        testMap.put('newVal', 999)
        self.assertAlmostEqual(13/47, testMap.table_load())

    def test_empty_buckets(self):
        """
        Tests the function that counts the number of empty buckets.
        """
        testMap = HashMap(100, hash_function_1)
        for i in range(150):
            testMap.put('key' + str(i), i * 100)

        self.assertEqual(431-150, testMap.empty_buckets())

        testMap.put('newValue', 1111)
        self.assertEqual(431-151, testMap.empty_buckets())

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

        resizedExpectedData = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            HashEntry('stra', 'a'),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            HashEntry('str0', 600),
            HashEntry('str1', 700),
            HashEntry('str2', 500),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        testMap.resize_table(1)     # Should do nothing since 1 < size of table
        self.assertEqual(4, testMap.get_size())
        self.assertEqual(29, testMap.get_capacity())

        for idx in range(len(resizedExpectedData)):
            if resizedExpectedData[idx] is None:
                self.assertEqual(resizedExpectedData[idx], testMap.get_underlying_list()[idx])
            else:
                self.assertEqual(resizedExpectedData[idx].key, testMap.get_underlying_list()[idx].key)
                self.assertEqual(resizedExpectedData[idx].value, testMap.get_underlying_list()[idx].value)

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

        expectedData = [
            None,
            HashEntry('str0', 600),
            HashEntry('str1', 700),
            HashEntry('str2', 500),
            HashEntry('stra', 'a'),
            None,
            None,
        ]

        testMap.remove('x')     # Removing non-existent key shouldn't do anything
        self.assertEqual(4, testMap.get_size())

        testMap.remove('stra')
        expectedData[4].is_tombstone = True     # Update expected data
        self.assertEqual(3, testMap.get_size())

        for idx in range(len(expectedData)):
            if expectedData[idx] is None:
                self.assertEqual(expectedData[idx], testMap.get_underlying_list()[idx])
            else:
                self.assertEqual(expectedData[idx].key, testMap.get_underlying_list()[idx].key)
                self.assertEqual(expectedData[idx].value, testMap.get_underlying_list()[idx].value)

    def test_clear(self):
        """
        Tests clearing the hash table.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(11):
            testMap.put('str' + str(i), i * 100)
        testMap.clear()

        expectedData = [None] * 37

        self.assertEqual(0, testMap.get_size())
        self.assertEqual(37, testMap.get_capacity())
        self.assertListEqual(expectedData, testMap.get_underlying_list())

    def test_get_keys_and_values(self):
        """
        Tests the get_keys_and_values method that returns a DynamicArray of tuples corresponding to each key and value.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        expectedTupleArray = [
            ('str0', 600),
            ('str1', 700),
            ('str2', 500),
            ('stra', 'a'),
        ]

        actualTupleArray = testMap.get_keys_and_values().get_underlying_list()
        self.assertListEqual(expectedTupleArray, actualTupleArray)

        del expectedTupleArray[0]
        testMap.remove('str0')
        actualTupleArray = testMap.get_keys_and_values().get_underlying_list()
        self.assertListEqual(expectedTupleArray, actualTupleArray)

    def test_iter(self):
        """
        Tests the built-in iteration capabilities of the data structure.
        """
        testMap = HashMap(3, hash_function_1)
        for i in range(8):
            testMap.put('str' + str(i % 3), i * 100)
        testMap.put('stra', 'a')

        counter = 0

        for item in testMap:
            match counter:
                case 0:
                    self.assertEqual('str0', item.key)
                    self.assertEqual(600, item.value)
                case 1:
                    self.assertEqual('str1', item.key)
                    self.assertEqual(700, item.value)
                case 2:
                    self.assertEqual('str2', item.key)
                    self.assertEqual(500, item.value)
                case 3:
                    self.assertEqual('stra', item.key)
                    self.assertEqual('a', item.value)

            counter += 1

        self.assertEqual(4, counter)      # Should have iterated 4 times for 4 items


if __name__ == '__main__':
    unittest.main()
