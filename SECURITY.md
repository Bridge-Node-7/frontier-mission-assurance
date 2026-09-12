# Security and Data Handling

This public repository must contain only public-safe software, documentation, and synthetic fixtures.

It must not contain credentials, secrets, private keys, personally identifying information, real external program identities in worked examples, proprietary data, private system details, restricted technical data, nonpublic performance values, internal URLs, private repository links, screenshots, or raw logs that reveal private context.

See [`OPSEC.md`](OPSEC.md) and [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md).

## Public GitHub is a disclosure surface

Treat public issues, pull requests, Actions logs, uploaded artifacts, Discussions, release notes, commit history, branch names, and filenames as publicly observable. Deleting a file later does not guarantee removal from forks, caches, clones, logs, or history.

## Executing research receipts

`fma receipt` is verification-only and does not execute the declared experiment command.

`fma reproduce` **does execute repository code**. It verifies declared input hashes first, runs the command without a shell, and verifies outputs afterward. This reduces some accidental command-injection paths but does not make untrusted code safe.

Do not run `fma reproduce` on an untrusted receipt, checkout, fork, pull request, or artifact. Review the command and code first and use an isolated environment when appropriate.

## Real-program deployment

Use a separate access-controlled workspace with explicit classification, identity, authorization, retention, audit logging, artifact signing, backup, and incident-response policies. Do not mirror real evidence into this public repository.

If sensitive information or credentials are committed, assume exposure occurred. Rotate affected credentials immediately and follow the relevant incident-response process. History rewriting alone is not sufficient remediation.
