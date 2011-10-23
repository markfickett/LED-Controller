#include "MovingPeak.h"
#include "Config.h"

#include "WProgram.h"

#define DEFAULT_INTERVAL	10
#define FALLOFF			0.2
#define BOUNCE_LIMIT_DEFAULT	4
#define WINDOW			3

LED_CONTROLLER_NAMESPACE_USING

MovingPeak::MovingPeak(const Color& color) :
	moveAndDecayInterval(DEFAULT_INTERVAL),
	bounces(0)
{
	baseColor = color;
	setIntensity(1.0);
	restart();
}

void MovingPeak::setIntensity(float intensity) {
	this->intensity = constrain(intensity, 0.0, 1.0);
}

void MovingPeak::setPosition(int position) {
	this->position = constrain(position, 0, STRIP_LENGTH-1);
}

void MovingPeak::setIncrement(int increment) {
	this->increment = increment > 0 ? 1 : -1;
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
		bounces++;
		if (bounces >= BOUNCE_LIMIT_DEFAULT) {
			expire();
		}
		moveAndDecayInterval.setInterval(
			moveAndDecayInterval.getInterval()*2);
		intensity *= FALLOFF;
	}
}

void MovingPeak::apply(Color* stripColors) {
	if (isExpired()) {
		return;
	}
	for(int i = max(0, position-WINDOW);
		i < min(STRIP_LENGTH, position+WINDOW+1); i++)
	{
		float localIntensity = intensity *
			pow(FALLOFF, abs(i - position));
		stripColors[i].add(baseColor.scaled(localIntensity));
	}
}

