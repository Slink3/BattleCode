import battlecode as bc
import random
import sys
import traceback
import time
import os

# Class containing initial data about planet map (passable terrain, karbonite)
class MyPlanetMap():
    def __init__(self, planetMap):
        self.width = planetMap.width
        self.height = planetMap.height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]
        self.karboniteMap = [[0 for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                location = bc.MapLocation(planetMap.planet, x, y)
                if (planetMap.is_passable_terrain_at(location)): 
                    self.map[x][self.width - 1 - y] = 1
                else:
                    self.map[x][self.width - 1 - y] = 0
                self.karboniteMap[x][self.width - 1 - y] = planetMap.initial_karbonite_at(location)

    def printMap(self):
        print("Printing map:")
        for y in range(self.height):
            mapString = ''
            for x in range(self.width):
                mapString += format(self.map[x][y], '2d')
            print(mapString)

    def printKarboniteMap(self):
        print("Printing Karbonite map:")
        for y in range(self.height):
            mapString = ''
            for x in range(self.width):
                mapString += format(self.karboniteMap[x][y], '2d')
            print(mapString)

    def printMaps(self):
        self.printMap()
        self.printKarboniteMap()

<<<<<<< HEAD
# Path class - contains stored path and can return next direction
=======

        

#Path class - contains stored path and can return next direction
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
class Path():
    def __init__(self):
        return super().__init__(**kwargs)

    def getNextDirection():
        directions = list(bc.Direction)
        return random.choice(directions)

    def isFinished():
        return False

<<<<<<< HEAD
# Worker class - each worker can store a path and knows if has a plan - is running along a path
class Worker():
    def __init__(self, id):
        print("Making worker: ", id)
        self.factoryBuildID = 0
        self.hasPlan = False
        self.workerUnitID = id
        self.buildsFactory = False
=======
#Worker class - each worker can store a path and knows if has a plan - is running along a path
class Worker():
    def __init__(self, id):
        print("making worker")
        print(id)
        self.factoryBuildID = 0;
        self.hasPlan = False
        self.workerUnitID = id
        self.buildsFactory = False


>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
    
# Class containing data about all units in current round
class UnitInfo():
    def __init__(self, gc):
        self.factoryCount = self.workerCount = self.knightCount = self.rangerCount = 0;
        self.mageCount = self.healerCount = 0
        for unit in gc.my_units():
            if (unit.unit_type == bc.UnitType.Factory):
                self.factoryCount += 1
            elif (unit.unit_type == bc.UnitType.Worker):
                self.workerCount += 1
            elif (unit.unit_type == bc.UnitType.Knight):
                self.knightCount += 1
            elif (unit.unit_type == bc.UnitType.Ranger):
                self.rangerCount += 1
            elif (unit.unit_type == bc.UnitType.Mage):
                self.mageCount += 1
            elif (unit.unit_type == bc.UnitType.Healer):
                self.healerCount += 1

def printTimeLeft(gc):
    print("Time left: ", gc.get_time_left_ms())

    
<<<<<<< HEAD
# Initialization logic
=======
   #initialization logic
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
def initializeWorkersAndGetTotalKarbonite():
    eMap = gc.starting_map(bc.Planet.Earth)
    KarboniteNeigbouthood = [[0 for x in range(eMap.width)] for y in range(eMap.height)]
    totalKarbonite = 0
    for y in range(eMap.height):
        for x in range(eMap.width):
                for a in range(5):
                        for b in range(5):
<<<<<<< HEAD
                            if x + a - 2 >= 0 and y + b - 2 >= 0 and x + a - 2 < eMap.width and y + b - 2 < eMap.height: 
                                location = bc.MapLocation(eMap.planet, x + a - 2, y + b - 2)
=======
                            if x+a-2>=0 and y+b-2>=0 and x+a-2 < eMap.width and y+b-2<eMap.height: 
                                location = bc.MapLocation(eMap.planet, x+a-2, y+b-2)
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
                                KarboniteNeigbouthood[x][y] += eMap.initial_karbonite_at(location)
                totalKarbonite += eMap.initial_karbonite_at(bc.MapLocation(eMap.planet, x, y))
    return totalKarbonite

    
<<<<<<< HEAD
# Unit game logic
=======
    # Unit game logic
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
def runWorkerLogic(worker, unitInfo, gc):
    # Current location of the unit

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

<<<<<<< HEAD
=======

>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
    unitLocation = gc.unit(worker.workerUnitID).location.map_location()
    nearbyUnits = gc.sense_nearby_units(unitLocation, 2)

    if worker.hasPlan:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                gc.move_robot(worker.workerUnitID, direction)
                return

    if worker.buildsFactory:
<<<<<<< HEAD
        # If the factory the worker is building is not finished, build it
        if gc.can_build(worker.workerUnitID, worker.factoryBuildID):
            gc.build(worker.workerUnitID, worker.factoryBuildID)
            return
        else:
            worker.buildsFactory = False
            print("Factory built")
            return  
=======
            # If the factory the worker is building is not finished, build it
            if gc.can_build(worker.workerUnitID, worker.factoryBuildID):
                gc.build(worker.workerUnitID, worker.factoryBuildID)
                return
            else:
                worker.buildsFactory = False
                print("Built factoory!")
                return  
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00

    # duplicating
    # If there are less than maxWorkers workers, then try to replicate
    if unitInfo.workerCount < maxWorkers:
        for direction in directions:
            if gc.can_replicate(worker.workerUnitID, direction):
                gc.replicate(worker.workerUnitID, direction)
                for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
<<<<<<< HEAD
                    if unit.unit_type == bc.UnitType.Worker:
=======
                    if unit.unit_type==bc.UnitType.Worker:
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
                        workers.append(Worker(unit.id))
                return

    # If there are less than maxFactories factories, then try to blueprint a factory
    if unitInfo.factoryCount < maxFactories:
        if gc.karbonite() > bc.UnitType.Factory.blueprint_cost():
            for direction in directions:
                if gc.can_blueprint(worker.workerUnitID, bc.UnitType.Factory, direction):
                    gc.blueprint(worker.workerUnitID, bc.UnitType.Factory, direction)
                    worker.buildsFactory=True
                    for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
                        if unit.unit_type==bc.UnitType.Factory:
                            worker.factoryBuildID = unit.id
                            print("Blueprinting")
                    return

    # If there is karbonite nearby, then try to harvest it 
    for direction in directions:
        adjacentLocation = unitLocation.add(direction)
        # Need to try/catch because if adjacentLocation is not on map, then karbonite_at() throws exception
        try:
            if gc.karbonite_at(adjacentLocation) > 0:
                if gc.can_harvest(worker.workerUnitID, direction):
                    gc.harvest(worker.workerUnitID, direction)
<<<<<<< HEAD
                    print("Harvesting")
=======
                    print("harvested")
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
                    return
        except Exception as e:
            continue
            
    # Search karbonite
    for direction in directions:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                gc.move_robot(worker.workerUnitID, direction)
                return

<<<<<<< HEAD
=======
   

   
     
   


>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
    #repairing comes last - least important
    for nearbyUnit in nearbyUnits:
        # If there are damaged factories nearby, then try to repair them
        if gc.can_repair(worker.workerUnitID, nearbyUnit.id):
            gc.repair(worker.workerUnitID, nearbyUnit.id)
            return
    
<<<<<<< HEAD
=======


>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
    return

def runKnightLogic(unit, unitInfo, gc):
    # If knight is in garrison, then do nothing
    if unit.location.is_in_garrison() or unit.location.is_in_space():
        return

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    # Current location of the unit
    unitLocation = unit.location.map_location()

    # Get enemy team
    if gc.team() == bc.Team.Red:
        enemyTeam = bc.Team.Blue
    else: 
        enemyTeam = bc.Team.Red 

    nearbyEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), enemyTeam)
    for nearbyEnemyUnit in nearbyEnemyUnits:
        # If there are enemy units nearby, then try to attack them
        if gc.is_attack_ready(unit.id):
            if gc.can_attack(unit.id, nearbyEnemyUnit.id):
                gc.attack(unit.id, nearbyEnemyUnit.id)
                return

    visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
    for visibleEnemyUnit in visibleEnemyUnits:
        # If there are visible enemy units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleEnemyUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return
            
    # Move randomly
    for direction in directions:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return

    return

