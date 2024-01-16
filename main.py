import field
import threading
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory
from time import sleep

from tkgpio import TkCircuit

# initialize the circuit inside the GUI

configuration = {
    "width": 300,
    "height": 200,
    "buttons": [
        {"x": 50, "y": 130, "name": "coop", "pin": 4},
        {"x": 250, "y": 130, "name": "amp", "pin": 17},
        {"x": 150, "y": 130, "name": "speaker", "pin": 18},
        {"x": 150, "y": 30, "name": "amp", "pin": 27}
    ]
}

circuit = TkCircuit(configuration)

m_alliance = 'blue'

coopButton = Button(4)
ampButton = Button(17)

speakerTrigger = Button(18)
ampTrigger = Button(27)

blueAuto = 0
redAuto = 0
blueTele = 0
redTele = 0
blueEnd = 0
redEnd = 0

matchState = 0

class amp(object):
      def __init__(self):
         self.notes = 0
         self.secondsRem = 0
         self.notesRem = 0
         self.coop = False

m_amp = amp()

def scoring_thread():
    while True:
        scores = field.scoreHandler()
        if scores == 0:
            continue
        blueAuto = scores['data']['Blue']['Score']['AutoPoints']
        redAuto = scores['data']['Red']['Score']['AutoPoints']
        blueTele = scores['data']['Blue']['Score']['TeleopPoints']
        redTele = scores['data']['Red']['Score']['TeleopPoints']
        blueEnd = scores['data']['Blue']['Score']['EndgamePoints']
        redEnd = scores['data']['Red']['Score']['EndgamePoints']


scoreUpdater = threading.Thread(target=scoring_thread)


def state_thread():
    while True:
        curr_state = field.timeHandler()
        if curr_state == 0:
            continue
        matchState = curr_state['data']['MatchState']
        print(matchState)


stateUpdater = threading.Thread(target=state_thread)

# Match States
# 0=Not Started
# 3=auto
# 4=grace period
# 5=teleop
# 6=post match
# 7=timeout


def addScore(ba=0, ra=0, bt=0, rt=0, be=0, re=0):
    ba = blueAuto + ba
    ra = redAuto + ra
    bt = blueTele + bt
    rt = redTele + rt
    be = blueEnd + be
    re = redEnd + re
    field.updateRealtimeScore(ba, ra, bt, rt, be, re)


def scoreNote(alliance, location):
   if matchState == 3 or matchState == 4:  # in auto/grace period
        if alliance == 'red':
            if location == 'speaker':
                addScore(ra=5)
                return 5
            if location == 'amp':
                m_amp.notes += 1
                addScore(ra=2)
                return 2
        if alliance == 'blue':
            if location == 'speaker':
                addScore(ba=5)
                return 5
            if location == 'amp':
                m_amp.notes += 1
                addScore(ba=2)
                return 2
   if matchState == 5:  # in teleop
        if alliance == 'red':
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    addScore(rt=5)
                    return 5
                addScore(rt=2)
                return 2
            if location == 'amp':
                m_amp.notes += 1
                addScore(rt=1)
                return 2
        if alliance == 'blue':
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    addScore(bt=5)
                    return 5
                addScore(bt=2)
                return 2
            if location == 'amp':
                ampNotes += 1
                addScore(bt=1)
                return 1
   return 0


def coopHandler():
    if coopButton.is_pressed and coop == False and m_amp.notes >= 1:
        print('coop')
        coop = True
        m_amp.secondsRem -= 1


coop_updater = threading.Thread(target=coopHandler)


def ampHandler():
    while True:
        if ampButton.is_pressed and m_amp.secondsRem <= 0 and m_amp.notesRem <= 0 and m_amp.notes >= 2:
            m_amp.notes -= 2
            m_amp.secondsRem = 10
            m_amp.notesRem = 4
        if m_amp.secondsRem <= 0 or m_amp.notesRem <= 0:
            m_amp.secondsRem = 0
            m_amp.notesRem = 0


amp_updater = threading.Thread(target=ampHandler)


def ampTimer():
    while True:
        while m_amp.secondsRem > 0:
            sleep(1)
            m_amp.secondsRem -= 1


time_updater = threading.Thread(target=ampTimer)


def speakerTriggerHandler():
    while True:
        if speakerTrigger.is_pressed:
            scoreNote(m_alliance, 'speaker')


speakerScoreUpdater = threading.Thread(target=speakerTriggerHandler)


def ampTriggerHandler():
    while True:
        if ampTrigger.is_pressed:
            print('amp')
            scoreNote(m_alliance, 'amp')


ampScoreUpdater = threading.Thread(target=ampTriggerHandler)


def resetHandler():
    while True:
        if matchState == 6:
            blueAuto = 0
            redAuto = 0
            blueTele = 0
            redTele = 0
            blueEnd = 0
            redEnd = 0
            m_amp.notes = 0
            coop = False
            m_amp.notesRem = 0
            m_amp.secondsRem = 0


resetUpdater = threading.Thread(target=resetHandler)


@circuit.run
def main():
    field.initConnections()

    scoreUpdater.start()
    stateUpdater.start()
    amp_updater.start()
    coop_updater.start()
    time_updater.start()
    speakerScoreUpdater.start()
    ampScoreUpdater.start()
    resetUpdater.start()
