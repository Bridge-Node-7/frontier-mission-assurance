# Evidence Validity Envelopes

A bare relationship such as `evidence supports claim` is often too weak for frontier systems. Evidence may be valid only for a particular modality, scale, code family, decoder, physical model, interface state, or experiment regime.

FTQC Assurance therefore records evidence applicability as explicit conditions.

## Evidence classes

The profile distinguishes evidence origin without converting class into quality:

- `THEORETICAL`
- `FORMAL`
- `SIMULATED`
- `CALCULATED`
- `EXPERIMENTAL`
- `REPRODUCED`
- `EXTERNAL_REPORTED`
- `EXPERT_ADJUDICATED`

## Applicability basis

Every envelope names a basis such as expert review, experiment, model, derivation, or declared assumption.

The profile separately records whether applicability is:

- `DECLARED` — asserted for the current record but not independently established here;
- `ESTABLISHED` — supported by a declared non-assumption basis under the profile contract.

`ESTABLISHED` still does not mean universal scientific truth. It means the record carries the required bounded basis for that applicability claim.

## Fail-closed behavior

When a changed system concept falls outside an envelope, FTQC Assurance reports `OUTSIDE_ENVELOPE`. It does not infer that the architecture fails. It means the prior evidence should not silently continue to support the same decision without review.
