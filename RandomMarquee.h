#pragma once

#include "Parameters.h"
#include "Color.h"
#include "Interval.h"

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
		bool update();
		void apply(Color* stripColors);
};
