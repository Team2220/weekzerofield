import field
import threading
from gpiozero import Device, Button
# from gpiozero.pins.mock import MockFactory
from time import sleep

# from tkgpio import TkCircuit

# initialize the circuit inside the GUI

# configuration = {
#     "width": 300,
#     "height": 200,
#     "buttons": [
#         {"x": 50, "y": 130, "name": "coop", "pin": 4},
#         {"x": 250, "y": 130, "name": "amp", "pin": 17},
#         {"x": 150, "y": 130, "name": "speakerscore", "pin": 18},
#         {"x": 150, "y": 30, "name": "ampscore", "pin": 27}
#     ]
# }

# circuit = TkCircuit(configuration)

m_alliance = 'blue'

coopButton = Button(4)
ampButton = Button(17)

speakerTrigger = Button(18)
ampTrigger = Button(27)


class match(object):
    matchState = 0

    def __init__(self):
        self.matchState = 0

        # self.blueAuto = 0
        # self.redAuto = 0
        # self.blueTele = 0
        # self.redTele = 0
        # self.blueEnd = 0
        # self.redEnd = 0


class amp(object):
    def __init__(self):
        self.notes = 0
        self.secondsRem = 0
        self.notesRem = 0
        self.coop = False


m_amp = amp()
m_match = match()


# def scoring_thread():
#     while True:
#         scores = field.scoreHandler()
#         if scores == 0:
#             continue
#         m_match.blueAuto = scores['data']['Blue']['Score']['AutoPoints']
#         m_match.redAuto = scores['data']['Red']['Score']['AutoPoints']
#         m_match.blueTele = scores['data']['Blue']['Score']['TeleopPoints']
#         m_match.redTele = scores['data']['Red']['Score']['TeleopPoints']
#         m_match.blueEnd = scores['data']['Blue']['Score']['EndgamePoints']
#         m_match.redEnd = scores['data']['Red']['Score']['EndgamePoints']


# scoreUpdater = threading.Thread(target=scoring_thread)


def state_thread():
    while True:
        curr_state = field.timeHandler()
        print(m_match.matchState)
        if curr_state == 0:
            continue
        m_match.matchState = curr_state['data']['MatchState']


stateUpdater = threading.Thread(target=state_thread)

def reconnect():
    while True:
        if field.getConnectionStatus() == False:
            field.closeConnections()
            field.initConnections()

# Match States
# 0=Not Started
# 3=auto
# 4=grace period
# 5=teleop
# 6=post match
# 7=timeout


# def addScore(ba=0, ra=0, bt=0, rt=0, be=0, re=0):
#     m_match.blueAuto += ba
#     m_match.redAuto += ra
#     m_match.blueTele += bt
#     m_match.redTele += rt
#     m_match.blueEnd += be
#     m_match.redEnd += re
#     field.updateRealtimeScore(
#         m_match.blueAuto,
#         m_match.redAuto,
#         m_match.blueTele,
#         m_match.redTele,
#         m_match.blueEnd,
#         m_match.redEnd
#     )


def scoreNote(location):
    if m_match.matchState == 3 or m_match.matchState == 4:  # in auto/grace period
        print('auto')
        if m_alliance == 'red':
            if location == 'speaker':
                field.addScore(ra=5, state=m_match.matchState)
                return 5
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(ra=2, state=m_match.matchState)
                return 2
        if m_alliance == 'blue':
            print('blue')
            if location == 'speaker':
                field.addScore(ba=5, state=m_match.matchState)
                print('scored')
                return 5
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(ba=2, state=m_match.matchState)
                return 2
    if m_match.matchState == 5:  # in teleop
        print('teleop' + str(m_match.matchState))
        if m_alliance == 'red':
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    field.addScore(rt=5, state=m_match.matchState)
                    return 5
                field.addScore(rt=2, state=m_match.matchState)
                return 2
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(rt=1, state=m_match.matchState)
                return 2
        if m_alliance == 'blue':
            print('blue')
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    field.addScore(bt=5, state=m_match.matchState)
                    return 5
                field.addScore(bt=2, state=m_match.matchState)
                print('scored')
                return 2
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(bt=1, state=m_match.matchState)
                return 1
    print('no score' + str(m_match.matchState))
    return 0


# def coopHandler():
#     if coopButton.is_pressed and coop == False and m_amp.notes >= 1:
#         print('coop')
#         coop = True
#         m_amp.secondsRem -= 1


# coop_updater = threading.Thread(target=coopHandler)


def ampHandler():
    while True:

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

def reconnect():
    while True:
        if field.getConnectionStatus() == False:
            field.closeConnections()
            field.initConnections()
            print('reconnecting')
            sleep(2)

reconnect_thread = threading.Thread(target=reconnect)

def pinger():
    while True:
        if field.ping_handler() != 0:
            field.wsSend('{"type":"pong"}')
            sleep(0.1)

pinger_thread = threading.Thread(target=pinger)

# def resetHandler():
#     while True:
#         if m_match.matchState == 6:
#             blueAuto = 0
#             redAuto = 0
#             blueTele = 0
#             redTele = 0
#             blueEnd = 0
#             redEnd = 0
#             m_amp.notes = 0
#             coop = False
#             m_amp.notesRem = 0
#             m_amp.secondsRem = 0


# resetUpdater = threading.Thread(target=resetHandler)


def scoreSpeaker():
    scoreNote('speaker')


def scoreAmp():
    scoreNote('amp')


def activateAmp():
    if ampButton.is_pressed and m_amp.secondsRem <= 0 and m_amp.notesRem <= 0 and m_amp.notes >= 2:
        m_amp.notes = 0
        m_amp.secondsRem = 10
        m_amp.notesRem = 4


# @circuit.run
def main():
    field.initConnections()

    # scoreUpdater.start()
    stateUpdater.start()
    amp_updater.start()
    # coop_updater.start()
    time_updater.start()
    # resetUpdater.start()
    reconnect_thread.start()
    pinger_thread.start()

    print('running')

    speakerTrigger.when_pressed = scoreSpeaker
    ampTrigger.when_pressed = scoreAmp
    ampButton.when_pressed = activateAmp

main()