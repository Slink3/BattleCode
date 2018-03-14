import battlecode as bc
import random
import sys
import traceback
import time
import os
import move
import workers
import structure
import fight
import info
import json


# Earth game logic
def runEarth(gc, unitInfo, mapInfo):
    for worker in workersInformation.workersList:
        workers.runWorkerLogic(worker, unitInfo, workersInformation, gc)

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Knight:
            fight.runKnightLogic(unit, unitInfo, mapInfo, gc)
        if unit.unit_type == bc.UnitType.Ranger:
            fight.runRangerLogic(unit, unitInfo, mapInfo, gc)
        if unit.unit_type == bc.UnitType.Mage:
            fight.runMageLogic(unit, unitInfo, mapInfo, gc)
        if unit.unit_type == bc.UnitType.Healer:
            fight.runHealerLogic(unit, unitInfo, mapInfo, gc)
        if unit.unit_type == bc.UnitType.Factory:
            structure.runFactoryLogic(unit, unitInfo, mapInfo, gc)
        if unit.unit_type == bc.UnitType.Rocket:
           structure.runRocketLogic(unit, unitInfo, mapInfo, gc)

# Mars game logic
def runMars(gc, unitInfo, mapInfo):
    for worker in workersInformation.marsWorkersList:
        workers.runWorkerLogicMars(worker, workersInformation, gc) 

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Knight:
            fight.runKnightLogic(unit, unitInfo, mapInfo, gc)
        elif unit.unit_type == bc.UnitType.Ranger:
            fight.runRangerLogic(unit, unitInfo, mapInfo, gc)
        elif unit.unit_type == bc.UnitType.Mage:
            fight.runMageLogic(unit, unitInfo, mapInfo, gc)
        elif unit.unit_type == bc.UnitType.Healer:
            fight.runHealerLogic(unit, unitInfo, mapInfo, gc)
        elif unit.unit_type == bc.UnitType.Factory:
            structure.runFactoryLogicMars(unit, unitInfo, mapInfo, gc)
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

mapInfo = info.MapInfo(gc)

#all workers will be stored
workersInformation = workers.WorkersInfo(gc)

for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Worker:
            workersInformation.workersList.append(workers.Worker(unit.id))

totKarb = workers.initializeWorkersAndGetTotalKarbonite(gc, workersInformation)
workersInformation.maxWorkers = min(totKarb / 150, 20)  #needs tweaking after testing - now /100 - that means at full workers some 33 turns to mine all without the movement
workersInformation.maxFactories = totKarb / 300

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Healer)
gc.queue_research(bc.UnitType.Healer)
gc.queue_research(bc.UnitType.Healer)


#grid = json.loads(gc.starting_map(bc.Planet.Earth).to_json())["is_passable_terrain"]
################
#    UPDATE    #
################

while True:
    try:
        unitInfo = info.UnitInfo(gc)
        if(gc.planet() == bc.Planet.Earth):
            #example usage for move
            #move.move(gc, gc.my_units()[0], grid, (20,20))
            runEarth(gc, unitInfo, mapInfo)
        else:
            runMars(gc, unitInfo, mapInfo)

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    gc.next_turn()

    sys.stdout.flush()
    sys.stderr.flush()
