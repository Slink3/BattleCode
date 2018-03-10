import battlecode as bc
import random
import sys
import traceback
import time
import collections

directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0, -1, 1, -2, 2]

def goto(gc, unit_id, dest):
	earthMap = gc.starting_map(bc.Planet.Earth)
	if gc.unit(unit_id).location.map_location() == dest: 
		return
	if gc.unit(unit_id).movement_heat() >= 10: 
		return
	toward = gc.unit(unit_id).location.map_location().direction_to(dest)
	for tilt in tryRotate:
		d = rotate(toward, tilt)
		newLoc = gc.unit(unit_id).location.map_location().add(d)
		if newLoc.x <= earthMap.width and newLoc.y <= earthMap.height:
			if gc.can_move(unit_id, d) and gc.unit(unit_id).movement_heat() < 10:
				gc.move_robot(unit_id, d)

def rotate(dir, amount):
    ind = directions.index(dir)
    return directions[(ind + amount) % 8]







