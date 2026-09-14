# Changelog

## 0.6.0 — resilience and trust semantics

- Made the authoritative public release-boundary scan operate on every Git-tracked file regardless of directory name, closing force-tracked build/cache disclosure bypasses while allowing untracked ephemeral caches to remain outside release scope.
- Added Research Receipt 3.1 with explicit per-output `EXACT`, `SEMANTICALLY_CHECKED`, and `RECORD_ONLY` assurance semantics while preserving an observed SHA-256 for every output.
- Required semantic outputs to name the exact same-output checks that define their bounded equivalence claim; record-only outputs make no equivalence claim.
- Added external execution chronology checks for `submitted_at <= started_at <= completed_at <= collected_at` and bound required calibration validity to the declared execution interval.
- Preserved Research Receipt 3.0 compatibility while making the strengthened 3.1 semantics explicit rather than silently redefining the existing contract.
- Hardened generated Mission Assurance Reports against decision laundering by carrying the PASS non-claims in the portable artifact, labeling evidence coverage as declared/unverified, surfacing validation-warning counts, and distinguishing undeclared assumptions from proof that no assumptions exist.
- Updated CLI summaries and public documentation so declared acceptance, scientific truth, and authenticated authorship remain visibly distinct.
- Updated current maturity, source validation, release receipt, package metadata, and citation metadata to the v0.6 line.

## 0.5.0 — research receipt v3

- Added Research Receipt v3 with explicit `EXACT_SHA256`, `NUMERIC_CHECKS`, and `HYBRID` output-acceptance modes while keeping declared code and inputs SHA-256 exact.
- Preserved every observed v3 output SHA-256 as provenance even when stochastic/numerical acceptance does not require byte identity.
- Added calibration/instrument-state provenance with explicit policy, identity, configuration hash, lineage, observation time, and validity-window checks.
- Added a bounded external/cluster contract that separates submission/environment evidence from result collection and verifies scheduler/job continuity, code/input manifests, environment identity, timeout/cancellation semantics, terminal state, and collected-output hashes without running a real cluster in public CI.
- Kept version-2 exact local reproduction semantics backward compatible.
- Improved reproduction diagnostics for undeclared Python helpers while retaining raw child stderr, and made invalid graph-status errors list the sorted allowed set.
