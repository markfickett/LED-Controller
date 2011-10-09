#include "LedStrip.h"

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
}

Color* LedStrip::getColors() {
	return colors;
}

