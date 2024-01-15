import field
import threading

field.initConnections()

blueAuto = 0
redAuto = 0
blueTele = 0
redTele = 0
blueEnd = 0
redEnd = 0

matchState = 0

def scoring_thread() :
    while True :
        scores = field.scoreHandler()
        if scores == 0 :
          continue
        blueAuto = scores['data']['Blue']['Score']['AutoPoints']
        redAuto = scores['data']['Red']['Score']['AutoPoints']
        blueTele = scores['data']['Blue']['Score']['TeleopPoints']
        redTele = scores['data']['Red']['Score']['TeleopPoints']
        blueEnd = scores['data']['Blue']['Score']['EndgamePoints']
        redEnd = scores['data']['Red']['Score']['EndgamePoints']

scoreUpdater = threading.Thread(target=scoring_thread)
scoreUpdater.start()

def state_thread() :
   while True :
      curr_state = field.timeHandler()
      if curr_state == 0 :
         continue
      matchState = curr_state['data']['MatchState']

stateUpdater = threading.Thread(target=state_thread)
stateUpdater.start()

# Match States
# 0=Not Started
# 3=auto
# 4=grace period
# 5=teleop
# 6=post match
# 7=timeout


def addScore(ba=0, ra=0, bt=0, rt=0, be=0, re=0) :
   ba = blueAuto + ba
   ra = redAuto + ra
   bt = blueTele + bt
   rt = redTele + rt
   be = blueEnd + be
   re = redEnd + re
   field.updateRealtimeScore(ba, ra, bt, rt, be, re)