#include "RandomMarquee.h"

#include "WProgram.h"

#define DEFAULT_MOVE_INTERVAL   10
#define DEFAULT_BRIGHT_INTERVAL	5
#define DEFAULT_SCALE_BRIGHT	1.0
#define DEFAULT_SCALE_DIM	0.3
#define DEFAULT_INCREMENT	1.0/8
#define MIN_INCREMENT		1e-2

LED_CONTROLLER_NAMESPACE_USING

RandomMarquee::RandomMarquee() : addColorInterval(DEFAULT_MOVE_INTERVAL),
	startIndex(0), brightInterval(DEFAULT_BRIGHT_INTERVAL),
	scaleBright(DEFAULT_SCALE_BRIGHT), scaleDim(DEFAULT_SCALE_DIM),
	increment(DEFAULT_INCREMENT), startOffset(0)
{
	setStartColors();
}

RandomMarquee::RandomMarquee(int brightInterval,
	float scaleBright, float scaleDim, float increment) :
	addColorInterval(DEFAULT_MOVE_INTERVAL),
	startIndex(0), brightInterval(brightInterval),
	scaleBright(scaleBright), scaleDim(scaleDim),
	increment(constrain(increment, MIN_INCREMENT, 1.0)), startOffset(0.0)
{
	setStartColors();
}

void RandomMarquee::setStartColors() {
	colors[0] = Color(0xFF0000); // bright Red
	colors[1] = Color(0x00FF00); // bright Green
	colors[2] = Color(0x0000FF); // bright Blue
	colors[3] = Color(0x010000); // faint red
	colors[4] = Color(0x800000); // 1/2 red (0x80 = 128 out of 256)
}

bool RandomMarquee::update() {
	if (addColorInterval.update()) {
		addColorInterval.clearExpired();
		if (advance()) {
			colors[startIndex].setRandom();
			Serial.print("setRandom at ");
			Serial.print(startIndex);
			Serial.println();
			// Dim the whole strip, make every fifth color brighter.
			float scaleAmount = startIndex % brightInterval == 0 ?
				scaleBright : scaleDim;
			colors[startIndex] =
				colors[startIndex].scaled(scaleAmount);
		}
		return true;
	} else {
		return false;
	}
}

bool RandomMarquee::advance() {
	startOffset -= increment;
	if (startOffset < 0.0) {
		startOffset += 1.0;
		startIndex -= 1;
		if (startIndex < 0) {
			startIndex = BUFFER_LENGTH - 1;
		}
		return true;
	}
	return false;
}

void RandomMarquee::setInterval(int interval) {
	addColorInterval.setInterval(interval);
}

void RandomMarquee::apply(Color* stripColors) {
	int outputIndex = 0;
	int sourceIndex = startIndex + 1;
	while(outputIndex < STRIP_LENGTH) {
		stripColors[outputIndex].add(
			colors[sourceIndex-1].scaled(1.0 - startOffset));
		if (sourceIndex >= BUFFER_LENGTH) {
			sourceIndex = 0;
		}
		stripColors[outputIndex].add(
			colors[sourceIndex].scaled(startOffset));
		outputIndex++;
		sourceIndex++;
	}
}

