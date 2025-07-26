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

    # Three parent classes? Yes, three.
    #   1. the overlay class, for access to the new methods
    #   2. _Overlay, the "engine" that delegates to the underlying object
    #   3. the original class of the base object, so that we conform to it
    #      (otherwise, for example, super() from a method of the base object
    #      wouldn't work when called from an overlay)
    class Overlaid(overlay_class, _Overlay, base_object.__class__):
        pass
    return Overlaid(base_object)


class _Overlay:
    '''A mix-in that implements the guts of the overlay mechanism.

    An instance of this class itself does nothing useful. It is meant
    to be combined with other classes via the "overlay" function above.'''

    def __init__(self, base):
        # Go through object.__setattr__ to avoid calling our magic setattr,
        # since we don't want to delegate the "base" attribute.
        # (In fact it would be an infinite recursion at this point!)
        object.__setattr__(self, 'base', base)

    def __getattr__(self, name):
        # Methods defined in the overlay will have already been resolved
        # by the time we get here. So, anything else should just be delegated
        # to the wrapped object.
        #
        # Note that we can't just allow multiple inheritance to take care of
        # this, because we need to delegate to the original *object*,
        # not just the original *class*.
        value = getattr(self.base, name)
        if type(value) == MethodType:
            # If we're getting a method, it's bound to the base object.
            # We need to rebind it so that its 'self' will point to us,
            # and be able to see our overlay methods.
            return value.__func__.__get__(self)
        else:
            return value

    def __setattr__(self, name, value):
        # All writes should just go through to the wrapped object.
        setattr(self.base, name, value)
