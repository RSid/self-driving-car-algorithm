class Utils:
    @staticmethod
    def stringified_list_of_names(people):
        return ', '.join([person.name for person in people])

    @staticmethod
    def get_taxicab_distance(location_one, location_two):
        return abs(location_one[0] - location_two[0]) + abs(location_one[1] - location_two[1])
