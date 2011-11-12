#pragma once

#include "Namespace.h"
#include "Config.h"
#include "Color.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Manages the colors of an addressable LED strip.
 *
 * The size of the strip is defined by STRIP_LENGTH.
 */
class LedStrip {
	private:
		Color colors[STRIP_LENGTH];
		const int dataPin;
		const int clockPin;
		const bool reverse;

	public:
		LedStrip(int dataPin, int clockPin, bool reverse=false);

		/** Set the pin modes. */
		void setup();

		/** Clear all the Colors. */
		void clear();

		/**
		 * Send all the Colors.
		 *
		 * This has all the Colors in the internal array send their
		 * bits, and then pauses with clockPin low for an additional
		 * 500 microseconds, causing the WS2081 ICs to switch from
		 * passing values along to showing colors.
		 */
		void send();

		/**
		 * Get the internal color array, so others can adjust it.
		 * The array is of size STRIP_LENGTH.
		 */
		Color* getColors();
};

LED_CONTROLLER_NAMESPACE_EXIT
