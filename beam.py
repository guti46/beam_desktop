"""Beam input validation and exact piecewise integration in feet and kips."""

from dataclasses import dataclass, field
from math import isfinite

import numpy as np
from numpy.polynomial import Polynomial


STEEL = "Steel"
WOOD = "Douglas Fir-Larch No. 2"
SIMPLE = "Simply supported"
CANTILEVER = "Cantilever"


@dataclass(frozen=True)
class Section:
    name: str
    inertia: float
    modulus: float
    weight: int = 0


SECTIONS = {
    STEEL: [Section(*row) for row in (
        ("W8x10", 30.8, 7.81, 10), ("W10x12", 53.8, 10.9, 12),
        ("W12x26", 204, 33.4, 26), ("W14x22", 199, 29.0, 22),
        ("W16x26", 301, 38.4, 26), ("W18x35", 510, 57.6, 35),
        ("W21x44", 843, 81.6, 44), ("W24x55", 1350, 114, 55),
    )],
    WOOD: [Section(*row) for row in (
        ("2x8", 47.63, 13.14), ("2x10", 98.93, 21.39),
        ("2x12", 177.98, 31.64),
    )],
}
MATERIAL = {STEEL: (29000, 30), WOOD: (1600, 0.900)}


@dataclass(frozen=True)
class Design:
    support: str = SIMPLE
    span: float = 20
    material: str = STEEL
    section: str = "W12x26"
    limit: int = 360
    points: tuple = ()
    uniforms: tuple = field(default_factory=lambda: ((1, 0, 20),))


def number(value, label):
    try:
        if isinstance(value, bool):
            raise ValueError
        result = float(value)
    except (ValueError, TypeError, OverflowError) as error:
        raise ValueError(f"{label} must be a finite number.") from error
    if not isfinite(result):
        raise ValueError(f"{label} must be a finite number.")
    return result


def normalize(design):
    span = number(design.span, "Span")
    if not 4 <= span <= 40:
        raise ValueError("Span must be between 4 and 40 ft.")
    if design.support not in (SIMPLE, CANTILEVER):
        raise ValueError("Choose a supported beam type.")
    if design.material not in (STEEL, WOOD):
        raise ValueError("Choose a listed material.")
    if design.section not in [item.name for item in SECTIONS[design.material]]:
        raise ValueError("Choose a listed section for this material.")
    limit = number(design.limit, "Deflection limit")
    if limit not in (240, 360):
        raise ValueError("Choose L/240 or L/360.")
    if len(design.points) > 10 or len(design.uniforms) > 10:
        raise ValueError("Use up to ten loads of each type.")

    def position(value, label):
        return min(span, max(0, number(value, label)))

    def magnitude(value, label):
        result = number(value, label)
        if result <= 0:
            raise ValueError(f"{label} must be positive.")
        return result

    points = tuple(
        (magnitude(p, f"Point load {i} magnitude"), position(x, f"Point load {i} position"))
        for i, (p, x) in enumerate(design.points, 1)
    )
    uniforms = []
    for i, (q, a, b) in enumerate(design.uniforms, 1):
        label = f"Uniform load {i}"
        start, end = position(a, f"{label} start"), position(b, f"{label} end")
        if start >= end:
            raise ValueError(f"{label} start must be before its end after clipping to the span.")
        uniforms.append((magnitude(q, f"{label} intensity"), start, end))
    return Design(design.support, span, design.material, design.section, int(limit), points, tuple(uniforms))


@dataclass(frozen=True)
class Extreme:
    value: float
    x: float | None


@dataclass(frozen=True)
class Check:
    actual: float
    allowable: float

    @property
    def utilization(self):
        return 100 * (self.actual / self.allowable)

    @property
    def margin(self):
        return self.allowable - self.actual

    @property
    def status(self):
        return "PASS" if self.actual <= self.allowable else "FAIL"


@dataclass
class Segment:
    start: float
    end: float
    shear: Polynomial
    moment: Polynomial
    deflection: Polynomial


def roots_inside(poly, width):
    return [
        root.real for root in poly.trim().roots()
        if abs(root.imag) < 1e-9 and 0 < root.real < width
    ]


def extreme(segments, response, derivative=None):
    candidates = []
    for segment in segments:
        poly = getattr(segment, response)
        width = segment.end - segment.start
        positions = [0, width]
        if derivative:
            positions.extend(roots_inside(poly.deriv(), width))
        candidates.extend((float(poly(x)), segment.start + x) for x in positions)
    value, position = max(candidates, key=lambda item: abs(item[0]))
    return Extreme(value, position if value else None)


