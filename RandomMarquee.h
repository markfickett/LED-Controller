#pragma once

#include "Namespace.h"
#include "Config.h"
#include "Color.h"
#include "Interval.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

#define BUFFER_LENGTH	STRIP_LENGTH+1

/**
 * A sequence of random Colors which moves along an LED strip.
 *
 * The colors may have fractional positions (sub-pixel; anti-aliased), providing
 * a smoother simulation of moving points of light.
 */
class RandomMarquee : public Pattern {
	private:
		Color colors[STRIP_LENGTH+1];
		Interval addColorInterval;
		int startIndex;
		float startOffset;
		const float increment;
		const int brightInterval;
		const float scaleBright, scaleDim;

		/**
		 * @return whether (true) the advance resulted in a full-index
		 *	advance, in which case a new color need be inserted), or
		 *	(false) if it only changed sub-integer positions.
		 */
		bool advance();

		/**
		 * Put some known colors at the beginning of the marquee.
		 */
		void setStartColors();
	public:
		RandomMarquee();

		/**
		 * @param brightInterval Make every nth color brighter.
		 * @param scaleBright scale factor by which to adjust every
		 *	nth (bright) color
		 * @param scaleDim scale factor by which to adjust all but the
		 *	nth (the dim) colors
		 * @param increment When advancing the color positions, move
		 *	by this amount, in (0, 1.0].
		 */
		RandomMarquee(int brightInterval,
			float scaleBright, float scaleDim, float increment);

		/**
		 * Every interval, shift all the Colors increment along
		 * the strip and add a new random Color at the beginning.
		 *
		 * @return whether the marquee changed (moved)
		 */
		bool update();
		void apply(Color* stripColors);

		/**
		 * Set the millisecond interval between moves.
		 */
		void setInterval(int interval);
};

LED_CONTROLLER_NAMESPACE_EXIT
