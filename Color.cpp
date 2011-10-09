#include "Color.h"

#include "WProgram.h"

#define BITS_PER_CHANNEL	8
#define BITS_PER_COLOR		24

Color::Color() {
	clear();
}

Color::Color(long combinedValue) {
	this->combinedValue = combinedValue;
}

void Color::clear() {
	combinedValue = 0;
}

void Color::setRandom() {
	clear();
	for(int i = 0; i < 3; i++) {
		combinedValue <<= BITS_PER_CHANNEL;
		combinedValue |= random(0xFF);	// random value in [0, 0xFF]
	}
}

void Color::add(Color& other) {
	// TODO: Handle overflow.
	combinedValue = other.combinedValue;
}

long Color::getCombinedValue() {
	return combinedValue;
}

void Color::send(int dataPin, int clockPin) {
	for(int bitNumber = BITS_PER_COLOR-1; bitNumber >= 0; bitNumber--) {
		digitalWrite(clockPin, LOW);

		// Specify the numeric constant 1 as a long so it is 32-bit,
		// as the default is 16-bit (not enough for our 24-bit color).
		long mask = 1L << bitNumber;
		digitalWrite(dataPin, combinedValue & mask ? HIGH : LOW);

		// Maximum input clock frequency for the WS2801 is 25MHz,
		// so no delay is required with a 16MHz Arduino Uno.
		digitalWrite(clockPin, HIGH);
	}
}
