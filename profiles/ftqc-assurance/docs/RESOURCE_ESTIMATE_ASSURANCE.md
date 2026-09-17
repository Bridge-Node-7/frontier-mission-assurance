# Resource Estimate Assurance

FTQC resource estimates are conditional outputs. Their decision meaning depends on the workload, algorithm representation, QEC assumptions, logical error target, physical model, architecture constraints, estimator identity, version, and configuration.

FTQC Assurance does not create a new quantum resource estimator.

The `Resource Estimate Receipt` records:

- which system concept and workload the estimate addresses;
- estimator identity and version;
- the assumptions the estimate depends on;
- the reported result;
- an optional FMA Research Receipt reference for exact computational provenance;
- the evidence-validity envelope that bounds applicability;
- whether the estimate is current, under review, or stale.

A changed assumption does not erase a historical estimate. It changes whether that estimate remains appropriate as the current decision basis.

`CURRENT` therefore means only that no declared dependency has made the receipt stale under this bounded profile. It is not a statement that the estimate is scientifically correct.
