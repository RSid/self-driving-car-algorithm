import itertools
from operator import attrgetter
from utils import Utils
from car import Car
from passenger import Passenger
from destination import Destination

class CityState:
    def __init__(self, x, y):
        self.max_rows = x
        self.max_columns = y
        self.car = Car(0,0)

    def get_locations_to_go(self):
        dropoffs = [passenger.dropoff for passenger in self.car.passengers]
        pickups = [person.pickup for person in self.car.pickup_requests]
        destinations = dropoffs + pickups
        return destinations

    def build_destinations(self, locations_to_go):
        destinations = [Destination(location, Utils.get_taxicab_distance(location, self.car.get_location())) for location in locations_to_go]
        return destinations

    def get_next_destination(self):
        locations_to_go = self.get_locations_to_go()
        if locations_to_go:
            destinations = self.build_destinations(locations_to_go)
            closest_to_car = min(destinations, key=attrgetter('distance_from_car'))
            [destination.build_cluster_weight(destinations, closest_to_car.distance_from_car) for destination in destinations]

            if any(weighted_dest.cluster_weight > 0 for weighted_dest in destinations):
                if (closest_to_car.distance_from_car < max(int(.5 * self.max_rows), int(.5 * self.max_columns))):
                    destinations = [destination for destination in destinations if destination.distance_from_car <= closest_to_car.distance_from_car]
                densest_cluster = max(destinations, key=attrgetter('cluster_weight'))
                return densest_cluster
            else:
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
