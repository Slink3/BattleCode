# never give up from mars :)
import battlecode as bc
import random
import sys
import traceback

def computeOptimalLandingPlace(marsMap):
	best = bc.MapLocation(bc.Planet.Mars, 0, 0)
	bestKarbonite = marsMap.initial_karbonite_at(best)

	for x in range(marsMap.width):
		for y in range(marsMap.height):
			mapLocation = bc.MapLocation(bc.Planet.Mars, x, y)
			nearbyKarbonite = computeNearbyKarbonite(marsMap, mapLocation)
			if marsMap.is_passable_terrain_at(mapLocation) and nearbyKarbonite > bestKarbonite:
				best = mapLocation
				bestKarbonite = nearbyKarbonite
	return best

def computeNearbyKarbonite(marsMap, mapLocation):
	directions = list(bc.Direction)
	totalKarbonite = 0
	for direction in directions:
		adjacentLocation = mapLocation.add(direction)
		try:
			totalKarbonite += marsMap.initial_karbonite_at(adjacentLocation)
		except Exception as e:
			continue
		
	print(totalKarbonite)
	return totalKarbonite

def launch(gc, marsMap, unitId):
	if gc.unit(unitId).structure_is_built():
		this_rocket = gc.unit(unitId)
	else:
		return
	garrison = this_rocket.structure_garrison()

	if len(garrison) >= 4:
		#destination = computeOptimalLandingPlace(marsMap)
		destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
		if gc.can_launch_rocket(this_rocket.id, destination):
			gc.launch_rocket(this_rocket.id, destination)
	else:
		if gc.round() >= 700 and len(garrison) >= 1:
			destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
			if gc.can_launch_rocket(this_rocket.id, destination):
				gc.launch_rocket(this_rocket.id, destination)



