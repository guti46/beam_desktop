"""Export calculated samples."""

import csv


def export_csv(path, analysis):
    with open(path, "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("x (ft)", "V (kips)", "M (kip-ft)", "Deflection (in)"))
        writer.writerows(analysis.rows())
