import battlecode as bc
import random
import sys
import traceback
import time
import os

# Path class - contains stored path and can return next direction
class Path():
    def __init__(self):
        return super().__init__(**kwargs)

    def getNextDirection():
        directions = list(bc.Direction)
        return random.choice(directions)

    def isFinished():
        return False

# Worker class - each worker can store a path and knows if has a plan - is running along a path
class Worker():
    def __init__(self, id):
        print("Making worker: ", id)
        self.factoryBuildID = 0
        self.hasPlan = False
        self.workerUnitID = id
        self.buildsFactory = False
    
# Class containing data about all units in current round
class UnitInfo():
    def __init__(self, gc):
        self.factoryCount = self.workerCount = self.knightCount = self.rangerCount = 0
        self.mageCount = self.healerCount = 0
        self.totalArmyCount = len(gc.my_units()) - len(workers)
        self.Research = bc.ResearchInfo()
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

    
# Initialization logic
def initializeWorkersAndGetTotalKarbonite():
    eMap = gc.starting_map(bc.Planet.Earth)
    KarboniteNeigbouthood = [[0 for x in range(eMap.width)] for y in range(eMap.height)]
    totalKarbonite = 0
    for x in range(eMap.width):    
        for y in range(eMap.height):
                for a in range(5):
                        for b in range(5):
                            if x + a - 2 >= 0 and y + b - 2 >= 0 and x + a - 2 < eMap.width and y + b - 2 < eMap.height: 
                                location = bc.MapLocation(eMap.planet, x + a - 2, y + b - 2)
                                #KarboniteNeigbouthood[x][y] += eMap.initial_karbonite_at(location)
                totalKarbonite += eMap.initial_karbonite_at(bc.MapLocation(eMap.planet, x, y))
    return totalKarbonite

    
# Unit game logic
def runWorkerLogic(worker, unitInfo, gc):
    # Current location of the unit

    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)

    if not gc.can_sense_unit(worker.workerUnitID):
        workers.remove(worker)
        return

    unitLocation = gc.unit(worker.workerUnitID).location.map_location()
    nearbyUnits = gc.sense_nearby_units(unitLocation, 2)

    if worker.hasPlan:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                gc.move_robot(worker.workerUnitID, direction)
                return

    if worker.buildsFactory:
        # If the factory the worker is building is not finished, build it
        if gc.can_build(worker.workerUnitID, worker.factoryBuildID):
            gc.build(worker.workerUnitID, worker.factoryBuildID)
            return
        else:
            worker.buildsFactory = False
            print("Factory built")
            return  

    # duplicating
    # If there are less than maxWorkers workers, then try to replicate
    if unitInfo.workerCount < maxWorkers:
        for direction in directions:
            if gc.can_replicate(worker.workerUnitID, direction):
                gc.replicate(worker.workerUnitID, direction)
                for unit in gc.sense_nearby_units(unitLocation.add(direction), 0):
                    if unit.unit_type == bc.UnitType.Worker:
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
                    print("Harvesting")
                    return
        except Exception as e:
            continue
            
    # Search karbonite
    for direction in directions:
        if gc.is_move_ready(worker.workerUnitID):
            if gc.can_move(worker.workerUnitID, direction):
                gc.move_robot(worker.workerUnitID, direction)
                return

    #repairing comes last - least important
    for nearbyUnit in nearbyUnits:
        # If there are damaged factories nearby, then try to repair them
        if gc.can_repair(worker.workerUnitID, nearbyUnit.id):
            gc.repair(worker.workerUnitID, nearbyUnit.id)
            return
    
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
    # unit is till to be unloaded
    if unit.location.is_in_garrison() or unit.location.is_in_space():
        return
    # get the location of the unit
    if unit.location.is_on_map():
        unitLocation = unit.location.map_location()

        # Randomize array of directions each turn
        directions = list(bc.Direction)
        random.shuffle(directions)

        # Get enemy team
        enemyTeam = bc.Team.Red
        if gc.team() == bc.Team.Red:
            enemyTeam = bc.Team.Blue
        if not gc.is_attack_ready(unit.id):
            return
        for direction in directions:
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    gc.move_robot(unit.id, direction)
                    return
        # get the closest units
        nearbyEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), enemyTeam)
        for nearbyEnemyUnit in nearbyEnemyUnits:
            if gc.is_attack_ready(unit.id):
                # if are on the level of sniping we can snipe
                if unitInfo.Research.get_level(bc.UnitType.Ranger) > 2:
                    if gc.can_attack(unit.id, nearbyEnemyUnit.id):
                        gc.can_begin_snipe(unit.id, nearbyEnemyUnit)
                        return
                # else we just do a regular attack
                if gc.can_attack(unit.id, nearbyEnemyUnit.id):
                    gc.attack(unit.id, nearbyEnemyUnit.id)
                    return
        # find the location of the enemy units
        visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
        for visibleEnemyUnit in visibleEnemyUnits:
            # check if the enemies are  in the range
            if visibleEnemyUnit.location.is_within_range(unit.attack_range(), visibleEnemyUnit.location):
                # if enemy is in the range then attack
                if gc.is_attack_ready(unit.id):
                    if gc.can_attack(unit.id, visibleEnemyUnit.id):
                        gc.attack(unit.id, visibleEnemyUnit.id)
                        return
            else:
                # if the unit is not in range then move closer to attack
                while visibleEnemyUnit.location.is_within_range(unit.attack_range(), visibleEnemyUnit.location) == False:
                    # if the visible ranger is not in the range then move towards the enemy
                    direction = unitLocation.direction_to(visibleEnemyUnit.location.map_location())
                    if gc.is_move_ready(unit.id):
                        if gc.can_move(unit.id, direction):
                            gc.move_robot(unit.id, direction)
                            return
    return

