import battlecode as bc
import random
import sys
import traceback
import time
import os
import rocket
import move
import workers


# Class containing data about all units in current round
class UnitInfo():
    def __init__(self, gc):
        self.factoryCount = self.workerCount = self.knightCount = self.rangerCount = 0
        self.mageCount = self.healerCount = self.rocketCount = 0
        self.totalArmyCount = len(gc.my_units()) - len(workersInformation.workersList)
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
            elif (unit.unit_type == bc.UnitType.Rocket):
                self.rocketCount += 1



def printTimeLeft(gc):
    print("Time left: ", gc.get_time_left_ms())


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
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
            
    # Move randomly
    for direction in directions:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
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
                            #gc.move_robot(unit.id, direction)
                            move.goto(gc, unit.id, unitLocation.add(direction))
                            return
        
        for direction in directions:
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    #gc.move_robot(unit.id, direction)
                    move.goto(gc, unit.id, unitLocation.add(direction))
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
            direction = unitLocation.direction_to(nearbyTeamUnit.location.map_location())
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    #gc.move_robot(unit.id, direction)
                    move.goto(gc, unit.id, unitLocation.add(direction))
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
                                    #gc.move_robot(unit.id, direction)
                                    move.goto(gc, unit.id, unitLocation.add(direction))
                                    return
        # Move randomly
        for direction in directions:
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    #gc.move_robot(unit.id, direction)
                    move.goto(gc, unit.id, unitLocation.add(direction))
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
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return

    # If there are visible enemy units nearby, just run!
    enemies = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, enemyTeam)
    if len(enemies) > 0:
        enemies = sorted(enemies, key=lambda x: x.location.map_location().distance_squared_to(unitLocation))
        enemy_loc = enemies[0].location.map_location()
        reverseEnemyDirection = enemy_loc.direction_to(unitLocation)
        if gc.can_move(unit.id, reverseEnemyDirection):
            #gc.move_robot(unit.id, reverseEnemyDirection)
            move.goto(gc, unit.id, unitLocation.add(reverseEnemyDirection))
            return
            
    # Move randomly
    for direction in directions:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
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
    if unitInfo.rangerCount < max(5, unitInfo.totalArmyCount * 0.6):
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): # TODO: 
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
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
    unitLocation = unit.location.map_location()
    print(len(unit.structure_garrison()))
    # find and load some workers into the rocket
    if len(unit.structure_garrison()) < 4: # TODO: We only load 4 workers for now
        nearbyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, gc.team())

        for nearU in nearbyUnits:
            if nearU.unit_type == bc.UnitType.Worker:
                if gc.can_load(unit.id, nearU.id):
                    gc.load(unit.id, nearU.id)
                    return
    else:
        rocket.launch(gc, gc.starting_map(bc.Planet.Earth), unit.id)
    return


# Earth game logic
def runEarth(gc):
    unitInfo = UnitInfo(gc)

    for worker in workersInformation.workersList:
        workers.runWorkerLogic(worker, unitInfo, workersInformation, gc)


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
    directions = list(bc.Direction)
    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Rocket:
            # ungarrison
            if len(unit.structure_garrison()) > 0:  
                for direction in directions:
                    if gc.can_unload(unit.id, direction):
                        gc.unload(unit.id, direction)
                        for newWorker in gc.sense_nearby_units(unit.location.map_location().add(direction), 0):
                            if newWorker.unit_type == bc.UnitType.Worker:
                                wrk = workers.Worker(newWorker.id)
                                workersInformation.marsWorkersList.append(wrk)
    for worker in workersInformation.marsWorkersList:
        workers.runWorkerLogicMars(worker, workersInformation, gc)
        print("worker running on mars")                    
    return


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
workersInformation = workers.WorkersInfo()

for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Worker:
            workersInformation.workersList.append(workers.Worker(unit.id))

totKarb = workers.initializeWorkersAndGetTotalKarbonite(gc, workersInformation)
workersInformation.maxWorkers = min(totKarb / 150, 20)  #needs tweaking after testing - now /100 - that means at full workers some 33 turns to mine all without the movement
workersInformation.maxFactories = totKarb / 300

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Healer)

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
