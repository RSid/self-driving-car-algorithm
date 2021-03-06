import unittest
import time
from rideshare import CityState
from rideshare import Passenger
from rideshare import Destination
import sys
from ddt import ddt, data, unpack

class TestRideshareInitialization(unittest.TestCase):

    def test_city_state(self):
        #GIVEN a new city
        city = CityState(2,2)

        #WHEN I get its car location
        car_location = city.car.get_location()

        #THEN I get the origin
        expected_location = (0,0)
        self.assertEqual(car_location, expected_location)


class TestSimpleRideshareScenarios(unittest.TestCase):
    def test_nothing_to_do(self):
        #GIVEN no requests and no passengers
        city_state = CityState(8,8)
        request = []

        #WHEN I increment time
        city_state.increment_time(request)

        #THEN the next destination does not change
        self.assertEqual(city_state.car.get_location(), (0,0))
        self.assertEqual(city_state.get_next_destination(), Destination((0,0), 0, None))

    def test_picks_up_passenger(self):
        #GIVEN a single rideshare request
        city_state = CityState(8,8)
        request = [{'name' : 'Hieronymous', 'start' : (1,0), 'end' : (1,2)}]

        #WHEN I increment time the expected amount
        city_state.increment_time(request)
        city_state.increment_time([])

        #THEN the passenger is picked up
        self.assertEqual(city_state.car.get_location(), (1,1))
        self.assertEqual(city_state.car.passengers, [Passenger(request[0])])

    def test_drops_off_passenger(self):
        #GIVEN a single rideshare passenger
        city_state = CityState(8,8)
        request = [{'name' : 'Hieronymous', 'start' : (1,0), 'end' : (1,2)}]
        city_state.increment_time(request)
        city_state.increment_time([])

        #WHEN I increment time the expected amount
        city_state.increment_time([])

        #THEN the passenger is droppped off
        self.assertEqual(city_state.car.get_location(), (1,2))
        self.assertTrue(len(city_state.car.passengers) == 0)


    def test_picks_closest_location(self):
        #GIVEN 2 requests
        city_state = CityState(8,8)
        first_pickup = {'name' : 'George', 'start' : (1,2), 'end' : (4,3)}
        request = [{'name' : 'Elon', 'start' : (3,5), 'end' : (8,7)},
                   first_pickup]

        #WHEN I increment time the expected amount with no new requests
        city_state.increment_time(request)

        #THEN I pick up the closest passenger first
        city_state.increment_time([])
        city_state.increment_time([])
        self.assertEqual(city_state.car.passengers[0], Passenger(first_pickup))

        #THEN I drop them off because that's closer than the next pickup
        city_state.increment_time([])
        city_state.increment_time([])
        city_state.increment_time([])
        city_state.increment_time([])
        self.assertEqual(len(city_state.car.passengers), 0)

    def test_picks_closest_location_irrespective_of_type(self):
        #GIVEN 2 requests
        city_state = CityState(8,8)
        first_pickup = {'name' : 'George', 'start' : (1,2), 'end' : (3,5)}
        request = [{'name' : 'Elon', 'start' : (4,3), 'end' : (8,7)},
                   first_pickup]

        #WHEN I increment time the expected amount with no new requests
        city_state.increment_time(request)

        #THEN I pick up the closest passenger first
        city_state.increment_time([])
        city_state.increment_time([])
        self.assertEqual(city_state.car.passengers[0], Passenger(first_pickup))

        #THEN I pick up the next person, because that's closer than the next dropoff
        city_state.increment_time([])
        city_state.increment_time([])
        city_state.increment_time([])
        city_state.increment_time([])
        self.assertEqual(len(city_state.car.passengers), 2)

    def test_provided_example(self):
        #GIVEN 2 requests
        city_state = CityState(10, 10)
        request = [{'name' : 'Elon', 'start' : (3,5), 'end' : (8,7)},
                   {'name' : 'George', 'start' : (1,2), 'end' : (4,3)}]

        #WHEN I increment time the expected amount with no new requests
        city_state.increment_time(request)

        #THEN the passengers are picked up and dropped off at the points I expect
        #in the amount of time I expect
        time_increments_required = 0
        while(city_state.car.passengers or city_state.car.pickup_requests):
            city_state.increment_time([])
            time_increments_required +=1

        self.assertEqual(time_increments_required, 16)

    def test_multiple_requests(self):
        #GIVEN an initial set of requests
        city_state = CityState(8,8)
        request = [{'name' : 'Elon', 'start' : (3,5), 'end' : (8,7)},
                   {'name' : 'George', 'start' : (1,2), 'end' : (4,3)}]
        city_state.increment_time(request)

        #WHEN I add more requests as I increment time
        time_increments_required = 0
        while(city_state.car.passengers or city_state.car.pickup_requests):
            if(time_increments_required == 5):
                city_state.increment_time([{'name' : 'Hieronymous', 'start' : (1,0), 'end' : (6,2)}])
            else:
                city_state.increment_time([])
            time_increments_required +=1

        #THEN they are taken into account
        self.assertEqual(time_increments_required, 37)

    def test_large_lopsided_city(self):
        #GIVEN a large, lopsided city
        city_state = CityState(2000, 1000)
        request = [{'name' : 'Elon', 'start' : (335,27), 'end' : (1500,7)},
                   {'name' : 'George', 'start' : (50,2), 'end' : (4,400)}]
        city_state.increment_time(request)

        #WHEN I navigate through it
        time_increments_required = 0
        while(city_state.car.passengers or city_state.car.pickup_requests):
            city_state.increment_time([])
            time_increments_required +=1

        #THEN the algorithm still functions
        self.assertEqual(time_increments_required, 2954)