def runMageLogic(unit, unitInfo, gc):
    # unit is till to be unloaded
    if unit.location.is_in_garrison() or unit.location.is_in_space():
        return
    # get the location of the unit if on the map
    if unit.location.is_on_map():
        unitLocation = unit.location.map_location()
        # Randomize array of directions each turn
        directions = list(bc.Direction)
        random.shuffle(directions)

        # Get enemy team
        enemyTeam = bc.Team.Red
        if gc.team() == bc.Team.Red:
            enemyTeam = bc.Team.Blue
        # look for team members for support for fighting
        nearbyTeamUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, gc.team())
        for nearbyTeamUnit in nearbyTeamUnits:
            direction = unitLocation.direction_to(nearbyTeamUnit.location.map_loaction())
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    gc.move_robot(unit.id, direction)
                    return
            # after moving to where team members are find the appropriate place to attack
                visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
                # check if the enemies are  in the range
                for visibleEnemyUnit in visibleEnemyUnits:
                    if visibleEnemyUnit.location.is_within_range(unit.attack_range(), visibleEnemyUnit.location):
                        # if enemy is in the range then attack
                        if gc.is_attack_ready(unit.id):
                            if gc.can_attack(unit.id, visibleEnemyUnit.id):
                                gc.attack(unit.id, visibleEnemyUnit.id)
                                return
                    else:
                        # if the unit is not in range then move closer to attack
                        while visibleEnemyUnit.location.is_within_range(unit.attack_range(), visibleEnemyUnit.location) == False:
                            # if the visible ranger is not in the range then move towards the enemy
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

    visibleAlliedUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, gc.team())
    for visibleAlliedUnit in visibleAlliedUnits:
        # If there are visible allied units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleAlliedUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return

    # If there are visible enemy units nearby, just run!
    enemies = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
    if len(enemies) > 0:
        enemies = sorted(enemies, key=lambda x: x.location.map_location().distance_squared_to(unitLocation))
        enemy_loc = enemies[0].location.map_location()
        reverseEnemyDirection = enemy_loc.direction_to(unitLocation)
        if gc.can_move(unit.id, reverseEnemyDirection):
            gc.move_robot(unit.id, reverseEnemyDirection)
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
    if unitInfo.rangerCount < max(5, unitInfo.totalArmyCount * 0.45):
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
            print("Producing ranger")
            return

    # If there are less than 5 mage, then produce a mage
    if unitInfo.mageCount < max(5, unitInfo.totalArmyCount * 0.15):
        if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
            gc.produce_robot(unit.id, bc.UnitType.Mage)
            print("Producing mage")
            return

    # If there are less than 5 rangers, then produce a healer
    if unitInfo.healerCount < unitInfo.totalArmyCount * 0.05:
        if gc.can_produce_robot(unit.id, bc.UnitType.Healer): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Healer)
            print("Producing healer")
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



#all workers will be stored
workers = []
for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Worker:
            workers.append(Worker(unit.id))
            print("Worker added: ", unit.id)

totKarb = initializeWorkersAndGetTotalKarbonite()
maxWorkers = min(totKarb / 150, 20)  #needs tweaking after testing - now /100 - that means at full workers some 33 turns to mine all without the movement
maxFactories = totKarb / 300

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



