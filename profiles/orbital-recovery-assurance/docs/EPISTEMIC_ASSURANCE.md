# Epistemic Assurance

Orbital recovery can fail even when hardware remains functional if the mission no longer has a defensible basis for knowing what state is real, which control path is trustworthy, or which authority is legitimate.

This profile therefore treats epistemic state as an assurance concern without creating a new operational authority.

## Epistemic Firewall

Evidence class and assessment state are different things.

Public evidence classes in this profile are:

- `observed` — directly recorded observation under the declared collection method;
- `calculated` — deterministic or numerical result derived from declared inputs;
- `inferred` — analytical conclusion that goes beyond direct observation;
- `simulated` — result produced by a declared model or synthetic environment;
- `reported` — externally supplied or human-reported information whose trust basis must be assessed separately.

Trust and authority states are separate bounded assessments. A model, analyst, or automated process must not silently rewrite an inference, simulation, or report as an observation.

**Reference rule:** inference may propose a claim, test, or next observation; it does not promote itself into verified evidence.

## Promotion discipline

The public profile does not define one universal evidence-admissibility policy for all missions. Real users must declare their local policy for what evidence is sufficient to support or verify a claim.

At minimum:

1. every non-unknown state must reference evidence;
2. evidence class remains visible through downstream review;
3. contradictions remain visible rather than being overwritten by a preferred explanation;
4. simulated or inferred output does not become observed evidence through repetition;
5. `verified` is not equivalent to high confidence and does not arise solely from a model score;
6. authority must come from the governed authority system, not from this profile;
7. a public profile PASS never authorizes a mission action.

## Why this matters

The profile is designed to answer a narrower question than mission control:

> What does the declared evidence justify us in treating as sufficiently supported for bounded decision preparation?

That boundary prevents analytical fluency from becoming operational truth.
