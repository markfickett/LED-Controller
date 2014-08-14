LED Controller
==============

Arduino and Python libraries to control addressable RGB LED strips. (Arduino side, targeting the [WS2812 from SparkFun](https://www.sparkfun.com/products/12027) and the [WS2801 from SparkFun (retired)](https://www.sparkfun.com/products/retired/10312)). Its primary aim is to provide a high-level interface, so the program writer can easily express things like 'I want a blue dot bouncing back and forth' or 'I want to add an orange cast to the whole strip'.

Example
-------

The library has a Python component which can be used to generate color data which is then sent to the C++ side on the Arduino (using [DataReceiver](https://github.com/markfickett/DataReceiver)); it can also be used entirely in C++. The examples directory contains demos for both approaches.

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

Limitations
-----------

Sub-pixel rendering on the Arduino in C++ (simulating points of color that lie between LEDs) seem to require too much computation for reasonably fast animation. Also, no optimization has been done for color computation (addition, lerping) or transmitting colors to the strip. However, color updates can be sent from Python at around 50 per second for a 32-LED strip, or 20Hz for 120 LEDs.

See Also
--------

* [fastspi](http://code.google.com/p/fastspi/) explicitly targets performance, as well as supporting multiple LED controller chipsets.
* [Adafruit_NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel) provides a simple interface on various microcontrollers for various RGB LED controllers.
* Using the library: a [continuous-integration build status light](http://www.markfickett.com/stuff/artPage.php?id=377), housing an LED strip in a plexiglass and paper enclosure.

