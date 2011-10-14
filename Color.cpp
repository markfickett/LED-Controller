#include "Color.h"

#include "WProgram.h"

#define BITS_PER_CHANNEL	8
#define CHANNEL_MAX		0xFF

LED_CONTROLLER_NAMESPACE_USING

Color::Color() {
	clear();
}

Color::Color(unsigned long combinedValue) {
	// This necessarily depends on specific implementation details.
	color[0] = combinedValue >> (2*BITS_PER_CHANNEL);
	color[1] = (combinedValue & 0x00FF00) >> (BITS_PER_CHANNEL);
	color[2] = combinedValue & 0x0000FF;
}

void Color::clear() {
	memset(color, 0, sizeof(color));
}

void Color::setRandom() {
	for(int i = 0; i < CHANNELS_PER_COLOR; i++) {
		// random value in [0, CHANNEL_MAX]
		color[i] = random(CHANNEL_MAX);
	}
}

void Color::add(const Color& other) {
	for(int i = 0; i < CHANNELS_PER_COLOR; i++) {
		unsigned int sum = color[i] + other.color[i];
		sum = min(CHANNEL_MAX, sum);
		color[i] = (byte)sum;
	}
}

Color Color::scaled(float f) {
	Color scaledColor = Color();
	for(int i = 0; i < CHANNELS_PER_COLOR; i++) {
		float s = f * float(color[i]);
		s = min(s, float(0xFF));
		s = max(0.0, s);
		scaledColor.color[i] = byte(s);
	}
	return scaledColor;
}

void Color::send(int dataPin, int clockPin) {
	for(int i = 0; i < CHANNELS_PER_COLOR; i++) {
		sendColorByte(dataPin, clockPin, color[i]);
	}
}

void Color::sendColorByte(int dataPin, int clockPin, byte c) {
	for(int bitNum = BITS_PER_CHANNEL-1; bitNum >= 0; bitNum--) {
		digitalWrite(clockPin, LOW);

		byte mask = 1 << bitNum;
		digitalWrite(dataPin, c & mask ? HIGH : LOW);

		// Maximum input clock frequency for the WS2801 is 25MHz,
		// so no delay is required with a 16MHz Arduino Uno.
		digitalWrite(clockPin, HIGH);
	}
}

