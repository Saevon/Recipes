class Watcher(type):
    '''
    Strange convolted registration
    '''
    def __init__(cls, name, bases, clsdict):
        if name != 'SuperClass':
            cls.register(name)

        super(Watcher, cls).__init__(name, bases, clsdict)

    def awesome(self):
        return self


print('loading SuperClass')

class SuperClass:
    __metaclass__ = Watcher

    CLASSES = []

    @classmethod
    def register(cls, data):
        SuperClass.CLASSES.append(cls)

    print('finished SuperClass')


print('loading Apple')

class Apple(SuperClass):
    print('finished Apple')



print('loading Apple')

class Cherry(SuperClass):
    print('finished Cherry')


print(SuperClass.CLASSES)












class Meta(type):
    def awesome(self):
        return self


class Animal(object):
    __metaclass__ = Meta

class Cat(Animal):
    pass

print(Animal.awesome())
print(Cat.awesome())

try:
    print(Cat().awesome())
except AttributeError:
    print('This should happen, instances do not use metaclass data')
else:
    print('This should not happen')












import re
import types

class ExposePublic(type):
    '''
    Probably better as a class decorator btw
    '''
    def __init__(cls, name, bases, clsdict):
        for attrName in dir(cls):
            match = re.match('expose_(?P<method>get|set)_(?P<name>.*)', attrName)
            if match is None:
                # We only want methods with the right name
                continue

            attr = getattr(cls, attrName)
            if type(attr) != types.MethodType:
                # Ignore non-methods
                continue

            cls.create_route(
                method=match.group('method'),
                route=match.group('name'),
                callback=attr,
            )

    def create_route(cls, method, route, callback):
        print(cls, method, route, callback)


class PublicAPI(object):
    __metaclass__ = ExposePublic

    def expose_get_jobs(request):
        return 404

    def expose_set_jobs(request):
        return 500











import collections

class OrderedAttrsType(type):

    @classmethod
    def __prepare__(meta, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(meta, name, bases, attrs, **kwds):
        print(list(attrs))
        # Do more stuff...

class A():
    __metaclass__ = OrderedAttrsType
    x = 1
    y = 2

# prints ['x', 'y'] rather than ['y', 'x']









class ListDict(dict):
    def __setitem__(self, key, value):
        self.setdefault(key, []).append(value)

class Metaclass(type):

    @classmethod
    def __prepare__(meta, name, bases, **kwds):
        return ListDict()

    def __new__(meta, name, bases, attrs, **kwds):
        print(attrs['foo'])
        # Do more stuff...

class A():
    __metaclass__ = Metaclass

    def foo(self):
        pass

    def foo(self, x):
        pass

# __prepare__ only works in python 3
# prints [<function foo at 0x...>, <function foo at 0x...>] rather than <function foo at 0x...>











class MetaMetaclass(type):
    def __new__(meta, name, bases, attrs):
        def __new__(meta, name, bases, attrs):
            cls = type.__new__(meta, name, bases, attrs)
            cls._label = 'Made in %s' % meta.__name__
            return cls
        attrs['__new__'] = __new__
        return type.__new__(meta, name, bases, attrs)

class China(type):
    __metaclass__ = MetaMetaclass

class Taiwan(type):
    __metaclass__ = MetaMetaclass

class A(object):
    __metaclass__ = China

class B(object):
    __metaclass__ = Taiwan

print(A._label) # Made in China
print(B._label) # Made in Taiwan




# https://stackoverflow.com/questions/392160/what-are-your-concrete-use-cases-for-metaclasses-in-python
#
#




class Final(type):
    def __init__(cls, name, bases, namespace):
        super(Final, cls).__init__(name, bases, namespace)
        for klass in bases:
            if isinstance(klass, Final):
                raise TypeError(str(klass.__name__) + " is final")


class DontInheritFrom(object):
    __metaclass__ = Final

try:
    class Deep(DontInheritFrom):
        pass
except TypeError:
    print('yay final class locked')
else:
    print('well that failed')









class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class TheOne(object):
    __metaclass__ = Singleton

    def __init__(self, value):
        self.value = value


print(TheOne(12).value)
print(TheOne(24).value)











class FilterClass(type):
    @classmethod
    def __prepare__(name, bases, **kwds):
        # Filters MUST be defined in order
        return collections.OrderedDict()

    def __init__(cls, name, bases, clsdict):
        cls._filters = []

        for attrName in dir(cls):
            attr = getattr(cls, attrName)
            if type(attr) != types.MethodType:
                # Ignore non-methods
                continue

            if not hasattr(attr, '_filter'):
                # Its not a filter method
                continue

            cls._filters.append(attr)

def stringfilter(func):
    '''
    Mark a method as a filter that will be auto run
    '''
    func._filter = True
    return func





class StringProcessor(object):
    __metaclass__ = FilterClass

    def __call__(self, string):
        output = string
        for _filter in self._filters:
            output = _filter(self, output)

        return output



class CamelCaseProcessor(StringProcessor):

    @stringfilter
    def remove_double_spaces(self, string):
        return string.replace('  ', ' ')

    @stringfilter
    def remove_double_underscores(self, string):
        return string.replace('__', '_')

    @stringfilter
    def space_to_camel(self, string):
        return re.sub('(\s|_)[a-zA-Z]', lambda match: match.group(0)[1].upper(), string)


class ClassCaseProcessor(CamelCaseProcessor):

    @stringfilter
    def capitalize(self, string):
        return string.capitalize()


camel_caser = CamelCaseProcessor()
class_caser = ClassCaseProcessor()


print(camel_caser('underscore_variable'))
print(class_caser('underscore_variable'))
