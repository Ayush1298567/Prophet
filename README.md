# Prophet

Prophet is a policy-bound evidence system for defensive exposure prioritization. It helps a security team decide which exposure class to harden first, explain why that decision is reasonable, validate only in safe fixture or approved-sandbox modes, and hand off review artifacts to SOC and platform teams.

```text
prioritize exposure → explain evidence → validate safely → hand off review artifacts
```

The product claim is deliberately narrow. Prophet does **not** discover zero-days, generate offensive payloads, test live infrastructure, or deploy controls autonomously. It produces an auditable "why this first" package from approved asset/SBOM metadata, public vulnerability context, policy checks, deterministic validation summaries, and safe handoff templates.

> The full operator manual — every Make wrapper, validation-sprint command, and CLI contract — lives in [`docs/README_DETAILED.md`](docs/README_DETAILED.md) and [`docs/CLI_REFERENCE.md`](docs/CLI_REFERENCE.md).

## Why this exists

When the vulnerability queue is larger than the team can clear, the same operational question recurs: what should be hardened first, and what evidence proves that decision was reasonable? CISA KEV/BOD pressure, EPSS signals, SBOM obligations, and leadership scrutiny all push on it. Prophet's wedge isn't another scanner or exposure graph — it's a repeatable defensive evidence loop:

- **Prioritize** — rank the exposure class that deserves attention first.
- **Explain** — show source basis, asset/SBOM basis, confidence, freshness, and assumptions.
- **Validate safely** — deterministic fixtures, localhost, or an explicitly approved sandbox only.
- **Hand off** — export evidence, audit, SIEM, and ticketing review templates with no production pushes.

## What works today

| Surface | Notes |
|---|---|
| Forecaster | Deterministic Python; no runtime LLM or external API dependency. |
| Asset import | Customer-safe CSV metadata with row-level cleanup reports and seedsets. |
| Asset-seeded OSINT | Policy-gated, fixture-backed public-source snapshots. |
| Contract validators | Reject payloads, credentials, live targets, procedural instructions, schema drift. |
| Exposure-class portfolio | Safe, non-operational defensive class recommendations for analyst review. |
| Sandbox runner | Deterministic localhost fixture validation for the edge-appliance profile. |
| Evidence export | Policy-bound JSON + Markdown evidence bundles from validated fixtures. |
| Integration handoff | Safe SIEM and ticketing review templates from validated evidence. |
| Policy linting | Validates pilot policies, allowed modes, source IDs, sandbox profiles, output paths. |
| React operator console | Fixture-backed end-to-end replay with human gate and validation status. |

Live collection (`PROPHET_ENABLE_VM_SCRAPER=1`) is disabled by default and requires an approved isolated plan. Private lab research is not packaged — the public repo ships safe interfaces and fixtures only.

## Architecture

```text
approved asset/SBOM metadata        sanitized public context
            |                                |
   assets/ import + seedset          world-side/ forecaster
            |                                |
            +----------------+---------------+
                             v
                cyber-side/ defensive portfolio
                             v
                sandbox_runner/ fixture validation
                             v
                evidence/ bundle + audit trail
                             |
            +----------------+---------------+
            v                                v
 integrations/ review templates    prophet-console/ evaluator UI
```

The contracts are the product boundary: `world-side/INTERFACE.md` (candidate/forecast schemas), `cyber-side/INTERFACE.md` (defense artifact schema), `cyber-side/validator.py` (payload and live-target rejection), `world-side/forecaster/models.py` (forecast safety and schema validation).

## Quickstart

Prove the defensive pilot loop from a fresh clone, no live collection, no code reading. Requires Python 3.9+.

```bash
./scripts/check-local-env.sh
./scripts/run-pilot-demo-smoke.sh
```

This runs policy linting, safe asset import, seeded OSINT, forecast refresh, sandbox validation, evidence + audit export, and SIEM/ticketing handoff — all fixture-backed and localhost-only — then verifies the output hash against `scripts/pilot-demo-smoke.sha256`.

Run the full Python contract suite:

```bash
make python-tests
```

Run the evaluator console (localhost-only control API + UI in one terminal):

```bash
(cd prophet-console && npm ci)
make console-demo   # UI at http://127.0.0.1:5173, control server at http://127.0.0.1:8787
```

## Safety model

Prophet is built to be evaluated as a defensive decision-and-validation system, not an exploit-delivery system.

- No live infrastructure testing from the public console.
- No raw scraper output crosses into the main app.
- No credentials, IPs, or operational hostnames in committed artifacts.
- No payload bytes in accepted JSON contracts.
- OSINT snapshots use only approved source IDs; `sandbox_runner` uses only approved profiles.
- Production validation runs only in approved, isolated, vulnerable-by-design sandboxes.

See `SECURITY.md` for operating rules.

## Repository map

```text
assets/             Customer-safe asset/SBOM fixtures, import CLI, tests.
cyber-side/         Defensive portfolio fixtures, artifact contract, validator.
docs/               Pilot, validation, safety, release, and readiness docs.
evidence/           Policy-bound JSON/Markdown evidence bundles and audit helpers.
integrations/       SIEM, ticketing, and audit handoff template exporters.
policy/             Pilot policy schema, examples, linting, and tests.
prophet-console/    React operator console, localhost control server, browser tests.
sandbox_runner/     Deterministic localhost sandbox simulation profiles.
scripts/            Smoke, validation, release-safety, and operator helpers.
world-side/         Forecaster, source sanitization, fixtures, and outputs.
```

Stack: pure-Python standard library on the backend (no numpy/pandas/requests — the forecasting is heuristic and deterministic by design); React 19 + TypeScript + Vite for the console. Lab-only exploit validation scaffolding is not part of the public product tree.
