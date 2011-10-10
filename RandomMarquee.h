#pragma once

#include "Namespace.h"
#include "Parameters.h"
#include "Color.h"
#include "Interval.h"

#define MOVE_INTERVAL   250

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * A sequence of random Colors which marches along an LED strip.
 */
class RandomMarquee{
	private:
		Color colors[STRIP_LENGTH];
		Interval addColorInterval;
		int startIndex;

		void advance();
	public:
		RandomMarquee();

		/**
		 * Every MOVE_INTERVAL, shift all the Colors one along the strip
		 * and add a new random Color at the beginning.
		 *
		 * @return whether the marquee changed (moved)
		 */
		bool update();
		void apply(Color* stripColors);
};

LED_CONTROLLER_NAMESPACE_EXIT
