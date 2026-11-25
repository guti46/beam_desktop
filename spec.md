# Project specification
# BeamCheck Pro — Beam Designer

## Purpose
Create a Python desktop beam design calculator for construction management and engineering students. The app allows users to choose a beam, apply loads, and see how the beam reacts. It calculates shear, bending moment, and deflection while checking whether the beam can safely handle the loads.

The goal is to make beam calculations easier to understand by showing the math and diagrams together.

## Users
Construction management students, statics students, and engineers who need to check basic steel or wood beams.

## Inputs

The starting inputs are those in the Starting Example: a 20-foot simply supported steel beam, W12x26, with one full-span uniform load of 1 kip/ft and no point loads.

### Beam Selection
- **Support:** No units. Options: simply supported or cantilever fixed at the left end. Default: simply supported. Control: dropdown.
- **Beam length:** Feet; range: 4 to 40 ft. Default: 20 ft. Control: range slider and numeric input.
- **Material:** No units. Options: steel or Douglas Fir-Larch No. 2 lumber. Default: steel. Control: dropdown.
- **Beam size:** No units. Options: the listed beam sizes for the selected material. Default: W12x26 for the starting steel selection. When the material changes, select the first listed size for the new material. Control: dropdown.

### Loads
- Allow 0 to 10 point loads and 0 to 10 uniform loads. The starting example has no point loads and one uniform load. Use Add and Remove buttons for each load type.
- **Point load magnitude:** Kips; range: positive finite values with no fixed upper limit; direction: downward. Default for each newly added point load: 10 kips. Control: numeric input.
- **Point load position:** Feet; effective range: 0 to the beam length. Values outside the beam are clipped to the nearest endpoint. Default for each newly added point load: midspan. Control: numeric input and dragging the load along the beam in 0.25-ft increments.
- **Uniform load magnitude:** Kips per foot; range: positive finite values with no fixed upper limit; direction: downward. Default for each newly added uniform load: 1 kip/ft. Control: numeric input.
- **Uniform load start and end positions:** Feet; effective range: 0 to the beam length, with out-of-span positions clipped to the nearest endpoint. Default: start at 0 ft and end at the full beam length. Control: two numeric inputs. Require start to be less than end after clipping; otherwise show a validation message.

### Deflection Limit
- **Deflection limit:** Dimensionless span ratio. Options: L/240 or L/360. Default: L/360. Control: dropdown.

All inputs update the calculations automatically.

### Steel Beam Properties
Elastic modulus E = 29,000 ksi.

Allowable bending stress Fb = 30 ksi.

| Beam | Ix (in⁴) | Sx (in³) | Weight (lb/ft) |
|---|---:|---:|---:|
| W8x10 | 30.8 | 7.81 | 10 |
| W10x12 | 53.8 | 10.9 | 12 |
| W12x26 | 204 | 33.4 | 26 |
| W14x22 | 199 | 29.0 | 22 |
| W16x26 | 301 | 38.4 | 26 |
| W18x35 | 510 | 57.6 | 35 |
| W21x44 | 843 | 81.6 | 44 |
| W24x55 | 1350 | 114 | 55 |

### Wood Beam Properties
Douglas Fir-Larch No. 2 lumber.

Elastic modulus E = 1,600 ksi.

Allowable bending stress Fb = 0.900 ksi.

| Beam | Ix (in⁴) | Sx (in³) |
|---|---:|---:|
| 2x8 | 47.63 | 13.14 |
| 2x10 | 98.93 | 21.39 |
| 2x12 | 177.98 | 31.64 |

## Calculations
Use vertical loads only. Let x increase from the left end of the beam. Applied load magnitudes are positive downward, support reactions are positive upward, positive bending moment is sagging, and downward deflection is positive. Define positive shear so that dM/dx = V; with downward load intensity positive, dV/dx = -q. Use these signs in the shear and moment diagrams; plot positive deflection downward.

### Variables and Units
- L: beam span, ft; L_in = 12L: beam span, in.
- x: position from the left end, ft; x_in = 12x: position, in.
- P_i: point load magnitude, kips; a_i: its position from the left end, ft.
- q_j: uniform load intensity, kip/ft; a_j and b_j: its start and end positions, ft.
- Q_j = q_j(b_j - a_j): resultant of uniform load j, kips; c_j = (a_j + b_j)/2: its location, ft.
- R_A and R_B: vertical support reactions, kips; M_A: cantilever fixed-end reaction moment, kip-ft.
- V(x): internal shear, kips; M(x): internal bending moment, kip-ft; y(x): downward beam deflection, in.
- E: elastic modulus, ksi (kip/in²); I = Ix: area moment of inertia, in⁴; Sx: section modulus, in³.
- Mmax: maximum absolute bending moment along the beam, kip-ft; fb: maximum bending stress, ksi; Fb: allowable bending stress, ksi.
- n: selected deflection-limit denominator, 240 or 360; δallow: allowable deflection, in; ymax: maximum absolute deflection, in.

