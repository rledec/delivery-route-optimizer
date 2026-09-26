import csv
from hash_table import HashTable
from package import Package
from address import addresses
from truck import Truck
import re

DELAYED_PACKAGES = {6, 25, 28, 32}
DELAYED_TIME = 65


# This function returns a float point value which represents the distance in miles between two addresses
# of the WGUPS route.  Each address is represented by an index number; get_distance takes two indexes
# as arguments and calculates the distance based on the values of distances.csv which are stored in the distances list
# distances.csv is a triangular matrix.  The same address list is in the column and the row creating symmetry.
# Because of this symmetry, each distance is only stored once to avoid redundancy.  This function
# checks to make sure that if they are not stored in this index pair, to find the value in its symmetric pair.
# And then return it.
# Big O Runtime: O(1)
# Big O Space Complexity: O(1)
def get_distance(i, j):
    if distances[i][j] is not None:
        return distances[i][j]
    else:
        return distances[j][i]

#This function takes in the string value of its function as an argument and returns the index value associated to it
#The index value is simply based on the order of addresses in the address list, from 0 to 39
# Big O Runtime: O(n)
# Big O Space Complexity: O(1)
def address_lookup(address_string):

    return addresses.index(address_string)

# This function contains the algorithm to get the packages delivered in the least mileage possible.  It uses a variant
# of the nearest-neighbor algorithm to solve it.  It takes in a truck as an argument, decides which package to deliver
# first based on the closest distance to the hub, and from there delivers each package based on the nearest address
# from its current address.  If there are multiple packages that need to be delivered at one address, it will deliver
# all packages to that address before moving onto the next address.
# Big O Runtime: O(n^2)
# Big O Space Complexity: O(n)
def truck_delivery_algorithm(truck):
    # This for loop goes through every package object referenced in that truck.packages list
    # and updates each package departure time to the current time of the truck
    for each in truck.packages:
        package_object = table.lookup(each)
        package_object.departure_time = truck.current_time

    #This while loop runs until every package on truck.packages is removed(delivered)
    while truck.packages:

        # This if statement checks to make sure that truck.packages[0] is not package 9, and if it is package 9
        # to check and make sure that the current time is not before 10:20 am, since the correct address will not
        # be known until that time.  140 represents 140 minutes from 8:00 am, which would equal 10:20 am.  If the if
        # statement is true, it will check to see if package 9 is the last package on the truck.  If it's the last
        # package, the clock will be sped up to 10:20 so the package can be delivered.  If it is not the last package,
        # then it will switch to the next package still on the list.
        if truck.packages[0] == 9 and truck.current_time < 140:
            if len(truck.packages) < 2:
                truck.current_time = 140
                continue
            else:
                first_package = table.lookup(truck.packages[1])
        else:
            first_package = table.lookup(truck.packages[0])





        # The following lines of code apply the nearest-neighbor algorithm to decide which
        # package should be delivered first based on nearest distance from its
        # current location.  It uses the get_distance function to find out the distance from its
        # current location to the first package on the trucks.packages list and stores that address in best_address,
        # as well as that distance value in shortest_distance
        best_address = first_package.address
        best_address_index = address_lookup(best_address)
        shortest_distance = get_distance(truck.current_location, best_address_index)

        # This for-loop will go through each package on the truck.package list.  It will compare the address distance
        # of all the packages with the address distance for the value of best_address.  If a distance value is found
        # with a lower value than shortest_distance, it will update shortest_distance with that distance value
        # and best_address, as well as best_address to the address associated with that distance.
        # Once this for-loop is done, shortest_distance will have the lowest distance value, and that will be
        # the address the truck will go to next
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

        # This block of code discovers the time that has elapsed since driving from its current address to the new
        # address.  Since the truck is going 18 miles an hour, time is found by dividing the distance by 18 and then
        # multiplying it by 60 to convert to minutes.  Next, the distance traveled is added to the truck's mileage.
        # the truck's current location is updated to the index of the address it traveled to.  And the time of the
        # truck is updated to reflect the current time after delivering those packages
        time = (shortest_distance / 18) * 60
        truck.miles += shortest_distance
        truck.current_location = best_address_index
        truck.current_time += time

        remove_list = []
        # Checks for all packages with the same address of the current location.  And delivers all of them, except
        # Package nine if it is before 10:20 am.  It will change the package's status to delivered, set the delivery_time
        # With truck.current_time, and add each delivered package to a remove_list.
        for each_package in truck.packages:

            package_object = table.lookup(each_package)

            # This if statement will update the address for package nine if the time is 10:20 am or later
            if package_object.package_id == 9:
                if truck.current_time < 140:
                    continue
                else:
                    package_object.address = "410 S State St"


            if package_object.address == best_address:
                    package_object.status = "delivered"
                    package_object.delivery_time = truck.current_time
                    remove_list.append(each_package)

        #This for-loop removes every pacakge on the remove_list from the truck.packages list.
        for each_package in remove_list:
            truck.packages.remove(each_package)


