class Passenger:
    def __init__(self, json):
        self.name = json['name']
        self.pickup = json['start']
        self.dropoff = json['end']

    def __eq__(self, other):
        return self.name == other.name and self.pickup == other.pickup and self.dropoff == other.dropoff
