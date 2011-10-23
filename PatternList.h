#pragma once

#include "Namespace.h"
#include "Color.h"
#include "Pattern.h"

LED_CONTROLLER_NAMESPACE_ENTER

/**
 * Provide a linked list to hold, update, and apply Patterns.
 *
 * The list also takes care of removing expired patterns.
 */
class PatternList {
	private:
		Pattern* pattern;
		PatternList* next;

		/**
		 * Remove and delete the 'next'. Take over
		 * any subsequent PatternLists.
		 */
		void removeNext();
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
		 * and insert it (taking ownership).
		 */
		void insert(Pattern* pattern);

		/**
		 * Insert the given node after this one. (This is preferable to
		 * append because it is constant time / stack space.)
		 *
		 * If the given node has any subsequent nodes, they are
		 * removed and deleted.
		 *
		 * Takes ownership.
		 */
		void insert(PatternList* next);

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
		 * Call apply on this node's Pattern, and recurr on 'next'.
		 */
		void apply(Color* stripColors);

		/**
		 * Delete any 'next' nodes, as well as any Pattern.
		 */
		~PatternList();
};

LED_CONTROLLER_NAMESPACE_EXIT
