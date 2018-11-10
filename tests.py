import unittest
import time
from rideshare import CityState
from rideshare import Passenger

class TestRideshareInitialization(unittest.TestCase):

    def test_city_state(self):
        #GIVEN a city that was instantiated as 2 x2
        city = CityState(2,2)

        #WHEN I get its grid
        city_grid = city.get_grid()

        #THEN I get the shape I expect
        expected_graph = [(0,0), (0,1), (1,0), (1,1)]
        self.assertEqual(city_grid, expected_graph)

    def test_cannot_instantiate_too_slow(self):
        #GIVEN a huge city
        city_start = time.time()

        #WHEN I instantiate it
        city_state = CityState(5000, 5000)

        #THEN it cannot take forever
        elapsed = time.time() - city_start
        self.assertTrue(elapsed < 3)
        print('END SCENARIO')

class TestSimpleRideshareScenarios(unittest.TestCase):
    def test_nothing_to_do(self):
        #GIVEN no requests
        city_state = CityState(8,8)
        request = []

        #WHEN I increment time
        city_state.increment_time(request)

        #THEN the state does not change
        self.assertEqual(city_state.car.get_location(), (0,0))
        self.assertEqual(city_state.get_closest_destination(), ((0,0), 0))
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

    def test_provided_example(self):
        #GIVEN 2 requests
        city_state = CityState(8,8)
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

    def test_cannot_run_too_slow(self):
        #GIVEN a huge city
        city_state = CityState(10000, 10000)

        request = [{'name' : 'Elon', 'start' : (335,27), 'end' : (1500,7)},
                   {'name' : 'George', 'start' : (50,2), 'end' : (4,400)}]
        city_state.increment_time(request)

        #WHEN I increment time
        start_time = time.time()
        city_state.increment_time(request)

        #THEN the method cannot take forever
        elapsed = time.time() - start_time
        print('Elapsed time increment:')
        print(elapsed)
        self.assertTrue(elapsed < 0.1)
        print('END SCENARIO')

if __name__ == '__main__':
    unittest.main()
