

# This class provides the hash table to store all the packages
class HashTable:
    def __init__(self):
        # Creates a list of 50 lists
        self.hash_table = [[] for _ in range (50)]

    # This method takes a value as an argument, and hashes it to
    # Discover which bucket to place it in.  For numbers greater than 50, like
    # 101, will be hashed to be put into the bucket 1.
    def hash_function(self,value):
        return value % len(self.hash_table)

    # This method allows values to be inserted into the hash table.  Values are
    # Stored as tuple pairs of the package_id and the package itself.  It is stored
    # This way because the package_id is needed to distinguish the package from other
    # packages in each bucket
    # Big O Runtime: O(1)
    # Big O Space Complexity: O(1)
    def insert(self, package_id, package):
        #The bucket index is found by hashing the package_id.  For example
        # A value 61 would be stored in bucket 11, so the index would be 11.
        index = self.hash_function(package_id)
        #This appends the package_id, package tuple into the bucket based on index
        self.hash_table[index].append((package_id, package))

    # This method looks up a specific package based on its package_id
    # And returns the package object based on that id
    # Big O Runtime: O(1)
    # Big O Space Complexity: O(1)
    def lookup(self, package_id):
        # Finds the index of the bucket the package is in
        index = self.hash_function(package_id)

        #Stores the bucket based on the index value into a variable
        bucket = self.hash_table[index]

        # This for-loop goes through each tuple in the bucket and searches for
        # The package_id that was passed as an argument, if it finds a match,
        # It returns the package of that package_id.  If it does not find it, it
        # returns nothing
        for key, package in bucket:
            if key == package_id:
                return package
        return None







 

