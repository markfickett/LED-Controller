/**
 * Test receiving colors over Serial and sending them to the LED strip.
 */

#include <newanddelete.h>
#include <ledcontroller.h>
#include <DataReceiver.h>

using LedController::LedStrip;
using LedController::Color;

#define PIN_LED_DATA	2	// red wire
#define PIN_LED_CLOCK	3	// green wire
#define PIN_STATUS_LED	13	// on-board

DataReceiver<1> dataReceiver;
LedStrip ledStrip = LedStrip(PIN_LED_DATA, PIN_LED_CLOCK);

#ifdef HALF_PRECISION
void unpackColorBytes(size_t size, const char* colorBytes,
	LedController::Color* colors)
{
	int byteIndex = 0;
	bool upper = false;
	for(int colorIndex = 0; colorIndex < STRIP_LENGTH && byteIndex < size;
		colorIndex++)
	{
		byte channelBuffer[3];
		for(int channel = 0; channel < 3 && byteIndex < size;
			channel++)
		{
			if (upper) {
				channelBuffer[channel] = 0x10 *
					((colorBytes[byteIndex] & 0xF0) >> 4);
				upper = false;
				byteIndex++;
			} else {
				channelBuffer[channel] = 0x10 *
					(colorBytes[byteIndex] & 0x0F);
				upper = true;
			}
		}
		colors[colorIndex].setChannelValues(
			channelBuffer[0], channelBuffer[1], channelBuffer[2]);
	}
}
#else
void unpackColorBytes(size_t size, const char* colorBytes,
	LedController::Color* colors)
{
	for(int c = 0, v = 0; c < STRIP_LENGTH && v + 2 < size; c++, v += 3) {
		colors[c].setChannelValues(
			colorBytes[v], colorBytes[v + 1], colorBytes[v + 2]);
	}
}
#endif

void colorChangeCb(size_t size, const char* colorBytes) {
	digitalWrite(PIN_STATUS_LED, HIGH);
	unpackColorBytes(size, colorBytes, ledStrip.getColors());
	ledStrip.send();
	digitalWrite(PIN_STATUS_LED, LOW);
}

void setup() {
	ledStrip.setup();
	dataReceiver.setup();
	pinMode(PIN_STATUS_LED, OUTPUT);

	ledStrip.clear();
	ledStrip.send();

	dataReceiver.addKey("COLORS", &colorChangeCb);

	dataReceiver.sendReady();
}

void loop() {
	dataReceiver.readAndUpdate();
}