def runRangerLogic(unit, unitInfo, gc):
    runKnightLogic(unit, unitInfo, gc) # TODO: Implement ranger logic
    return

def runMageLogic(unit, unitInfo, gc):
    runKnightLogic(unit, unitInfo, gc) # TODO: Implement mage logic
    return

def runHealerLogic(unit, unitInfo, gc):
    # If healer is in garrison, then do nothing
    if unit.location.is_in_garrison() or unit.location.is_in_space():
        return

    # Current location of the unit
    unitLocation = unit.location.map_location()

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    nearbyAlliedUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), gc.team())
    for nearbyAlliedUnit in nearbyAlliedUnits:
        # If there are wounded allied units nearby, then try to heal them
        if gc.is_heal_ready(unit.id):
            if gc.can_heal(unit.id, nearbyAlliedUnit.id):
                gc.heal(unit.id, nearbyAlliedUnit.id)
                return

    visibleAlliedUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
    for visibleAlliedUnit in visibleAlliedUnits:
        # If there are visible allied units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleAlliedUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return
            
    # Move randomly
    for direction in directions:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return

    return

def runFactoryLogic(unit, unitInfo, gc):
    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)
    
    # If the structure is not built, then do nothing
    if not unit.structure_is_built():
        return

    # Try to unload existing units from structure's garrison
    directions = list(bc.Direction)
    for direction in directions:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            print("Unloading unit")
            return

    # If there are less than 5 knights, then produce a knight
    if unitInfo.knightCount < 5:
        if gc.can_produce_robot(unit.id, bc.UnitType.Knight): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Knight)
            print("Producing knight")
            return
