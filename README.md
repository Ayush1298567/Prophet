# VANTAGE

> *Adversaries scatter their signals across domains. VANTAGE is the position above the noise — where the picture becomes one, and the next move becomes visible.*

**Project for:** 3rd Annual NatSec Hackathon · Shack15, San Francisco · May 2-3, 2026
**Problem statements addressed:** PS3 (Mission Command & Control) primary; PS1 (Sensor Analysis & Integration) and PS5 (General National Security) secondary.
**License:** MIT (open source per hackathon rules)

---

## TL;DR

VANTAGE is a multi-agent intelligence platform that turns the public-data firehose — AIS, ADS-B, news, sanctions lists, satellite imagery, cyber telemetry — into a real-time picture of what adversaries are *actually doing*. Where today's C2 systems show commanders **what is happening**, VANTAGE tells them **what is about to happen, what it means, what is being hidden, and how it all connects.**

A swarm of four specialized agents — a Forecaster, a Translator, an Unmasker, and a Synthesizer — runs continuously over live data, with the operator sitting in the human-in-the-loop seat that the AI can never bypass.

We can build a working version in 24 hours.

---

## Why VANTAGE Exists

Today's C2 stack — Palantir Gotham, Maven Smart System, Anduril Lattice, ATAK — has solved sensing, fusion, and dashboarding. But operators still complain about four hard gaps:

1. **They are reactive, not predictive.** Modern systems alert *after* a vessel goes dark, *after* a flight drops off radar, *after* the convoy is hit. They don't tell you what's *about* to happen.
2. **They show data, not meaning.** Operators get raw tracks and tentative IDs. A non-expert (a commander, a cabinet secretary, a coalition partner) can't read what the data implies for *their* decision.
3. **They miss active deception.** Adversaries spoof AIS, change MMSI, switch flags, ghost their transponders, and run ship-to-ship transfers in the dark. Most "anomaly" detectors notice *absence* of signal — they don't notice *active lies*.
4. **They're siloed by domain.** Maritime tools don't talk to cyber tools don't talk to news/SIGINT. Adversaries operate across all of them at once. A coordinated probe at sea + a port-network intrusion + a state-media announcement is one operation; today's C2 sees three unrelated alerts.

VANTAGE is built around closing exactly these four gaps.

---

## What VANTAGE Does — Four Agents, Four Promises

### 🔮 The FORECASTER — predicts what's about to happen
Maintains a library of "evasion patterns" mined from historical AIS/ADS-B gaps and their context. Continuously runs every tracked entity against the library using nearest-neighbor similarity on time-series features (heading volatility, owner-history, proximity to chokepoints, prior gap-frequency). When match-confidence crosses a threshold, raises a soft alert: *"Entity X likely to go dark within N minutes."*

**Demo moment:** a soft countdown timer next to a tanker — *"Predicted dark event in 00:23:14"* — and then it actually goes dark on stage. Once the judges see that happen live, you've won the round.

### 🗣️ The TRANSLATOR — explains what matters, to whom
Same evidence, different audiences. The same alert reads as:

| Audience | What they see |
|---|---|
| Tactical operator | "AIS gap, vessel 9342847, Hormuz at 27.4°N 56.8°E, ROE check requested" |
| Theater commander | "Iranian-linked tanker, sanctions hit on owner, fits ship-to-ship transfer pattern, 7th evasion this quarter" |
| Cabinet-level | "Iran is moving sanctioned crude through the Strait. ~$80M shipment. Likely buyer: China." |
| Public-facing | "An oil tanker is doing something unusual near the Strait of Hormuz." |

Built as one Codex agent with role personas. Cached completions. A single dropdown on each alert: **"Show me as ___."**

**Demo moment:** judge flips the dropdown live. Watches the same alert become actionable for four different people.

### 🎭 The UNMASKER — detects active deception
This is the one that turns judges' heads. Every other anomaly tool notices when a signal disappears. VANTAGE notices when a signal is *actively lying*.

