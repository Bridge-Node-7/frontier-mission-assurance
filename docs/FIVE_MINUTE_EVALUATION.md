# Five-Minute Evaluation

This path validates the public FMA reference locally using source-neutral fixtures and the reviewed build toolchain.

## 1. Create an isolated environment

FMA pins its build backend so the clean evaluation path is explicit and reproducible. Install the reviewed build tools inside the isolated environment, then use them for the editable install.

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

## 2. Run the reference evaluation

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

The reference fixture includes a deliberate critical evidence gap. The PASS confirms that FMA surfaced and handled the declared condition as designed rather than converting incomplete evidence into a stronger mission claim.

## 3. Inspect individual controls

Use `fma validate`, `fma assumptions`, `fma coverage`, `fma impact`, `fma receipt`, `fma decision`, and `fma report` for individual checks. Each subcommand provides positional help and an example through `fma <command> --help`.

`fma receipt` verifies receipt structure, declared hashes, and acceptance metadata without executing the receipt command.

`fma reproduce` is the explicit trusted-code reproduction path. For a version-2 receipt it verifies code and inputs, requires the command to execute the declared entrypoint directly, runs that entrypoint in a fresh temporary workspace where declared outputs are absent, and then verifies the newly produced outputs and numerical criteria.

Interpreter modes such as `python -c`, `python -m`, or stdin execution cannot satisfy entrypoint binding merely by mentioning the entrypoint later in the command. The fresh workspace is an integrity boundary that prevents stale outputs from satisfying reproduction. Trusted code executes with the permissions and ambient capabilities of the host, so reproduction belongs in an environment appropriate for that code.
