import field

class MatchScore:
    redAuto = 0
    redTeleop = 0
    redEndgame = 0

    blueAuto = 0
    blueTeleop = 0
    blueEndgame = 0

    def updateArena(self):
        field.updateRealtimeScore(self.blueAuto, self.redAuto, self.blueTeleop, self.redTeleop, self.blueEndgame, self.redEndgame)
    
    def addScore(self, alliance, location, score):
        if alliance == 'red':
            if location == 'auto':
                self.redAuto += score
            if location == 'teleop':
                self.redTeleop += score
            if location == 'endgame':
                self.redEndgame += score
        if alliance == 'blue':
            if location == 'auto':
                self.blueAuto += score
            if location == 'teleop':
                self.blueTeleop += score
            if location == 'endgame':
                self.blueEndgame += score
        self.updateArena()