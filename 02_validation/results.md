# BeamCheck Pro validation

Force and shear are in kips, moment in kip-ft, stress in ksi, deflection in inches, and locations in feet. Numeric tolerances are 0.005 in the applicable units and 0.01 ft for positions.

| Case | Result | Expected | Actual | Match |
|---|---|---:|---:|---|
| 1. Full-span uniform | left | 10 | 10 | PASS |
| 1. Full-span uniform | right | 10 | 10 | PASS |
| 1. Full-span uniform | shear | 10 | 10 | PASS |
| 1. Full-span uniform | moment | 50 | 50 | PASS |
| 1. Full-span uniform | moment_x | 10 | 10 | PASS |
| 1. Full-span uniform | stress | 17.96 | 17.96407 | PASS |
| 1. Full-span uniform | deflection | 0.61 | 0.60852 | PASS |
| 1. Full-span uniform | deflection_x | 10 | 10 | PASS |
| 1. Full-span uniform | allowable | 0.67 | 0.66667 | PASS |
| 1. Full-span uniform | bending | PASS | PASS | PASS |
| 1. Full-span uniform | drift | PASS | PASS | PASS |
| 1. Full-span uniform | V at 0 ft, inside | 10 | 10 | PASS |
| 1. Full-span uniform | V at 20.0 ft, inside | -10 | -10 | PASS |
| 2. Off-center point | left | 7.5 | 7.5 | PASS |
| 2. Off-center point | right | 2.5 | 2.5 | PASS |
| 2. Off-center point | shear | 7.5 | 7.5 | PASS |
| 2. Off-center point | moment | 37.5 | 37.5 | PASS |
| 2. Off-center point | moment_x | 5 | 5 | PASS |
| 2. Off-center point | stress | 13.47 | 13.47305 | PASS |
| 2. Off-center point | deflection | 0.34 | 0.34017 | PASS |
| 2. Off-center point | deflection_x | 8.82 | 8.81966 | PASS |
| 2. Off-center point | allowable | 0.67 | 0.66667 | PASS |
| 2. Off-center point | bending | PASS | PASS | PASS |
| 2. Off-center point | drift | PASS | PASS | PASS |
| 3. Cantilever tip | left | 5 | 5 | PASS |
| 3. Cantilever tip | fixed | 50 | 50 | PASS |
| 3. Cantilever tip | shear | 5 | 5 | PASS |
| 3. Cantilever tip | moment | 50 | 50 | PASS |
| 3. Cantilever tip | moment_x | 0 | 0 | PASS |
| 3. Cantilever tip | stress | 17.96 | 17.96407 | PASS |
| 3. Cantilever tip | deflection | 0.49 | 0.48682 | PASS |
| 3. Cantilever tip | deflection_x | 10 | 10 | PASS |
| 3. Cantilever tip | allowable | 0.33 | 0.33333 | PASS |
| 3. Cantilever tip | bending | PASS | PASS | PASS |
| 3. Cantilever tip | drift | FAIL | FAIL | PASS |
| 4. Wood beam | left | 3.6 | 3.6 | PASS |
| 4. Wood beam | right | 3.6 | 3.6 | PASS |
| 4. Wood beam | shear | 3.6 | 3.6 | PASS |
| 4. Wood beam | moment | 10.8 | 10.8 | PASS |
| 4. Wood beam | moment_x | 6 | 6 | PASS |
| 4. Wood beam | stress | 6.06 | 6.05891 | PASS |
| 4. Wood beam | deflection | 1.77 | 1.76852 | PASS |
| 4. Wood beam | deflection_x | 6 | 6 | PASS |
| 4. Wood beam | allowable | 0.4 | 0.4 | PASS |
| 4. Wood beam | bending | FAIL | FAIL | PASS |
| 4. Wood beam | drift | FAIL | FAIL | PASS |
| 4. Wood beam | V at 0 ft, inside | 3.6 | 3.6 | PASS |
| 4. Wood beam | V at 12.0 ft, inside | -3.6 | -3.6 | PASS |
| 5. No loads | left | 0 | 0 | PASS |
| 5. No loads | right | 0 | 0 | PASS |
| 5. No loads | shear | 0 | 0 | PASS |
| 5. No loads | shear_x | N/A | N/A | PASS |
| 5. No loads | moment | 0 | 0 | PASS |
| 5. No loads | moment_x | N/A | N/A | PASS |
| 5. No loads | stress | 0 | 0 | PASS |
| 5. No loads | deflection | 0 | 0 | PASS |
| 5. No loads | deflection_x | N/A | N/A | PASS |
| 5. No loads | allowable | 0.67 | 0.66667 | PASS |
| 5. No loads | bending | PASS | PASS | PASS |
| 5. No loads | drift | PASS | PASS | PASS |
| 5. No loads | bending_use | 0 | 0 | PASS |
| 5. No loads | deflection_use | 0 | 0 | PASS |
| 5. No loads | recommended | W8x10 | W8x10 | PASS |
| 6. Combined | left | 15 | 15 | PASS |
| 6. Combined | right | 15 | 15 | PASS |
| 6. Combined | shear | 15 | 15 | PASS |
| 6. Combined | moment | 100 | 100 | PASS |
| 6. Combined | moment_x | 10 | 10 | PASS |
| 6. Combined | stress | 35.93 | 35.92814 | PASS |
| 6. Combined | deflection | 1.1 | 1.09533 | PASS |
| 6. Combined | deflection_x | 10 | 10 | PASS |
| 6. Combined | allowable | 0.67 | 0.66667 | PASS |
| 6. Combined | bending | FAIL | FAIL | PASS |
| 6. Combined | drift | FAIL | FAIL | PASS |
| 6. Combined | V at 0 ft, inside | 15 | 15 | PASS |
| 6. Combined | V at 20.0 ft, inside | -15 | -15 | PASS |
| 7. Clipped | left | 10 | 10 | PASS |
| 7. Clipped | right | 20 | 20 | PASS |
| 7. Clipped | shear | 10 | 10 | PASS |
| 7. Clipped | moment | 50 | 50 | PASS |
| 7. Clipped | moment_x | 10 | 10 | PASS |
| 7. Clipped | stress | 17.96 | 17.96407 | PASS |
| 7. Clipped | deflection | 0.61 | 0.60852 | PASS |
| 7. Clipped | deflection_x | 10 | 10 | PASS |
| 7. Clipped | allowable | 0.67 | 0.66667 | PASS |
| 7. Clipped | bending | PASS | PASS | PASS |
| 7. Clipped | drift | PASS | PASS | PASS |
| 7. Clipped | V at 0 ft, inside | 10 | 10 | PASS |
| 7. Clipped | V at 20.0 ft, inside | -10 | -10 | PASS |
| 8. No section passes | left | 100 | 100 | PASS |
| 8. No section passes | right | 100 | 100 | PASS |
| 8. No section passes | shear | 100 | 100 | PASS |
| 8. No section passes | moment | 500 | 500 | PASS |
| 8. No section passes | moment_x | 10 | 10 | PASS |
| 8. No section passes | stress | 52.63 | 52.63158 | PASS |
| 8. No section passes | deflection | 0.92 | 0.91954 | PASS |
| 8. No section passes | deflection_x | 10 | 10 | PASS |
| 8. No section passes | allowable | 0.67 | 0.66667 | PASS |
| 8. No section passes | bending | FAIL | FAIL | PASS |
| 8. No section passes | drift | FAIL | FAIL | PASS |
| 8. No section passes | recommended | N/A | N/A | PASS |
| 8. No section passes | V at 0 ft, inside | 100 | 100 | PASS |
| 8. No section passes | V at 20.0 ft, inside | -100 | -100 | PASS |

103 of 103 comparisons passed across 8 cases.
