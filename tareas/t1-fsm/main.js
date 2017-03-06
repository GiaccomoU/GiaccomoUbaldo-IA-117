const eventEmiter = require ('./event-emiter');
const Personaje = require ('./personaje');

/**
 * Ciclo principal
 */
setInterval(() => {
  eventEmiter.update();
  eventEmiter.send("update");
}, 500);

const p1 = new Personaje("p1");
//eventEmiter.send("apagar");

var flip = 0;
setInterval(() => {
  console.log(`flip: ${flip}`);
  if (flip === 0) {
    eventEmiter.send("molestar");
    flip = 0;
  } else if(flip === 1){
    eventEmiter.send("enojar");
    flip = 1;
  }
  else {
    eventEmiter.send("enfurecer");
    flip = 2;
  }
}, 2000);