from operator import attrgetter

class Cluster:
    def __init__(self, label, destinations):
        self.destinations = destinations
        self.destination_closest_to_car = min(destinations, key=attrgetter('distance_from_car'))
        self.label = label
        self.size = len(destinations)

    def set_weight(self, normalized_size_weight, normalized_distance_weight):
        self.weight = normalized_size_weight + normalized_distance_weight
