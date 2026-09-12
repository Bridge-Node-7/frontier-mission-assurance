from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
values = []
with (BASE / "data" / "measurements.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        values.append(int(row["outcome"]))

result = {
    "n": len(values),
    "estimate_z": sum(values) / len(values),
    "method": "mean of synthetic +/-1 outcomes",
}
(BASE / "outputs").mkdir(exist_ok=True)
(BASE / "outputs" / "result.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
