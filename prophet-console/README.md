# Prophet Console

The Prophet Console is the real-time web UI for Prophet's prediction pipeline. It displays:

- **Strike windows** — when the target is most vulnerable, from the Forecaster
- **Strike vectors** — how adversaries will likely strike, from the Forecaster
- **Exploit generation stream** — live agent reasoning as the Exploit Engine runs
- **Zero-day defense** — generated patch + Sigma rule, once the exploit loop completes

## Stack

React + TypeScript + Vite. No backend required for the demo — the Console loads forecaster output from static JSON files and replays recorded agent events.

## Run

```bash
cd prophet-console
npm install
npm run dev
# opens at http://localhost:5173
```

## How it connects to Prophet

### Forecaster data

Forecaster output lives in `world-side/outputs/*.json`. The Console loads it via `src/data/worldSide.ts`.

```ts
// src/data/worldSide.ts
import { getForecastForCandidate } from './worldSide';
const forecast = getForecastForCandidate('cs-fixture-edge-appliance-001');
// → { strike_windows: [...], strike_vectors: [...], strategic_frame: {...}, summary: {...} }
```

To use a freshly generated forecast: run the Forecaster, copy output to `world-side/outputs/`, update the candidate mapping in `worldSide.ts`.

### Exploit Engine stream

In the demo, the exploit agent stream is replayed from `src/data/mockEvents.ts` via `src/data/replayController.ts`. When Idan's live exploit engine is ready, wire its SSE stream to the same event types.

## Key components

| Component | What it shows |
|---|---|
| `StrikeWindowTimeline` | Strike windows from the Forecaster (ranked, dated, with confidence) |
| `ForecastPanel` | Strike vectors + strategic frame |
| `AgentStream` | Live reasoning stream from the Exploit Engine |
| `ExploitPanel` | Zero-day exploit prediction result |
| `DefencePanel` | Generated patch + Sigma rule |
| `ApprovalGate` | Human review gate between exploit and defense phases |
| `PhaseProgress` | Four-phase progress bar (INTEL → PLAN → EXECUTE → DEFEND) |
| `TriageQueue` | CVE triage queue (ranked candidates) |
| `PerlinHero` | Animated landing page background (Perlin noise, visual only) |
| `PreflightChecklist` | Pre-run environment checks |
| `LiveFeedTicker` | Scrolling geopolitical signal feed |
| `HistoricalAnalogyCard` | Historical campaign analogy cards |
| `LabTopology` | Lab environment topology diagram |
| `RunbookDrawer` | Collapsible runbook panel |
| `SourceCitation` | Source citation badges |
