#pragma once

#include "Namespace.h"
#include "Config.h"
#include "Color.h"
#include "Interval.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

#define STATE_CHAR_PASSED	'p'
#define STATE_CHAR_FAILED	'f'
#define STATE_CHAR_BROKEN	'b'

/**
 * A Pattern which represents a list of states. Visually, it is a sequence of
 * colors, drawing from a small set of colors (green, black, blinking) which
 * represents a set of states (passing, failed, broken) for tests.
 */
class StateList : public Pattern {
	public:
		typedef enum {
			PASSED,
			FAILED,
			BROKEN
		} State;
	private:
		int numKnownStates;
		bool blinkOn;
		Interval brokenBlinkInterval;
		bool colorsChanged;
		Color* stateColors[STRIP_LENGTH];
		float historyScale;

		static Color colorPassed;
		Color colorPassedDim;
		static Color colorFailed;
		Color colorFailedDim;
		Color colorBroken;
		Color colorBrokenDim;
	public:
		StateList();

		void parseStates(const char* stateString);

		/**
		 * Set the factor by which to scale all but the first (most
		 * recent) state's colors. (Expected: dim all but the current
		 * state.)
		 */
		void setHistoryScale(float scale);

		bool update();
		void apply(Color* stripColors);
};

LED_CONTROLLER_NAMESPACE_EXIT