Use the clipped load positions and boundaries specified in Inputs.

When no point or uniform loads are present, set support reactions (including the fixed-end reaction moment), shear, moment, bending stress, and deflection to zero. Report the locations of zero extrema as N/A because the response is constant along the span. The allowable deflection remains L_in/n; both checks pass with zero utilization. Apply the normal beam-recommendation rules.

### Reactions, Shear, and Moment
Calculate reactions from static equilibrium. For a simply supported beam with supports at x = 0 and x = L:

Q_j = q_j(b_j - a_j)

R_B = [Σ(P_i a_i) + Σ(Q_j c_j)] / L

R_A = ΣP_i + ΣQ_j - R_B

For a cantilever fixed at the left end:

R_A = ΣP_i + ΣQ_j

|M_A| = Σ(P_i a_i) + Σ(Q_j c_j)

In reaction equations, all distances are in feet, so reactions are in kips and moments are in kip-ft. For shear and moment along the beam, q(x) is the downward load intensity in kip/ft. A point load P_i causes a downward jump of P_i in V(x). Evaluate shear on both sides of each point load. A load clipped to a support is included in that support's reaction; calculate internal shear and moment only within the beam, using one-sided values from inside the span at its ends.

Calculate V(x), M(x), and y(x) at intervals of 1 ft or less and at all point-load locations and uniform-load boundaries.

### Deflection
Use E and I for the selected beam, treating the beam as a prismatic member with constant EI. Convert position to inches and moment to kip-in before integrating:

x_in = 12x

M_in(x_in) = 12M(x)

EI d²y/dx_in² = -M_in(x_in)

For a simply supported beam, use y(0) = 0 and y(L_in) = 0. For a cantilever fixed at the left end, use y(0) = 0 and dy/dx_in(0) = 0.

Refine calculations between grid points to locate maximum absolute shear, maximum absolute moment, and maximum absolute deflection and their positions. Include beam ends, load boundaries, and both sides of point loads when checking extrema. Locate moment extrema where V(x) = 0 and deflection extrema where the slope dy/dx_in = 0.

### Numerical Precision and Validation Tolerances
- Keep full precision internally. Use unrounded values for pass/fail checks and margins.
- Refine extrema locations to within 0.01 ft and values to within the corresponding numeric tolerance. When comparing validation results, use these absolute tolerances: force/reactions/shear ±0.005 kip; moment ±0.005 kip-ft; stress ±0.005 ksi; deflection/allowable deflection ±0.005 in; extrema locations ±0.01 ft.
- Display results rounded to 2 decimal places, omitting unnecessary trailing zeros, unless more precision is needed to communicate a result or pass/fail comparison.
- If an input or intermediate calculation produces a non-finite result, show an explicit error instead of a result or PASS status.

### Bending Stress and Check
Calculate maximum bending stress using:

fb = 12Mmax / Sx

The factor 12 converts kip-ft to kip-in; with Sx in in³, fb is in ksi. The beam passes when:

fb ≤ Fb

Calculate bending utilization and remaining margin as:

Bending utilization (%) = 100fb / Fb

Bending margin = Fb - fb (ksi)

### Deflection Check
Allow the user to choose n = 240 or n = 360. Calculate allowable deflection using span in inches:

δallow = L_in / n

The beam passes when:

ymax ≤ δallow

Calculate deflection utilization and remaining margin as:

Deflection utilization (%) = 100ymax / δallow

Deflection margin = δallow - ymax (in)

### Beam Recommendation
Recommend the lightest listed beam that passes both bending and deflection checks. For steel, compare section weights and use the larger Ix to break ties. For lumber, recommend the first passing size in the table. If no listed beam passes, state that none pass and do not recommend a failing beam.

### Units
- Force and shear: kips
- Length and load positions: feet; use inches for deflection calculations
- Distributed load intensity: kip/ft
- Moment and reaction moment: kip-ft; use kip-in for deflection integration
- Stress: ksi
- Deflection: inches

## Outputs

### Beam Drawing
Show a visual drawing of the beam that includes:
- Beam length
- Support locations
- Point loads represented by arrows
- Uniform loads represented by multiple arrows
- Support reactions with values and units; show the fixed-end reaction moment for a cantilever.
- Load positions and magnitudes with units.

### Engineering Diagrams
Show three diagrams underneath the beam drawing:

1. Shear force diagram
2. Bending moment diagram
3. Deflection diagram

