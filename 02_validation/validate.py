"""Report each specification value against the production solver."""

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beam import Analysis, CANTILEVER, Design, WOOD


base = Design()
cases = [
    ("Full-span uniform", base, dict(left=10, right=10, shear=10, moment=50, moment_x=10,
         stress=17.96, deflection=.61, deflection_x=10, allowable=.67, bending="PASS", drift="PASS")),
    ("Off-center point", replace(base, points=((10, 5),), uniforms=()),
     dict(left=7.5, right=2.5, shear=7.5, moment=37.5, moment_x=5, stress=13.47,
          deflection=.34, deflection_x=8.82, allowable=.67, bending="PASS", drift="PASS")),
    ("Cantilever tip", replace(base, support=CANTILEVER, span=10, points=((5, 10),), uniforms=()),
     dict(left=5, fixed=50, shear=5, moment=50, moment_x=0, stress=17.96,
          deflection=.49, deflection_x=10, allowable=.33, bending="PASS", drift="FAIL")),
    ("Wood beam", replace(base, span=12, material=WOOD, section="2x10", uniforms=((.6, 0, 12),)),
     dict(left=3.6, right=3.6, shear=3.6, moment=10.8, moment_x=6, stress=6.06,
          deflection=1.77, deflection_x=6, allowable=.40, bending="FAIL", drift="FAIL")),
    ("No loads", replace(base, uniforms=()),
     dict(left=0, right=0, shear=0, shear_x=None, moment=0, moment_x=None, stress=0,
          deflection=0, deflection_x=None, allowable=.67, bending="PASS", drift="PASS",
          bending_use=0, deflection_use=0, recommended="W8x10")),
    ("Combined", replace(base, points=((10, 10),)),
     dict(left=15, right=15, shear=15, moment=100, moment_x=10, stress=35.93,
          deflection=1.10, deflection_x=10, allowable=.67, bending="FAIL", drift="FAIL")),
    ("Clipped", replace(base, points=((10, 22),), uniforms=((1, -2, 22),)),
     dict(left=10, right=20, shear=10, moment=50, moment_x=10, stress=17.96,
          deflection=.61, deflection_x=10, allowable=.67, bending="PASS", drift="PASS")),
    ("No section passes", replace(base, section="W24x55", uniforms=((10, 0, 20),)),
     dict(left=100, right=100, shear=100, moment=500, moment_x=10, stress=52.63,
          deflection=.92, deflection_x=10, allowable=.67, bending="FAIL", drift="FAIL",
          recommended=None)),
]


def observed(result):
    return dict(left=result.left, right=result.right, fixed=result.fixed,
                shear=abs(result.shear.value), shear_x=result.shear.x,
                moment=abs(result.moment.value), moment_x=result.moment.x,
                stress=result.bending.actual, deflection=result.deflection.actual,
                deflection_x=result.maximum_deflection.x, allowable=result.deflection.allowable,
                bending=result.bending.status, drift=result.deflection.status,
                bending_use=result.bending.utilization, deflection_use=result.deflection.utilization,
                recommended=result.recommendation.name if result.recommendation else None)


def display(value):
    if isinstance(value, float):
        return f"{value:.5f}".rstrip("0").rstrip(".")
    return "N/A" if value is None else str(value)


def validate():
    lines = [
        "# BeamCheck Pro validation", "",
        "Force and shear are in kips, moment in kip-ft, stress in ksi, deflection in inches, "
        "and locations in feet. Numeric tolerances are 0.005 in the applicable units and "
        "0.01 ft for positions.", "",
        "| Case | Result | Expected | Actual | Match |",
        "|---|---|---:|---:|---|",
    ]
    failures = 0
    count = 0
    for i, (name, design, expected) in enumerate(cases, 1):
        result = Analysis(design)
        actual = observed(result)
        for key, value in expected.items():
            measured = actual[key]
            if isinstance(value, (int, float)):
                match = measured is not None and abs(measured - value) <= (.01 if key.endswith("_x") else .005)
            else:
                match = measured == value
            lines.append(f"| {i}. {name} | {key} | {display(value)} | {display(measured)} | {'PASS' if match else 'FAIL'} |")
            failures += not match
            count += 1
        if i in (1, 4, 6, 7, 8):
            for x, sign in ((0, 1), (result.design.span, -1)):
                expected_shear = sign * expected["shear"]
                measured = float(result.sample(x)[0])
                match = abs(measured - expected_shear) <= .005
                lines.append(f"| {i}. {name} | V at {x} ft, inside | {expected_shear} | {display(measured)} | {'PASS' if match else 'FAIL'} |")
                failures += not match
                count += 1
    lines.extend(["", f"{count - failures} of {count} comparisons passed across {len(cases)} cases."])
    Path(__file__).with_name("results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    validate()
