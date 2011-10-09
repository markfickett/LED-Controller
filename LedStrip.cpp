#include "LedStrip.h"

#include "WProgram.h"

LedStrip::LedStrip() {
}

void LedStrip::clear() {
	for(int i = 0; i < STRIP_LENGTH; i++) {
		colors[i].clear();
	}
}

void LedStrip::send(int dataPin, int clockPin) {
	for(int i = 0; i < STRIP_LENGTH; i++) {
		colors[i].send(dataPin, clockPin);
	}

	// Pull clock low to put strip into reset/post mode.
	digitalWrite(clockPin, LOW);
	delayMicroseconds(500); // Wait for 500us to go into reset.
}

Color* LedStrip::getColors() {
	return colors;
}

