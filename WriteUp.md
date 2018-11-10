I'm storing the state of the city in a class, which in turn instantiates a car class when an instance of it is created.

The instance of a city maintains a list of destinations, consisting of all the locations of people waiting for pickup and all the locations current passengers wish to be dropped off at.

It determines the closest destination compared to the current location of the car object on each time step. However, it doesn't blindly go to the nearest destination. Instead, it assigns weights to each destination based on how close it is to other destinations on our list. If it finds a cluster of destinations that are all near each other and less than half of the map away, it will prefer them to nearer locations.

I decided to do it this way because it seemed like it would be more efficient to maximize speed for the greatest number of people. However, doing so blindly could result in ridiculously long wait for friends of mine who never happened to be going near/coming from a cluster of other people. Ideally, checking that the cluster isn't significantly farther away than solitary individuals will help prevent bias against them in the algorithm.
