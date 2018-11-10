from utils import Utils

class Destination:
    def __init__(self, location, distance_from_car):
        self.location = location
        self.distance_from_car = distance_from_car
        self.cluster_weight = 0


    def build_cluster_weight(self, destinations, closest_location_distance):
        distance_to_neighbors = [Utils.get_taxicab_distance(neighbor.location, self.location) for neighbor in destinations if neighbor.location != self.location]
        #let's say locations are clustered 'close' if they're closer to each other
        #than the otherwise nearest location is to the car
        close_neighbors = [neighbor_distance for neighbor_distance in distance_to_neighbors if neighbor_distance <= closest_location_distance]
        if close_neighbors:
            self.cluster_weight = len(close_neighbors)

    def __eq__(self, other):
        return self.location == other.location and self.distance_from_car == other.distance_from_car and self.cluster_weight == other.cluster_weight
