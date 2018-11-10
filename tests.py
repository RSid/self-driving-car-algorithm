import unittest
import time
from rideshare import CityState
from rideshare import Passenger
from rideshare import Destination
import sys

class TestRideshareInitialization(unittest.TestCase):

    def test_city_state(self):
        #GIVEN a city that was instantiated as 2 x2
        city = CityState(2,2)

        #WHEN I get its car location
        car_location = city.car.get_location()

        #THEN I get the origin
        expected_location = (0,0)
        self.assertEqual(car_location, expected_location)


class TestSimpleRideshareScenarios(unittest.TestCase):
    def test_nothing_to_do(self):
        #GIVEN no requests
        city_state = CityState(8,8)
        request = []

        #WHEN I increment time
        city_state.increment_time(request)

        #THEN the state does not change
        self.assertEqual(city_state.car.get_location(), (0,0))
        self.assertEqual(city_state.get_next_destination(), Destination((0,0), 0))
        print('END SCENARIO')

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
        print('END SCENARIO')

    def test_drops_off_passenger(self):
        #GIVEN a single rideshare passenger
        city_state = CityState(8,8)
        request = [{'name' : 'Hieronymous', 'start' : (1,0), 'end' : (1,2)}]
        city_state.increment_time(request)
        city_state.increment_time([])

        #WHEN I increment time the expected amount
        city_state.increment_time([])

        #THEN the passenger is picked up
        self.assertEqual(city_state.car.get_location(), (1,2))
        self.assertTrue(len(city_state.car.passengers) == 0)
        print('END SCENARIO')


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
        print('END SCENARIO')

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
        print('END SCENARIO')

    def test_provided_example(self):
        #GIVEN 2 requests
        city_state = CityState(10, 10)
        request = [{'name' : 'Elon', 'start' : (3,5), 'end' : (8,7)},
                   {'name' : 'George', 'start' : (1,2), 'end' : (4,3)}]

        #WHEN I increment time the expected amount with no new requests
        city_state.increment_time(request)

        #THEN the passengers are picked up and dropped off at the points I expect
        time_increments_required = 0
        while(city_state.car.passengers or city_state.car.pickup_requests):
            city_state.increment_time([])
            time_increments_required +=1

        self.assertEqual(time_increments_required, 16)
        print('END SCENARIO')

class TestComplexRideshareScenarios(unittest.TestCase):
    def test_multiple_requests(self):
        #GIVEN an initial set of requests
        city_state = CityState(8,8)
        request = [{'name' : 'Elon', 'start' : (3,5), 'end' : (8,7)},
                   {'name' : 'George', 'start' : (1,2), 'end' : (4,3)}]
        city_state.increment_time(request)

        #WHEN I add more requests as I increment time

        #THEN they are taken into account
        time_increments_required = 0
        while(city_state.car.passengers or city_state.car.pickup_requests):
            if(time_increments_required == 5):
                city_state.increment_time([{'name' : 'Hieronymous', 'start' : (1,0), 'end' : (6,2)}])
            else:
                city_state.increment_time([])
            time_increments_required +=1

        self.assertEqual(time_increments_required, 37)
        print('END SCENARIO')

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
        print('END SCENARIO')

    def test_prefer_dense_clusters_to_closer_locales(self):
        #GIVEN a set of requests, 1 of which is close and 2 of which are far but near each other
        city_state = CityState(50,50)
        close_person = {'name' : 'McCavity', 'start' : (10,10), 'end' : (10,10)}
        request = [close_person,
                   {'name' : 'Ishmael', 'start' : (15,4), 'end' : (4,3)},
                   {'name' : 'Mieville', 'start' : (15,5), 'end' : (8,7)}]

        #WHEN I decide which destination to choose
        city_state.increment_time(request)

        #THEN it is in the dense cluster even though it's further away
        next_destination = city_state.get_next_destination()
        self.assertEqual(next_destination.location, (15,4))

    def test_prefer_closer_locales_if_densest_cluster_is_far(self):
        #GIVEN a set of requests, 1 of which is close and 2 of which are very comparatively far, but near each other
        city_state = CityState(100,100)
        close_person = {'name' : 'McCavity', 'start' : (1,2), 'end' : (10,10)}
        request = [close_person,
                   {'name' : 'Ishmael', 'start' : (100,5), 'end' : (4,3)},
                   {'name' : 'Mieville', 'start' : (100,6), 'end' : (8,7)}]

        #WHEN I decide which destination to choose
        city_state.increment_time(request)

        #THEN it is in the dense cluster even though it's further away
        next_destination = city_state.get_next_destination()
        self.assertEqual(next_destination.location, (1,2))

if __name__ == '__main__':
    unittest.main()
