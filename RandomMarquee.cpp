#include "RandomMarquee.h"

#include "WProgram.h"

#define DEFAULT_MOVE_INTERVAL   250

LED_CONTROLLER_NAMESPACE_USING

RandomMarquee::RandomMarquee() : addColorInterval(DEFAULT_MOVE_INTERVAL) {
	startIndex = 0;

	// Put some known values at the start of the marquee.
	colors[0] = Color(0xFF0000); // bright Red
	colors[1] = Color(0x00FF00); // bright Green
	colors[2] = Color(0x0000FF); // bright Blue
	colors[3] = Color(0x010000); // faint red
	colors[4] = Color(0x800000); // 1/2 red (0x80 = 128 out of 256)
}

bool RandomMarquee::update() {
	addColorInterval.update();
	if (addColorInterval.isExpired()) {
		addColorInterval.clearExpired();
		advance();
		colors[startIndex].setRandom();
		// Dim the whole strip, make every fifth color brighter.
		float scaleAmount = startIndex % 5 == 0 ?
			0.03 : 0.005;
		colors[startIndex] = colors[startIndex].scaled(scaleAmount);
		return true;
	} else {
		return false;
	}
}

void RandomMarquee::advance() {
	startIndex = startIndex - 1;
	if (startIndex < 0) {
		startIndex += STRIP_LENGTH;
	}
}

void RandomMarquee::setInterval(int interval) {
	addColorInterval.setInterval(interval);
}

void RandomMarquee::apply(Color* stripColors) {
	int i = 0;
	for(int sourceIndex = startIndex; sourceIndex < STRIP_LENGTH;
		i++, sourceIndex++)
	{
		stripColors[i].add(colors[sourceIndex]);
	}
	for(int sourceIndex = 0; i < STRIP_LENGTH; i++, sourceIndex++) {
		stripColors[i].add(colors[sourceIndex]);
	}
}

