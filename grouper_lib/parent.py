import itertools



class ParentFinder(object):
    '''
    Finds which parent an item should go under
    '''

    def __init__(self):
        self.__parents = {}

    def hash(self, item):
        if item.prefix:
            return item.prefix
        else:
            return item.group_name

    def add(self, parent):
        # Make sure we can find unsorted items
        # (regardless whether the group allows it, we need to claffisy it to reject them)
        if parent.prefix is not None:
            hash_string = parent.prefix
            self.__parents[hash_string.lower()] = parent

        # Now we add just the groups by themselves
        for group in parent.keys():
            hash_string = None
            if parent.prefix:
                hash_string = parent.prefix + '~' + group
            else:
                hash_string = group

            self.__parents[hash_string.lower()] = parent

    def find(self, item):
        hash_string = self.hash(item)

        return self.__parents.get(hash_string.lower(), None)


class ParentGroup(object):

    def __init__(self, name, folder, keys, synonyms=None, hide=False, prefix=None, allow_unsorted=False):
        '''
        allow_unsorted:   Allows arbitrary subgroups??
        '''
        self.name = name
        self.folder = folder
        self._keys = keys

        if synonyms is None:
            synonyms = {}
        self.synonyms = {key.lower(): val for key,val in synonyms.items()}

        self.hide = hide

        self.prefix = prefix
        self.allow_unsorted = allow_unsorted

        if self.allow_unsorted:
            self._keys.append('Misc')

    def keys(self):
        for key in self._keys:
            yield key.lower()
        for key in self.synonym_keys():
            yield key.lower()

    def synonym_keys(self):
        for key in self.synonyms.keys():
            yield key.lower()

    def clean_group(self, group):
        if group is None:
            return self.name

        if group.lower() in self.synonym_keys():
            return self.synonyms.get(group.lower())

        return group

    def __str__(self):
        return self.name

    def check_validity(self, file):
        has_valid_group_name = file.group_name.lower() in self.keys()
        has_prefix = file.prefix is not None

        if not has_valid_group_name and not has_prefix:
            # if neither the prefix nor group are valid, then this MUST be an unsorted item

            # Unsorted files are completely disallowed
            if not self.allow_unsorted:
                return "Unsorted item"

            # Unsorted items must use the parent prefix as the group name
            #   Unless they're already in the appropriate folder
            if file.group_name.lower() != self.prefix.lower():
                return "Unsorted item whose prefix isn't the Group Name"

        elif not has_valid_group_name:
            if self.allow_unsorted:
                # FIXME: don't edit here
                file.group_name = 'Misc'
            else:
                # Since this isn't one of those unsorted ones, it must be valid...
                return "Invalid Subgroup: {}".format(file.group_name)
        elif has_prefix and self.prefix.lower() != file.prefix.lower():
            # Items with a prefix MUST have the right one
            return "Invalid Parent Group (prefix): {}".format(file.prefix)

        return None

