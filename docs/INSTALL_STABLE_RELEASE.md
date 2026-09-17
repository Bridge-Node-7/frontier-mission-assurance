# Install a Stable Release

Use a published GitHub Release when you need a stable FMA artifact. The default branch may contain source that is newer than the latest stable release.

A stable release is produced by the repository's explicit Stable Release workflow and includes:

- a source archive;
- a Python wheel;
- a release-artifact SHA-256 manifest;
- a tracked-source SHA-256 manifest;
- a CycloneDX SBOM;
- GitHub provenance attestations when the platform makes them available.

## 1. Select the release

Open the repository's GitHub **Releases** page and use the latest non-prerelease release appropriate for your evaluation.

Do not infer stability from the `VERSION` file on the default branch alone.

## 2. Download the verification set

For release `vX.Y.Z`, the published set is expected to include:

```text
frontier-mission-assurance-vX.Y.Z.zip
frontier_mission_assurance-X.Y.Z-py3-none-any.whl
FMA-vX.Y.Z-SOURCE-SHA256SUMS
FMA-vX.Y.Z-SBOM.cdx.json
FMA-vX.Y.Z-SHA256SUMS
```

## 3. Verify integrity

On macOS or Linux, place the downloaded release artifacts in one directory and run:

```bash
sha256sum -c FMA-vX.Y.Z-SHA256SUMS
```

On Windows, calculate SHA-256 with PowerShell and compare the values to the published manifest:

```powershell
Get-FileHash .\frontier_mission_assurance-X.Y.Z-py3-none-any.whl -Algorithm SHA256
Get-FileHash .\frontier-mission-assurance-vX.Y.Z.zip -Algorithm SHA256
```

When GitHub attestation verification is part of your environment, verify the wheel and source archive against this repository's published provenance before installation.

## 4. Install the wheel in an isolated environment

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ./frontier_mission_assurance-X.Y.Z-py3-none-any.whl
.venv/bin/fma --version
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install .\frontier_mission_assurance-X.Y.Z-py3-none-any.whl
.\.venv\Scripts\fma.exe --version
```

The reported version should match the release selected in step 1.

## 5. Verify the source archive when using bundled profiles

The core wheel contains the `frontier_assurance` package and CLI. Public profile validators, source-neutral examples, and release documentation are distributed through the source archive.

Unpack the source archive and verify tracked-source hashes before running its reference/profile evaluators:

```bash
unzip frontier-mission-assurance-vX.Y.Z.zip
cd frontier-mission-assurance
sha256sum -c ../FMA-vX.Y.Z-SOURCE-SHA256SUMS
python scripts/evaluate_public_reference.py
python scripts/validate_profile_manifests.py .
```

Run only the profile evaluations relevant to your review.

## Verification meaning

Checksum, attestation, package-install, schema, and reference-evaluation PASS states establish only the controls they actually exercised. They do not establish scientific validity, system readiness, safety, security authorization, supplier qualification, regulatory acceptance, or permission for consequential action.

## Rights and governed use

A stable artifact does not expand the rights granted by [`../LICENSE`](../LICENSE). For evaluation scope and use beyond the public evaluation posture, see [`USE_AND_EVALUATION.md`](USE_AND_EVALUATION.md).
