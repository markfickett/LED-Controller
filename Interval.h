#pragma once

#include "Namespace.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Track time intervals, including handling clock wrapping.
 * Example usage:
 *	Interval i = Interval(500); // timer for 0.5s
 *	...
 *	void loop() {
 *		// Call update() often to check the clock.
 *		if (i.update()) { // return value is isExpired()
 *			// Do something twice a second.
 *			...
 *			i.clearExpired();
 *			// Now isExpired() will not return true until another
 *			// 500ms from when the Interval last expired.
 *		}
 *	}
 */
class Interval {
	private:
		unsigned long intervalMillis;
		unsigned long lastExpiredMillis;
		bool expired;

	public:
		/**
		 * Create a new Interval which (when update() is called) will
		 * set its expired status to true every intervalMillis ms.
		 */
		Interval(unsigned long intervalMillis);

		/**
		 * Check the clock, and set the expired status to true if
		 * at least the interval has elapsed since last expiration.
		 * @return whether the interval is (still) expired
		 */
		bool update();

		bool isExpired();

		/**
		 * Clear the expired status (until a call to update() sets it).
		 */
		void clearExpired();

		/**
		 * Set a new interval in milliseconds. This has no effect on
		 * the expired status, and the new interval is measured from
		 * the last expiration time (not the time of method call).
		 */
		void setInterval(int newIntervalMillis);

		int getInterval();
};

LED_CONTROLLER_NAMESPACE_EXIT
