from types import MethodType


def overlay(overlay_class, base_object):
    class Overlaid(overlay_class, _Overlay, base_object.__class__):
        pass
    return Overlaid(base_object)


class _Overlay:
    '''An instance of Overlay is a wrapper around an object,
    shadowing one or more methods of the object's class.
    All other attribute accesses (including assignments) will be
    delegated to the wrapped object.

    An instance of this class itself does nothing useful. It is meant
    to be subclassed, with the subclass defining one or more methods
    to be shadowed.
    '''

    def __init__(self, base):
        # Go through object.__setattr__ to avoid calling our magic setattr,
        # since we don't want to delegate this attribute.
        # (In fact it would be an infinite recursion at this point!)
        object.__setattr__(self, 'base', base)

    def __getattr__(self, name):
        # Methods defined in the overlay will have already been resolved
        # by the time we get here. So, anything else should just be delegated
        # to the wrapped object.
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
