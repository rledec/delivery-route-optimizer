import csv
from hash_table import HashTable
from package import Package
from address import addresses
from truck import Truck
import re

DELAYED_PACKAGES = {6, 25, 28, 32}
DELAYED_TIME = 65


# Returns the distance between two address indices in the symmetric distance matrix.
# Runtime: O(1) | Space: O(1)
def get_distance(i, j):
    if distances[i][j] is not None:
        return distances[i][j]
    else:
        return distances[j][i]

# Returns the index of an address in the address list.
# Runtime: O(n) | Space: O(1)
def address_lookup(address_string):

    return addresses.index(address_string)

# Delivers all packages assigned to a truck using a greedy nearest-neighbor strategy.
# At each stop, the truck selects the closest remaining delivery address and delivers
# all eligible packages at that location before continuing.
# Runtime: O(n^2) | Space: O(n)
def truck_delivery_algorithm(truck):
    # This for loop goes through every package object referenced in that truck.packages list
    # and updates each package departure time to the current time of the truck
    for each in truck.packages:
        package_object = table.lookup(each)
        package_object.departure_time = truck.current_time

    #This while loop runs until every package on truck.packages is removed(delivered)
    while truck.packages:

        # Package 9 cannot be delivered until its corrected address becomes available at 10:20 AM.
        # If it is the only package remaining, advance the truck clock to the correction time.
        if truck.packages[0] == 9 and truck.current_time < 140:
            if len(truck.packages) < 2:
                truck.current_time = 140
                continue
            else:
                first_package = table.lookup(truck.packages[1])
        else:
            first_package = table.lookup(truck.packages[0])





        # Initialize the nearest candidate using the first eligible package.
        best_address = first_package.address
        best_address_index = address_lookup(best_address)
        shortest_distance = get_distance(truck.current_location, best_address_index)

        # Find the closest eligible delivery address from the truck's current location.
        for each_package in truck.packages:
            if each_package == 9 and truck.current_time < 140:
                continue
            else:
                package_object = table.lookup(each_package)
                address_index = address_lookup(package_object.address)
                distance = get_distance(truck.current_location, address_index)
                if distance < shortest_distance:
                    shortest_distance = distance
                    best_address = package_object.address
                    best_address_index = address_index

        # Update mileage, location, and elapsed time for the selected delivery stop.
        time = (shortest_distance / 18) * 60
        truck.miles += shortest_distance
        truck.current_location = best_address_index
        truck.current_time += time

        remove_list = []
        # Deliver all eligible packages assigned to the selected address.
        for each_package in truck.packages:

            package_object = table.lookup(each_package)

            # Apply Package 9's corrected address once it becomes available.
            if package_object.package_id == 9:
                if truck.current_time < 140:
                    continue
                else:
                    package_object.address = "410 S State St"


            if package_object.address == best_address:
                    package_object.status = "delivered"
                    package_object.delivery_time = truck.current_time
                    remove_list.append(each_package)

        # Remove delivered packages from the truck's remaining workload.
        for each_package in remove_list:
            truck.packages.remove(each_package)


# Returns a package's delivery status at the requested time.
# Runtime: O(1) | Space: O(1)
def status(package_id, query_time):
    package_object = table.lookup(package_id)
    delivery_time = minutes_to_timestamp(package_object.delivery_time)
    if query_time < DELAYED_TIME and package_id in DELAYED_PACKAGES:
        return "Delayed"
    elif query_time < package_object.departure_time:
        return "At Hub"
    elif query_time < package_object.delivery_time:
        return "En Route"
    else:
        return f"Delivered at {delivery_time}"

