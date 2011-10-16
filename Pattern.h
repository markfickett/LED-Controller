#pragma once

#include "Namespace.h"
#include "Color.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Define an interface for color pattern to be displayed on an LED strip.
 */
class Pattern {
	private:
		bool expired;
	public:
		Pattern();

		/**
		 * Determine the new color pattern to display, based on state,
		 * typically to include elapsed time (for animated patterns).
		 * (Noop default implementation. See
		 * http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1167672075
		 * for pure-virtual discussion.)
		 * @return whether the pattern changed
		 */
		virtual bool update();

		/**
		 * Render this pattern.
		 * (Noop default implementation.)
		 * @param stripColors an array of STRIP_LENGTH Colors to be
		 *	adjusted (added to or set) to show this Pattern
		 */
		virtual void apply(Color* stripColors);

		/**
		 * @return true if this pattern has stopped contributing to the
		 *	displayed color (such as for a Pattern that fades out)
		 */
		bool isExpired();

		/**
		 * Make isExpired return true. Since expiration may result in
		 * garbage collection, it is not reversable.
		 */
		void expire();
};

LED_CONTROLLER_NAMESPACE_EXIT
