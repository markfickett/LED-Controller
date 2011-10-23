#pragma once

/**
 * Define the LED Controller library namespace and related macros.
 */

#define LED_CONTROLLER_VERSION v0_1

#define LED_CONTROLLER_NAMESPACE LedController

#define LED_CONTROLLER_NAMESPACE_ENTER namespace LED_CONTROLLER_NAMESPACE { \
namespace LED_CONTROLLER_VERSION {

#define LED_CONTROLLER_NAMESPACE_EXIT } \
using namespace LED_CONTROLLER_VERSION; \
}

#define LED_CONTROLLER_NAMESPACE_USING using namespace LED_CONTROLLER_NAMESPACE;

