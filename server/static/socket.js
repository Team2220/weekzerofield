const socket = new WebSocket('ws://172.16.20.6:8700');

function send(data) {
  socket.send(JSON.stringify(data));
}

function sendScore(alliance, state, score) {
  send({
    type: 'addScore', 'data': { "alliance": alliance, "state": state, "score": score }
  });
  console.log('Score sent');
  alert('Score sent: ' + score);
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

function decrement(element) {
  element = document.getElementById(element);
  let value = element.value;
  if (value > 0) {
    element.value = value - 1;
  }
  if (value == "") {
    element.value = 0;
  }
}

function increment(element) {
  element = document.getElementById(element);
  let value = element.value;
  if (value < 3) {
    element.value = parseInt(value) + 1;
  }
  if (value == "") {
    element.value = 1;
  }
}

//If the user presses the enter key, the score will be calculated
document.addEventListener('keydown', function (event) {
  if (event.keyCode === 13) {
    calcScores();
  }
});

//Gray out the decrement button if the value is 0
function checkDecrement(element) {
  let value = document.getElementById(element).value;
  let downButton = document.getElementById(element + 'down');
  if (value == 0) {
    downButton.style.backgroundColor = 'rgb(84, 84, 84)';
    downButton.style.boxShadow = 'none';
  } else {
    downButton.style.backgroundColor = 'rgb(159, 0, 0)';
    downButton.style.boxShadow = 'black 0px 0px 5px';
  }
}

//Gray out the increment button if the value is 3
function checkIncrement(element) {
  let value = document.getElementById(element).value;
  let upButton = document.getElementById(element + 'up');
  if (value == 3) {
    upButton.style.backgroundColor = 'rgb(84, 84, 84)';
    upButton.style.boxShadow = 'none'
  } else {
    upButton.style.backgroundColor = 'rgb(0,  159, 0)';
    upButton.style.boxShadow = 'black 0px 0px 5px';
  }
}

//Change the alliance color based on the alliance selected
function changeAlliance() {
  let allianceSelector = document.getElementById('allianceSelector');
  let alliance = allianceSelector.value;
  if (alliance == 'red') {
    allianceSelector.style.backgroundColor = 'rgb(159, 0, 0)';
    document.getElementById('body').style.backgroundColor = 'rgb(159, 0, 0)';
  } else {
    allianceSelector.style.backgroundColor = 'rgb(0, 0, 159)';
    document.getElementById('body').style.backgroundColor = 'rgb(0, 0, 159)';
  }
}

//Constantly check if the spinners should be grayed out
setInterval(function () {
  checkDecrement('parked');
  checkIncrement('parked');
  checkDecrement('hanging');
  checkIncrement('hanging');
  checkDecrement('spotlit');
  checkIncrement('spotlit');
  checkDecrement('trap');
  checkIncrement('trap');
}, 100);

//Constantly check if the alliance color should be changed
setInterval(function () {
  changeAlliance();
}, 100);