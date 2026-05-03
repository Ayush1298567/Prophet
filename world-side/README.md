# Forecaster — World Side

The Forecaster is Prophet's geopolitical intelligence engine. It ingests chatter and world-event signals, fuses them with a historical campaign corpus, and outputs a **strike window** (when) and **strike vector** (how) for a given exploit candidate.

**Owner:** Ayush

## What it outputs

Given an exploit candidate (JSON from the Exploit Engine), the Forecaster produces a `world_forecast` with:

- `strike_windows` — ranked time windows when an adversary is most likely to activate the exploit, with confidence scores, trigger signals, and historical analogies
- `strike_vectors` — ranked attack methods most consistent with the geopolitical context (e.g. edge-appliance initial access, supply chain, destructive wiper)
- `strategic_frame` — adversary class, target scope, forecast assumptions
- `summary` — one-line and recommended demo path

Full schema is in `INTERFACE.md`.

## What it does NOT do

- Does not predict specific CVEs or generate exploit code — that is the Exploit Engine's job
- Does not identify live targets — sector-level only
- Does not run on live infrastructure — all scraping is isolated to the scraper machine

## Directory layout

```
world-side/
├── README.md              ← this file
├── INTERFACE.md           ← JSON contract with Exploit Engine
├── forecaster/            ← Python forecasting engine
│   ├── generator.py       ← main entry point
│   ├── matcher.py         ← historical analogy matching
│   ├── scoring.py         ← window + vector scoring
│   ├── models.py          ← data models
│   ├── features.py        ← feature extraction
│   ├── loaders.py         ← corpus loaders
│   ├── corpus.py          ← corpus assembly
│   ├── chatter.py         ← chatter signal processing
│   ├── sources.py         ← source registry
│   └── cli.py             ← CLI entry point
├── scraper/               ← isolated scraper machine (SSH only)
│   ├── ACCESS.md          ← scraper architecture + OPSEC
│   ├── TEAMMATE_SETUP.md  ← 5-min SSH setup for teammates
│   ├── scraper_side/      ← scraper Python package
│   ├── config/            ← source catalog
│   └── bin/               ← collection + sanitization scripts
├── data/                  ← geopolitical corpus (research artifacts)
│   ├── historical_pairings.md    ← geopolitical event → cyber campaign pairs
│   ├── calendar_events.md        ← forward-looking threat calendar (May–Nov 2026)
│   ├── indictments_state.md      ← state-affiliated cyber indictments snapshot
│   └── sanctions_state.md        ← sanctions snapshot
├── fixtures/              ← exploit candidate mocks for dev/test
└── outputs/               ← generated forecasts
    ├── golden-*.json      ← hand-verified reference outputs
    └── generated-*.json   ← machine-generated outputs
```

## How to run

```bash
cd world-side
pip install -r scraper/requirements.txt

# Generate a forecast from a fixture candidate
python -m forecaster.cli --candidate fixtures/exploit-candidate-edge-appliance.json
# Output goes to world-side/outputs/
```

## Connecting to the Console

The Console (`prophet-console/src/data/worldSide.ts`) loads forecasts from `world-side/outputs/`. Golden fixtures are pre-loaded for the demo. To use a freshly generated forecast, copy it to `outputs/` and update the loader.

Live scraper data requires SSH access to the isolated scraper machine — see `scraper/TEAMMATE_SETUP.md`.
