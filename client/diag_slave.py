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


def state_thread():
    while True:
        curr_state = field.timeHandler()
        print(m_match.matchState)
        if curr_state == 0:
            continue
        m_match.matchState = curr_state['data']['MatchState']


stateUpdater = threading.Thread(target=state_thread)


def scoreNote(location):
    if m_match.matchState == 3 or m_match.matchState == 4:  # in auto/grace period
        print('auto')
        if m_alliance == 'red':
            if location == 'speaker':
                field.addScore(ra=5)
                return 5
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(ra=2)
                return 2
        if m_alliance == 'blue':
            print('blue')
            if location == 'speaker':
                field.addScore(ba=5)
                print('scored')
                return 5
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(ba=2)
                return 2
    if m_match.matchState == 5:  # in teleop
        print('teleop' + str(m_match.matchState))
        if m_alliance == 'red':
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    field.addScore(rt=5)
                    return 5
                field.addScore(rt=2)
                return 2
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(rt=1)
                return 2
        if m_alliance == 'blue':
            print('blue')
            if location == 'speaker':
                if m_amp.secondsRem > 0 or m_amp.notesRem > 0:
                    field.addScore(bt=5)
                    return 5
                field.addScore(bt=2)
                print('scored')
                return 2
            if location == 'amp':
                m_amp.notes += 1
                field.addScore(bt=1)
                return 1
    print('no score' + str(m_match.matchState))
    return 0


def scoreSpeaker():
    scoreNote('speaker')


def scoreAmp():
    scoreNote('amp')


def testScoring():
    while True:
        scoreSpeaker()
        sleep(1)
        scoreAmp()
        sleep(1)
        print('scored')

scoringtest_thread = threading.Thread(target=testScoring)

def main():
    field.initConnections()

    stateUpdater.start()
    scoringtest_thread.start()

main()