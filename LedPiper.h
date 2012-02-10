#pragma once

#include "Namespace.h"
#include "Config.h"
#include "Color.h"
#include "LedStrip.h"

#include "WProgram.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Manage transferral of color data from Serial (via DataReceiver) to LEDs
 * (via LedStrip).
 *
 * See the examples/ for demo usage.
 */
class LedPiper {
	private:
		LedStrip ledStrip;

		static void unpackColorBytes(
			size_t size, const char* colorBytes, Color* colors);
	public:
		/**
		 * Initialize the internal LedStrip.
		 */
		LedPiper(int dataPin, int clockPin);

		/**
		 * Call the internal LedStrip's setup; clear it and display
		 * the blank (all-black) state.
		 */
		void setup();

		/**
		 * Read the byte array (from serial) and set the Color values
		 * of the LedStrip accordingly, then update the LEDs.
		 */
		void setColorsAndSend(size_t size, const char* colorBytes);

		/**
		 * The expected data key which will be used for color data
		 * sent over Serial. (To be used with DataReceiver::addKey.)
		 */
		static const char* KEY;
};

LED_CONTROLLER_NAMESPACE_EXIT

