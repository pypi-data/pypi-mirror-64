from itertools import chain
from typing import (Iterable,
                    List,
                    Sequence)

from .core.delaunay import Triangulation
from .core.utils import (contour_to_segments as _contour_to_segments,
                         flatten as _flatten)
from .hints import (Contour,
                    Point,
                    Segment,
                    Triangle)

Triangulation = Triangulation


def delaunay(points: Iterable[Point]) -> Triangulation:
    """
    Returns Delaunay triangulation of the points.

    :param points: points to triangulate
    :returns: triangulation of the points.
    """
    return Triangulation.from_points(points)


def constrained_delaunay(border: Contour,
                         holes: Sequence[Contour] = (),
                         *,
                         extra_points: Sequence[Point] = (),
                         extra_constraints: Iterable[Segment] = ()
                         ) -> Triangulation:
    """
    Returns constrained Delaunay triangulation of the polygon
    given by border and holes (with potentially extra points and constraints).

    :param border: border of the polygon.
    :param holes: holes of the polygon.
    :param extra_points:
        additional points to be presented in the triangulation.
    :param extra_constraints:
        additional constraints to be presented in the triangulation.
    :returns: triangulation of the border, holes & extra points
    considering constraints.
    """
    result = delaunay(chain(border, _flatten(holes), extra_points))
    border_segments = _contour_to_segments(border)
    result.constrain(chain(border_segments,
                           _flatten(map(_contour_to_segments, holes)),
                           extra_constraints))
    result.bound(border_segments)
    result.cut(holes)
    return result


def delaunay_triangles(points: Sequence[Point]) -> List[Triangle]:
    """
    Returns Delaunay subdivision of the points into triangles.

    :param points: points to triangulate
    :returns: Delaunay subdivision of the points into triangles.

    >>> (delaunay_triangles([(0, 0), (3, 0), (0, 3)])
    ...  == [((0, 0), (3, 0), (0, 3))])
    True
    >>> (delaunay_triangles([(0, 0), (3, 0), (3, 3), (0, 3)])
    ...  == [((0, 3), (3, 0), (3, 3)), ((0, 0), (3, 0), (0, 3))])
    True
    >>> (delaunay_triangles([(0, 0), (3, 0), (1, 1), (0, 3)])
    ...  == [((0, 0), (3, 0), (1, 1)),
    ...      ((0, 0), (1, 1), (0, 3)),
    ...      ((0, 3), (1, 1), (3, 0))])
    True
    """
    return delaunay(points).triangles()


def constrained_delaunay_triangles(border: Contour,
                                   holes: Sequence[Contour] = (),
                                   *,
                                   extra_points: Sequence[Point] = (),
                                   extra_constraints: Sequence[Segment] = ()
                                   ) -> List[Triangle]:
    """
    Returns subdivision of the polygon given by border and holes
    (with potentially extra points and constraints)
    into triangles.

    :param border: border of the polygon.
    :param holes: holes of the polygon.
    :param extra_points:
        additional points to be presented in the triangulation.
    :param extra_constraints:
        additional constraints to be presented in the triangulation.
    :returns: subdivision of the border, holes & extra points
    considering constraints into triangles.

    >>> (constrained_delaunay_triangles([(0, 0), (3, 0), (0, 3)])
    ...  == [((0, 0), (3, 0), (0, 3))])
    True
    >>> (constrained_delaunay_triangles([(0, 0), (3, 0), (3, 3), (0, 3)])
    ...  == [((0, 3), (3, 0), (3, 3)), ((0, 0), (3, 0), (0, 3))])
    True
    >>> (constrained_delaunay_triangles([(0, 0), (3, 0), (1, 1), (0, 3)])
    ...  == [((0, 0), (3, 0), (1, 1)),
    ...      ((0, 0), (1, 1), (0, 3))])
    True
    """
    return (constrained_delaunay(border, holes,
                                 extra_points=extra_points,
                                 extra_constraints=extra_constraints)
            .triangles())
