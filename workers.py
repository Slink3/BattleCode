import battlecode as bc
import random
import move
import json

# Worker class - each worker can store a path and knows if has a plan - is running along a path


class Worker():

    def __init__(self, id):
        self.factoryBuildID = 0
        self.hasPlan = False
        self.workerUnitID = id
        self.buildsFactory = False


# class to store all the info necessary for workers logic
class WorkersInfo():

    def __init__(self, gc):
        self.workersList = []
        self.maxWorkers = 0
        self.maxFactories = 0
        self.currentKarbonite = []
        self.cummulativeCarbonite = []
        self.marsWorkersList = []
        self.grid = grid = json.loads(gc.starting_map(bc.Planet.Earth).to_json())["is_passable_terrain"]

# Initialization logic
def initializeWorkersAndGetTotalKarbonite(gc, workersInformation):
    eMap = gc.starting_map(bc.Planet.Earth)
    KarboniteNeigbouthood = [[0 for y in range(eMap.height)] for x in range(eMap.width)]
    currentKarbonite = [[0 for y in range(eMap.height)] for x in range(eMap.width)]
    totalKarbonite = 0
    for x in range(eMap.width):
        for y in range(eMap.height):
                for a in range(5):
                        for b in range(5):
                            if x + a - 2 >= 0 and y + b - 2 >= 0 and x + a - 2 < eMap.width and y + b - 2 < eMap.height: 
                                location = bc.MapLocation(eMap.planet, x + a - 2, y + b - 2)
                                KarboniteNeigbouthood[x][y] += eMap.initial_karbonite_at(location)
                currentKarbonite[x][y] = eMap.initial_karbonite_at(bc.MapLocation(eMap.planet, x, y))
                totalKarbonite += eMap.initial_karbonite_at(bc.MapLocation(eMap.planet, x, y))

    workersInformation.currentKarbonite = currentKarbonite
    workersInformation.cummulativeCarbonite = KarboniteNeigbouthood
    for wrk in workersInformation.workersList:
        setWorkerPlan(wrk,workersInformation,gc)
    return totalKarbonite



def setWorkerPlan(wrk,workersInformation,gc):
    eMap = gc.starting_map(bc.Planet.Earth)
    quality = [[0 for y in range(eMap.height)] for x in range(eMap.width)]
    for x in range(eMap.width):
        for y in range(eMap.height):
            quality[x][y] = workersInformation.cummulativeCarbonite[x][y] / (1+(gc.unit(wrk.workerUnitID)).location.map_location().distance_squared_to(bc.MapLocation(eMap.planet, x, y)))
    bestLocation = (gc.unit(wrk.workerUnitID)).location.map_location()
    currentMax = 0
    for x in range(eMap.width):
        for y in range(eMap.height):
            if quality[x][y] > currentMax:
                currentMax = quality[x][y]
                bestLocation = bc.MapLocation(eMap.planet,x,y)
    wrk.hasPlan = True
    wrk.destination = bestLocation
    return

# Local search for karbonite
def lookForNearbyKarbonite(wrk, workersInformation, gc):
    max = 0
    eMap = gc.starting_map(bc.Planet.Earth)
    loc = gc.unit(wrk.workerUnitID).location.map_location()
    unitLoc = gc.unit(wrk.workerUnitID).location.map_location()
    for x in range(-3,3):
        for y in range(-3,3):
            if unitLoc.x + x >=0 and unitLoc.x + x < eMap.width and  unitLoc.y + y >=0 and unitLoc.y + y < eMap.height:
                if workersInformation.currentKarbonite[unitLoc.x + x][ unitLoc.y + y] > max:
                    max=  workersInformation.currentKarbonite[unitLoc.x + x][unitLoc.y + y]
                    loc = bc.MapLocation(eMap.planet,unitLoc.x + x,unitLoc.y + y)
    return loc

