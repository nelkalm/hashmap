## Hashmap
Two HashMap implementations in Python with two different collision resolution methods: open addressing with quadratic probing and separate chaining.

## Dependencies
The HashMap implementation with separate chaining is dependent on the following data structures:

 - `LinkedList`
 - `DynamicArray`

The HashMap implementation with open addressing is dependent on the following data structure:

 - `DynamicArray`
 - `HashEntry`

All of those data structures are available in the `ds.py` file. Additionally, it also contains two hash functions required by the HashMap implementation.

## Usage
A HashMap can be declared by the following:

    m = HashMap(53, hash_function_1)

We can a key-value pair into the HashMap:

    m.put('str' + str(100), 250)

We can get the value by key; returns the value if successful, or `None` if the key is not found.

    m.get('str100')   # return 250
    m.get('A')        # return None

We can remove the key and its associated value from the HashMap:

    m.remove('str100')
    m.get('str100')		# return None

Other methods include `contains_key()`, `clear()`, `empty_buckets()`, `resize_table()`, `table_load()`, `get_keys()`, and a standalone `find_mode()` function. The HashMap implementation with open addressing includes an iterator method to enable the HashMap to iterate across itself.

Class method descriptions:

 - `contains_key()`: returns `True` if the given key is in the hash map. `False` otherwise.
 - `clear()`: clears the contents of the hash map.
 - `empty_buckets()`: returns the number of empty buckets in the hash table.
 - `resize_table()`: changes the capacity of the internal hash table.
 - `table_load()`: returns the current hash table load factor. The load factor is defined as the ratio of the hash table size to its capacity.
 - `get_keys_and_values()`: returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
 
 `find_mode()` is a standalone function that returns a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the array, and an integer that represents the highest frequency (how many times they appear). This function is impletemented `O(n)` time complexity.
