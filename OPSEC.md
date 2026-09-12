# OPSEC for Public Use

Frontier Mission Assurance is designed so the **public codebase can stay generic while real evidence stays private**.

## Golden rule

> Public repository = software + synthetic fixtures only.

Do not use this public repository, its issues, pull requests, Actions logs, Discussions, release notes, or artifacts to store real customer/program evidence.

## Never paste into public GitHub

- personal names, direct contact information, private usernames, or account identifiers;
- external company, customer, supplier, partner, investor, or employer names in live case material;
- internal project names, codenames, ticket numbers, document IDs, repository links, or private URLs;
- exact internal architecture, performance, schedule, pricing, capacity, vulnerability, or procurement data;
- screenshots, raw logs, terminal history, stack traces containing private paths, or exported notebook metadata;
- credentials, API keys, tokens, cookies, certificates, private keys, `.env` files, or authentication material;
- export-controlled, controlled, classified, legally restricted, or contractually protected data.

## Public IDs

Use synthetic IDs such as:

- `MISSION-001`
- `CLAIM-004`
- `ASSUMP-012`
- `EVID-SYN-007`
- `DEC-003`

Do not encode real organization names, facility names, supplier names, employee initials, ticket numbers, or dates into identifiers.

## Private deployment pattern

Keep real work in a separate access-controlled repository or evidence store:

```text
public frontier-mission-assurance
        │
        └── reusable schemas + CLI + synthetic examples

private assurance workspace
        ├── real graph
        ├── authorized evidence
        ├── private receipts
        ├── signed artifacts
        └── access / retention / audit policy
```

Do not create a Git submodule or public link from the public repository to the private workspace.

## Before every public push

1. Run the automated scanner: `python scripts/opsec_scan.py .`.
2. Review `git diff --cached` manually.
3. Check newly added URLs, filenames, screenshots, logs, and fixtures.
4. Confirm examples are synthetic and generic.
5. Confirm no private repository or storage locators are present.
6. Confirm CI logs will not print sensitive source material.

Automation reduces mistakes; it cannot determine whether every proper noun or technical value is sensitive. Human review remains mandatory.
