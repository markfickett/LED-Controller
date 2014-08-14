/**
 * Demonstrate using DataReceiver to read color data from Serial, and using
 * ColorPiper to transfer (pipe) that color data to the LED strip.
 *
 * See the *.py in this directory, which generate and send colors.
 */


#include <DataReceiver.h>
#include <ledcontroller.h>

#define PIN_LED_DATA	2	// red wire
#define PIN_LED_CLOCK	3	// green wire

DataReceiver<1> dataReceiver;
LedController::LedPiper ledPiper(PIN_LED_DATA, PIN_LED_CLOCK);

void setColorsAndSend(size_t size, const char* colorBytes) {
	ledPiper.setColorsAndSend(size, colorBytes);
}

void setup() {
	dataReceiver.setup();
	ledPiper.setup();
	dataReceiver.addKey(LedController::LedPiper::KEY, &setColorsAndSend);
	dataReceiver.sendReady();
}

void loop() {
	dataReceiver.readAndUpdate();
}

