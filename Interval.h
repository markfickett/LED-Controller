#pragma once

#include "Namespace.h"

LED_CONTROLLER_NAMESPACE_ENTER

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
		void setInterval(int newIntervalMillis);
};

LED_CONTROLLER_NAMESPACE_EXIT
