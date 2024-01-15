import websocket
import json

ws = websocket.WebSocket()
wsScore = websocket.WebSocket()

wsURL = "ws://127.0.0.1:8080/match_play/websocket"
scoreURL="ws://127.0.0.1:8080/displays/announcer/websocket?displayId=100"

def initConnections() :
    ws.connect(wsURL)
    wsScore.connect(scoreURL)

def wsSend(packet) :
    ws.send(packet)

def subTeam(tnum, pos) :
    wsSend('{"type":"substituteTeam","data":{"team":' + tnum + ',"position":"' + pos + '"}}')

def bypTeam(pos) :
    wsSend('{"type":"toggleBypass","data":"' + pos + '"}')

def startMatch(mute='false') :
    wsSend('{"type":"startMatch","data":{"muteMatchSounds":' + mute + '}}')
    
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
    wsSend('{"type":"startTimeout","data":' + time + '}')

def setTestMatchName(name) :
    wsSend('{"type":"setTestMatchName","data":"' + name + '"}')
    
def updateRealtimeScore(ba, ra, bt, rt, be, re) :
    wsSend('{"type":"updateRealtimeScore","data":{"blueAuto":1' + ba + '"redAuto":' + ra + ',"blueTeleop":' + bt + ',"redTeleop":' + rt + ',"blueEndgame":' + be + ',"redEndgame":' + re + '}}')

def scoreHandler() : 
    #receive and parse
    rawmsg = wsScore.recv()
    msg = json.loads(rawmsg)

    #ignore if not score update
    if msg['type'] != 'realtimeScore' :
        return 0
    return msg

def timeHandler() :
    rawmsg = wsScore.recv()
    msg = json.loads(rawmsg)

    if msg['type'] != 'matchTime' :
        return 0
    return msg