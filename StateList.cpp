#include "StateList.h"

#include "WProgram.h"

LED_CONTROLLER_NAMESPACE_USING

#define BROKEN_BLINK_INTERVAL	1000

Color StateList::colorPassed(0x004400);
Color StateList::colorFailed(0x440000);

StateList::StateList() : numKnownStates(0), blinkOn(false), statesChanged(true),
	brokenBlinkInterval(BROKEN_BLINK_INTERVAL), colorBroken()
{}

void StateList::parseStates(const char* stateString) {
	statesChanged = true;
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
		switch(stateString[i]) {
			case STATE_CHAR_PASSED:
				stateColors[numKnownStates] = &colorPassed;
				break;
			case STATE_CHAR_FAILED:
				stateColors[numKnownStates] = &colorFailed;
				break;
			case STATE_CHAR_BROKEN:
				stateColors[numKnownStates] = &colorBroken;
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

bool StateList::update() {
	bool updated = statesChanged;
	statesChanged = false;
	if (brokenBlinkInterval.update()) {
		brokenBlinkInterval.clearExpired();
		updated = true;
		blinkOn = !blinkOn;
		colorBroken.setCombinedValue(blinkOn ? 0x440000 : 0x110000);
	}
	return updated;
}

void StateList::apply(Color* stripColors) {
	for(int i = 0; i < numKnownStates && i < STRIP_LENGTH; i++) {
		stripColors[i].add(*stateColors[i]);
	}
}

