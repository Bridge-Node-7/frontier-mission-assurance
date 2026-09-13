# Five-Minute Evaluation

This path demonstrates the public reference without executing receipt commands or contacting a remote service.

## 1. Create an isolated environment

FMA pins its build backend so the clean-adopter path is explicit and reproducible. Install those exact build tools inside the isolated environment before the editable install, then disable build isolation so pip uses the reviewed local backend versions.

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "setuptools==84.0.0" "wheel==0.48.0"
.venv/bin/python -m pip install --no-build-isolation -e .
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "setuptools==84.0.0" "wheel==0.48.0"
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
```

## 2. Run the bounded evaluation

### macOS / Linux

```bash
.venv/bin/python scripts/evaluate_public_reference.py
```

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe scripts/evaluate_public_reference.py
```

Expected final line:

```text
RESULT - PUBLIC REFERENCE EVALUATION PASS
```

The synthetic fixture intentionally retains a visible critical evidence gap. A PASS means the reference mechanics behaved as declared; it does not mean the synthetic system is mission-ready.

## 3. Optional deeper inspection

Use `fma validate`, `fma assumptions`, `fma coverage`, `fma impact`, `fma receipt`, `fma decision`, and `fma report` for individual checks. Each subcommand provides positional help and an example through `fma <command> --help`.

`fma receipt` remains non-executing. The bundled version-2 receipt binds declared code, inputs, outputs, and numerical acceptance checks.

`fma reproduce` is intentionally excluded from the bounded evaluation because it executes trusted receipt-declared code. For a version-2 receipt it first verifies code and inputs, requires the command to execute the declared entrypoint directly (or as the first Python script argument), then runs that entrypoint in a fresh temporary workspace where declared outputs are absent, and finally verifies the new outputs and numerical criteria. Interpreter modes such as `python -c`, `python -m`, or stdin execution cannot satisfy entrypoint binding merely by mentioning the entrypoint later in the command. The workspace prevents stale outputs from satisfying a reproduction PASS, but it is not a sandbox or hermetic environment. Run reproduction only on trusted code after review.
