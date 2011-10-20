#pragma once

#include "Namespace.h"
#include "Color.h"
#include "Interval.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Represent a spot of bright color with sharp falloff on either side
 * which moves back and forth across the LED strip.
 *
 * The spot bounces at the strip's ends, and at each bounce reduces in
 * both velocity and intensity.
 */
class MovingPeak {
	private:
		Color baseColor;
		float intensity;
		Interval moveAndDecayInterval;
		int position;
		int increment;
		int bounces;
		bool expired;

		void advance();
	public:
		/**
		 * Create a new peak which, at its most intense, is the given
		 * color. It starts at the 0 end of the strip, moving quickly.
		 */
		MovingPeak(const Color& color);
		MovingPeak();

		void setColor(const Color& color);

		/**
		 * Set the base intensity (from which the peak's sides will
		 * further fall from).
		 */
		void setIntensity(float intensity);

		/**
		 * Reset the peak's intensity, velocity, and position,
		 * and clear its expired status.
		 */
		void restart();

		/**
		 * Update the peak's position/intensity/velocity, depending on
		 *	elapsed time.
		 * @return whether it changed.
		 */
		bool update();

		/**
		 * Add this peak's colors to the strip, for output.
		 */
		void apply(Color* stripColors);

		bool isExpired();
		void expire();
};

LED_CONTROLLER_NAMESPACE_EXIT
 
