from copy import deepcopy
from queue import PriorityQueue
from Point import Point
import math

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''


class AIModule:

    def createPath(self, map_):
        pass


'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''


class StupidAI(AIModule):

    def createPath(self, map_):
        path = []
        explored = []
        # Get starting point
        path.append(map_.start)
        current_point = deepcopy(map_.start)

        # Keep moving horizontally until we match the target
        while (current_point.x != map_.goal.x):
            # If we are left of goal, move right
            if current_point.x < map_.goal.x:
                current_point.x += 1
            # If we are right of goal, move left
            else:
                current_point.x -= 1
            path.append(deepcopy(current_point))

        # Keep moving vertically until we match the target
        while (current_point.y != map_.goal.y):
            # If we are left of goal, move right
            if current_point.y < map_.goal.y:
                current_point.y += 1
            # If we are right of goal, move left
            else:
                current_point.y -= 1
            path.append(deepcopy(current_point))

        # We're done!
        return path


class Djikstras(AIModule):

    def createPath(self, map_):
        q = PriorityQueue()
        cost = {}
        prev = {}
        explored = {}
        for i in range(map_.width):
            for j in range(map_.length):
                cost[str(i) + ',' + str(j)] = math.inf
                prev[str(i) + ',' + str(j)] = None
                explored[str(i) + ',' + str(j)] = False
        current_point = deepcopy(map_.start)
        current_point.comparator = 0
        cost[str(current_point.x) + ',' + str(current_point.y)] = 0
        q.put(current_point)
        while q.qsize() > 0:
            # Get new point from PQ

            v = q.get()
            if explored[str(v.x) + ',' + str(v.y)]:
                continue

            explored[str(v.x) + ',' + str(v.y)] = True
            # Check if popping off goal
            if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
                break
            # Evaluate neighbors
            neighbors = map_.getNeighbors(v)
            for neighbor in neighbors:
                alt = map_.getCost(v, neighbor) + cost[str(v.x) + ',' + str(v.y)]
                if alt < cost[str(neighbor.x) + ',' + str(neighbor.y)]:
                    cost[str(neighbor.x) + ',' + str(neighbor.y)] = alt
                    neighbor.comparator = alt
                    prev[str(neighbor.x) + ',' + str(neighbor.y)] = v
                q.put(neighbor)

        path = []
        while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
            path.append(v)
            v = prev[str(v.x) + ',' + str(v.y)]
        path.append(map_.getStartPoint())
        path.reverse()
        return path


class AStarExp(AIModule):

    def createPath(self, map_):
        q = PriorityQueue()
        cost = {}
        prev = {}
        explored = {}
        for i in range(map_.width):
            for j in range(map_.length):
                cost[str(i) + ',' + str(j)] = math.inf
                prev[str(i) + ',' + str(j)] = None
                explored[str(i) + ',' + str(j)] = False
        current_point = deepcopy(map_.start)
        current_point.comparator = 0
        cost[str(current_point.x) + ',' + str(current_point.y)] = 0
        q.put(current_point)
        while q.qsize() > 0:
            # Get new point from PQ
            v = q.get()

            # if explored[str(v.x) + ',' + str(v.y)]:
            # continue

            explored[str(v.x) + ',' + str(v.y)] = True

            # Check if popping off goal
            if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
                break
            # Evaluate neighbors
            neighbors = map_.getNeighbors(v)

            for neighbor in neighbors:
                alt = map_.getCost(v, neighbor) + cost[str(v.x) + ',' + str(v.y)]
                if alt < cost[str(neighbor.x) + ',' + str(neighbor.y)]:
                    cost[str(neighbor.x) + ',' + str(neighbor.y)] = alt

                    neighbor.comparator = alt + self.heuristic(neighbor, map_, v)

                    prev[str(neighbor.x) + ',' + str(neighbor.y)] = v
                q.put(neighbor)

        path = []
        while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
            path.append(v)
            v = prev[str(v.x) + ',' + str(v.y)]
        path.append(map_.getStartPoint())
        path.reverse()
        return path

    def heuristic(self, neighbor, map_, v):
        chebDistance = max(abs(map_.getEndPoint().x - neighbor.x), abs(map_.getEndPoint().y - neighbor.y))
        deltaH = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y) - map_.getTile(v.x, v.y)

        if neighbor.__gt__(v):
            return 2 * deltaH + max(0, chebDistance - deltaH)
        elif neighbor.__lt__(v):
            return (math.pow(2, (deltaH / chebDistance))) * chebDistance
        elif neighbor.__eq__(v):
            return chebDistance


