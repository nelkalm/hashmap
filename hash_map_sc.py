# Name: Nelson Lu
# Date: 12/2/2022
# Description: A HashMap implementation using separate chaining for collision resolution.
#           It includes the following methods: put(), get(), remove(), contains_key(),
#           clear(), empty_buckets(), resize_table(), table_load(), get_keys().
#          It also includes a separate find_mode() function using a HashMap to find
#           the mode of an array.


from ds import (DynamicArray, LinkedList, SLNode,
                hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
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
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
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
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value is replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is added.
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Compute the element???s bucket using the hash function
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Search the data structure at that bucket for the element using the key
        # (e.g., iterate through the items in the linked list).

        # Find the location in DA matching the index
        # if it's empty, append new key/value pair
        if self._buckets[index].length() == 0:
            self._buckets[index].insert(key, value)
            self._size += 1

        # if it's not empty, find the node containing the key and replace the value
        else:
            target_node = self._buckets[index].contains(key)
            # if no match, create a node
            # else, replace new value
            if target_node is None:
                self._buckets[index].insert(key, value)
                self._size += 1
            else:
                target_node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """
        if new_capacity < 1:
            return

        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Recompute hash of existing keys
        # # Rehashing all links

        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        old_buckets = self._buckets
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0

        for i in range(old_buckets.length()):
            for link_node in old_buckets[i]:
                self.put(link_node.key, link_node.value)

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        for link_node in self._buckets[index]:
            if link_node.key == key:
                return link_node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map. False otherwise.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        for link_node in self._buckets[index]:
            if link_node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        match = False
        for link_node in self._buckets[index]:
            if link_node.key == key:
                match = True
                self._buckets[index].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        output_da = DynamicArray()
        for i in range(self._buckets.length()):
            for link_node in self._buckets[i]:
                output_da.append((link_node.key, link_node.value))
        return output_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing, in this order, a dynamic array comprising the mode 
    (most occurring) value/s of the array, and an integer that represents the highest 
    frequency (how many times they appear).

    Algorithm:
    1. check element exists in hashmap
    2. if it doesn't exist, put element into hashmap with key=element, value=1
    3. if it does, get the key and increment the value
        -if value > max_freq, set max_freq to value
    """
    map = HashMap()
    max_freq = 1

    for i in range(da.length()):
        if map.contains_key(da[i]):
            element_freq = map.get(da[i])
            element_freq += 1
            map.put(da[i], element_freq)
            if element_freq > max_freq:
                max_freq = element_freq
        else:
            map.put(da[i], 1)

    mode = DynamicArray()
    all_keys_values = map.get_keys_and_values()
    for i in range(all_keys_values.length()):
        if all_keys_values[i][1] == max_freq:
            mode.append(all_keys_values[i][0])
    return mode, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nTest Case - put test 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())
        # print(m.empty_buckets(), round(m.table_load(), 2),
        #       m.get_size(), m.get_capacity())

    print("\nTest Case - put test 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())
        # print(m.empty_buckets(), round(m.table_load(), 2),
        #       m.get_size(), m.get_capacity())

    print("\nTest Case - empty_buckets test 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nTest Case - empty_buckets test 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nTest Case - table_load test 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nTest Case - table_load test 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nTest Case - clear test 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nTest Case - clear test 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nTest Case - resize test 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))

    print("\nTest Case - resize test 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(),
              m.get_capacity(), round(m.table_load(), 2))

    print("\nTest Case - get test 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nTest Case - get test 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nTest Case - contains_key test 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nTest Case - contains_key test 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nTest Case - remove test 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nTest Case - get_keys_and_values test 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nTest Case - find_mode test 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nTest Case - find_mode test 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint",
            "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"],
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
