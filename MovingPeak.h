#pragma once

#include "Namespace.h"
#include "Color.h"
#include "Interval.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Represent a spot of bright color with sharp falloff on either side
 * which moves back and forth across the LED strip.
 *
 * The spot bounces at the strip's ends, and at each bounce reduces in
 * both velocity and intensity.
 */
class MovingPeak : public Pattern {
	private:
		Color baseColor;
		float intensity;
		Interval moveAndDecayInterval;
		int position;
		int increment;
		int bounces;

		void advance();
	public:
		/**
		 * Create a new peak which, at its most intense, is the given
		 * color. It starts at the 0 end of the strip, moving quickly.
		 */
		MovingPeak(const Color& color);

		/**
		 * Set the base intensity (from which the peak's sides will
		 * further fall from).
		 */
		void setIntensity(float intensity);

		/**
		 * Set the peak's current position.
		 * Clamped to [0, STRIP_LENGTH).
		 */
		void setPosition(int position);

		/**
		 * Set the peak's increment (direction of travel).
		 * Calmped to -1 or 1.
		 */
		void setIncrement(int increment);

		/**
		 * Reset the peak's intensity, velocity, and position.
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
};

LED_CONTROLLER_NAMESPACE_EXIT
 
