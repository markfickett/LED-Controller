/**
 * Demo the addressable LED strip from SparkFun (based on the WS2801 IC).
 *
 * This is heavily based on code by Nathan Seidle of SparkFun Electronics,
 * released in 2011 in the public domain (that is, under the Beerware license).
 * The original example [in version history or at
 * http://www.sparkfun.com/datasheets/Components/LED/LED_Strip_Example.pde ]
 * contains more technical details, which here are noted at relevant points in
 * the code.
 *
 * This example code displays bright red, green, and blue, then trickles
 * random colors down the LED strip.
 *
 * The electrical connections for the strip are:
 *	Power, 5V and Ground (a red/black pair). The listed requirement is 1.8A,
 *		but USB power seems to be sufficient.
 * and data (connect to the end with the arrow pointing into the strip), one of:
 *	4-pin data:
 *		Blue = 5V
 *		Red = SDI (Serial Data Input)
 *		Green = CKI (Clock Input)
 *		Black = GND
 *	5-pin data:
 *		2-pin Red+Black = 5V/GND
 *		Green = CKI
 *		Red = SDI
 */

#include <ledcontroller.h>

using LedController::Color;
using LedController::LedStrip;
using LedController::RandomMarquee;

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

RandomMarquee marquee = RandomMarquee();
LedStrip ledStrip = LedStrip();

void setup() {
	pinMode(PIN_SDI, OUTPUT);
	pinMode(PIN_CKI, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee.update();
	marquee.apply(ledStrip.getColors());
	ledStrip.send(PIN_SDI, PIN_CKI);

	delay(2000);
}

void loop() {
	if (marquee.update()) {
		ledStrip.clear();
		marquee.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

