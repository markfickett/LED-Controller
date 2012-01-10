#pragma once

#include "Namespace.h"
#include "Config.h"
#include "Color.h"
#include "Interval.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * A sequence of random Colors which marches along an LED strip.
 */
class RandomMarquee : public Pattern {
	private:
		Color colors[STRIP_LENGTH];
		Interval addColorInterval;
		int startIndex;
		const int brightInterval;
		const float scaleBright, scaleDim;

		void advance();

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
		 */
		RandomMarquee(int brightInterval,
			float scaleBright, float scaleDim);

		/**
		 * Every interval, shift all the Colors one along the strip
		 * and add a new random Color at the beginning.
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