Checks invariants the adversary cannot help breaking:
- **Kinematic plausibility** — could a ship physically have moved that far in that time?
- **Identity persistence** — has the MMSI / IMO / name been quietly changed?
- **Flag-of-convenience switches** — flag changes that precede sketchy runs by weeks
- **STS transfer signatures** — two vessels co-located, both AIS off, neither in port
- **Sensor-truth disagreement** — what AIS *claims* vs. what Danti's satellite imagery *shows*

When any invariant breaks, the Unmasker raises a flag with the specific contradiction.

**Demo moment:** side-by-side panel — *Claims* (left, white) vs. *Reality* (right, red). "Vessel claims to be 80km from here. Satellite says it's 400m off our pier."

### 🕸️ The SYNTHESIZER — connects across domains, surfaces intent
Runs a sliding temporal window across all feeds (maritime, aviation, news/GDELT, sanctions, optionally Shodan/Censys for cyber-side probes). Clusters events by time + geography + actor and asks the LLM: *"do these tell a coherent story?"* — with strong constraints to admit "no narrative" rather than confabulate.

When a story emerges, surfaces *one* unified alert that proposes the narrative and shows the receipts.

**Demo moment:** three boring individual alerts on the dashboard — a tanker incident, a port-system anomaly, a Xinhua statement. Then the Synthesizer pops up with one card: *"Possible coordinated probe — confidence 0.74"* with the four contributing events as expandable evidence. The judges understand they just saw *intent* synthesized from noise.

---

## Architecture

```
                     ┌─────────────────────────────────┐
   Live data feeds → │   Ingest layer (Python async)   │
                     │   AIS · ADS-B · GDELT ·         │
                     │   OpenSanctions · Danti · news  │
                     └──────────────┬──────────────────┘
                                    │ event stream
                     ┌──────────────▼──────────────────┐
                     │      AGENT SWARM (Codex)         │
                     │                                  │
                     │   FORECASTER ─┐                  │
                     │   UNMASKER ───┼─→ alert queue   │
                     │   SYNTHESIZER ┘                  │
                     │                                  │
                     │   TRANSLATOR ← (per-audience)    │
                     └──────────────┬──────────────────┘
                                    │ structured alerts
                     ┌──────────────▼──────────────────┐
                     │     VANTAGE CONSOLE (React)         │
                     │  • Live world map (Deck.gl)      │
                     │  • Swarm activity panel          │
                     │  • Audience dropdown             │
                     │  • Evidence drill-down           │
                     │  • Human-in-the-loop gate        │
                     └─────────────────────────────────┘
```

Tools (Danti, OpenSanctions, AIS history, satellite imagery) wrapped as **MCP servers** so any agent can call any tool. Each agent has a structured-output schema (Pydantic) and a hard 8-second timeout with a fallback path. Memory is a small SQLite-backed event store that persists across investigations so the swarm can recognize repeat-offender patterns.

---

## The 60-Second Demo Arc

1. **Open with a live world map.** Thousands of vessels and aircraft moving in real time. Mention this is real data, right now.
2. **The Forecaster ticks.** A tanker in the Strait of Hormuz gets a soft countdown — *"predicted dark event in 23 min."*
3. **It happens.** Vessel goes dark on stage. Forecaster confidence ratchets up.
4. **The Unmasker overlays.** A separate panel: *Claims* vs. *Reality*. Owner-on-paper says one thing; OpenSanctions says another. Kinematics impossible.
5. **The Synthesizer connects.** A second alert from the cyber feed (a port-system probe at Fujairah) joins the maritime alert, plus a Xinhua release about "freedom of navigation." One card pops: *"Likely coordinated probe — 0.74."*
6. **The Translator switches voices.** Judge picks "show me as cabinet secretary." The same alert becomes one paragraph the SecDef would actually read.
7. **The human gate.** Operator must accept or reject the synthesized alert before it propagates. *"Nothing happens without human sign-off."*
8. **Close:** *"Built in 24 hours. Running on real data. Open source."*

Total: 60 seconds. Three "holy shit" moments (the predicted dark event, the deception unmask, the cross-domain narrative). Judges remember.

---

## Tech Stack

