LED Controller
==============

Arduino library to control an addressable RGB LED strip (specifically, [this one from SparkFun](http://www.sparkfun.com/products/10312). Its primary aim is to provide a high-level interface, so the program writer can easily express things like 'I want a blue dot bouncing back and forth' or 'I want to add an orange cast to the whole strip'.

Example
-------

	#include <ledcontroller.h>
	Color orange(0xFF6600);
	RandomMarquee marquee; // manages an array of colors
	LedStrip ledStrip(PIN_DATA, PIN_CLOCK);
	void setup() {
		ledStrip.setup(); // set pin modes
	}
	void loop() {
		// marquee has a timeout, only changes after some ms
		if (marquee.update()) {
			// clear for the next 'frame'
			ledStrip.clear();
			// always put a dim orange dot on the 5th LED
			ledStrip.getColors()[4].add(orange.scaled(0.5));
			// add marquee's colors to the output buffer
			marquee.apply(ledStrip.getColors());
			// push to the LED strip
			ledStrip.send();
		}
	}

The examples directory contains runnable .pde example code.

Limitations
-----------

Sub-pixel rendering (simulating points of color that lie between LEDs) seem to require too much computation for reasonably fast animation as the library is designed. Also, no optimization has been done for color computation (addition, lerping) or transmitting colors to the strip.

See Also
--------

[fastspi](http://code.google.com/p/fastspi/) explicitly targets performance, as well as supporting multiple LED controller chipsets.

