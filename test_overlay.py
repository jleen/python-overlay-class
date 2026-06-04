from overlay import overlay


class Parent:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count += 1

    def current(self):
        return self.count

    def name(self):
        return 'Parent'

    def self_name(self):
        return self.name()


class Child(Parent):
    def super_name(self):
        return super().name()

    def inc_twice(self):
        self.count += 2

    def name(self):
        return 'Child'


class FooOverlay:
    def name(self):
        return 'Foo'


class BarOverlay:
    def name(self):
        return 'Bar'


class ThriceOverlay:
    def inc(self):
        self.count += 3


def test_child():
    child = Child()
    assert child.name() == 'Child'
    assert child.self_name() == 'Child'
    assert child.super_name() == 'Parent'


def test_overlay():
    foo = overlay(FooOverlay, Child())
    assert foo.name() == 'Foo'
    assert foo.self_name() == 'Foo'
    assert foo.super_name() == 'Parent'


def test_two_overlays():
    foo = overlay(FooOverlay, Child())
    bar = overlay(BarOverlay, foo)
    assert bar.name() == 'Bar'
    assert bar.self_name() == 'Bar'
    assert bar.super_name() == 'Parent'


def test_underlying_access():
    underlying = Parent()
    assert underlying.count == 0
    underlying.inc()
    assert underlying.count == 1

    overlaid = overlay(ThriceOverlay, underlying)
    assert underlying.count == 1
    assert overlaid.count == 1

    underlying.inc()
    assert underlying.count == 2
    assert overlaid.count == 2

    overlaid.inc()
    assert underlying.count == 5
    assert overlaid.count == 5


def test_class_conformance():
    foo = overlay(FooOverlay, Child())
    assert isinstance(foo, Parent)
    assert isinstance(foo, Child)


def test_double_overlay():
    foo = overlay(FooOverlay, Child())
    foofoo = overlay(FooOverlay, foo)
    barfoo = overlay(BarOverlay, foo)
    foobarfoo = overlay(FooOverlay, barfoo)

    assert foofoo.name() == 'Foo'
    assert foofoo.self_name() == 'Foo'
    assert foofoo.super_name() == 'Parent'
    
    assert barfoo.name() == 'Bar'
    assert barfoo.self_name() == 'Bar'
    assert barfoo.super_name() == 'Parent'

    assert foobarfoo.name() == 'Foo'
    assert foobarfoo.self_name() == 'Foo'
    assert foobarfoo.super_name() == 'Parent'