**Core**
- Python 3.12 async backend (FastAPI + Server-Sent Events for live updates)
- React + TypeScript console (Vite, Tailwind, shadcn/ui)
- Deck.gl + Mapbox GL for the live world map
- SQLite (event store) + Qdrant (vector memory)
- OpenAI Agents SDK for the swarm orchestration
- MCP Python SDK for tool wrappers

**Data**
- AIS firehose: aishub.net + MarineCadastre historical
- ADS-B: OpenSky Network public API
- News: GDELT 15-min event feed + NewsAPI
- Entities: OpenSanctions + Wikidata grounding
- Geo intel & satellite: Danti
- Optional cyber: Shodan, Censys

**Models**
- OpenAI Codex / GPT-class for agents (per hackathon partner access)
- `sentence-transformers` (all-MiniLM-L6-v2) for cheap semantic clustering
- `scipy.spatial` for nearest-neighbor pattern matching

---

## Partner Tool Fit

| Partner | Role in VANTAGE | Why it matters |
|---|---|---|
| **OpenAI Codex** | Powers the four agents; written in JSON-schema'd ReAct loops | Built for exactly this; partner access removes the cost question |
| **Danti** | Geospatial intel + satellite imagery for the Unmasker | Underused by other teams = differentiation; gives Unmasker its punch line |
| **Palantir AIP** | (Optional) ontology + dashboard if a teammate is fluent | Fastest path to enterprise polish; skip if Foundry's learning curve eats too much time |

**Honest call:** for a 24-hour build, prioritize Codex + Danti + open stack. Add Palantir AIP only if a team member already knows Foundry — otherwise Workshop's learning curve will burn 6-8 hours you can't afford.

---

## Build Plan — 24 Hours, 4 People

### Hour 0-4 · Scaffolding (everyone)
- Repo stand-up, Codex access confirmed, Danti account live
- Data feeds connected and streaming to a local event log
- Bare React shell with map and an empty alert panel

### Hour 4-12 · Pillars in parallel
- **Person 1 — Forecaster.** Pattern-mining script over historical AIS gaps; nearest-neighbor matcher; Codex agent wrapper with confidence calibration.
- **Person 2 — Unmasker.** Kinematic + identity invariant checkers; Danti integration for sat-imagery cross-check; "Claims vs. Reality" panel.
- **Person 3 — Synthesizer + Translator.** Sliding-window event clustering; LLM narrative proposer with strict "no story" fallback; audience-persona translator.
- **Person 4 — Console + demo.** React map, swarm activity panel with live agent traces, audience dropdown, evidence drill-down. **Owns the demo script and rehearses it five times.**

### Hour 12-18 · Integration + agent debate panel
- All four agents publishing to one alert queue
- Visible agent reasoning trace on the right side of the console
- Pre-load three "hero scenarios" with cached real data so demo timing is deterministic
- Wrap external tools as MCP servers

### Hour 18-22 · Polish + scenario cache
- Smooth out the demo path — every click should feel intentional
- Pre-cache evidence packets for the three hero alerts
- Build a "live mode" / "demo mode" toggle so a quiet data window can't kill the pitch
- README, repo polish, license, GitHub public

### Hour 22-24 · Submission + dry runs
- Record the 1-minute demo video required for submission
- Push all dependencies, write quickstart, verify clean clone works
- Three full demo dry runs against a cold console

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Live data is too quiet during demo | "Live mode" / "demo mode" toggle with three pre-cached hero scenarios |
| LLM hallucinates a narrative | Synthesizer prompt forces "no narrative" output when evidence is thin; show source receipts on every claim |
| Agent latency stalls demo | 8-second hard timeout per agent; fallback to last-known-good; pre-warm model contexts |
| Unmasker triggers false positive on stage | Use historically-validated dark-vessel cases for the demo; show the kinematic math, not just the verdict |
| Looks like "ChatGPT for generals" | The four-agent swarm trace panel makes the work visible. Show debate, show tool calls, show evidence trails. |
| Scope creep into Battle Staff territory | Stay disciplined: this hackathon = the four pillars only. Battle Staff is the "what we'd build next" slide. |

---

## Why VANTAGE Wins (mapped to judging criteria)

