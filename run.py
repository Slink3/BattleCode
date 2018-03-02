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
        print('Printing map:')
        for y in range(self.height):
            mapString = ''
            for x in range(self.width):
                mapString += format(self.map[x][y], '2d')
            print(mapString)

    def printKarboniteMap(self):
        print('Printing Karbonite map:')
        for y in range(self.height):
            mapString = ''
            for x in range(self.width):
                mapString += format(self.karboniteMap[x][y], '2d')
            print(mapString)

    def printMaps(self):
        self.printMap()
        self.printKarboniteMap()

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
    print('Time left: ', gc.get_time_left_ms())


# Unit game logic
def runWorkerLogic(unit, unitInfo, gc):
    # Current location of the unit
    unitLocation = unit.location.map_location()

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    # If there are less than 5 workers, then try to replicate
    if unitInfo.workerCount < 5:
        for direction in directions:
            if gc.can_replicate(unit.id, direction):
                gc.replicate(unit.id, direction)
                return

    # If there are less than 5 factories, then try to blueprint a factory
    if unitInfo.factoryCount < 3:
        if gc.karbonite() > bc.UnitType.Factory.blueprint_cost():
            for direction in directions:
                if gc.can_blueprint(unit.id, bc.UnitType.Factory, direction):
                    gc.blueprint(unit.id, bc.UnitType.Factory, direction)
                    return

    nearbyUnits = gc.sense_nearby_units_by_team(unitLocation, 2, gc.team())
    for nearbyUnit in nearbyUnits:
        # If there are unfinished factories nearby, then try to build them them
        if gc.can_build(unit.id, nearbyUnit.id):
            gc.build(unit.id, nearbyUnit.id)
            return
        # If there are damaged factories nearby, then try to repair them
        elif gc.can_repair(unit.id, nearbyUnit.id):
            gc.repair(unit.id, nearbyUnit.id)
            return
    
    # If there is karbonite nearby, then try to harvest it 
    for direction in directions:
        adjacentLocation = unitLocation.add(direction)
        # Need to try/catch because if adjacentLocation is not on map, then karbonite_at() throws exception
        try:
            if gc.karbonite_at(adjacentLocation) > 0:
                if gc.can_harvest(unit.id, direction):
                    gc.harvest(unit.id, direction)
                    return
        except Exception as e:
            continue
            
    # Search karbonite
    for direction in directions:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return

    return

def runKnightLogic(unit, unitInfo, gc):
    # Current location of the unit
    unitLocation = unit.location.map_location()

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    # Get enemy team
    if gc.team() == bc.Team.Red:
        enemyTeam = bc.Team.Blue
    else: 
        enemyTeam = bc.Team.Red 

    # If knight is in garrison, then do nothing
    if unit.location.is_in_garrison():
        return

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
        direction = unitLocation.direction_to(visibleEnemyUnit)
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
    # Current location of the unit
    unitLocation = unit.location.map_location()

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    # If healer is in garrison, then do nothing
    if unit.location.is_in_garrison():
        return

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
        direction = unitLocation.direction_to(visibleAlliedUnit)
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
    # If the structure is not built, then do nothing
    if not unit.structure_is_built():
        return

    # Try to unload existing units from structure's garrison
    for direction in directions:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            return

    # If the structure can produce a new robot, then
    if gc.can_produce_robot(unit.id, bc.UnitType.Knight): # TODO: 
        gc.produce_robot(unit.id, bc.UnitType.Knight)
        return

    return

def runRocketLogic(unit, unitInfo, gc):
    # TODO: Implement rocket logic
    return


# Earth game logic
def runEarth(gc):
    unitInfo = UnitInfo(gc)

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Worker:
            runWorkerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Knight:
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