# Displays package details and delivery status for a requested time.
# Runtime: O(1) | Space: O(1)
def display_package(package_object, time_in_hours_minutes):
    time_in_minutes = timestamp_to_minutes(time_in_hours_minutes)
    package_status = status(package_object.package_id, time_in_minutes)
    departure_time = minutes_to_timestamp(package_object.departure_time)
    if package_object.package_id == 9:
        if time_in_minutes < 140:
            package_object.address = "300 State St"
    if package_status == "At Hub":
        print(
            f"Package {package_object.package_id:<5} | Truck: {package_object.truck_id:<5} | {package_object.address:<40} | {package_object.city:<20} | {package_object.zip_code:<8} | "
            f"Departure time: {"n/a":<12} | Deadline: {package_object.deadline:<12} Status: {package_status:<10}")
    else:
        print(
             f"Package {package_object.package_id:<5} | Truck: {package_object.truck_id:<5} | {package_object.address:<40} | {package_object.city:<20} | {package_object.zip_code:<8} | "
             f"Departure time: {departure_time:<12} | Deadline: {package_object.deadline:<12} Status: {package_status:<10}")

# Converts a 12-hour timestamp into minutes elapsed since 8:00 AM.
# Runtime: O(1) | Space: O(1)
def timestamp_to_minutes(string_time):
    string_time = string_time.lower()
    parsed = re.split(r'[:\s]', string_time)

    if parsed[2] == "am" and parsed[0] == "12":
        parsed[0] = 0
    minutes = int(parsed[0]) * 60
    if parsed[2] == "pm":
        minutes += 720
    minutes += int(parsed[1])
    minutes -= 480
    return minutes

# Converts minutes elapsed since 8:00 AM into a readable 12-hour timestamp.
# Runtime: O(1) | Space: O(1)
def minutes_to_timestamp(number):
    total_minutes = int(round(number + 480))
    hour = total_minutes // 60
    minute = total_minutes % 60
    if hour >= 12:
        sign = "PM"
    else:
        sign = "AM"
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12
    return f"{hour}:{minute:02} {sign}"

# Provides a CLI for querying one package or all packages at a specified time.
# Runtime: O(n) | Space: O(1)
def package_lookup():
    lookup_choice = input("Press 1 to look up a single package\n"
                          "Press 2 to look up all packages ")

    timestamp = input("Enter time in format: hh:mm am/pm (e.g. 2:00 pm) ")

    if lookup_choice == "1":
        package_id_choice = int(input("Enter package ID: "))
        package_choice = table.lookup(package_id_choice)
        display_package(package_choice, timestamp)

    elif lookup_choice == "2":
        for package in range(1, 41):
            this_package = table.lookup(package)
            display_package(this_package, timestamp)
    else:
        print("Invalid input")


# Store package records in the custom hash table.

table = HashTable()


# Load package data from CSV and insert each package into the hash table.
with open ("package.csv") as file:

    reader = csv.reader(file)

    next(reader)

    for row in reader:
        package = Package(
            int(row[0].strip()),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )

        table.insert(package.package_id, package)

# Load the delivery distance matrix from CSV.
distances = []
with open("distances_v2.csv") as file:
    reader = csv.reader(file)

    for row in reader:
        distance_row = []
        for value in row:

            if value == "":
                distance_row.append(None)
            else:
                distance_row.append(float(value))
        distances.append(distance_row)

# Create the delivery fleet and assign packages to each truck.
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)
truck1_list = [1,13,14,15,16,19,20,29,30,31,34,37,40]
truck2_list = [3,6,18,25,28,32,33,35,36,38,39]
truck3_list = [2,4,5,7,8,9,10,11,12,17,21,22,23,24,26,27]
truck1.load(truck1_list, table)
truck2.load(truck2_list, table)
truck3.load(truck3_list, table)


# Run each truck's route according to its departure constraints.
# Truck 2 departs at 9:05 AM, and Truck 3 departs when Truck 1 returns.
truck_delivery_algorithm(truck1)
truck2.current_time = 65
truck_delivery_algorithm(truck2)
truck3.current_time = truck1.current_time
truck3.departure_time = truck1.current_time
truck_delivery_algorithm(truck3)


print(f'Truck 1 miles {truck1.miles}')
print(f'Truck 2 miles {truck2.miles}')
print(f'Truck 3 miles {truck3.miles}')
total_miles = truck1.miles + truck2.miles + truck3.miles
print(f"Total miles: {total_miles}")

# Start the interactive package-status lookup.
package_lookup()