class Analysis:
    def __init__(self, design):
        self.design = design = normalize(design)
        span = design.span
        simple = design.support == SIMPLE
        total = sum(p for p, _ in design.points) + sum(q * (b - a) for q, a, b in design.uniforms)
        torque = sum(p * x for p, x in design.points)
        torque += sum(q * (b - a) * ((a + b) / 2) for q, a, b in design.uniforms)
        self.right = torque / span if simple else 0.0
        self.left = total - self.right
        self.fixed = 0.0 if simple else torque
        if not all(map(isfinite, (total, torque, self.left, self.right))):
            raise ValueError("Loads are too large to produce finite beam results.")

        events = {0: [0., 0.], span: [0., 0.]}
        for p, x in design.points:
            events.setdefault(x, [0., 0.])[0] += p
        for q, a, b in design.uniforms:
            events.setdefault(a, [0., 0.])[1] += q
            events.setdefault(b, [0., 0.])[1] -= q
        self.boundaries = sorted(events)
        self.segments = []
        shear, moment, intensity = self.left, -self.fixed, 0.0
        slope = displacement = 0.0
        # Integrate -M expressed in kip-ft. Factor 12³ converts both derivatives
        # to feet and moment to kip-in. Divide by EI after finding extrema.
        with np.errstate(over="raise", invalid="raise"):
            for start, end in zip(self.boundaries, self.boundaries[1:]):
                point, change = events[start]
                shear -= point
                intensity += change
                v = Polynomial([shear, -intensity])
                m = v.integ(k=moment)
                y = (-m).integ(m=2, k=[slope, displacement])
                self.segments.append(Segment(start, end, v, m, y))
                width = end - start
                shear, moment, slope, displacement = v(width), m(width), y.deriv()(width), y(width)

            if simple:
                correction = -displacement / span
                for segment in self.segments:
                    segment.deflection += Polynomial([correction * segment.start, correction])

            self.shear = extreme(self.segments, "shear")
            self.moment = extreme(self.segments, "moment", True)
            self.unscaled = extreme(self.segments, "deflection", True)
            self.section = next(item for item in SECTIONS[design.material] if item.name == design.section)
            self.bending, self.deflection = self.checks(self.section)
            self.maximum_deflection = Extreme(self.unscaled.value * self.factor(self.section), self.unscaled.x)
            candidates = SECTIONS[design.material]
            if design.material == STEEL:
                candidates = sorted(candidates, key=lambda item: (item.weight, -item.inertia))
            self.recommendation = next(
                (item for item in candidates if all(check.status == "PASS" for check in self.checks(item))),
                None,
            )

    def factor(self, section):
        elasticity, _ = MATERIAL[self.design.material]
        return 12 ** 3 / (elasticity * section.inertia)

    def checks(self, section):
        _, allowable = MATERIAL[self.design.material]
        bending = Check(float(abs(self.moment.value) * 12 / section.modulus), allowable)
        deflection = Check(float(abs(self.unscaled.value) * self.factor(section)),
                           self.design.span * 12 / self.design.limit)
        if not all(isfinite(value) for check in (bending, deflection)
                   for value in (check.actual, check.utilization)):
            raise ValueError("Loads are too large to produce finite beam results.")
        return bending, deflection

    def sample(self, x, side="right"):
        index = np.searchsorted(self.boundaries, x, side=side) - 1
        segment = self.segments[min(len(self.segments) - 1, max(0, index))]
        offset = x - segment.start
        deflection = segment.deflection(offset) * self.factor(self.section)
        if x == 0 or (x == self.design.span and self.design.support == SIMPLE):
            deflection = 0.0
        return segment.shear(offset), segment.moment(offset), deflection

    def rows(self):
        """Include both internal shear limits at an interior point load."""
        points = {x for _, x in self.design.points if 0 < x < self.design.span}
        extrema = (self.shear, self.moment, self.maximum_deflection)
        grid = np.linspace(0, self.design.span, int(np.ceil(self.design.span * 4)) + 1)
        positions = set(self.boundaries)
        for x in [*grid, *(peak.x for peak in extrema if peak.x is not None)]:
            if all(abs(x - position) > 1e-10 for position in positions):
                positions.add(x)
        for x in sorted(positions):
            if x in points:
                yield (x, *self.sample(x, "left"))
            yield (x, *self.sample(x))
