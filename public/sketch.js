let trigger = false;
let triggerTime = 0;

function setup() {
  createCanvas(windowWidth, windowHeight);
  noStroke();
}

function draw() {
  background(0, 10); // subtle fade effect

  if (trigger && millis() - triggerTime < 1000) {
    for (let i = 0; i < 50; i++) {
      fill(random(255), 0, random(255), 150);
      ellipse(random(width), random(height), random(10, 100));
    }
  }
}

function activateTrigger() {
  trigger = true;
  triggerTime = millis();
}