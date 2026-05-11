# Sandbox Container Target

Date: 2026-05-11

This target describes what Prophet must prove before any non-fixture sandbox
runner is packaged for a buyer pilot. It does not package or run a public
container profile, does not enable live validation, and does not change the
current fixture-backed pilot.

## Current State

The current public sandbox runner is deterministic and fixture-backed:

- `sandbox_runner` accepts only named fixture profiles in the public pilot.
- The run manifest schema allows only `mode: fixture`.
- The CLI rejects `mode: container` unless a sanitized customer approval record
  is supplied and `PROPHET_ENABLE_SANDBOX_RUNNER=1` is set.
- Even after those gates, the public repo still fails closed because no public
  container profiles are packaged.
- The generated run manifest records `safety.no_network_egress: true`,
  `safety.no_live_targets: true`, `safety.no_payloads: true`,
  `safety.no_credentials: true`, and `safety.no_raw_logs: true`.

This is enough for the local buyer pilot because no network validation is
performed. It is not enough to claim production sandbox isolation.

## Future Container Acceptance Target

Before container mode can be considered for a paid or sponsored pilot, every
container run must produce a reviewable manifest with:

- Image provenance: image reference, image digest, build context SHA-256,
  Containerfile or Dockerfile SHA-256, and optional SBOM SHA-256.
- No-egress proof: network disabled or explicit deny-all egress policy, DNS
  disabled or denylisted, and a recorded check result.
- Resource limits: CPU quota, memory limit, pids limit, writable disk limit,
  and hard timeout.
- Runtime hardening: read-only filesystem where practical, no privileged mode,
  dropped Linux capabilities, non-root user, and explicit mount list.
- Data boundary: no live targets, no credentials, no arbitrary URLs, no raw log
  retention, and write-only ignored runtime output paths.
- Approval boundary: sanitized customer approval, policy allowlist, operator
  approval, and audit event before any non-fixture mode runs.

## Required Future Tests

Do not mark the reproducible container work complete until automated tests
prove all of these fail closed:

- Missing or malformed image digest.
- Missing build context or Containerfile hash.
- Missing no-egress proof.
- Any network-enabled or privileged container setting.
- Missing CPU, memory, pids, disk, or timeout limit.
- Raw log retention, credential fields, hostnames, IPs, or target URLs.
- Container mode without customer approval, policy allowlist, and operator
  approval.

The existing tests only prove the current public boundary: fixture mode works,
container mode is not publicly packaged, and the run manifest keeps raw logs
out.

## Release Rule

Do not describe Prophet as having a reproducible, no-egress, resource-limited
sandbox container until a real container build path, manifest fields, verifier,
and tests exist for the exact release commit. Until then, use this language:

```text
Prophet currently uses deterministic fixture-backed localhost sandbox artifacts.
Container sandbox packaging is a future buyer-pilot hardening target and is not
enabled in the public pilot.
```
