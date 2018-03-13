import battlecode as bc

class MapInfo():
    def __init__(self, gc):
        self.width = gc.starting_map(bc.Planet.Earth).width
        self.height = gc.starting_map(bc.Planet.Earth).height

        self.startingFriendlyLocations = []
        for unit in gc.my_units():
            self.startingFriendlyLocations.append(unit.location.map_location())

        self.startingEnemyLocations = []
        for startingFriendlyLocation in self.startingFriendlyLocations:
            self.startingEnemyLocations.append(bc.MapLocation(bc.Planet.Earth, self.width - startingFriendlyLocation.x, self.height - startingFriendlyLocation.y))

# Class containing data about all units in current round
class UnitInfo():
    def __init__(self, gc):
        self.myTeam = gc.team()
        if gc.team() == bc.Team.Red:
            self.enemyTeam = bc.Team.Blue
        else: 
            self.enemyTeam = bc.Team.Red 
        
        self.factoryCount = self.workerCount = self.knightCount = self.rangerCount = 0
        self.mageCount = self.healerCount = self.rocketCount = 0
        self.earthFactoryCount = self.earthWorkerCount = self.earthKnightCount = self.earthRangerCount = 0
        self.earthMageCount = self.earthHealerCount = self.earthRocketCount = 0
        self.marsFactoryCount = self.marsWorkerCount = self.marsKnightCount = self.marsRangerCount = 0
        self.marsMageCount = self.marsHealerCount = self.marsRocketCount = 0

        self.earthVisibleEnemyUnits = []
        self.marsVisibleEnemyUnits = []

        self.earthFriendlyUnits = []
        self.marsFriendlyUnits = []

        self.earthFriendlyWoundedUnits = []
        self.marsFriendlyWoundedUnits = []

        self.Research = bc.ResearchInfo()

        for unit in gc.my_units():
            if unit.location.is_on_planet(bc.Planet.Earth):
                self.earthFriendlyUnits.append(unit)
                if unit.health < unit.max_health:
                    self.earthFriendlyWoundedUnits.append(unit)
            elif unit.location.is_on_planet(bc.Planet.Mars):
                self.marsFriendlyUnits.append(unit)
                if unit.health < unit.max_health:
                    self.marsFriendlyWoundedUnits.append(unit)

            if (unit.unit_type == bc.UnitType.Factory):
                self.factoryCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthFactoryCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsFactoryCount += 1
            elif (unit.unit_type == bc.UnitType.Worker):
                self.workerCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthWorkerCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsWorkerCount += 1
            elif (unit.unit_type == bc.UnitType.Knight):
                self.knightCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthKnightCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsKnightCount += 1
            elif (unit.unit_type == bc.UnitType.Ranger):
                self.rangerCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthKnightCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsKnightCount += 1
            elif (unit.unit_type == bc.UnitType.Mage):
                self.mageCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthMageCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsMageCount += 1
            elif (unit.unit_type == bc.UnitType.Healer):
                self.healerCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthHealerCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsHealerCount += 1
            elif (unit.unit_type == bc.UnitType.Rocket):
                self.rocketCount += 1
                if unit.location.is_on_planet(bc.Planet.Earth):
                    self.earthRocketCount += 1
                elif unit.location.is_on_planet(bc.Planet.Mars):
                    self.marsRocketCount += 1

            
            if(unit.location.is_on_map() and unit.location.is_on_planet(bc.Planet.Earth)):
                self.earthVisibleEnemyUnits.extend(gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, self.enemyTeam))
            if(unit.location.is_on_map() and unit.location.is_on_planet(bc.Planet.Mars)):
                self.marsVisibleEnemyUnits.extend(gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, self.enemyTeam))


        self.totalCount = len(gc.my_units())
        self.totalArmyCount = self.totalCount - self.workerCount

        self.totalEarthCount = self.earthFactoryCount + self.earthWorkerCount + self.earthKnightCount + self.earthRangerCount + self.earthMageCount + self.earthHealerCount + self.earthRocketCount
        self.totalEarthArmyCount = self.totalEarthCount - self.earthWorkerCount
        self.totalMarsCount = self.marsFactoryCount + self.marsWorkerCount + self.marsKnightCount + self.marsRangerCount + self.marsMageCount + self.marsHealerCount + self.marsRocketCount
        self.totalmMrsArmyCount = self.totalMarsCount - self.marsWorkerCount