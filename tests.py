import unittest
from rideshare import CityState

class TestRideshareInitialization(unittest.TestCase):

    def test_city_state(self):
        #GIVEN a city that was instantiated as 2 x2
        city = CityState(2,2)

        #WHEN I get its grid
        city_grid = city.get_grid()

        #THEN I get the shape I expect
        expected_graph = [(0,0), (0,1), (1,0), (1,1)]
        self.assertEqual(city_grid, expected_graph)

class TestRideshareScenarios(unittest.TestCase):
    def setUp(self):
        self.city_state = CityState(8,8)

    def test_nothing_to_do(self):
        #GIVEN no requests
        request = []

        #WHEN I increment time
        self.city_state.increment_time(request)

        #THEN the state does not change
        self.assertEqual(self.city_state.car.get_location(), (0,0))

if __name__ == '__main__':
    unittest.main()
