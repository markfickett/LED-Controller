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

		/** Send all the Colors. */
		void send(int dataPin, int clockPin);

		/** Get the internal color array, so others can adjust it. */
		Color* getColors();
};
