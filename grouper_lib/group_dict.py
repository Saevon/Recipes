from collections import defaultdict


class GroupDict(object):
    '''
    A List of both pre-sorted and not-sorted items
    '''

    def __init__(self):
        self.__groups = defaultdict(set)
        # All items that are indexed (mapped by the index group)
        self.__indexed_groups = defaultdict(set)
        # All indexes the items have (mapped by the index group)
        self.__indexed_values = defaultdict(set)

        self.__invalid_groups = set()
        self.__duplicates = defaultdict(set)
        self.__hidden_groups = set()

    def remove(self, item):
        '''
        Removes an item from the groups
        '''
        if item.is_pre_sorted:
            self.__indexed_groups[item.indexed_group].discard(item)

        self.__groups[item.group].discard(item)


    def add(self, item, is_hidden=False):
        '''
        Adds an item to the groups
        '''
        if is_hidden:
            self.__hidden_groups.add(item.group)

        if item.is_pre_sorted:
            if item.indexed_group in self.__invalid_groups:
                # This item is part of an invalid group, which can't be handled right now
                return

            sorted_group = self.__indexed_values[item.indexed_group]
            if item.index in sorted_group:
                # The group needs to be invalidated
                self.invalidate(item.indexed_group, item)

                # Don't add the item to any groups, its invalid
                return

            self.__indexed_groups[item.indexed_group].add(item)
            sorted_group.add(item.index)

        self.__groups[item.group].add(item)

    def invalidate(self, indexed_group, item):
        '''
        Invalidates an entire group forever
        '''
        self.__invalid_groups.add(indexed_group)
        self.__duplicates[indexed_group] = set([item])

        dead_items = list(self.__indexed_groups[indexed_group])

        for dead_item in dead_items:
            self.__groups[dead_item.group].remove(dead_item)
            if dead_item.index == item.index:
                self.__duplicates[indexed_group].add(dead_item)

    def iteritems(self):
        '''
        Returns all valid items
        '''
        for item in self.__groups.iteritems():
            yield item

    def is_valid(self):
        '''
        Returns whether there where any invalid items
        '''
        return len(self.__invalid_groups) == 0

    def invalid_groups(self):
        '''
        Returns all invalid groups (as a pair of [group_name, items])
        '''
        for group in self.__invalid_groups:
            yield [group, self.__duplicates[group]]

    def visible_groups(self):
        '''
        Returns all the valid group keys that are visible
        '''
        all_groups = set(
            self.__groups.iterkeys(),
        )

        # Remove hidden items
        all_groups.difference_update(self.__hidden_groups)

        return all_groups


    def get_count(self, group):
        '''
        Returns how many items exist for the given group
        '''
        return len(self.__groups[group])
