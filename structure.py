import battlecode as bc
import random
import move


def computeOptimalLandingPlace(marsMap):
	bestKarbonite = 0
	best = None

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
		while(not marsMap.is_passable_terrain_at(destination)):
			destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
		if gc.can_launch_rocket(this_rocket.id, destination):
			gc.launch_rocket(this_rocket.id, destination)
	else:
		if gc.round() >= 700 and len(garrison) >= 1:
			while(not marsMap.is_passable_terrain_at(destination)):
				destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
			if gc.can_launch_rocket(this_rocket.id, destination):
				gc.launch_rocket(this_rocket.id, destination)


def runFactoryLogic(unit, unitInfo, mapInfo, gc):
    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)
    
    # If the structure is not built, then do nothing
    if not unit.structure_is_built():
        return

    # Try to unload existing units from structure's garrison
    for direction in directions:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            print("Unloading unit")
            return

    # If there are less than 5 knights, then produce a knight
    if unitInfo.knightCount < max(5, unitInfo.totalArmyCount * 0.35):
        if gc.can_produce_robot(unit.id, bc.UnitType.Knight): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Knight)
            print("Producing knight")
            return

    # If there are less than 5 rangers, then produce a ranger
    if unitInfo.rangerCount < max(5, unitInfo.totalArmyCount * 0.6):
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
            print("Producing ranger")
            return

    # If there are less than 5 mages, then produce a mage
    '''
    if unitInfo.mageCount < max(0, unitInfo.totalArmyCount * 3):
        if gc.can_produce_robot(unit.id, bc.UnitType.Mage): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Mage)
            print("Producing mage")
            return
    '''

    # If there are less than 5 rangers, then produce a healer
    if unitInfo.healerCount < unitInfo.totalArmyCount * 0.05:
        if gc.can_produce_robot(unit.id, bc.UnitType.Healer): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Healer)
            print("Producing healer")
            return

    return

def runRocketLogic(unit, unitInfo, mapInfo, gc):
    unitLocation = unit.location.map_location()

    # find and load some workers into the rocket
    if len(unit.structure_garrison()) < 4: # TODO: We only load 4 units for now
        nearbyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, gc.team())

        for nearU in nearbyUnits:
            if gc.can_load(unit.id, nearU.id):
                gc.load(unit.id, nearU.id)
                return
    else:
        launch(gc, gc.starting_map(bc.Planet.Mars), unit.id)
    return

def runFactoryLogicMars(unit, unitInfo, gc):
    runFactoryLogic(unit, unitInfo, gc)
    return

def runRocketLogicMars(unit, workers, workersInformation, gc):
     # Try to unload existing units from structure's garrison
    if len(unit.structure_garrison()) > 0:  
        for direction in directions:
            if gc.can_unload(unit.id, direction):
                gc.unload(unit.id, direction)
                for newWorker in gc.sense_nearby_units(unit.location.map_location().add(direction), 0):
                    if newWorker.unit_type == bc.UnitType.Worker:
                        wrk = workers.Worker(newWorker.id)
                        workersInformation.marsWorkersList.append(wrk)
                        return
    return

directions = list(bc.Direction)