# Black-Sky Exercise Pattern

A Black-Sky exercise is a synthetic or isolated assurance exercise used to test whether unsupported assumptions are prevented from becoming operational truth when mission evidence degrades or conflicts.

It is not a cyberattack playbook and does not contain live command procedures.

## Synthetic exercise conditions

Useful combinations include:

- contradictory telemetry;
- stale or disputed authority state;
- clock disagreement;
- software/configuration drift;
- ground-path outage;
- delayed communications;
- sensor disagreement;
- hidden common dependency loss;
- incomplete interface knowledge;
- post-intervention evidence gaps.

## Evaluation questions

The exercise asks:

1. Did inferred or simulated information get mislabeled as observed evidence?
2. Were correlated evidence sources mistaken for independent witnesses?
3. Did the system preserve the human authority boundary?
4. Were unsafe options excluded across the declared credible state set?
5. Did the assessment identify useful next evidence rather than merely produce more data?
6. Did requalification remain fail-closed when post-change evidence was incomplete?
7. What were TTC, TTE, TTMC, TTT, and TTV?
8. Which architecture or evidence changes would reduce Time-to-Trust without weakening the assurance boundary?

## Recommended outputs

- synthetic Recovery Evidence Record;
- Recovery Option Assessment;
- provenance-correlation components;
- requalification result;
- recovery timeline metrics;
- list of unsupported assumptions prevented from promotion;
- explicit reopen conditions.

A passing exercise demonstrates only bounded behavior in the declared synthetic environment.
