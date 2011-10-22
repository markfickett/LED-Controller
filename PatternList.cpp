#include "PatternList.h"

#include <newanddelete.h>

#include "WProgram.h"

LED_CONTROLLER_NAMESPACE_USING

PatternList::PatternList(Pattern* pattern) : next(NULL) {
	this->pattern = pattern;
}

PatternList::PatternList() : pattern(NULL), next(NULL) {}

void PatternList::append(Pattern* pattern) {
	PatternList* list = new PatternList(pattern);
	if (list == NULL) {
		Serial.print("!l");
		Serial.flush();
		return;
	}
	append(list);
}

void PatternList::append(PatternList* next) {
	if (this->next == NULL) {
		this->next = next;
	} else {
		this->next->append(next);
	}
}

void PatternList::removeNext() {
	if (next == NULL) {
		return;
	}

	PatternList* oldNext = next;
	next = oldNext->next;
	oldNext->next = NULL;
	delete oldNext;

	Serial.print("x");
	Serial.flush();
}

bool PatternList::update() {
	bool updated = false;
	if (pattern != NULL) {
		updated |= pattern->update();
	}
	if (next != NULL) {
		updated |= next->update();
		if (next->pattern != NULL && next->pattern->isExpired()) {
			removeNext();
		}
	}
	return updated;
}

void PatternList::apply(Color* stripColors) {
	if (pattern != NULL) {
		pattern->apply(stripColors);
	}
	if (next != NULL) {
		next->apply(stripColors);
	}
}

PatternList::~PatternList() {
	delete next;
	delete pattern;
}

