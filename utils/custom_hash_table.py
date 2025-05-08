class PackageHashTable:

    # The constructor for hash table to determine size and create table
    # Also, adds a count attribute that is incremented with each insertion
    def __init__(self, num_packages):
        self.size = _next_prime(num_packages * 2)
        self.table = [[] for _ in range(self.size)]
        self.count = 0

    # Hash function for computing index for insert into table
    # Hash function uses built-in Python hash(package_key) function and then
    # mods that value by table size to get index value for insert
    def _hash(self, key):
        return hash(key) % self.size

    # Insert function for hash table: defines bucket index values using
    # the _hash method on the package key.
    # Then search the hash table for an empty bucket using separate chaining
    # for collision resolution by storing kv pairs in a list at each bucket index.
    # If the key already exists in the table, the value corresponding to that key is
    # updated and a message is concatenated onto the existing note to indicate
    # that the ID is a duplicate.
    # Appends the package to the bucket list when an open index is found,
    # and then increments the counter for the number of elements in the hash table
    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, existing_value) in enumerate(bucket):
            if k == key:
                existing_value.append_note("DUPLICATE PACKAGE ID")
                bucket[i] = (key, existing_value)
                return
        bucket.append((key, value))
        self.count += 1

    # get method for retrieving hash table elements' values by their key
    def get(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

# defining static method to generate the next prime that is
# greater than argument 'num'
def _next_prime(num):
    def is_prime(x):
        if x <= 1:
            return False
        for i in range(2, x):
            if x % i == 0:
                return False
        return True
    while not is_prime(num):
        num += 1
    return num
