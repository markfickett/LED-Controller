/**
 * Demonstrate using DataReceiver to read color data from Serial, and using
 * Adafruit_NeoPixel to transfer that color data to a WS2812 LED strip.
 *
 * To be used with ../frompy/*.py which generate and send colors.
 */


#include <DataReceiver.h>

// https://github.com/adafruit/Adafruit_NeoPixel for
// learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide
#include <Adafruit_NeoPixel.h>

#define PIN_LED_DATA	6	// green wire

DataReceiver<1> dataReceiver;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(
    120, PIN_LED_DATA, NEO_GRB + NEO_KHZ800);


/**
 * Copies byte values sent over serial to NeoPixel.
 */
void setColorsAndSend(size_t size, const char* colorBytes) {
  for (int p = 0; p < strip.numPixels() && (p * 3) + 2 < size; p++) {
    int i = p * 3;
    strip.setPixelColor(p, colorBytes[i], colorBytes[i + 1], colorBytes[i + 2]);
  }
  strip.show();
}


void setup() {
	dataReceiver.setup();
	strip.begin();
  strip.show();
	dataReceiver.addKey("COLORS", &setColorsAndSend);
	dataReceiver.sendReady();
}


void loop() {
	dataReceiver.readAndUpdate();
}
