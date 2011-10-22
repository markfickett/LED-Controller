#pragma once

#include "Namespace.h"

// This is assumed to be 3 by various Color implementation details.
#define CHANNELS_PER_COLOR	3

#ifndef byte
typedef unsigned char byte;
#endif

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Provide convenience methods around colors for an LED strip.
 */
class Color {
	private:
		/**
		 * This is an RGB triple, each channel most significant bit
		 * first (which is the default for bytes, but also necessary
		 * for the {@link send()} implementation.
		 */
		byte color[CHANNELS_PER_COLOR];

		/** @see {@link send()} */
		static void sendColorByte(int dataPin, int clockPin, byte c);

	public:
		/**
		 * Create a new Color, defaulting to black: (0, 0, 0).
		 */
		Color();

		/**
		 * Create a new Color with the given combined-value color.
		 * @param combinedValue a color specified as a 24-bit number,
		 *	for example 0xFF0066 (equivalent to rgb(255, 0, 102))
		 */
		Color(unsigned long combinedValue);

		/** Reset the Color to black. */
		void clear();

		/**
		 * Set the Color to a random value. This sets each channel
		 * to a random number in its linear brightness range.
		 */
		void setRandom();

		/**
		 * Add another Color to this one. Clamp overflow per-channel.
		 */
		void add(const Color& other);

		/**
		 * Get a scaled version of this color.
		 * @param f fraction of this color's brightness (linearly,
		 *	and uniformly across channels)
		 */
		Color scaled(float f);

		/**
		 * Send the Color's data on the given pins. These pins should
		 * previously have been set as digital output pins.
		 *
		 * When clockPin is set high, the WS2801 IC stores the current
		 * dataPin value as grayscale data for the current color
		 * component. When clockPin is low, the IC moves on to the next
		 * bit and it is safe to change the dataPin value.
		 *
		 * @param dataPin "serial gray scale data input" (SDI) on the
		 *	WS2801 IC: to receive color value data
		 * @param clockPin "data clock input" (CKI) on the WS2801 IC:
		 *	the clock pin associated with data input
		 */
		void send(int dataPin, int clockPin);
};

LED_CONTROLLER_NAMESPACE_EXIT