class AStarDiv(AIModule):

    def createPath(self, map_):
        q = PriorityQueue()
        cost = {}
        prev = {}
        explored = {}
        for i in range(map_.width):
            for j in range(map_.length):
                cost[str(i) + ',' + str(j)] = math.inf
                prev[str(i) + ',' + str(j)] = None
                explored[str(i) + ',' + str(j)] = False
        current_point = deepcopy(map_.start)
        current_point.comparator = 0
        cost[str(current_point.x) + ',' + str(current_point.y)] = 0
        q.put(current_point)

        while q.qsize() > 0:
            # Get new point from PQ
            v = q.get()

            if explored[str(v.x) + ',' + str(v.y)]:
                continue

            explored[str(v.x) + ',' + str(v.y)] = True

            # Check if popping off goal
            if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
                break
            # Evaluate neighbors
            neighbors = map_.getNeighbors(v)

            for neighbor in neighbors:
                alt = map_.getCost(v, neighbor) + cost[str(v.x) + ',' + str(v.y)]
                if alt < cost[str(neighbor.x) + ',' + str(neighbor.y)]:
                    cost[str(neighbor.x) + ',' + str(neighbor.y)] = alt = alt

                    neighbor.comparator = alt + self.heuristic(map_, neighbor, v)

                    prev[str(neighbor.x) + ',' + str(neighbor.y)] = v
                q.put(neighbor)

        path = []
        while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
            path.append(v)
            v = prev[str(v.x) + ',' + str(v.y)]
        path.append(map_.getStartPoint())
        path.reverse()
        return path

    def heuristic(self, map_, neighbor, v):
        modifiedChebDistance = max(abs(map_.getEndPoint().x - neighbor.x), abs(map_.getEndPoint().y - neighbor.y))
        edgeCase = math.floor(math.log(map_.getTile(v.x, v.y), 2))
        return max((modifiedChebDistance - edgeCase) / 2, 0)


class AStarMSH(AIModule):

    def createPath(self, map_):
        q = PriorityQueue()
        cost = {}
        prev = {}
        explored = {}
        for i in range(map_.width):
            for j in range(map_.length):
                cost[str(i) + ',' + str(j)] = math.inf
                prev[str(i) + ',' + str(j)] = None
                explored[str(i) + ',' + str(j)] = False
        current_point = deepcopy(map_.start)
        current_point.comparator = 0
        cost[str(current_point.x) + ',' + str(current_point.y)] = 0
        q.put(current_point)
        while q.qsize() > 0:
            # Get new point from PQ
            v = q.get()

            # if explored[str(v.x) + ',' + str(v.y)]:
            # continue
            explored[str(v.x) + ',' + str(v.y)] = True

            # Check if popping off goal
            if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
                break
            # Evaluate neighbors
            neighbors = map_.getNeighbors(v)
            for neighbor in neighbors:
                alt = map_.getCost(v, neighbor) + cost[str(v.x) + ',' + str(v.y)]
                if alt < cost[str(neighbor.x) + ',' + str(neighbor.y)]:
                    cost[str(neighbor.x) + ',' + str(neighbor.y)] = alt = alt

                    neighbor.comparator = alt + self.heuristic(neighbor, map_, v)

                    prev[str(neighbor.x) + ',' + str(neighbor.y)] = v
                q.put(neighbor)

        path = []
        while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
            path.append(v)
            v = prev[str(v.x) + ',' + str(v.y)]
        path.append(map_.getStartPoint())
        path.reverse()
        return path

    def heuristic(self, neighbor, map_, v):
        chebDistance = max(abs(map_.getEndPoint().x - neighbor.x), abs(map_.getEndPoint().y - neighbor.y))
        deltaH = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y) - map_.getTile(v.x, v.y)

        if neighbor.__gt__(v):
            return 2 * deltaH + max(0, chebDistance - deltaH)
        elif neighbor.__lt__(v):
            return (math.pow(2, (deltaH / chebDistance))) * chebDistance
        elif neighbor.__eq__(v):
            return chebDistance
