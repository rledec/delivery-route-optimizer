

# This class represents each truck in the WGUPS system.  It is given attributes such
# as its current location, miles, and time.  It also has a list to store the packages
# that will be assigned to that truck
class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.current_location = 0
        self.miles = 0
        self.current_time = 0
        self.departure_time = 0

    # This method takes a package list and appends all of its contents to the packages
    # list of the truck, it also sets the package.truck_id to the truck_id of the truck
    # it's being loaded onto
    # Big O Runtime: O(n)
    # Big O Space Complexity: O(1)
    def load(self,package_list,hash_table):
        for package_id in package_list:
            self.packages.append(package_id)
            package_object = hash_table.lookup(package_id)
            package_object.truck_id = self.truck_id



