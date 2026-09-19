# Threat Model

## Assets

- integrity of the public reference implementation;
- confidentiality of nonpublic program information;
- integrity and provenance of declared evidence artifacts;
- integrity of declared research code, inputs, outputs, and acceptance checks;
- clarity of human decision authority;
- integrity of release provenance and CI evidence.

## Trust boundaries

1. **Repository publication boundary** — treat repository content, issue/PR text,
   workflow logs, and release artifacts as publishable.
2. **Local validation boundary** — graph and receipt files may be malformed or adversarial.
3. **Reproduction boundary** — `fma reproduce` executes trusted repository code and is not a sandbox or hermetic execution environment.
4. **Operational record boundary** — authoritative case records remain governed by
   the systems and environments responsible for them.
5. **Supply-chain boundary** — package dependencies and CI Actions can change independently of FMA source unless pinned/recorded.

## Primary threats and controls

| Threat | Control | Residual risk |
|---|---|---|
| Accidental disclosure | synthetic-only policy, fail-closed file/URL scanner, manual contextual review | automation cannot infer every sensitive proper noun/value |
| Path escape in receipts | resolved-path containment checks | trusted code executed by reproduction can still access its environment |
| Artifact tampering | SHA-256 code/input/output binding + numerical acceptance | hashes prove bytes, not truth or source credibility |
| Stale output falsely satisfying reproduction | version-2 reproduction runs in a fresh temporary workspace where declared outputs are absent before execution | trusted code can still obtain data from undeclared ambient host resources |
| Analysis-code drift | version-2 `code` artifacts are hash-bound before execution and `experiment.entrypoint` must be declared and referenced by the command | the host interpreter, libraries, operating system, and other ambient dependencies are not automatically made hermetic |
| Malicious receipt command | verification is non-executing; reproduction is explicit, requires version-2 integrity checks, and uses `shell=False` | reproduction executes trusted code with host permissions and is not a sandbox |
| Dependency/CI drift | immutable Action SHAs, environment fingerprint, hosted matrix | Python package resolution can still change when ranges are intentionally broad |
| False confidence from green checks | scoped PASS semantics, explicit control counts, and disclaimers | human misinterpretation remains possible |
| Sensitive context in CI/logs | public-safe fixtures only; no real program evidence | future contributors/operators can still make mistakes |
| Stale decision basis | dependency-impact visibility and explicit reopen conditions | FMA does not autonomously determine when external reality changed |

## Reproduction integrity model

For a version-2 executable receipt, the intended machine-checkable path is:

```text
DECLARED CODE + DECLARED INPUTS
        ↓ verify hashes
FRESH TEMPORARY WORKSPACE
        ↓ outputs absent
TRUSTED DECLARED ENTRYPOINT
        ↓ shell=False
FRESH DECLARED OUTPUTS
        ↓ verify hashes + numerical checks
REPRODUCTION PASS
```

This establishes a stronger causal relationship between the declared code/input set and the verified output than an in-place rerun over a dirty working directory. It does not prove scientific truth, sandbox the code, prevent trusted code from reading ambient host resources, or establish complete environment equivalence.

## Security non-goals

FMA is not an authentication, authorization, encryption, classification, DLP, secrets-management, secure-storage, sandboxing, containerization, or hermetic-build system. Those controls belong to the deployment environment.
