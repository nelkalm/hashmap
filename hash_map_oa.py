# Name: Nelson Lu
# OSU Email: luhun@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/2/2022
# Description: A HashMap implementation using quadratic probing for collision resolution.
#           It includes the following methods: put(), get(), remove(), contains_key(),
#           clear(), empty_buckets(), resize_table(), table_load(), get_keys(), __iter__(), __next__().

# @TODO: remove random module
import random

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
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value is replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is added.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Compute initial index
        hash = self._hash_function(key)
        index = hash % self._capacity

        # If the hash table array at initial index is empty, insert the element there and stop
        if self._buckets[index] == None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # If the key exists, replace with new value
        elif self._buckets[index].key == key:
            self._buckets[index].value = value
            if self._buckets[index].is_tombstone is True:
                self._buckets[index].is_tombstone = False
                self._size += 1
        else:
            # Probe until we find either the element we’re looking for, or an empty spot
            j = 1
            index_qp = (index + (j ** 2)) % self._capacity
            while self._buckets[index_qp] is not None and self._buckets[index_qp].key != key:
                index_qp = (index + (j ** 2)) % self._capacity
                j += 1
            # If spot is empty, create hash entry
            if self._buckets[index_qp] is None:
                self._buckets[index_qp] = HashEntry(key, value)
                self._size += 1
            # If not, replace with new value
            else:
                self._buckets[index_qp].value = value
                if self._buckets[index_qp].is_tombstone is True:
                    self._buckets[index_qp].is_tombstone = False
                    self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i] is None:
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """
        if new_capacity < self._size:
            return

        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # new_hash_map = HashMap(new_capacity, self._hash_function)
        # initialize new buckets
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        old_buckets = self._buckets

        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0

        for i in range(old_buckets.length()):
            if old_buckets[i] is not None:
                if old_buckets[i].is_tombstone is False:
                    self.put(old_buckets[i].key, old_buckets[i].value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        """
        # Compute the hash
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return None

        if self._buckets[index].is_tombstone:
            return None

        # If the index location is not empty, check to see if key is there
        # If it's not there, use quadratic probing to see if it's displaced
        if self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return self._buckets[index].value
            else:
                # Probe until we find either the element we’re looking for, or an empty spot
                j = 1
                index_qp = (index + (j ** 2)) % self._capacity
                while self._buckets[index_qp] is not None and self._buckets[index_qp].key != key:
                    index_qp = (index + (j ** 2)) % self._capacity
                    j += 1

                if self._buckets[index_qp] is None:
                    return None
                if self._buckets[index_qp].key == key:
                    return self._buckets[index_qp].value
                if self._buckets[index_qp].key != key:
                    return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map. False otherwise.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return False

        if self._buckets[index].is_tombstone:
            return False

        if self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return True
            else:
                # Probe until we find either the element we’re looking for, or an empty spot
                j = 1
                index_qp = (index + (j ** 2)) % self._capacity
                while self._buckets[index_qp] is not None and self._buckets[index_qp].key != key:
                    index_qp = (index + (j ** 2)) % self._capacity
                    j += 1

                if self._buckets[index_qp] is None:
                    return False
                if self._buckets[index_qp].key == key:
                    return True
                if self._buckets[index_qp].key != key:
                    return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        # if self.contains_key(key) is False:
        #     return
        if self._buckets[index].key == key:
            self._buckets[index].is_tombstone = True
            self._size -= 1
        else:
            # Probe until we find either the element we’re looking for, or an empty spot
            j = 1
            index_qp = (index + (j ** 2)) % self._capacity
            while self._buckets[index_qp] is not None and self._buckets[index_qp].key != key:
                index_qp = (index + (j ** 2)) % self._capacity
                j += 1
            if self._buckets[index_qp].key is None:
                return
            if self._buckets[index_qp].key != key:
                return
            if self._buckets[index_qp].key == key:
                self._buckets[index_qp].is_tombstone = True
                self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        output_da = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone == False:
                output_da.append(
                    (self._buckets[i].key, self._buckets[i].value))
        return output_da

    def __iter__(self):
        """
        Creates iterator for loop.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Obtains next value and advances iterator.
        """
        current_bucket = self._buckets[self.index]

        if self.index > self._buckets.length() - 1:
            raise StopIteration

        if current_bucket is not None and current_bucket.is_tombstone is False:
            self.index += 1
            return current_bucket
        else:
            while current_bucket is None or current_bucket.is_tombstone:
                self.index += 1
                current_bucket = self._buckets[self.index]

                if self.index == self._buckets.length() - 1:
                    raise StopIteration

            # if current_bucket.is_tombstone is False:
            not_none_bucket = self._buckets[self.index]

            self.index += 1
            return not_none_bucket

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    # print("\nMy Test")
    # print("-------------------")
    # m = HashMap(5, hash_function_2)
    # print(m)
    # print("\nAdding str100 to the map")
    # hash = hash_function_2('str100')
    # print(hash)
    # m.put("str100", 100)
    # print(m)
    # print(m.empty_buckets(), round(m.table_load(), 2),
    #       m.get_size(), m.get_capacity())
    # m.put("str200", 200)
    # m.put("str300", 300)
    # print(m)
    # print(m.empty_buckets(), round(m.table_load(), 2),
    #       m.get_size(), m.get_capacity())
    # m.put("str100", 1000)
    # print(m)
    # print(m.empty_buckets(), round(m.table_load(), 2),
    #       m.get_size(), m.get_capacity())
    # m.put("str400", 400)
    # m.put("str500", 500)
    # print(m)
    # print(m.empty_buckets(), round(m.table_load(), 2),
    #       m.get_size(), m.get_capacity())

    # print("\nPDF - put test example")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(15):
    #     m.put('str' + str(i), i * 100)
    #     print(m.empty_buckets(), round(m.table_load(), 2),
    #           m.get_size(), m.get_capacity())
    # print(m)

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    # #     # if i % 25 == 24:
    # #     #     print(m.empty_buckets(), round(m.table_load(), 2),
    # #     #           m.get_size(), m.get_capacity())
    # #     print(m.empty_buckets(), round(m.table_load(), 2),
    # #           m.get_size(), m.get_capacity())
    # print(m)

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2),
    #               m.get_size(), m.get_capacity())
    # #     print(i, m.empty_buckets(), round(m.table_load(), 2),
    # #           m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(),
    #       m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(),
    #       m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # m.put('some key', 75)
    # print(m.get_size(), m.get_capacity())
    # m.remove('some key')
    # print(m.get_size(), m.get_capacity())
    # print(m)
    # m.resize_table(163)
    # print('Table resized')
    # print(m.get_size(), m.get_capacity())
    # print(m)

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(),
    #           m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key3982890'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # print(hash_function_1('key3982890') % 107)

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(10, 300, 7):
    #     m.put('key' + str(i), i * 10)
    # print(m)
    # m.get('key9481683')
    # print(m.get('key9481683'))
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - self example")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(10, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m)

    # print(m.contains_key('234'))

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # print(m)
    # m.resize_table(12)
    # print()
    # print(m)
    # print(m.get_keys_and_values())

    # print("\nPDF - additional remove test with random values")
    # print("------------------------")
    # m = HashMap(30, hash_function_1)
    # for i in range(40):
    #     r_n = random.randrange(-1000, 1000, 39)
    #     m.put('key' + str(abs(r_n)), r_n)
    #     # if r_n % 2 == 0:
    #     #     m.remove('key' + str(abs(r_n)))
    # # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # # m2 = m
    # # print(m2)
    # # m2.put('key' + str(200), 200)
    # # print(m2)
    # # print(m)
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # print(m)
    # for i in range(10):
    #     m.put('key' + str(i * 100), i * 100)
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # print(m)
    # for i in range(10):
    #     m.remove('key' + str(i * 100))
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # print(m)

    # m.resize_table(137)
    # m.put('key797', -797)
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # m.resize_table(137)
    # # print(m)

    # m.remove('key797')
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # # print(m)

    print("\nGS Typed Out")
    m = HashMap(106, hash_function_1)
    m.put('key' + '15', 85)
    m.remove('key15')
    m.put('key' + '49', -182)
    m.put('key' + '420', -463)
    m.put('key' + '234', -133)
    m.put('key' + '901', -287)
    m.remove('key901')
    m.put('key' + '173', -448)
    m.put('key' + '155', 281)
    m.put('key' + '454', -267)
    m.put('key' + '167', 256)
    m.put('key' + '906', 2)
    m.remove('key906')
    m.put('key' + '358', 554)
    m.remove('key358')
    m.put('key' + '728', 6941)
    m.put('key' + '558', -841)
    m.remove('key558')
    m.put('key' + '397', 248)
    m.remove('key397')
    m.put('key' + '817', 360)
    m.put('key' + '849', -469)
    m.put('key' + '886', -429)
    m.put('key' + '896', 810)
    m.remove('key896')
    m.put('key' + '375', -526)
    m.put('key' + '565', -892)
    m.put('key' + '889', 121)
    m.put('key' + '477', 1000)
    m.put('key' + '663', -942)
    m.put('key' + '790', -963)
    m.put('key' + '819', 400)
    m.put('key' + '623', 32)
    m.put('key' + '186', 835)
    m.put('key' + '207', 392)
    m.put('key' + '515', -717)
    m.put('key' + '537', -337)

    print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    print(m)

    print('remove(key375)')
    m.remove('key375')
    print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    print(m)

    # m.put('key797', -797)
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # # print(m)

    # m.remove('key797')
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # print(m)
    # for item in m:
    #     if item.value % 2 == 0:
    #         m.remove(item.key)
    # # print(m)
    # m2 = m
    # print(f'capacity {m2.get_capacity()}, size {m2.get_size()}')
    # print(m2)
    # m2.remove('key727')
    # print(f'capacity {m2.get_capacity()}, size {m2.get_size()}')
    # print(m2)
    # print(hash_function_1('key375') % 107)
    # m.remove('key493')
    # print(f'capacity {m.get_capacity()}, size {m.get_size()}')
    # print(m)
    # print(m.get_size(), m.get_capacity())
    # print(m.contains_key('key26'))
    # m.remove('key26')
    # print(m.get_size(), m.get_capacity())
    # print(m)
    # m.put('key26', 52)
    # print(m.get_size(), m.get_capacity())
    # print(m)
    # m.remove('key26')
    # print(m.get_size(), m.get_capacity())
    # print(m)

    # m.resize_table(2)
    # print(m)
    # m.put('20', '200')
    # print(m)
    # m.remove('1')
    # print(m)

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
