from utils import Utils

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
