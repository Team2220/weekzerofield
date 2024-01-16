import field
import threading
from gpiozero import Button
from time import sleep

m_alliance = 'blue'

coopButton = Button(4)
ampButton = Button(17)

speakerTrigger = Button(18)
ampTrigger = Button(27)

field.initConnections()

blueAuto = 0
redAuto = 0
blueTele = 0
redTele = 0
blueEnd = 0
redEnd = 0

matchState = 0

ampNotes = 0
coop = False
amplifyNotesRem = 0
amplifySecRem = 0

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

def scoreNote(alliance, location) :
    if matchState == 3 or matchState == 4:
        if alliance == 'red' :
            if location == 'speaker' :
               addScore(ra=5)
               return 5
            if location == 'amp' :
               ampNotes += 1
               addScore(ra=2)
               return 2
        if alliance == 'blue' :
            if location == 'speaker' :
                addScore(ba=5)
                return 5
            if location == 'amp' :
                ampNotes += 1
                addScore(ba=2)
                return 2
    if matchState == 5 :
        if alliance == 'red' :
          if location == 'speaker' :
             addScore(rt=2)
             return 2
          if location == 'amp' :
             ampNotes += 1
             addScore(rt=1)
             return 2
        if alliance == 'blue' :
           if location =='speaker' :
              addScore(bt=2)
              return 2
           if location == 'amp' :
              ampNotes += 1
              addScore(bt=1)
              return 1
    return 0

def coopHandler() :
   if coopButton.is_pressed() and coop == False and ampNotes >= 1:
      coop = True
      ampNotes -= 1

coop_updater = threading.Thread(target=coopHandler)
coop_updater.start()

def ampHandler() :
   while True :
      if ampButton.is_pressed() and amplifySecRem == 0 and amplifyNotesRem <= 0 and ampNotes >= 2:
         ampNotes -= 2
         amplifySecRem = 10
         amplifyNotesRem = 4 
      if amplifySecRem <= 0 or amplifyNotesRem <=  0 :
         amplifySecRem = 0
         amplifyNotesRem = 0

amp_updater = threading.Thread(target=ampHandler)
amp_updater.start()

def ampTimer() :
   while True :
      while amplifySecRem > 0 :
         sleep(1)
         amplifySecRem -= 1

time_updater = threading.Thread(target=ampTimer)
time_updater.start()