# This function will give the delivery status of a package at a given time.  It will compare the query_time passed
# As an argument with the package's delivery time and departure time.  It will return it's status based on these
# Comparisons.  If the pacakge status if sound to be delivered, it will also give the delivery_time for that package
# Big O Runtime: O(1)
# Big O Space Complexity: O(1)
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

# This function prints package information, useful for CLI prompts.  It uses the timestamp_to_minutes function to
# Print the time in hours:minutes format to be more readable to the user
# Big O Runtime: O(1)
# Big O Space Complexity: O(1)
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

# This function converts hours:minutes format to minutes; it is used for user input, which is expected to be in
# hours:minutes format, and convert it to minutes format which is how the Truck class and truck_delivery_algorithm
# read time.  This is accomplished by parsing the string input, and converting into minutes from 8:00 am
# Big O Runtime: O(1)
# Big O Space Complexity: O(1)
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

# This function converts time in minutes to hours:minutes format.  This function is used to convert time into a readable
# format for the user.  It is accomplished by adding 480 to the minute value passed as an argument.  This is done
# because 480 is the amount of minutes from 12:00 am to 8:00 am.  Once it's converted into minutes from midnight, it is
# then converted into the correct hour and minutes using division and modulation.  Once the hour is discovered, the
# AM/PM is added based on if the hours is over 12.
# Big O Runtime: O(1)
# Big O Space Complexity: O(1)
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

# This function provides a CLI for a user to look up the package status
# based on a certain time.  The user is able to either select the package status of
# a single package or every package at once.
# Big O Runtime: O(n)
# Big O Space Complexity: O(1)
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


# Hash table object is created from the HashTable() class.  This table will hold all the packages from package.csv

table = HashTable()


# This code opens the package.csv file.  It goes through each row, and adds all the contents of that row to a package
# object.  Then it adds the package to the hash table.
with open ("package.csv") as file:
    # Turns the file into an object that can be looped through row by row
    reader = csv.reader(file)
    # Skips the first row
    next(reader)
    #Builds a package with the contents of each row
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
        # Adds the package into the hash table
        table.insert(package.package_id, package)

# This following code creates a two-dimensional list called distances, and populates it with the contents in the
# distances.csv file
distances = []
with open("distances_v2.csv") as file:
    reader = csv.reader(file)

    for row in reader:
        distance_row = []
        for value in row:
            # value = value.strip("\ufeff")
            if value == "":
                distance_row.append(None)
            else:
                distance_row.append(float(value))
        distances.append(distance_row)

# The following code creates the truck objects for each truck that exists for this assignment.  It then fills the
# Trucks with the packages assigned to each truck.
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)
truck1_list = [1,13,14,15,16,19,20,29,30,31,34,37,40]
truck2_list = [3,6,18,25,28,32,33,35,36,38,39]
truck3_list = [2,4,5,7,8,9,10,11,12,17,21,22,23,24,26,27]
truck1.load(truck1_list, table)
truck2.load(truck2_list, table)
truck3.load(truck3_list, table)


# This following block of code runs the delivery algorithm on truck1.  It then sets the time of truck2 to 65 which
# translates to 9:05 am.  This is because truck2 contains the packages that won't arrive from the airport to the
# hub until 9:05 am.  Then the delivery algorithm is run on truck2.  Next, the departure time of truck3 is set to the
# current time of truck1, since truck3 will leave once truck 3 gets back. After the time is set for truck 3, the
# truck_delivery_algorithm is run on it
truck_delivery_algorithm(truck1)
truck2.current_time = 65
truck_delivery_algorithm(truck2)
truck3.current_time = truck1.current_time
truck3.departure_time = truck1.current_time
truck_delivery_algorithm(truck3)


# print(f"Truck1 current time: {minutes_to_timestamp(truck1.current_time)}")
# print(f"Truck2 current time: {minutes_to_timestamp(truck2.current_time)}")

print(f'Truck 1 miles {truck1.miles}')
print(f'Truck 2 miles {truck2.miles}')
print(f'Truck 3 miles {truck3.miles}')
total_miles = truck1.miles + truck2.miles + truck3.miles
print(f"Total miles: {total_miles}")

# Calls package_lookup to provide a CLI for the user to look up the package status
# At a given time
package_lookup()




