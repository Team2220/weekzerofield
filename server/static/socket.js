const socket = new WebSocket('ws://localhost:8700');

function send(data) {
  socket.send(JSON.stringify(data));
}

function sendScore(alliance, state, score) {
  send({
    type: 'addScore', 'data': {"alliance": alliance, "state": state, "score": score}});
    console.log('Score sent');
}

function calcScores() {
  allianceSelector = document.getElementById('allianceSelector');
  parkedRobots = document.getElementById('parked');
  hangingRobots = document.getElementById('hanging');
  spotlitRobots = document.getElementById('spotlit');
  trapScores = document.getElementById('trap');

  let alliance = allianceSelector.value;
  let parked = parkedRobots.value;
  let hanging = hangingRobots.value;
  let spotlit = spotlitRobots.value;
  let trap = trapScores.value;

  let noLight = hanging - spotlit;
  let light = spotlit;

  let score = 1 * parked + 3 * noLight + 4 * light + 5 * trap;

  sendScore(alliance, '12', score);
};