# Interview puzzle solution
Prompt was to build an algorithm for an autonomous vehicle for a ride sharing company. The problem space was simplified to a finite, grid-shaped city, 
and a situation in which the car could only move 1 block at a time and we only cared about its position at the vertecies in the grid. Requests at each 
timestep would be json that looked like this: `[{'name': 'Fred','start': (3,5),'end': (8,7)}, {'name': 'Fred','start': (6,1),'end': (10,2)}]`
