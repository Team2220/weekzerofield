import fms

class MatchScore:
    redAuto = 0
    redTeleop = 0
    redEndgame = 0

    blueAuto = 0
    blueTeleop = 0
    blueEndgame = 0

    def updateArena(self):
        fms.updateRealtimeScore(self.blueAuto, self.redAuto, self.blueTeleop, self.redTeleop, self.blueEndgame, self.redEndgame)
    
    def addScore(self, alliance, state, score):
        if alliance == 'red':
            if state == 'auto':
                self.redAuto += score
            if state == 'teleop':
                self.redTeleop += score
            if state == 'endgame':
                self.redEndgame += score
        if alliance == 'blue':
            if state == 'auto':
                self.blueAuto += score
            if state == 'teleop':
                self.blueTeleop += score
            if state == 'endgame':
                self.blueEndgame += score
        self.updateArena()