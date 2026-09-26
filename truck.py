

# Represents a delivery truck and tracks its assigned packages, location, mileage, and time.
class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.current_location = 0
        self.miles = 0
        self.current_time = 0
        self.departure_time = 0

    # Loads assigned packages onto the truck and records the truck assignment.
    # Runtime: O(n) | Space: O(1)
    def load(self, package_list, hash_table):
        for package_id in package_list:
            self.packages.append(package_id)
            package_object = hash_table.lookup(package_id)
            package_object.truck_id = self.truck_id



