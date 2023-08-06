import pytest
from typedobject import TypedObject


def test_no_dunder():
    with pytest.raises(TypeError):
        # pylint: disable=unused-variable
        class X(TypedObject):
            __hello__: int

def test_superprivate():
    class X(TypedObject):
        __hello: int

        def foo(self):
            return self.__hello

    x = X(1)
    assert x.foo() == 1
