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
            self.__parents[hash_string] = parent

        # Now we add just the groups by themselves
        for group in itertools.chain(parent.keys, parent.synonyms.keys()):
            hash_string = None
            if parent.prefix:
                hash_string = parent.prefix + '~' + group
            else:
                hash_string = group

            self.__parents[hash_string] = parent


    def find(self, item):
        hash_string = self.hash(item)

        return self.__parents.get(hash_string, None)


class ParentGroup(object):

    def __init__(self, name, folder, keys, synonyms=None, hide=False, prefix=None, allow_unsorted=False):
        self.name = name
        self.folder = folder
        self.keys = keys

        if synonyms is None:
            synonyms = {}
        self.synonyms = synonyms

        self.hide = hide

        self.prefix = prefix
        self.allow_unsorted = allow_unsorted

    def __iter__(self):
        for key in self.keys:
            yield key
        for key in self.synonyms.keys():
            yield key

    def clean_group(self, group):
        if group is None:
            return self.name

        if group in self.synonyms.keys():
            return self.synonyms.get(group)

        return group

    def __str__(self):
        return self.name

    def is_valid(self, file):
        has_valid_group_name = file.group_name in self.keys
        has_prefix = file.prefix is not None

        if not has_valid_group_name and not has_prefix:
            # if neither the prefix nor group are valid, then this MUST be an unsorted item
            if not self.allow_unsorted:
                return False
            if file.group_name != self.prefix:
                # Unsorted items must use the parent prefix as the group name
                return False
        elif not has_valid_group_name:
            # Since this isn't one of those unsorted ones, it must be valid...
            return False
        elif has_prefix and self.prefix != file.prefix:
            # Items with a prefix MUST have the right one
            return False

        return True

