#include "MovingPeak.h"
#include "Parameters.h"

#include "WProgram.h"

#define DEFAULT_INTERVAL	10
#define FALLOFF			0.2

LED_CONTROLLER_NAMESPACE_USING

MovingPeak::MovingPeak(const Color& color) :
	moveAndDecayInterval(DEFAULT_INTERVAL)
{
	baseColor = color;
	setIntensity(1.0);
	restart();
}

void MovingPeak::setIntensity(float intensity) {
	this->intensity = constrain(intensity, 0.0, 1.0);
}

void MovingPeak::restart() {
	moveAndDecayInterval.setInterval(DEFAULT_INTERVAL);
	position = 0;
	increment = 1;
}

bool MovingPeak::update() {
	moveAndDecayInterval.update();
	if (moveAndDecayInterval.isExpired()) {
		moveAndDecayInterval.clearExpired();
		advance();
		return true;
	} else {
		return false;
	}
}

void MovingPeak::advance() {
	position += increment;
	boolean bounced = false;
	if (position >= STRIP_LENGTH) {
		bounced = true;
		increment = -1;
	} else if (position <= 0) {
		bounced = true;
		increment = 1;
	}
	if (bounced) {
		// TODO: Eventually decay to death / stop updating.
		moveAndDecayInterval.setInterval(
			moveAndDecayInterval.getInterval()*2);
		intensity *= FALLOFF;
	}
}

void MovingPeak::apply(Color* stripColors) {
	for(int i = 0; i < STRIP_LENGTH; i++) {
		float localIntensity = intensity *
			pow(FALLOFF, abs(i - position));
		stripColors[i].add(baseColor.scaled(localIntensity));
	}
}

