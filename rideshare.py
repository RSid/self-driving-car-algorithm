import itertools
from operator import attrgetter

class Utils:
    @staticmethod
    def stringified_list_of_names(people):
        return ', '.join([person.name for person in people])

class Car:
    def __init__(self, x, y):
        self.x_loc = x
        self.y_loc = y
        self.passengers = []
        self.pickup_requests = []

    def alter_x_loc(self, delta):
        self.x_loc = self.x_loc + delta

    def alter_y_loc(self, delta):
        self.y_loc = self.y_loc + delta

    def distance_to_movement(self, distance):
        if distance > 0:
            return 1
        elif distance <0:
            return -1
        else:
            return 0

    def move(self, destination):
        if destination == self.get_location():
            return
        if destination[0] == self.x_loc:
            distance = destination[1] - self.y_loc
            delta = self.distance_to_movement(distance)
            self.alter_y_loc(delta)
        else:
            distance = destination[0] - self.x_loc
            delta = self.distance_to_movement(distance)
            self.alter_x_loc(delta)

    def get_location(self):
        return (self.x_loc, self.y_loc)

    def show_location(self):
        print('Car located at: ' + str(self.x_loc) + "," + str(self.y_loc))

    def do_pickups(self):
        passengers_available_for_pickup = [person for person in self.pickup_requests if person.pickup == self.get_location()]
        if passengers_available_for_pickup:
            print('Passengers picked up: ' + Utils.stringified_list_of_names(passengers_available_for_pickup))
        self.passengers.extend(passengers_available_for_pickup)
        self.pickup_requests = [person for person in self.pickup_requests if person not in self.passengers]

    def do_dropoffs(self):
        passengers_at_destination = [passenger for passenger in self.passengers if passenger.dropoff == self.get_location()]
        if passengers_at_destination:
            print('Passengers dropped off: ' + Utils.stringified_list_of_names(passengers_at_destination))
        self.passengers = [passenger for passenger in self.passengers if passenger not in passengers_at_destination]

    def print_status(self):
        self.show_location()
        if self.passengers:
            print('Riding: ' + Utils.stringified_list_of_names(self.passengers))

class Passenger:
    def __init__(self, json):
        self.name = json['name']
        self.pickup = json['start']
        self.dropoff = json['end']

    def __eq__(self, other):
        return self.name == other.name and self.pickup == other.pickup and self.dropoff == other.dropoff

class Destination:
    def __init__(self, location, distance_from_car):
        self.location = location
        self.distance_from_car = distance_from_car
        self.cluster_weight = 0

    def __eq__(self, other):
        return self.location == other.location and self.distance_from_car == other.distance_from_car and self.cluster_weight == other.cluster_weight

class CityState:
    def __init__(self, x, y):
        self.max_rows = x
        self.max_columns = y
        self.car = Car(0,0)

    def get_taxicab_distance(self, destination, car_location):
        return abs(destination[0] - car_location[0]) + abs(destination[1] - car_location[1])

    def get_locations_to_go(self):
        dropoffs = [passenger.dropoff for passenger in self.car.passengers]
        pickups = [person.pickup for person in self.car.pickup_requests]
        destinations = dropoffs + pickups
        return destinations

    def build_destinations(self, locations_to_go):
        destinations = [Destination(location, self.get_taxicab_distance(location, self.car.get_location())) for location in locations_to_go]
        return destinations

    def get_next_destination(self):
        locations_to_go = self.get_locations_to_go()
        if locations_to_go:
            destinations = self.build_destinations(locations_to_go)
            closest_to_car = min(destinations, key=attrgetter('distance_from_car'))
            return closest_to_car
        else:
            return Destination(self.car.get_location(), 0)

    def increment_time(self, requestJson):
        if  requestJson:
            new_pickups = [Passenger(person) for person in requestJson]
            self.car.pickup_requests.extend(new_pickups)
        next_destination = self.get_next_destination()
        self.car.move(next_destination.location)
        self.car.do_pickups()
        self.car.do_dropoffs()
        self.car.print_status()
