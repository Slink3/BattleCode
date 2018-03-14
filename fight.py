import battlecode as bc
import random
import info
import move

def findEnemyUnitLocation(gc, unit, enemyUnitsLocation):
    closestEnemyUnitLocation = None
    
    unitLocation = unit.location.map_location()

    if len(enemyUnitsLocation) > 0:
        closestEnemyUnitLocation = enemyUnitsLocation[0]

        # To prevent timeout
        if(gc.get_time_left_ms() < 5000):
            return closestEnemyUnitLocation

        closestEnemyUnitDistance = unitLocation.distance_squared_to(closestEnemyUnitLocation)


    for enemyUnitLocation in enemyUnitsLocation:
        enemyUnitDistance = unitLocation.distance_squared_to(enemyUnitLocation)
        if enemyUnitDistance < closestEnemyUnitDistance:
            closestEnemyUnitLocation = enemyUnitLocation
            closestEnemyUnitDistance = enemyUnitDistance

    return closestEnemyUnitLocation

def findFriendlyUnitLocation(gc, unit, friendlyUnitsLocation):
    closestFriendlyUnitLocation = None

    unitLocation = unit.location.map_location()

    for friendlyUnitLocation in friendlyUnitsLocation:
        if friendlyUnitLocation is not unitLocation:
            closestFriendlyUnitLocation = friendlyUnitLocation

            # To prevent timeout
            if(gc.get_time_left_ms() < 5000):
                return closestEnemyUnitLocation

            closestFriendlyUnitDistance = unitLocation.distance_squared_to(closestFriendlyUnitLocation)
            break

    if not closestFriendlyUnitLocation is None:
        for friendlyUnitLocation in friendlyUnitsLocation:
            if friendlyUnitLocation is not unitLocation:
                friendlyUnitDistance = unitLocation.distance_squared_to(friendlyUnitLocation)
                if friendlyUnitDistance < closestFriendlyUnitDistance:
                    closestFriendlyUnitLocation = friendlyUnitLocation
                    closestFriendlyUnitDistance = unitLocation.distance_squared_to(closestFriendlyUnitLocation)
                
    return closestFriendlyUnitLocation


