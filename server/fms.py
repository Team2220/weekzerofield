import websocket
import json
from time import sleep

ws = websocket.WebSocket()
wsScore = websocket.WebSocket()

wsURL = "ws://172.16.20.5:8080/match_play/websocket"
# scoreURL="ws://127.0.0.1:8080/displays/announcer/websocket?displayId=100"

def initConnections() :
    try :
        ws.connect(wsURL)
        print('Connected to ' + wsURL)
    except ConnectionRefusedError:
        print(f'The connection to {wsURL} was refused. Retrying...')
        sleep(2)
        initConnections()
    # try :
    #     wsScore.connect(scoreURL)
    #     print('Connected to ' + scoreURL)
    # except ConnectionRefusedError:
    #     print(f'The connection to {scoreURL} was refused. Retrying...')
    #     sleep(2)
    #     initConnections()

def getConnectionStatus() :
    if ws.connected :
        return True
    return False

def wsSend(packet) :
    ws.send(packet)
    print(packet)

def subTeam(tnum, pos) :
    wsSend('{"type":"substituteTeam","data":{"team":' + str(tnum) + ',"position":"' + pos + '"}}')

def bypTeam(pos) :
    wsSend('{"type":"toggleBypass","data":"' + pos + '"}')

def startMatch(mute='false') :
    wsSend('{"type":"startMatch","data":{"muteMatchSounds":' + str(mute) + '}}')
    
def abortMatch() :
    wsSend('{"type":"abortMatch"}')

def signalVolunteers() :
    wsSend('{"type":"signalVolunteers"}')

def signalReset() :
    wsSend('{"type":"signalReset"}')

def commitResults() :
   print('err')

def discardResults() :
    print('err')

def setAudienceDisplay(display) :
    wsSend('{"type":"setAudienceDisplay","data":"' + display + '"}')

def setAllianceStationDisplay(display) :
    wsSend('{"type":"setAllianceStationDisplay","data":"' + display + '"}')

def startTimeout(time=480) :
    wsSend('{"type":"startTimeout","data":' + str(time) + '}')

def setTestMatchName(name) :
    wsSend('{"type":"setTestMatchName","data":"' + name + '"}')
    
def updateRealtimeScore(ba, ra, bt, rt, be, re) :
    scoreFormat = {"type":"updateRealtimeScore","data":{"blueAuto":0,"redAuto":0,"blueTeleop":0,"redTeleop":0,"blueEndgame":0,"redEndgame":0}}

    scoreFormat['data']['blueAuto'] = ba
    scoreFormat['data']['redAuto'] = ra
    scoreFormat['data']['blueTeleop'] = bt
    scoreFormat['data']['redTeleop'] = rt
    scoreFormat['data']['blueEndgame'] = be
    scoreFormat['data']['redEndgame'] = re

    toSend = json.dumps(scoreFormat)
    wsSend(toSend)

# def scoreHandler() : 
#     #receive and parse
#     rawmsg = wsScore.recv()
#     msg = json.loads(rawmsg)

#     #ignore if not score update
#     if msg['type'] != 'realtimeScore' :
#         return 0
#     return msg

def timeHandler() :
    rawmsg = ws.recv()
    print(rawmsg)
    msg = json.loads(rawmsg)

    if msg['type'] != 'arenaStatus' :
        return 0
    return msg

def cacheHandler() :
    return ws.recv()

def closeConnections() :
    ws.close()
    wsScore.close()