import pytest

def test_readme():
    # pylint: disable=unused-variable

    from typedobject import TypedObject

    class Point(TypedObject):
        x: int
        y: int

    pt1 = Point(10, 20)
    pt2 = Point(x=10, y=20)
    assert pt1 == pt2

    class Rectangle(TypedObject):
        pt1: Point
        pt2: Point

        def __init__(self, x1, y1, x2, y2):
            self.pt1 = Point(x1, y1)
            self.pt2 = Point(x2, y2)

        def area(self):
            return (self.pt2.x - self.pt1.x) * (self.pt2.y - self.pt1.y)

    rect = Rectangle(1, 1, 3, 3)
    assert rect.area() == 4

    assert isinstance(rect, Rectangle)
    assert not isinstance(rect, Point)

    class RoundedRect(Rectangle):
        corner_radius: int

    rr = RoundedRect(Point(1, 1), Point(3, 3), 1)

    with pytest.raises(AttributeError):
        rect.width = 2

    with pytest.raises(TypeError):
        class RectangleWithAPoint(Rectangle, Point):
            pass

    class TwoDObjectMixin:
        def area(self):
            return self.width() * self.height()

    class Rectangle2(TypedObject, TwoDObjectMixin):
        pt1: Point
        pt2: Point