# Unit game logic
def runWorkerLogic(worker, unitInfo, workersInformation, gc):
    # Current location of the unit

    # every 150 turns increase max number of factories
    if gc.round() % 150:
        workersInformation.maxFactories += 1
    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    if not gc.can_sense_unit(worker.workerUnitID) or gc.unit(worker.workerUnitID).location.is_in_garrison():
        workersInformation.workersList.remove(worker)
        return

    if gc.team() == bc.Team.Red:
        enemyTeam = bc.Team.Blue
    else: 
        enemyTeam = bc.Team.Red 

    unitLocation = gc.unit(worker.workerUnitID).location.map_location()
    nearbyUnits = gc.sense_nearby_units(unitLocation, 3)
    nearbyEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, gc.unit(worker.workerUnitID).vision_range, enemyTeam)

    #flee from enemy army

    for nearbyEnemyUnit in nearbyEnemyUnits:
        if nearbyEnemyUnit.unit_type == bc.UnitType.Ranger or nearbyEnemyUnit.unit_type == bc.UnitType.Knight or nearbyEnemyUnit.unit_type == bc.UnitType.Mage:
            move.gofrom(gc,worker.workerUnitID,nearbyEnemyUnit.location.map_location())
            worker.hasPlan = False
            return


    # If there are less than maxWorkers workers, then try to replicate
    if unitInfo.workerCount < workersInformation.maxWorkers:
        for direction in directions:
            if gc.can_replicate(worker.workerUnitID, direction):
                gc.replicate(worker.workerUnitID, direction)
                for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
                    if unit.unit_type == bc.UnitType.Worker:
                        wrk = Worker(unit.id)
                        workersInformation.workersList.append(wrk)
                        if gc.round() < 50:
                            setWorkerPlan(wrk,workersInformation,gc)
                return

    # go according to plan
    if worker.hasPlan:
        move.goto(gc, worker.workerUnitID, worker.destination)
        if worker.destination.distance_squared_to((gc.unit(worker.workerUnitID)).location.map_location()) < 5:
            worker.hasPlan = False
        return

    # building a factory
    if worker.buildsFactory:
        # If the factory the worker is building is not finished, build it
        if gc.can_build(worker.workerUnitID, worker.factoryBuildID):
            gc.build(worker.workerUnitID, worker.factoryBuildID)
            return
        else:
            worker.buildsFactory = False
            return

    # If there are less than maxFactories factories, then try to blueprint a factory
    if unitInfo.factoryCount < workersInformation.maxFactories:
        if gc.karbonite() > bc.UnitType.Factory.blueprint_cost():
            for direction in directions:
                if gc.can_blueprint(worker.workerUnitID, bc.UnitType.Factory, direction):
                    gc.blueprint(worker.workerUnitID, bc.UnitType.Factory, direction)
                    worker.buildsFactory=True
                    for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
                        if unit.unit_type==bc.UnitType.Factory:
                            worker.factoryBuildID = unit.id
                    return

    # If there is no rocket, then build one
    if (unitInfo.rocketCount == 0 and gc.round()>200) or gc.round()>650:   #don't know about the constant?
        if gc.karbonite() > bc.UnitType.Rocket.blueprint_cost():
            for direction in directions:
                if gc.can_blueprint(worker.workerUnitID, bc.UnitType.Rocket, direction):
                    gc.blueprint(worker.workerUnitID, bc.UnitType.Rocket, direction)
                    worker.buildsFactory = True
                    for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
                        if unit.unit_type == bc.UnitType.Rocket:
                            worker.factoryBuildID = unit.id
                        return  

    # If there is karbonite nearby, then try to harvest it 
    for direction in directions:
        adjacentLocation = unitLocation.add(direction)
        # Need to try/catch because if adjacentLocation is not on map, then karbonite_at() throws exception
        try:
            if gc.karbonite_at(adjacentLocation) > 0:
                if gc.can_harvest(worker.workerUnitID, direction):
                    gc.harvest(worker.workerUnitID, direction)
                    workersInformation.currentKarbonite[gc.unit(worker.workerUnitID).location.map_location().add(direction).x][gc.unit(worker.workerUnitID).location.map_location().add(direction).x] -= 3
                    return
        except Exception as e:
            continue

    # Search karbonite
    for direction in directions:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                # gc.move_robot(worker.workerUnitID, direction)
                move.goto(gc, worker.workerUnitID, unitLocation.add(direction))
                return


    # repairing comes last - least important
    for nearbyUnit in nearbyUnits:
        # If there are damaged factories nearby, then try to repair them
        if gc.can_repair(worker.workerUnitID, nearbyUnit.id):
            gc.repair(worker.workerUnitID, nearbyUnit.id)
            return
    return

    # if everything failed, try to just go randomly...
    for direction in directions:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                # gc.move_robot(worker.workerUnitID, direction)
                move.goto(gc, worker.workerUnitID, unitLocation.add(direction))
                return


def runWorkerLogicMars(worker, workersInformation, gc):

    if not gc.can_sense_unit(worker.workerUnitID) or gc.unit(worker.workerUnitID).location.is_in_garrison():
        workersInformation.marsWorkersList.remove(worker)
        return
    unitLocation = gc.unit(worker.workerUnitID).location.map_location()

    directions = list(bc.Direction)
    random.shuffle(directions)

      # If there is karbonite nearby, then try to harvest it 
    for direction in directions:
        adjacentLocation = unitLocation.add(direction)
        # Need to try/catch because if adjacentLocation is not on map, then karbonite_at() throws exception
        try:
            if gc.karbonite_at(adjacentLocation) > 0:
                if gc.can_harvest(worker.workerUnitID, direction):
                    gc.harvest(worker.workerUnitID, direction)
                    return
        except Exception as e:
            continue

    # Search karbonite
    for direction in directions:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                # gc.move_robot(worker.workerUnitID, direction)
                move.goto(gc, worker.workerUnitID, unitLocation.add(direction))
                return


