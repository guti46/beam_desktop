# BeamCheck Pro Desktop

BeamCheck Pro is a Tkinter calculator for simply supported and cantilever beams under vertical point and uniform loads. It displays reactions, shear, moment, deflection, bending and deflection checks, and a section recommendation.

## Install and run

Open a terminal in this folder and run:

```powershell
python -m pip install -r requirements.txt
python -m tkinter
python app.py
```

Close the Tkinter test window before starting the app. The app opens on Case 1 from the specification.

## Save and export

- Use **File → Save** to keep a beam design as JSON. Use **File → Open** to restore it.
- Use **Export CSV** to open the sampled results in Excel. An interior point load has two rows at its position, first the shear immediately before the load and then the shear immediately after it.
- Use **Export Calculation PDF** for a printable calculation sheet with the inputs, diagrams, and checks.

Run `python 02_validation/validate.py` to check all eight specification cases. See [expected and actual results](02_validation/results.md), the [example CSV](03_output/case-1.csv), and the [example calculation sheet](03_output/case-1.pdf).

This calculator is for classroom and preliminary use.