@ddt
class TestComplexRideshareScenarios(unittest.TestCase):
    def test_prefer_clusters_to_individuals(self):
        #GIVEN a set of requests, 1 of which is close and 2 of which are farther, but near each other
        city_state = CityState(50,50)
        close_person = {'name' : 'McCavity', 'start' : (10,10), 'end' : (10,11)}
        closest_cluster_location_start = (25,4)
        request = [close_person,
                   {'name' : 'Ishmael', 'start' : closest_cluster_location_start, 'end' : (4,3)},
                   {'name' : 'Mieville', 'start' : (25,5), 'end' : (8,7)}]

        #WHEN I decide which destination to choose
        city_state.increment_time(request)

        #THEN it is in the cluster even though it's further away
        next_destination = city_state.get_next_destination()
        self.assertEqual(next_destination.location, closest_cluster_location_start)

    def test_prefer_larger_clusters_to_smaller(self):
        #GIVEN a set of clustered requests, 1 of which is closer and 1 of which is farther, but larger
        city_state = CityState(50,50)
        individual = [{'name' : 'Queequeg', 'start' : (10,10), 'end' : (40,10)}]

        closer_cluster = [{'name' : 'McCavity', 'start' : (30,10), 'end' : (40,10)},
            {'name' : 'Mistoffoles', 'start' : (30,11), 'end' : (20,10)}]

        closest_large_cluster_location_start = (35,4)
        farther_larger_cluster = [{'name' : 'Ishmael', 'start' : closest_large_cluster_location_start, 'end' : (4,3)},
            {'name' : 'Mieville', 'start' : (35,5), 'end' : (8,17)},
            {'name' : 'Starbuck', 'start' : (35,6), 'end' : (30,7)}]

        request = individual + closer_cluster + farther_larger_cluster

        #WHEN I decide which destination to choose
        city_state.increment_time(request)

        #THEN it is in the larger cluster even though it's further away
        next_destination = city_state.get_next_destination()
        self.assertEqual(next_destination.location, closest_large_cluster_location_start)

    #Let's check that our city shape-derived value of epsilon still leads to good clustering
    #in lopsided & square cities alike
    @data((800, 800, 100, 500), (800, 5, 100, 400), (50, 1000, 60, 500))
    @unpack
    def test_prefer_close_small_cluster_if_larger_cluster_is_very_far(self, city_x, city_y, close_seed_value, far_seed_value):
        #GIVEN a set of clustered requests, 1 of which is close and 1 of which is very far
        city_state = CityState(city_x, city_y)
        dummy_end_locale = (8,8)
        individual = [{'name' : 'Queequeg', 'start' : (2,10), 'end' : (40,10)}]

        expected_next_destination = (close_seed_value, close_seed_value + 1)
        closer_cluster = [{'name' : 'McCavity', 'start' : expected_next_destination, 'end' : dummy_end_locale},
            {'name' : 'Mistoffoles', 'start' : (close_seed_value, close_seed_value + 2), 'end' : dummy_end_locale}]

        distant_large_cluster = [{'name' : 'Ishmael', 'start' : (far_seed_value + 1, city_y - 1), 'end' : dummy_end_locale},
            {'name' : 'Mieville', 'start' : (far_seed_value, city_y - 1), 'end' : dummy_end_locale},
            {'name' : 'Starbuck', 'start' : (far_seed_value + 2, city_y - 1), 'end' : dummy_end_locale}]

        request = individual + closer_cluster + distant_large_cluster

        #WHEN I decide which destination to choose
        city_state.increment_time(request)

        #THEN it is in the smaller cluster, even though a larger one exists
        next_destination = city_state.get_next_destination()
        self.assertEqual(next_destination.location, expected_next_destination)

    def test_cannot_run_too_slow(self):
          #GIVEN a huge city
          city_state = CityState(sys.maxsize, sys.maxsize)

          request = [{'name' : 'Person' + str(i), 'start' : (335,27), 'end' : (sys.maxsize, sys.maxsize)} for i in range(2000)]
          city_state.increment_time(request)

          #WHEN I increment time
          start_time = time.time()
          city_state.increment_time(request)

          #THEN the method cannot take forever
          elapsed = time.time() - start_time
          print('Elapsed time increment:')
          print(elapsed)
          self.assertTrue(elapsed < 0.5)

if __name__ == '__main__':
    unittest.main()
