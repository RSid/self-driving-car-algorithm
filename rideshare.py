import itertools
from operator import itemgetter
from operator import attrgetter
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from utils import Utils
from car import Car
from passenger import Passenger
from destination import Destination
from cluster import Cluster

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

    def build_clusters(self, locations_to_go):
        avg_map_size = (self.max_rows + self.max_columns)/2
        epsilon = int(round(.10 * avg_map_size))
        clustering = DBSCAN(eps=epsilon, min_samples=2).fit(locations_to_go)
        locations_with_cluster_labels = []
        for index, location in enumerate(locations_to_go):
            if index in clustering.core_sample_indices_:
                labeled_location = (location, clustering.labels_[index])
            else:
                labeled_location = (location, None)
            locations_with_cluster_labels.append(labeled_location)
        groups = itertools.groupby(locations_with_cluster_labels, itemgetter(1))
        clusters = [Cluster(key, self.build_destinations(list(value))) for key, value in groups]

        normalized_cluster_sizes = preprocessing.scale([cluster.size for cluster in clusters])
        normalized_cluster_distances = preprocessing.scale([cluster.destination_closest_to_car.distance_from_car for cluster in clusters])
        for index, cluster in enumerate(clusters):
            cluster.set_weight(normalized_cluster_sizes[index], normalized_cluster_distances[index])
        return clusters

    def build_destinations(self, clustered_locations):
        destinations = [Destination(clustered_location[0], Utils.get_taxicab_distance(clustered_location[0], self.car.get_location()), clustered_location[1]) for clustered_location in clustered_locations]
        return destinations

    def get_next_destination(self):
        locations_to_go = self.get_locations_to_go()
        if locations_to_go:
            clusters = self.build_clusters(locations_to_go)
            selected_cluster = max(clusters, key=attrgetter('weight'))
            return selected_cluster.destination_closest_to_car
        return Destination(self.car.get_location(), 0, None)

    def increment_time(self, requestJson):
        if  requestJson:
            new_pickups = [Passenger(person) for person in requestJson]
            self.car.pickup_requests.extend(new_pickups)
        next_destination = self.get_next_destination()
        print(next_destination.location)
        self.car.move(next_destination.location)
        self.car.do_pickups()
        self.car.do_dropoffs()
        self.car.print_status()
