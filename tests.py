import unittest
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

if __name__ == '__main__':
    unittest.main()