| Criterion | Weight | VANTAGE's answer |
|---|---|---|
| **Technical Demo** | 35% | Working system on real live data. Three "holy shit" demo moments in under 60 seconds. Visible multi-agent trace. |
| **Military Impact** | 30% | Closes the four hardest gaps in current C2 (predictive · contextualization · deception · cross-domain). Every gap is a documented operator pain point. |
| **Creativity** | 25% | Four-agent swarm with visible debate, audience-aware translation, and active-deception detection are all under-explored. The "Claims vs. Reality" Unmasker pattern is fresh. |
| **Presentation** | 10% | "Today's C2 systems show commanders what's happening. VANTAGE tells them what's about to happen — and what it means." One sentence, locked in. |

---

## Future Direction (the "what we'd build next" slide)

VANTAGE is the awareness layer. The natural extension is **AI Battle Staff**: layer the U.S. Army's MDMP (Military Decision Making Process) on top, with specialized planning agents (S-2 intel, S-3 ops, S-4 logistics, S-5 plans) consuming VANTAGE alerts and producing courses of action with risk profiles. The commander gets not just *what's happening and why*, but *here are three ways to respond, ranked.*

Mention this in the pitch as a roadmap slide. Don't try to build it.

---

## Recommended Repos to Borrow From

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — swarm orchestration
- [pyais](https://github.com/M0r13n/pyais) — AIS message parser
- [dump1090](https://github.com/antirez/dump1090) — ADS-B decoder
- [Microsoft GraphRAG](https://github.com/microsoft/GraphRAG) — entity extraction backbone (for the Synthesizer)
- [Kepler.gl](https://github.com/keplergl/kepler.gl) / [Deck.gl](https://github.com/visgl/deck.gl) — geospatial viz
- [OpenSanctions](https://github.com/opensanctions/opensanctions) — entity grounding
- [milsymbol](https://github.com/spatialillusions/milsymbol) — military symbology if we want a TAK-flavored alert layer
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — tool wrappers

A fuller curation lives in `context/repo_explore.md`.

---

## Naming Notes

**VANTAGE** has two load-bearing meanings:
- A *vantage point* is a position from which you see what others can't — the elevation that turns scattered noise into a single picture → cross-domain synthesis
- *Vantage* (as in "advantage," "the upper hand") is what you have when you see the adversary's move before they make it → predictive forecasting and tempo

Both meanings describe what the product does. The name is short, plain English, easy to say on stage, and sounds confident without being a tryhard acronym. Don't backronym it.

---

## Submission Checklist

- [ ] GitHub repo public
- [ ] MIT license file
- [ ] README with quickstart (`make demo` runs the pre-cached hero scenarios)
- [ ] 1-minute demo video uploaded to YouTube/Loom and linked in submission
- [ ] All teammates listed
- [ ] Problem statement: PS3 selected
- [ ] Submission form: https://cerebralvalley.ai/e/3rd-annual-natsec-hackathon/submit

---

## Appendix: Key References

- [3rd Annual NatSec Hackathon](https://cerebralvalley.ai/e/3rd-annual-natsec-hackathon)
- [DoD Directive 3000.09 (autonomy in weapons)](https://www.dau.edu/blogs/new-dod-directive-300009-autonomy-weapon-systems)
- [Anduril Lattice — what we're not trying to clone](https://www.anduril.com/lattice/command-and-control)
- [Palantir Gotham / AIP — our architectural inspiration](https://www.palantir.com/platforms/gotham/)
- [Cursor on Target schema (FreeTAK docs)](https://freetakteam.github.io/FreeTAKServer-User-Docs/About/architecture/mil_std_2525/)
- [OpenSky Network](https://opensky-network.org/) · [aishub](https://www.aishub.net/) · [GDELT](https://www.gdeltproject.org/) · [OpenSanctions](https://www.opensanctions.org/)

Sister docs in `context/`:
- `hackathon_resources.md` — full hacker-resources packet (rules, schedule, prizes, partner access)
- `PS3_brainstorm_brief.md` — the wider research that led to VANTAGE (placeholder; add when written)
- `repo_explore.md` — full curated repo list (placeholder; add when written)
