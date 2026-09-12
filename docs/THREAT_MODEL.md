# Threat Model

## Assets

- integrity of the public reference implementation;
- confidentiality of nonpublic program information;
- integrity and provenance of declared evidence artifacts;
- clarity of human decision authority;
- integrity of release provenance and CI evidence.

## Trust boundaries

1. **Public repository boundary** — everything committed, discussed, logged, or released may become durable disclosure.
2. **Local validation boundary** — graph and receipt files may be malformed or adversarial.
3. **Reproduction boundary** — `fma reproduce` executes trusted repository code and is not a sandbox.
4. **Private-workspace boundary** — real program evidence must remain in a separate access-controlled environment.
5. **Supply-chain boundary** — package dependencies and CI Actions can change independently of FMA source unless pinned/recorded.

## Primary threats and controls

| Threat | Control | Residual risk |
|---|---|---|
| Accidental disclosure | synthetic-only policy, fail-closed file/URL scanner, manual contextual review | automation cannot infer every sensitive proper noun/value |
| Path escape in receipts | resolved-path containment checks | trusted code executed by reproduction can still access its environment |
| Artifact tampering | SHA-256 input/output binding + numerical acceptance | hashes prove bytes, not truth or source credibility |
| Malicious receipt command | verification is non-executing; reproduction is explicit and uses `shell=False` | reproduction is not a sandbox |
| Dependency/CI drift | immutable Action SHAs, environment fingerprint, hosted matrix | Python package resolution can still change when ranges are intentionally broad |
| False confidence from green checks | scoped PASS semantics and disclaimers | human misinterpretation remains possible |
| Private context in CI/logs | public-safe fixtures only; no real program evidence | future contributors/operators can still make mistakes |
| Stale decision basis | dependency-impact visibility and explicit reopen conditions | FMA does not autonomously determine when external reality changed |

## Security non-goals

FMA is not an authentication, authorization, encryption, classification, DLP, secrets-management, secure-storage, or sandboxing system. Those controls belong to the deployment environment.
