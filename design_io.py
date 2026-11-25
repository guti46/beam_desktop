"""Read and write BeamCheck Pro design files."""

from dataclasses import asdict
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from beam import Analysis, Design


def save_design(path, analysis):
    path = Path(path)
    payload = {"version": 1, "design": asdict(analysis.design)}
    temp_path = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temp_path = Path(stream.name)
            json.dump(payload, stream, indent=2, allow_nan=False)
            stream.write("\n")
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def open_design(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or type(payload.get("version")) is not int or payload["version"] != 1:
        raise ValueError("This file is not a supported BeamCheck Pro design.")
    entries = payload.get("design")
    if not isinstance(entries, dict) or entries.keys() != Design.__dataclass_fields__.keys():
        raise ValueError("The design file is missing fields or has unrecognized fields.")
    for key, width in (("points", 2), ("uniforms", 3)):
        loads = entries[key]
        if not isinstance(loads, list) or any(not isinstance(row, list) or len(row) != width for row in loads):
            raise ValueError("The design file contains an invalid load.")
    return Analysis(Design(**entries)).design
