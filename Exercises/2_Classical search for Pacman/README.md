# Exercise on search algorithms
Note: solution code not provided as per license.)

## The Pacman project

In this exercise, I completed the methods of a `genericSearch` function that is used by Pacman via a `SearchAgent` class. 
This generic search algorithm takes a `PositionSearchProblem` and a queueing strategy and performs a search given that strategy.
These strategies are of course well-known search algorithms. They are implemented as separate functions that are used by `genericSearch`.

## Strategies implementation:

### Stack: a LIFO (Last In First Out) list:
* depthFirstSearch(problem): the set of candidates consist of the descendant positions of a chosen root node child.

### Queue: a FIFO (First In First Out) list:
* breadthFirstSearch(problem): the set of candidates consist of the positions/nodes at the same level, e.g. one hop away.

### PriorityQueue: popped item at start or end of queue depending on heuristic:
* aStarSearch(problem, heuristic): A* improves breadthFirstSearch by deciding with other position to consider based on some heuristic, e.g. remaining distance to goal.
* uniformCostSearch(problem): implemented as A* search without heuristic.


## Heuristics:
For a search position problem, the heuristics and metrics that are likely to be a function of distance and it is the case here.

* ManhattanDistance: measures the length of a path consisting of horizontal and vertical segments.
* EuclidianDistance: measures of distance "as the crow flies".
