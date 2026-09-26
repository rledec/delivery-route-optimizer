

# Represents a package and tracks its delivery information and status.
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

        # Delivery tracking
        self.status = "At Hub"
        self.departure_time = None
        self.delivery_time = None



