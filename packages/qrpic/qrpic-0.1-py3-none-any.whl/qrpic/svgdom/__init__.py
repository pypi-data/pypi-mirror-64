import re
from enum import Enum
from math import pi, sin, cos
from typing import NamedTuple

from shapely.geometry import LinearRing, LineString, Polygon
from svg.path import parse_path, CubicBezier, Close

from qrpic.geom import complex_to_point
from qrpic.itertools import grouper


class ParseError(Exception):
    pass


class Unit(Enum):
    PIXELS = 'px'
    POINTS = 'pt'
    PICAS = 'pc'
    CENTIMETERS = 'cm'
    MILLIMETERS = 'mm'
    INCHES = 'in'
    USER = ''


_CONVERSION_TABLE_INCH_REAL_MEASURES =  {
    Unit.POINTS: 1 / 72,
    Unit.PICAS: 1 / 6,
    Unit.CENTIMETERS: 1 / 2.54,
    Unit.MILLIMETERS: 1 / 25.4,
    Unit.INCHES: 1.0,
}
CONVERSION_TABLE_INCH_REAL_MEASURES_REVERSE = {
    unit: 1 / val for unit, val in _CONVERSION_TABLE_INCH_REAL_MEASURES.items()
}


class Rect(NamedTuple):
    x: float
    y: float
    width: float
    height: float


class Measure(NamedTuple):
    value: float
    unit: Unit

    @classmethod
    def from_string(cls, string: str):
        match = re.fullmatch(rf'(\d+(?:.\d+)?)({"|".join(v.value for v in Unit)})', string)

        if match is None:
            raise ValueError

        return cls(float(match.group(1)), Unit(match.group(2)))

    def convert(self, unit: Unit, ppi=96):
        if self.unit == unit:
            return self

        if self.unit is Unit.USER or self.unit is Unit.PIXELS:
            unitless = self.value
        else:
            unitless = _CONVERSION_TABLE_INCH_REAL_MEASURES[self.unit] * ppi * self.value

        if unit is Unit.USER or unit is Unit.PIXELS:
            return Measure(unitless, unit)
        else:
            return Measure(_CONVERSION_TABLE_INCH_REAL_MEASURES[unit] / ppi * unitless, unit)


def parse_svg_viewbox(tree, ppi=96):
    root = tree.getroot()

    if 'viewBox' in root.attrib:
        x, y, width, height = (Measure.from_string(value.strip()) for value in root.attrib['viewBox'].split(' '))
    else:
        x = Measure(0, Unit.USER)
        y = Measure(0, Unit.USER)
        width = None
        height = None

        if 'width' in root.attrib:
            width = Measure.from_string(root.attrib['width'].strip())
        if 'height' in root.attrib:
            height = Measure.from_string(root.attrib['height'].strip())

        if width is None and height is None:
            raise ParseError('missing width or height or viewBox - unable to determine svg dimensions')

        if width is None:
            width = height
        elif height is None:
            height = width
        else:
            raise AssertionError

    # Convert viewbox units to unitless/user values.
    x, y, width, height = (v.convert(Unit.USER, ppi).value for v in (x, y, width, height))
    viewbox = Rect(x, y, width, height)

    return viewbox


def parse_svg_geometry(tree, resolution=32, ppi=96):
    root = tree.getroot()

    shapes = []

    for child in root:
        match = re.fullmatch(r'{[^}]*?\}(.*)', child.tag)
        tag = match.group(1)

        if tag == 'rect':
            x = Measure.from_string(child.attrib['x']).convert(Unit.USER, ppi).value if 'x' in child.attrib else 0
            y = Measure.from_string(child.attrib['y']).convert(Unit.USER, ppi).value if 'y' in child.attrib else 0
            width = Measure.from_string(child.attrib['width']).convert(Unit.USER, ppi).value
            height = Measure.from_string(child.attrib['height']).convert(Unit.USER, ppi).value

            geom = LinearRing([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

            shapes.append(geom)

        elif tag == 'path':
            path = parse_path(child.attrib['d'])

            # Path specs are always specified in user units, so no conversion necessary.
            # See https://www.w3.org/TR/SVG/paths.html.
            # TODO I need to either define a polygon or a line string or a line ring, depending on whether it is filled
            #   or not.
            points = []
            for primitive in path[:-1]:
                if isinstance(primitive, CubicBezier):
                    for i in range(resolution):
                        x = i / (resolution - 1)
                        pt = complex_to_point(
                            (1 - x)**3 * primitive.start +
                            3 * (1 - x)**2 * x * primitive.control1 +
                            3 * (1 - x) * x**2 * primitive.control2 +
                            x**3 * primitive.end)
                        points.append(pt)
                elif isinstance(primitive, Close):
                    # Closing shapes should only appear at the end. This is not perfectly checked here,
                    # but it's enough for now.
                    pass
                else:
                    points.append(complex_to_point(primitive.end))

            if isinstance(path[-1], Close):
                geom = Polygon(points)
            else:
                geom = LineString(points)

            shapes.append(geom)

        elif tag == 'line':
            x1 = Measure.from_string(child.attrib['x1']).convert(Unit.USER, ppi).value
            y1 = Measure.from_string(child.attrib['y1']).convert(Unit.USER, ppi).value
            x2 = Measure.from_string(child.attrib['x2']).convert(Unit.USER, ppi).value
            y2 = Measure.from_string(child.attrib['y2']).convert(Unit.USER, ppi).value

            geom = LineString([(x1, y1), (x2, y2)])

            shapes.append(geom)

        elif tag == 'polygon':
            geom = Polygon(parse_points(child.attrib['points']))

            shapes.append(geom)

        elif tag == 'polyline':
            # TODO polylines have a default filling, which alters the shape.
            geom = LineString(parse_points(child.attrib['points']))

            shapes.append(geom)

        elif tag == 'circle':
            cx = Measure.from_string(child.attrib['cx']).convert(Unit.USER, ppi).value
            cy = Measure.from_string(child.attrib['cy']).convert(Unit.USER, ppi).value
            r = Measure.from_string(child.attrib['r']).convert(Unit.USER, ppi).value

            circle = []
            for i in range(resolution):
                angle = i * 2 * pi / resolution
                pt = (cx + cos(angle) * r, cy + sin(angle) * r)
                circle.append(pt)

            geom = Polygon(circle)

            shapes.append(geom)

        elif tag == 'ellipse':
            cx = Measure.from_string(child.attrib['cx']).convert(Unit.USER, ppi).value
            cy = Measure.from_string(child.attrib['cy']).convert(Unit.USER, ppi).value
            rx = Measure.from_string(child.attrib['rx']).convert(Unit.USER, ppi).value
            ry = Measure.from_string(child.attrib['ry']).convert(Unit.USER, ppi).value

            circle = []
            for i in range(resolution):
                angle = i * 2 * pi / resolution
                pt = (cx + cos(angle) * rx, cy + sin(angle) * ry)
                circle.append(pt)

            geom = Polygon(circle)

            shapes.append(geom)

    return shapes


def parse_points(pts):
    return [(float(x), float(y)) for x, y in grouper(re.split(r'[ ,]+', pts), 2)]
