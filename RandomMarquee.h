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

		void advance();
	public:
		RandomMarquee();

		/**
		 * Every interval, shift all the Colors one along the strip
		 * and add a new random Color at the beginning.
		 *
		 * @return whether the marquee changed (moved)
		 */
		bool update();
		void apply(Color* stripColors);

		/**
		 * Set the interval between moves.
		 */
		void setInterval(int interval);
};

LED_CONTROLLER_NAMESPACE_EXIT