Use the same horizontal distance scale for all diagrams, with the distance axis labeled in feet. Label the vertical axes and values with units: shear in kips, moment in kip-ft, and deflection in inches. Use the sign conventions specified in Calculations, including plotting positive deflection downward.

Label each diagram's maximum absolute value and its location, with units.

When hovering over a diagram, display shear, moment, and deflection at that location with a shared vertical guide. At a point load, show shear values immediately to the left and right of the load.

If a response is zero throughout the span, show its maximum value as 0 and its location as N/A.

### Beam Safety Results
Show two separate result cards:

**Bending Check**
- Actual and allowable bending stress in ksi
- Percentage of bending capacity used
- PASS or FAIL

**Deflection Check**
- Actual maximum and allowable deflection in inches
- Percentage of allowable deflection used
- PASS or FAIL

Show an overall beam status: PASS only when both checks pass; otherwise show FAIL.

Use these colors for the percentage indicators:
- Green: Below 70%
- Yellow: 70% to 100%
- Red: Above 100%

### Additional Features
- Display a load summary with point-load magnitudes and positions, and uniform-load intensities and start/end positions, with units. When there are no loads, show “No applied loads.”
- Show the remaining bending and deflection margins with units.
- Recommend the best passing size for the selected material: the lightest passing steel beam or the first passing lumber size in the table. Show the size, bending and deflection results, and steel weight when available.
- Provide a button to apply the recommendation; applying it selects that beam and updates the results.
- If no listed beam passes, show “No listed beam passes” and disable the apply button.
- Display a short explanation of why a beam passes or fails.
- Provide a Reset Example button to restore the original example.

## Look and Feel
Make the app look like a clean, modern construction engineering tool. Use a white or light-neutral background, dark readable text, and navy blue as the main accent. Keep the visual hierarchy clear and avoid unnecessary decoration.

Use distinct, high-contrast diagram colors: navy/blue for shear, teal for moment, and orange for deflection. Reserve green, yellow, and red for the safety status indicators, and include PASS/FAIL text so status is not communicated by color alone.

Use navy primary styling for Add Point Load, Add Uniform Load, and Apply Recommendation buttons. Use secondary styling for Remove and Reset Example buttons. Give every button a clear text label.

### Layout
On a computer, use a two-column layout:

**Left column:**
- Beam settings
- Material selection
- Beam size
- Load inputs
- Add and remove load buttons

**Right column:**
- Beam drawing
- Shear diagram
- Moment diagram
- Deflection diagram
- Safety results
- Recommended beam

Use independently scrollable desktop panels so crowded load lists and diagrams remain accessible.

### Starting Example
When the app opens, automatically load this example:

- Simply supported beam
- 20-foot span
- Steel W12x26
- Uniform load of 1 kip/ft
- Load applied across the entire beam
- Deflection limit L/360

Load the starting example and calculate its beam drawing, diagrams, and safety results immediately. Users can scroll through the plots and results.

Every input should have a clear label with its units.

## Validation

### Test 1: Simply Supported Beam With Uniform Load
- Support: simply supported
- Span: 20 ft
- Beam: steel W12x26
- Uniform load: 1 kip/ft over the full span
- Deflection limit: L/360

Expected results:
- Left reaction: 10 kips
- Right reaction: 10 kips
- Maximum absolute shear: 10 kips immediately inside each support
- Maximum absolute moment: 50 kip-ft at 10 ft
- Bending stress: 17.96 ksi
- Maximum deflection: 0.61 in at 10 ft
- Allowable deflection L/360: 0.67 in
- Bending: PASS
- Deflection: PASS

### Test 2: Simply Supported Beam With Point Load
- Support: simply supported
- Span: 20 ft
- Beam: steel W12x26
- Point load: 10 kips at 5 ft
- Deflection limit: L/360

Expected results:
- Left reaction: 7.5 kips
- Right reaction: 2.5 kips
- Maximum absolute shear: 7.5 kips in the left span segment
- Maximum absolute moment: 37.5 kip-ft at 5 ft
- Bending stress: 13.47 ksi
- Maximum deflection: 0.34 in at approximately 8.82 ft
- Allowable deflection L/360: 0.67 in
- Bending: PASS
- Deflection: PASS

### Test 3: Cantilever Beam
- Support: cantilever fixed at the left end
- Span: 10 ft
- Beam: steel W12x26
- Point load: 5 kips at the free end
- Deflection limit: L/360

Expected results:
- Vertical reaction: 5 kips
- Fixed-end moment magnitude: 50 kip-ft
- Maximum absolute shear: 5 kips along the span
- Maximum absolute moment: 50 kip-ft at the fixed end
- Bending stress: 17.96 ksi
- Bending: PASS
- Maximum deflection: 0.49 in at the free end
- Allowable deflection L/360: 0.33 in
- Deflection: FAIL

