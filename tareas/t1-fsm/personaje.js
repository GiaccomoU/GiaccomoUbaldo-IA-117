"use strict";

const State = require('./state')
const Fsm = require('./fsm')
const eventEmitter = require('./event-emiter')

var inc = 0;

class Descansando extends State{
  accepts(event) {
    console.log("[Descansando]" + JSON.stringify(event));
    return event.msg === "herir";
  }

  onEnter(eventEmitter, fsm) {
    fsm.owner().elementoEnSuArea();
  }

  onUpdate(eventEmitter, fsm) {
    fsm.owner().show();
  }
}

class Molesto extends State {
  accepts(event) {
    console.log("[Molesto]" + JSON.stringify(event));
    return event.msg === "herir";
  }

  onEnter(eventEmitter, fsm) {
    fsm.owner().herir();
  }

  onUpdate(eventEmitter, fsm) {
    fsm.owner().show();
  }
}

class Enojado extends State {
  accepts(event) {
    console.log("[Enojado]" + JSON.stringify(event));
    return event.msg === "sanar";
  }

  onEnter(eventEmitter, fsm) {
    console.log("[Enojado] onEnter" );
    fsm.owner().sanar();
  }

  onUpdate(eventEmitter, fsm) {
    fsm.owner().show();
  }
}

class Furioso extends State {
  accepts(event) {
    console.log("[Furioso]" + JSON.stringify(event));
    return event.msg === "sanar";
  }

  onEnter(eventEmitter, fsm) {
    console.log("[Furioso] onEnter" );
    fsm.owner().sanar();
  }

  onUpdate(eventEmitter, fsm) {
    fsm.owner().show();
  }
}

const states = [new Furioso(), new Enojado(), new Molesto(), new Descansando()];

class Personaje {
  constructor(id) {
    this._id = id;
    this._estado = "Descansando";
    const miFsm = new Fsm(this, states);
    eventEmitter.register(miFsm);
  }

  id() {
    return this._id;
  }

  elementoEnSuArea() {
    if(this._estado === "Descansando"){
      this._estado = "Molesto";
    }
  }

  elementoFueraDeSuArea() {
    if(this._estado === "Molesto"){
      this._estado = "Descansando";
    }
  }

  herir() {
    if(this._estado === "Molesto"){
      this._estado = "Enojado";
    }else if(this._estado === "Enojado"){
      this._estado = "Furioso";
    }else if(this._estado === "Furioso"){
      this._estado = "Furioso";
    }
  }

  sanar() {
    if(this._estado === "Molesto"){
      this._estado = "Descansando";
    }else if(this._estado === "Furioso"){
      this._estado = "Enojado";
    }
  }

  show() {
    if (this._estado === "Descansando") {
      console.log(`[Personaje] ${this.id()} + Descansando`);
    } else if(this._estado === "Molesto") {
      console.log(`[Personaje] ${this.id()} + Molesto` );
    } else if(this._estado === "Enojado") {
      console.log(`[Personaje] ${this.id()} + Enojado` );
    } else {
      console.log(`[Personaje] ${this.id()} + Furioso` );
    }
  }
}

module.exports = Personaje