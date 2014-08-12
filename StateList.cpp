#include "StateList.h"

#include "Arduino.h"

LED_CONTROLLER_NAMESPACE_USING

#define BROKEN_BLINK_INTERVAL	1000

Color StateList::colorPassed(0x00FF00);
Color StateList::colorFailed(0xFF0000);

StateList::StateList() : numKnownStates(0), blinkOn(false), colorsChanged(true),
	brokenBlinkInterval(BROKEN_BLINK_INTERVAL),
	colorBroken(), colorBrokenDim(),
	colorPassedDim(colorPassed), colorFailedDim(colorFailed),
	historyScale(1.0)
{}

void StateList::parseStates(const char* stateString) {
	colorsChanged = true;
	numKnownStates = 0;
	int i = 0;
	while(stateString[i] != '\0') {
		if (numKnownStates >= STRIP_LENGTH) {
			Serial.print("StateList ran out of space, trauncating: "
				"more than ");
			Serial.print(STRIP_LENGTH);
			Serial.print(" states (characters) in \"");
			Serial.print(stateString);
			Serial.println("\".");
			return;
		}
		bool isFirst = i == 0;
		switch(stateString[i]) {
			case STATE_CHAR_PASSED:
				stateColors[numKnownStates] = isFirst ?
					&colorPassed : &colorPassedDim;
				break;
			case STATE_CHAR_FAILED:
				stateColors[numKnownStates] = isFirst ?
					&colorFailed : &colorFailedDim;
				break;
			case STATE_CHAR_BROKEN:
				stateColors[numKnownStates] = isFirst ?
					&colorBroken : &colorBrokenDim;
				break;
			default:
				Serial.print("Invalid state (character) \"");
				Serial.print(stateString[i]);
				Serial.print("\" at index ");
				Serial.print(i);
				Serial.print(" of state string \"");
				Serial.print(stateString);
				Serial.println("\", trauncating.");
				return;
		}
		i++;
		numKnownStates++;
	}
}

void StateList::setHistoryScale(float scale) {
	if (scale != historyScale) {
		colorsChanged = true;
		historyScale = scale;
		colorPassedDim = colorPassed.scaled(historyScale);
		colorFailedDim = colorFailed.scaled(historyScale);
	}
}

bool StateList::update() {
	bool updated = colorsChanged;
	colorsChanged = false;
	if (brokenBlinkInterval.update()) {
		brokenBlinkInterval.clearExpired();
		updated = true;
		blinkOn = !blinkOn;
		colorBroken.setCombinedValue(blinkOn ? 0xFF0000 : 0x440000);
		colorBrokenDim = colorBroken.scaled(historyScale);
	}
	return updated;
}

void StateList::apply(Color* stripColors) {
	for(int i = 0; i < numKnownStates && i < STRIP_LENGTH; i++) {
		stripColors[i].add(*stateColors[i]);
	}
}

