const socket = new WebSocket('ws://localhost:8700');

function send(data) {
  socket.send(JSON.stringify(data));
}

function sendScore(RA, RT, RE, BA, BT, BE) {
  send({
    type: 'addScore',
    RA,
    RT,
    RE,
    BA,
    BT,
    BE
  });
}