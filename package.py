

# This class represents the package in the WGUPS system.  It includes the attributes
# Required in the rubric.  Every package is initially set to At Hub because it has not
# Yet left.  Departure time and Delivery time are set to none and updated once the truck
# leaves the hub and when the package is delivered respectively.
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck_id = None

        # delivery tracking
        self.status = "At Hub"
        self.departure_time = None
        self.delivery_time = None



