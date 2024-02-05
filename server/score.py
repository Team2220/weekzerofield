import fms

class MatchScore:
    redAuto = 0
    redTeleop = 0
    redEndgame = 0

    blueAuto = 0
    blueTeleop = 0
    blueEndgame = 0

    def __init__(self):
        self.redAuto = 0
        self.redTeleop = 0
        self.redEndgame = 0

        self.blueAuto = 0
        self.blueTeleop = 0
        self.blueEndgame = 0
    
    def reset(self):
        self.redAuto = 0
        self.redTeleop = 0
        # self.redEndgame = 0

        self.blueAuto = 0
        self.blueTeleop = 0
        # self.blueEndgame = 0

    def updateArena(self):
        fms.updateRealtimeScore(self.blueAuto, self.redAuto, self.blueTeleop, self.redTeleop, self.blueEndgame, self.redEndgame)
        
    
    def addScore(self, alliance, state, score):
        if alliance == 'red':
            if state == 3:
                self.redAuto += score
            if state == 5:
                self.redTeleop += score
            if state == 12:
                self.redEndgame += score
        if alliance == 'blue':
            if state == 3:
                self.blueAuto += score
            if state == 5:
                self.blueTeleop += score
            if state == 12:
                self.blueEndgame += score
        self.updateArena()