import battlecode as bc
import random
import sys
import traceback
import time
import os
import rocket
import move
import workers
import structure
import fight
import info
import json

def printTimeLeft(gc):
    print("Time left: ", gc.get_time_left_ms())


# Earth game logic
def runEarth(gc):
    unitInfo = info.UnitInfo(gc)

    for worker in workersInformation.workersList:
        workers.runWorkerLogic(worker, unitInfo, workersInformation, gc)

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Knight:
            fight.runKnightLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Ranger:
            fight.runRangerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Mage:
            fight.runMageLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Healer:
            fight.runHealerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Factory:
            structure.runFactoryLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Rocket:
            structure.runRocketLogic(unit, unitInfo, gc)

    printTimeLeft(gc)

# Mars game logic
def runMars(gc):
    unitInfo = info.UnitInfo(gc)

    for worker in workersInformation.marsWorkersList:
        workers.runWorkerLogicMars(worker, workersInformation, gc) 

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Knight:
            fight.runKnightLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Ranger:
            fight.runRangerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Mage:
            fight.runMageLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Healer:
            fight.runHealerLogic(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Factory:
            structure.runFactoryLogicMars(unit, unitInfo, gc)
        elif unit.unit_type == bc.UnitType.Rocket:
            structure.runRocketLogicMars(unit, workers, workersInformation, gc)
                              
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
workersInformation = workers.WorkersInfo(gc)

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

#grid = json.loads(gc.starting_map(bc.Planet.Earth).to_json())["is_passable_terrain"]
################
#    UPDATE    #
################

while True:
    try:
        if(gc.planet() == bc.Planet.Earth):
            #example usage for move
            #move.move(gc, gc.my_units()[0], grid, (20,20))
            runEarth(gc)
        else:
            runMars(gc)

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    gc.next_turn()

    sys.stdout.flush()
    sys.stderr.flush()
