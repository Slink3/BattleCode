import battlecode as bc

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
        self.Research = bc.ResearchInfo()
        self.VisibleEnemyUnits = []
        self.woundedFriendlyUnits = []
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

            
            if(unit.location.is_on_map()):
                self.VisibleEnemyUnits.extend(gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, self.enemyTeam))


        self.totalCount = len(gc.my_units())
        self.totalArmyCount = self.totalCount - self.workerCount