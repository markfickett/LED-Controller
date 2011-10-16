#pragma once

#include "Namespace.h"
#include "Color.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Provide a doubly linked list to hold, update, and apply Patterns.
 *
 * The list also takes care of removing expired patterns.
 */
class PatternList {
	private:
		Pattern* pattern;
		PatternList* prev;
		PatternList* next;

		void remove();
	public:
		/**
		 * Create a new unconnected list node. The node holds and
		 * takes ownership of the given pattern.
		 */
		PatternList(Pattern* pattern);

		/**
		 * Create a new list node with no Pattern (to use as a root).
		 */
		PatternList();

		/**
		 * Create a new PatternList to hold the given Pattern,
		 * and append it (taking ownership).
		 */
		void append(Pattern* pattern);

		/**
		 * Connect the given node to the end of the list. If applicable,
		 * disconnect its old 'previous' (but keep its 'next's).
		 * Takes ownership.
		 */
		void append(PatternList* next);

		/**
		 * Update this node's Pattern, and recurr.
		 *
		 * After the 'next' updates (if present), if its Pattern
		 * isExpired, remove and delete the 'next' (and consequently
		 * its pattern).
		 *
		 * @return whether this or any subsequent pattern updated.
		 */
		bool update();

		/**
		 * Call this node's Pattern, and recurr.
		 */
		void apply(Color* stripColors);

		/**
		 * Delete any 'next' nodes, as well as any Pattern. This does
		 * not clean up the 'previous' node's link.
		 */
		~PatternList();
};

LED_CONTROLLER_NAMESPACE_EXIT
