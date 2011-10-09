#pragma once

/**
 * Provide convenience methods around colors for an LED strip.
 */

class Color {
	public:
		/** Create a new black Color. */
		Color();

		/** Create a new Color with the given combined-value color. */
		Color(long combinedValue);

		/** Reset the Color to black. */
		void clear();

		/** Set the Color to a random value. */
		void setRandom();

		/**
		 * Get the combined Color value, suitable for pushing to the
		 * LED strip. This is a 24 bit value (8 bits for each primary),
		 * in RGB order, each color value most-significant-bit first,
		 * as R7..R0, G7..G0, B7..B0.
		 */
		long getCombinedValue();

		/**
		 * Add another Color to this one. Clamp overflow per-channel.
		 */
		void add(Color& other);

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
	private:
		long combinedValue;
};
