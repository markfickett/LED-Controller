#pragma once

/**
 * Track time intervals, including handling clock wrapping.
 */

class Interval {
	private:
		unsigned long intervalMillis;
		unsigned long lastExpiredMillis;
		bool expired;

	public:
		Interval(unsigned long intervalMillis);
		bool update();
		bool isExpired();
		void clearExpired();
};
