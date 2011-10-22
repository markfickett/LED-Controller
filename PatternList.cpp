#include "PatternList.h"

#include <newanddelete.h>

#include "WProgram.h"

LED_CONTROLLER_NAMESPACE_USING

PatternList::PatternList(Pattern* pattern) : prev(NULL), next(NULL) {
	this->pattern = pattern;
}

PatternList::PatternList() : pattern(NULL), prev(NULL), next(NULL) {}

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
		if (next->prev) {
			next->prev->next = NULL;
		}
		next->prev = this;
	} else {
		this->next->append(next);
	}
}

void PatternList::remove() {
	PatternList* oldNext = next;
	PatternList* oldPrev = prev;
	next = prev = NULL;
	if (oldPrev != NULL) {
		oldPrev->next = oldNext;
	}
	if (oldNext != NULL) {
		oldNext->prev = oldPrev;
	}
}

bool PatternList::update() {
	bool updated = false;
	if (pattern != NULL) {
		updated |= pattern->update();
	}
	if (next != NULL) {
		updated |= next->update();
		if (next->pattern != NULL && next->pattern->isExpired()) {
			next->remove();
			delete next;
			Serial.print("x");
			Serial.flush();
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

