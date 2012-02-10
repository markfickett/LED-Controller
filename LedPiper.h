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
 */
class LedPiper {
	private:
		LedStrip ledStrip;
		static void unpackColorBytes(
			size_t size, const char* colorBytes, Color* colors);
	public:
		LedPiper(int dataPin, int clockPin);
		void setup();
		void setColorsAndSend(size_t size, const char* colorBytes);
		static const char* KEY;
};

LED_CONTROLLER_NAMESPACE_EXIT

