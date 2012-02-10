/**
 * Test receiving colors over Serial and sending them to the LED strip.
 */

#include <newanddelete.h>
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

