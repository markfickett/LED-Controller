/**
 * Nathan Seidle
 * SparkFun Electronics 2011
 *
 * This code is public domain but you buy me a beer if you use this and we meet
 * someday (Beerware license).
 *
 * Controlling an LED strip with individually controllable RGB LEDs. This stuff
 * is awesome.
 *
 * The SparkFun (individually controllable) RGB strip contains a bunch of
 * WS2801 ICs. These are controlled over a simple data and clock setup. The
 * WS2801 is really cool! Each IC has its own internal clock so that it can do
 * all the PWM for that specific LED for you. Each IC requires 24 bits of
 * 'greyscale' data. This means you can have 256 levels of red, 256 of blue,
 * and 256 levels of green for each RGB LED. REALLY granular.
 *
 * To control the strip, you clock in data continually. Each IC automatically
 * passes the data onto the next IC. Once you pause for more than 500us, each
 * IC 'posts' or begins to output the color data you just clocked in. So, clock
 * in (24bits * 32LEDs = ) 768 bits, then pause for 500us. Then repeat if you
 * wish to display something new.
 *
 * This example code will display bright red, green, and blue, then 'trickle'
 * random colors down the LED strip.
 *
 * You will need to connect 5V/Gnd from the Arduino (USB power seems to be
 * sufficient).
 *
 * For the data pins, please pay attention to the arrow printed on the strip.
 * You will need to connect to the end that is the begining of the arrows (data
 * connection)--->
 *
 * If you have a 4-pin connection:
 * Blue = 5V
 * Red = SDI
 * Green = CKI
 * Black = GND
 *
 * If you have a split 5-pin connection:
 * 2-pin Red+Black = 5V/GND
 * Green = CKI
 * Red = SDI
 */

#include "Parameters.h"
#include "Color.h"
#include "RandomMarquee.h"
#include "LedStrip.h"

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

RandomMarquee marquee = RandomMarquee();
LedStrip ledStrip = LedStrip();
Color stripColors[STRIP_LENGTH];

void setup() {
	pinMode(PIN_SDI, OUTPUT);
	pinMode(PIN_CKI, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee.update();
	marquee.apply(ledStrip.getColors());
	ledStrip.send(PIN_SDI, PIN_CKI);

	Serial.begin(9600);
	Serial.println("Hello! Setup complete.");

	delay(2000);
}

void loop() {
	if (marquee.update()) {
		ledStrip.clear();
		marquee.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

// Take the current strip color array and push it out.
void sendColors() {
	/*
	 * Once the 24 bits have been delivered, the IC immediately relays
	 *	these bits to its neighbor.
	 * Pulling the clock low for 500us or more causes the IC to post the
	 *	data.
	 */

	for(int ledNumber = 0; ledNumber < STRIP_LENGTH; ledNumber++) {
		Color c(stripColors[ledNumber]);
		c.send(PIN_SDI, PIN_CKI);
	}

	// Pull clock low to put strip into reset/post mode.
	digitalWrite(PIN_CKI, LOW);
	delayMicroseconds(500); // Wait for 500us to go into reset.
}
