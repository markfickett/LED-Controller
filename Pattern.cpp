#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_USING

Pattern::Pattern() : expired(false) { }

bool Pattern::update() { return false; }

void Pattern::apply(Color* stripColors) {}

bool Pattern::isExpired() { return expired; }

void Pattern::expire() { expired = true; }