<<<<<<< HEAD

    # If there are less than 5 rangers, then produce a ranger
    if unitInfo.rangerCount < 5:
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
            print("Producing mage")
            return

    # If there are less than 5 rangers, then produce a healer
    if gc.can_produce_robot(unit.id, bc.UnitType.Healer): # TODO: 
        gc.produce_robot(unit.id, bc.UnitType.Healer)
        print("Producing healer")
=======
    # If the structure can produce a new robot, then
    if gc.can_produce_robot(unit.id, bc.UnitType.Knight): # TODO: 
        gc.produce_robot(unit.id, bc.UnitType.Knight)
        print("producing robots")
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
        return

    return

def runRocketLogic(unit, unitInfo, gc):
    # TODO: Implement rocket logic
    return


# Earth game logic
def runEarth(gc):
    unitInfo = UnitInfo(gc)

    for worker in workers:
        runWorkerLogic(worker, unitInfo, gc)


    for unit in gc.my_units():
<<<<<<< HEAD
=======
        #if unit.unit_type == bc.UnitType.Worker:
        #    runWorkerLogic(unit, unitInfo, gc)
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00
        if unit.unit_type == bc.UnitType.Knight:
            runKnightLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Ranger:
            runRangerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Mage:
            runMageLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Healer:
            runHealerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Factory:
            runFactoryLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Rocket:
            runRocketLogic(unit, unitInfo, gc)

    printTimeLeft(gc)

# Mars game logic
def runMars(gc):
    # TODO:
    print('Mars')



#####################################################################################
#                                       MAIN                                        #
#####################################################################################

################
#  BEGIN PLAY  #
################

# Get the game controller
gc = bc.GameController()
random.seed(6137)

earthMap = MyPlanetMap(gc.starting_map(bc.Planet.Earth)) # TODO: Maybe redundant
marsMap = MyPlanetMap(gc.starting_map(bc.Planet.Mars)) # TODO: Maybe redundant

#earthMap.printKarboniteMap()

#all workers will be stored
workers = []
for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Worker:
            workers.append(Worker(unit.id))
<<<<<<< HEAD
            print("Worker added: ", unit.id)

totKarb = initializeWorkersAndGetTotalKarbonite()
maxWorkers = totKarb / 150  #needs tweaking after testing - now /100 - that means at full workers some 33 turns to mine all without the movement
maxFactories = totKarb / 300
=======
            print("added worker ")
            print(unit.id)

totKarb = initializeWorkersAndGetTotalKarbonite()
maxWorkers = totKarb/150  #needs tweaking after testing - now /100 - that means at full workers some 33 turns to mine all without the movement
maxFactories = totKarb/300
>>>>>>> ec0ae829e97ee0a5281bd7b03c2ac6c4c502ed00

################
#    UPDATE    #
################

while True:
    try:
        if(gc.planet() == bc.Planet.Earth):
            runEarth(gc)
        else:
            runMars(gc)

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    gc.next_turn()

    sys.stdout.flush()
    sys.stderr.flush()



