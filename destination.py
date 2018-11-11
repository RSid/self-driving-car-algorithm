class Destination:
    def __init__(self, location, distance_from_car, cluster_label):
        self.location = location
        self.distance_from_car = distance_from_car
        self.cluster_label = cluster_label

    def __eq__(self, other):
        return self.location == other.location and self.distance_from_car == other.distance_from_car
