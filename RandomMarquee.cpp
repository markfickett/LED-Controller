#include "RandomMarquee.h"

#include "WProgram.h"

#define DEFAULT_MOVE_INTERVAL   255/8
#define DEFAULT_BRIGHT_INTERVAL	5
#define DEFAULT_SCALE_BRIGHT	0.02
#define DEFAULT_SCALE_DIM	0.01
#define DEFAULT_INCREMENT	1.0/8.0
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
		startIndex -= startIndex;
		if (startIndex < 0) {
			startIndex = STRIP_LENGTH - 1;
			return true;
		}
	}
	return false;
}

void RandomMarquee::setInterval(int interval) {
	addColorInterval.setInterval(interval);
}

void RandomMarquee::apply(Color* stripColors) {
	int i = 0;
	for(int sourceIndex = startIndex; sourceIndex < STRIP_LENGTH;
		i++, sourceIndex++)
	{
		stripColors[i].add(colors[sourceIndex].scaled(1.0-startOffset));
		stripColors[i+1].add(colors[sourceIndex].scaled(startOffset));
	}
	for(int sourceIndex = 0; i < STRIP_LENGTH; i++, sourceIndex++) {
		stripColors[i].add(colors[sourceIndex].scaled(1.0-startOffset));
		stripColors[i+1].add(colors[sourceIndex].scaled(startOffset));
	}
}

