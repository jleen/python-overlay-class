from ast import Attribute
from types import MethodType


def overlay(overlay_class, base_object):
    '''An overlay is a wrapper around an object,
    shadowing one or more methods of the object's class.

    To construct an overlay around a given base object,
    call this function with the base object along with an
    "overlay class" that defines the methods you wish to
    add or shadow.

    All other attribute accesses (including assignments) will be
    delegated to the wrapped object.'''

    # The wrapper object needs to have two parent classes:
    #   1. the overlay class, for access to the new methods
    #   2. the original class of the base object, for access to the original methods
    #      AND so that the overlaid class conforms to the base class
    #      (otherwise, for example, super() from a method of the base object
    #      wouldn't work when called from an overlay)
    class Overlaid(base_object.__class__):
        # We explicitly define a trivial initializer.
        #
        # The base object was already initialized when it was constructed,
        # before the overlay came into the picture.  Reinitializing it would
        # just reset its state, which is counter to the goal of an overlay.
        #
        # We don’t run the overlay class’s initializer either,
        # since you really shouldn’t define an initializer for an overlay.
        # (An overlay has no storage of its own, so what would you be initializing?)
        def __init__(self):
            pass

        def __getattribute__(self, name):
            try:
                return getattr(overlay_class, name).__get__(self)
            except AttributeError:
                return object.__getattribute__(self, name)

        def __getattr__(self, name):
            # Methods defined in the overlay or the base will have already been resolved
            # by the time we get here. So, anything else should just be delegated
            # to the wrapped object.
            #
            # Note that we can't just allow multiple inheritance to take care of
            # this, because we need to delegate to the original *object*,
            # not just the original *class*.
            #return getattr(base_object, name)
            return getattr(base_object, name)

        def __setattr__(self, name, value):
            # All writes should just go through to the wrapped object.
            setattr(base_object, name, value)

    return Overlaid()
