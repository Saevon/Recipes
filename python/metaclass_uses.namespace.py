# A basic Namespace metaclass for Python
#
# Suppose that you want to conveniently abuse classes as namespaces.
# For me, this means avoiding having to splatter @staticmethod all over my class definitions; it's both repetitive make-work and distracting when I'm looking at the source code.
# Clearly the solution to this problem is a metaclass to do all of the work for me. Here's one, which is deliberately somewhat simple:

from types import FunctionType


class NSMeta(type):
    def __new__(mcs, cname, bases, attrs):
        new_attrs = {}
        for key, method in attrs.items():
            if isinstance(method, FunctionType):
                method = staticmethod(method)
            new_attrs[key] = method

        return type.__new__(mcs, cname, bases, new_attrs)

# Inherit from this class:
class Namespace(object):
    __metaclass__ = NSMeta


# An example:
class uint16(Namespace):
    def encode(val):
        pass

    def decode(data):
        pass