# Unit game logic
def runKnightLogic(unit, unitInfo, mapInfo, gc):
    # If knight is in garrison, then do nothing
    if not unit.location.is_on_map():
        return

    # Current location of the unit
    unitLocation = unit.location.map_location()

    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

        if unit.location.map_location().planet == bc.Planet.Earth:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyUnitsLocation)
        else:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyUnitsLocation)

        if not FriendlyUnitLocation is None:
            direction = unitLocation.direction_to(FriendlyUnitLocation)
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
        return


    # Randomize array of directions each turn
    randomDirections = move.directions
    random.shuffle(randomDirections)

    
    # If there are enemy units in ability range, then try to javelin them
    if unit.is_ability_unlocked():
        if gc.is_javelin_ready(unit.id):
            javelinRangeEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.ability_range(), unitInfo.enemyTeam)
            for javelinRangeEnemyUnit in javelinRangeEnemyUnits:
                if gc.can_javelin(unit.id, javelinRangeEnemyUnit.id):
                    gc.javelin(unit.id, javelinRangeEnemyUnit.id)
                    return


    # If there are enemy melee range, then try to attack them
    meleeRangeEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), unitInfo.enemyTeam)
    for meleeRangeEnemyUnit in meleeRangeEnemyUnits:
        if gc.can_attack(unit.id, meleeRangeEnemyUnit.id):
            gc.attack(unit.id, meleeRangeEnemyUnit.id)
            return

    '''
    visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.enemyTeam)
    for visibleEnemyUnit in visibleEnemyUnits:
        # If there are visible enemy units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleEnemyUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
    '''

    if not gc.is_move_ready(unit.id):
        return
        
    # Try to move to closest enemy unit
    if unit.location.map_location().planet == bc.Planet.Earth:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.earthVisibleEnemyUnitsLocation)
    else:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.marsVisibleEnemyUnitsLocation)

    if not EnemyUnitLocation is None:
        direction = unitLocation.direction_to(EnemyUnitLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Try to move to starting enemy location
    for startingEnemyLocation in mapInfo.startingEnemyLocations:
        direction = unitLocation.direction_to(startingEnemyLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Move randomly
    for direction in randomDirections:
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    return

def runRangerLogic(unit, unitInfo, mapInfo, gc):
    # If ranger is in garrison or space, then do nothing
    if not unit.location.is_on_map():
        return

    if unit.ranger_is_sniping():
        return

    # Current location of the unit
    unitLocation = unit.location.map_location()

    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

        if unit.location.map_location().planet == bc.Planet.Earth:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyUnitsLocation)
        else:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyUnitsLocation)

        if not FriendlyUnitLocation is None:
            direction = unitLocation.direction_to(FriendlyUnitLocation)
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    #gc.move_robot(unit.id, direction)
                    move.goto(gc, unit.id, unitLocation.add(direction))
                    return
        return

    # Randomize array of directions each turn
    randomDirections = move.directions
    random.shuffle(randomDirections)

    # Attack the closest units
    nearbyEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), unitInfo.enemyTeam)
    for nearbyEnemyUnit in nearbyEnemyUnits:
        if gc.can_attack(unit.id, nearbyEnemyUnit.id):
            gc.attack(unit.id, nearbyEnemyUnit.id)
            return
    
    # If there are enemy units in ability range, then try to snipe them
    if unit.is_ability_unlocked():
        if gc.is_begin_snipe_ready(unit.id):
            if unit.location.map_location().planet == bc.Planet.Earth:
                visibleEnemyUnitsLocation = unitInfo.earthVisibleEnemyUnitsLocation
            else:
                visibleEnemyUnitsLocation = unitInfo.marsVisibleEnemyUnitsLocation

            for eachEnemyUnitLocation in visibleEnemyUnitsLocation:
                '''
                # Snipe only knights, rangers and mages
                if eachEnemyUnitLocation.unit_type == bc.UnitType.Worker or eachEnemyUnitLocation.unit_type == bc.UnitType.Rocket or eachEnemyUnitLocation.unit_type == bc.UnitType.Factory:
                    break
                '''
                if gc.can_begin_snipe(unit.id, eachEnemyUnitLocation):
                    gc.begin_snipe(unit.id, eachEnemyUnitLocation)
                    return

    '''
    visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.enemyTeam)
    for visibleEnemyUnit in visibleEnemyUnits:
        # If there are visible enemy units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleEnemyUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
    '''
        
    if not gc.is_move_ready(unit.id):
        return

    # Try to move to closest enemyUnit
    if unit.location.map_location().planet == bc.Planet.Earth:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.earthVisibleEnemyUnitsLocation)
    else:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.marsVisibleEnemyUnitsLocation)

    if not EnemyUnitLocation is None:
        direction = unitLocation.direction_to(EnemyUnitLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Try to move to starting enemy location
    for startingEnemyLocation in mapInfo.startingEnemyLocations:
        direction = unitLocation.direction_to(startingEnemyLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Move randomly
    for direction in randomDirections:
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    return

'''
def runMageLogic(unit, unitInfo, mapInfo, gc):
    # If mage is in garrison or space, then do nothing
    if not unit.location.is_on_map():
        return

    # get the location of the unit
    unitLocation = unit.location.map_location()

    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return
        
        if unit.location.map_location().planet == bc.Planet.Earth:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyUnitsLocation)
        else:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyUnitsLocation)

        if not FriendlyUnitLocation is None:
            direction = unitLocation.direction_to(FriendlyUnitLocation)
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
        return

    # Randomize array of directions each turn
    randomDirections = move.directions
    random.shuffle(randomDirections)

       


    # look for team members for support for fighting
    nearbyTeamUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.myTeam)
    for nearbyTeamUnit in nearbyTeamUnits:
        direction = unitLocation.direction_to(nearbyTeamUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
        # after moving to where team members are find the appropriate place to attack
            visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.enemyTeam)
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

    if not gc.is_move_ready(unit.id):
        return

    # Try to move to closest enemyUnit
    if unit.location.map_location().planet == bc.Planet.Earth:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.earthVisibleEnemyUnitsLocation)
    else:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.marsVisibleEnemyUnitsLocation)
        
    if not EnemyUnitLocation is None:
        direction = unitLocation.direction_to(EnemyUnitLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Try to move to starting enemy location
    for startingEnemyLocation in mapInfo.startingEnemyLocations:
        direction = unitLocation.direction_to(startingEnemyLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Move randomly
    for direction in randomDirections:
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return

    return
'''

def runHealerLogic(unit, unitInfo, mapInfo, gc):
    # If healer is in garrison or space, then do nothing
    if not unit.location.is_on_map():
        return

    # Current location of the unit
    unitLocation = unit.location.map_location()

    if gc.is_heal_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

        if unit.location.map_location().planet == bc.Planet.Earth:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyUnitsLocation)
        else:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyUnitsLocation)

        if not FriendlyUnitLocation is None:
            direction = unitLocation.direction_to(FriendlyUnitLocation)
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
        return



    # Randomize array of directions each turn
    directions = list(bc.Direction)
    random.shuffle(directions)


    nearbyAlliedUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), unitInfo.myTeam)
    for nearbyAlliedUnit in nearbyAlliedUnits:
        # If there are wounded allied units nearby, then try to heal them
        if gc.can_heal(unit.id, nearbyAlliedUnit.id):
            gc.heal(unit.id, nearbyAlliedUnit.id)
            return

    '''
    visibleAlliedUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.myTeam)
    for visibleAlliedUnit in visibleAlliedUnits:
        # If there are visible allied units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleAlliedUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
    '''

    if not gc.is_move_ready(unit.id):
        return

    # If there are visible enemy units nearby, just run!
    enemies = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.enemyTeam)
    if len(enemies) > 0:
        enemies = sorted(enemies, key=lambda x: x.location.map_location().distance_squared_to(unitLocation))
        enemy_loc = enemies[0].location.map_location()
        reverseEnemyDirection = enemy_loc.direction_to(unitLocation)
        if gc.can_move(unit.id, reverseEnemyDirection):
            #gc.move_robot(unit.id, reverseEnemyDirection)
            move.goto(gc, unit.id, unitLocation.add(reverseEnemyDirection))
            return

    # Try to move to closest friendly unit
    if unit.location.map_location().planet == bc.Planet.Earth:
        FriendlyUnit = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyWoundedUnits)
    else:
        FriendlyUnit = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyWoundedUnits)

    if not FriendlyUnit is None:
        direction = unitLocation.direction_to(FriendlyUnit.location.map_location())
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Try to move to starting enemy location
    for startingEnemyLocation in mapInfo.startingEnemyLocations:
        direction = unitLocation.direction_to(startingEnemyLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Move randomly
    for direction in randomDirections:
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    return
