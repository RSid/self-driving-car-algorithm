#How to run
You can test out my solution by importing the CityState class from rideshare.py. You can then create a new 10 x 10 city like so:

`city = CityState(10, 10)`

You can then increment a time step and make requests like so:

`city.increment_time([{'name' : 'George', 'start' : (1,2), 'end' : (4,3)}])`

Alternately, you can run the automated test suite by running `python tests.py`


#Solution writeup
I'm storing the state of the city in a class, which in turn instantiates a car class located at the map origin and an empty request queue when created. Given that you mentioned the request json could be infinite, I did add some handling that will put requests into a queue if there are so many that it would substantially slow processing. Requests in the queue are handled in order during subsequent time steps.

At each time step, the city aggregates a list of all the places the car needs to go in order to pick people up and drop them off. It uses the dbscan algorithm to find clusters of destinations. It then takes the size of each cluster and the distance of the closest point in the cluster to the car and normalizes them, so that they can be added together to provide an overall weight for the cluster. The car's next destination will be the closest destination in the cluster with the highest weight. I tried a couple of clustering algorithms, but dbscan with an epsilon equal to 1% of the average map shape seemed to produce results most in line with my expectations.

I decided the distance of clusters and their size were the most important factors in prioritizing where the car should go next because they seemed like the easiest way to efficiently make a large number of people happy.
