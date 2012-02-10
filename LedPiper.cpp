#include "LedPiper.h"

LED_CONTROLLER_NAMESPACE_USING

LedPiper::LedPiper(int dataPin, int clockPin) :
	ledStrip(dataPin, clockPin)
{ }

void LedPiper::setup() {
	ledStrip.setup();
	ledStrip.clear();
	ledStrip.send();
}

void LedPiper::setColorsAndSend(size_t size, const char* colorBytes) {
	unpackColorBytes(size, colorBytes, ledStrip.getColors());
	ledStrip.send();
}

#ifdef HALF_PRECISION
void LedPiper::unpackColorBytes(size_t size, const char* colorBytes,
	Color* colors)
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
void LedPiper::unpackColorBytes(size_t size, const char* colorBytes,
	Color* colors)
{
	for(int c = 0, v = 0; c < STRIP_LENGTH && v + 2 < size; c++, v += 3) {
		colors[c].setChannelValues(
			colorBytes[v], colorBytes[v + 1], colorBytes[v + 2]);
	}
}
#endif

const char* LedPiper::KEY = DATA_RECEIVER_COLOR_KEY;
