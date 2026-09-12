# Attribution and Priority

Scientific Discovery Assurance records chronology without automatically deciding ownership, authorship, inventorship, or legal priority.

The profile can represent separate events for:

- concept
- construction
- proof
- formalization
- publication
- replication
- validation

A `ResearchPriorityReceipt` binds a declared artifact reference to a SHA-256 value and records the available time/signature evidence.

## Priority states

- `UNANCHORED` — only local or otherwise non-trusted timing evidence is available.
- `EXTERNALLY_ANCHORED` — a separately referenced external anchor is declared and verified.
- `SIGNATURE_VERIFIED` — separately referenced signature evidence is declared and verified.

A local clock value is never sufficient by itself to establish trusted priority.

These records provide evidence for later human or institutional review. They do not determine legal rights or scientific credit.