### Test 4: Wood Beam
- Support: simply supported
- Span: 12 ft
- Beam: Douglas Fir-Larch No. 2, 2x10
- Uniform load: 0.6 kip/ft over the full span
- Deflection limit: L/360

Expected results:
- Left reaction: 3.6 kips
- Right reaction: 3.6 kips
- Maximum absolute shear: 3.6 kips immediately inside each support
- Maximum absolute moment: 10.8 kip-ft at 6 ft
- Bending stress: 6.06 ksi
- Maximum deflection: approximately 1.77 in at 6 ft
- Allowable deflection L/360: 0.40 in
- Bending: FAIL
- Deflection: FAIL

The original classroom example lists a smaller moment and deflection for Test 4, but those values do not match a 12-foot span with a 0.6-kip/ft uniform load across the full span. Use the stated inputs and the specified engineering equations.

### Test 5: No Loads
- Support: simply supported
- Span: 20 ft
- Beam: steel W12x26
- Point loads: none
- Uniform loads: none
- Deflection limit: L/360

Expected results:
- Left and right reactions: 0 kips
- Maximum absolute shear: 0 kips; location N/A
- Maximum absolute moment: 0 kip-ft; location N/A
- Maximum bending stress: 0 ksi
- Maximum deflection: 0 in; location N/A
- Allowable deflection L/360: 0.67 in
- Bending and deflection utilization: 0%
- Bending: PASS
- Deflection: PASS
- Recommendation follows the normal rules: W8x10 is the lightest passing steel beam.

### Test 6: Combined Point and Uniform Loads
- Support: simply supported
- Span: 20 ft
- Beam: steel W12x26
- Uniform load: 1 kip/ft over the full span
- Point load: 10 kips at 10 ft
- Deflection limit: L/360

Expected results:
- Left and right reactions: 15 kips each
- Maximum absolute shear: 15 kips immediately inside each support
- Maximum absolute moment: 100 kip-ft at 10 ft
- Bending stress: 35.93 ksi
- Maximum deflection: 1.10 in at 10 ft
- Allowable deflection L/360: 0.67 in
- Bending: FAIL
- Deflection: FAIL

### Test 7: Loads Clipped to Beam Ends
- Support: simply supported
- Span: 20 ft
- Beam: steel W12x26
- Uniform load: 1 kip/ft from -2 ft to 22 ft; clipped to 0–20 ft
- Point load: 10 kips at 22 ft; clipped to 20 ft at the right support
- Deflection limit: L/360

Expected results:
- Left reaction: 10 kips
- Right reaction: 20 kips
- Maximum absolute shear: 10 kips immediately inside each support
- Maximum absolute moment: 50 kip-ft at 10 ft
- Bending stress: 17.96 ksi
- Maximum deflection: 0.61 in at 10 ft
- Allowable deflection L/360: 0.67 in
- Bending: PASS
- Deflection: PASS

### Test 8: No Listed Beam Passes
- Support: simply supported
- Span: 20 ft
- Material and beam: steel W24x55
- Uniform load: 10 kip/ft over the full span
- Deflection limit: L/360

Expected results:
- Left and right reactions: 100 kips each
- Maximum absolute shear: 100 kips immediately inside each support
- Maximum absolute moment: 500 kip-ft at 10 ft
- Bending stress: 52.63 ksi
- Maximum deflection: 0.92 in at 10 ft
- Allowable deflection L/360: 0.67 in
- Bending: FAIL
- Deflection: FAIL
- No listed steel beam passes; show the no-passing message and disable Apply Recommendation.

## Out of Scope
The File menu provides Save and Open for a local JSON design. Store the support, span, material, section, deflection limit, point loads, and uniform loads. Recalculate on open and leave the current design in place if an invalid file is selected.

The app will not calculate:
- Beam self-weight
- Shear stress or shear-capacity checks; it only calculates shear force and displays the shear diagram
- Lateral-torsional buckling
- Continuous beams
- Load combinations
- Detailed connection design
- Building-code compliance or certified engineering approval

This tool is for learning and preliminary calculations only; it does not provide final structural design, code compliance, or certified engineering approval.

## Build Requirements
- Run locally with Python, Tkinter, NumPy, and Matplotlib.
- Start the app with `python app.py`. Keep calculations separately callable for validation.
- Use the copied `index.html` as the reference for behavior and keep its original contents.
- Record each stage and its results in `prompts.md` and commit each stage.

### CSV export
The Export CSV button writes UTF-8 CSV with columns for x (ft), V (kips), M (kip-ft), and downward deflection (in). Include both one-sided shear values in left-to-right order at interior point loads.
