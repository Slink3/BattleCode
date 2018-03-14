import battlecode as bc
import random
import sys
import traceback
import time
import collections
from collections import deque
import itertools

directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0, -1, 1, -2, 2]
tryRotateFrom = [4, -3, 3, -2, 2]

move_dict = {   "N":bc.Direction.North,
                "E":bc.Direction.East,
                "W":bc.Direction.West,
                "S":bc.Direction.South,
                "NE":bc.Direction.Northeast,
                "SE":bc.Direction.Southeast,
                "NW":bc.Direction.Northwest,
                "SW":bc.Direction.Southwest,
            }


def goto(gc, unit_id, dest):
	if dest.planet == bc.Planet.Earth:
		planetMap = gc.starting_map(bc.Planet.Earth)
	else:
		planetMap = gc.starting_map(bc.Planet.Mars)

	if gc.unit(unit_id).location.map_location() == dest: 
		return
	if gc.unit(unit_id).movement_heat() >= 10: 
		return
	toward = gc.unit(unit_id).location.map_location().direction_to(dest)
	for tilt in tryRotate:
		d = rotate(toward, tilt)
		newLoc = gc.unit(unit_id).location.map_location().add(d)
		if newLoc.x <= planetMap.width and newLoc.y <= planetMap.height:
			if gc.can_move(unit_id, d) and gc.unit(unit_id).movement_heat() < 10:
				gc.move_robot(unit_id, d)

# For fleeing from enemies
def gofrom(gc, unit_id, dest):
	if dest.planet == bc.Planet.Earth: 
		planetMap = gc.starting_map(bc.Planet.Earth)
	else:
		planetMap = gc.starting_map(bc.Planet.Mars)

	if gc.unit(unit_id).location.map_location() == dest: 
		return
	if gc.unit(unit_id).movement_heat() >= 10: 
		return
	toward = gc.unit(unit_id).location.map_location().direction_to(dest)
	for tilt in tryRotateFrom:
		d = rotate(toward, tilt)
		newLoc = gc.unit(unit_id).location.map_location().add(d)
		if newLoc.x <= planetMap.width and newLoc.y <= planetMap.height:
			if gc.can_move(unit_id, d) and gc.unit(unit_id).movement_heat() < 10:
				gc.move_robot(unit_id, d)


def rotate(dir, amount):
    ind = directions.index(dir)
    return directions[(ind + amount) % 8]

def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and maze[row + 1][col]:
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and maze[row][col + 1]:
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph

def find_path_bfs(maze, start, goal):
    #start, goal = (1, 1), (len(maze) - 2, len(maze[0]) - 2)
    queue = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while queue:
        path, current = queue.popleft()
        if current == goal:

            result =  ''.join(i for i, _ in itertools.groupby(path.replace("NE", "-NE-").replace("EN", "-NE-").replace("NW", "-NW-").replace("WN", "-NW-").replace("ES", "-SE-").replace("SE", "-SE-").replace("WS", "-SW-").replace("SW", "-SW-").replace("EE", "-E-E-").replace("WW", "-W-W-").replace("SS", "-S-S-").replace("NN", "-N-N-")))
            return result[1:-1]
            # return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!"

def move(gc, unit, grid, goal):
	path = [move for move in find_path_bfs(grid, (len(grid)-1-unit.location.map_location().y, unit.location.map_location().x), goal).split("-") if move in move_dict]
	while len(path)!=0:
		try:
			if gc.is_move_ready(unit.id) and gc.can_move(unit.id, move_dict[path[0]]):
				#print((len(grid)-1-unit.location.map_location().y, unit.location.map_location().x))
				gc.move_robot(unit.id, move_dict[path[0]])
				#print((len(grid)-1-unit.location.map_location().y, unit.location.map_location().x))
				path.pop(0)
			#else:
				#print((len(grid)-1-unit.location.map_location().y, unit.location.map_location().x), path[0])
				#print("could not move this time")
		except Exception as e:
			print('Error:', e)
			traceback.print_exc()
		sys.stdout.flush()
		sys.stderr.flush()
		gc.next_turn()







