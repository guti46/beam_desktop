# BeamCheck Pro Desktop prompt log

## How I led the project

I asked for a plan before any setup or coding. I wanted to see how my existing BeamCheck Pro calculator would become a desktop app, what information the assistant needed, and how we would verify it. I had the assistant refine the feature plan, then gave it the go-ahead to complete the project.

## What I wanted from the build

| My direction | What changed | Did it work? |
|---|---|---|
| Use my existing BeamCheck Pro calculator as the reference. Put the Python version in its own `beam_desktop` project and update the spec before building. | Set up a separate Git repository and adapted the spec for Python and Tkinter. | Python, Tkinter, NumPy, and Matplotlib ran successfully. |
| Get the calculator working before adding file features. Check the reactions, diagrams, bending, and deflection against the cases in my spec. | Built the calculator and an expected-versus-actual validation table. | All 103 comparisons across eight cases passed. Case 1 showed 10 kips at each support, 50 kip-ft at midspan, 17.96 ksi bending stress, and 0.61 in deflection. |
| Work through the three desktop features in order. Update the spec, try each feature in the app, and rerun the beam checks before moving on. | Save/Open came first, followed by the Excel CSV and then the PDF calculation sheet. | All 103 comparisons passed again after each feature. |
| Make sure Save/Open restores a design I can keep working on, including the support, span, material, section, deflection limit, and loads. | Added Save and Open to the File menu using JSON design files. | A non-default design reopened with the same settings and loads. An invalid file left the current design in place. |
| Export position, shear, moment, and deflection in a CSV I can open in Excel. | Added the CSV button and included both shear values at an interior point load. | Excel opened all four columns. The midspan moment in Case 1 was 50 kip-ft, and the point-load check preserved the shear jump. |
| Put the beam inputs at the top of the calculation sheet and make the plots and pass/fail checks easy to read. | Added the PDF export with inputs, reactions, diagrams, and bending and deflection checks. | The assistant reviewed the rendered Case 1 sheet and a sheet with 20 loads. |
| Finish with a README, a public GitHub repository, and a ZIP I can turn in. | Documented how to install and run the app, published the commits, and packaged the project. | The repository was verified and the ZIP passed its integrity check. |

My follow-up focused on what was ready to turn in. The assistant confirmed the ZIP and repository link and identified the personal Case 1 check and Learning Suite upload as my remaining steps. I then asked for this log to spell out my direction and the result of each stage.
