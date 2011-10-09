#pragma once

#include "Parameters.h"
#include "Color.h"

/**
 * Manages the colors of an addressable LED strip.
 */
class LedStrip {
	private:
		Color colors[STRIP_LENGTH];

	public:
		LedStrip();

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
		void send(int dataPin, int clockPin);

		/** Get the internal color array, so others can adjust it. */
		Color* getColors();
};
