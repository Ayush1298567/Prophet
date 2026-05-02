# VANTAGE — Project Scope (Living Doc)

> Internal working document. The README is the polished pitch; this is where we lock in the maximum coherent version of the product. **Mode: maximum coherent ambition.** With AI-assisted development we are not constrained by typical hackathon hour-counts — we are constrained by what we can rehearse, demo, and defend on stage. Every section here is the full version, not the MVP.
>
> Where the maximum version genuinely wins, we take the maximum version. Where the minimum is *correct* (8s timeouts, 4 personas, 60s submission video, one primary demo region), we defend the minimum and explain why. **Bigger ≠ better; coherent ambition wins.**

**Status:** ideation → locked-in scope
**Last updated:** 2026-05-02

---

## 0. North Star

VANTAGE is the position above the noise. From the right vantage point, scattered signals across maritime, aviation, cyber, news, finance, satellite, and drone-derived imagery become a single picture — and the next move becomes visible.

We are building a **multi-agent intelligence platform** that does what today's command-and-control stack can't:
- predicts adversary moves before they happen,
- detects active deception by cross-checking what's claimed against what's actually true,
- surfaces intent across domains as a single coherent narrative,
- translates the result for whoever needs to act on it,
- and gives the operator a 3D, time-scrubbed, drone-and-satellite-grounded world to reason in.

Built for the intelligence staff officer (S-2) who has to brief a commander before the morning sync. The product is **decision support, not weapons employment.** Every recommendation has receipts. Every action has a human gate. Aligned with DoD Directive 3000.09 from the first commit.

This is not a hackathon prototype. We are building the production-quality v1 of a real defense product, on a hackathon timeline, with AI-assisted engineering.

---

## 1. The Opportunity

### The four gaps in modern C2

Today's stack — Palantir Gotham/AIP/Maven, Anduril Lattice, ATAK — has won at sensing, fusion, and dashboarding. But operators still hit four hard walls:

1. **Reactive, not predictive.** The system alerts *after* a vessel goes dark, *after* a flight drops off radar, *after* the convoy is hit. There's no mechanism to surface "this entity is *about* to do something."
2. **Data, not meaning.** Operators get tracks and tentative IDs. A non-expert (commander, secretary, coalition partner) cannot read what the data implies for *their* decision.
3. **Misses active deception.** Adversaries spoof AIS, change MMSIs, swap flags, ghost transponders, run STS transfers in the dark. Current "anomaly" detectors notice *absence* of signal — not *active lies*.
4. **Siloed by domain.** Maritime tools don't talk to cyber tools don't talk to news/SIGINT. Adversaries operate across all of them in the same operation; today's C2 sees three unrelated alerts.

VANTAGE is built around closing exactly these four gaps.

### Why now

- **CJADC2** is the DoD's umbrella for unifying C2 across services and coalition partners. CENTCOM has a deployed MVP since spring 2024. New AI tools can plug in.
- **Palantir AIP got DIA classified-network accreditation in late 2024** for GPT-class models. The era of "no LLMs near classified data" is officially over.
- **Anduril won a multi-billion Army C2 consolidation contract.** New entrants need a clear gap-in-the-stack story; "we make Lattice smarter at the prediction and deception layers" is exactly that.
- **Gray-zone activity is the dominant operating mode.** Houthi attacks in the Red Sea, Russian shadow fleet, Chinese maritime militia, severed Baltic cables — all cases where today's C2 is structurally weak.
- **3D Gaussian splatting hit production-grade in 2024-2025.** A photorealistic 3D world model is now achievable on a laptop GPU. No incumbent C2 has this.

---

## 2. Hackathon Context

3rd Annual NatSec Hackathon, Shack15 SF, May 2-3 2026. Hacking 1145 Sat → 1200 Sun. ~3-min pitch + 1-2 min Q&A in round 1; top six demo on stage. $20k for 1st, scaling to $4k for 5th. Public GitHub repo at submission, MIT license, all work from scratch on-site, up to 4 teammates, 1-min demo video required. Partners: OpenAI Codex, Danti (geo intel), Palantir AIP. Primary problem statement: **PS3 (Mission C2)**. Secondary: PS1 (sensor fusion), PS5 (general).

**Judging weights:** Technical Demo 35% · Military Impact 30% · Creativity 25% · Presentation 10%. Our scoring story:
- *Technical:* live system on real public data, 3D world, multi-model agent ensemble, visible reasoning, full provenance.
- *Military Impact:* every gap we close is a documented operator pain point; full DoD 3000.09 compliance posture.
- *Creativity:* four-agent swarm with visible debate, audience-aware translation, active-deception detection, Gaussian-splat reality grounding, knowledge-graph multi-hop reasoning.
- *Presentation:* one locked tagline, three rehearsed demo packs (Hormuz / Taiwan / Black Sea), real ships, real chokepoints, real ownership trails.

> The 24-hour build budget is a *demo deadline*, not a scope ceiling. AI-assisted development eliminates the "we ran out of time to add X" excuse. We do not slack on any axis. Every feature we ship is rehearsed, reliable, and defensible under stage Q&A.

---

## 3. The Agent Swarm

### 3.1 Forecaster — predicts what's about to happen

**Goal:** "Entity X likely to do Y within N minutes" with calibrated confidence and full historical receipts.

**Architecture (max version):**

1. **Pattern library — 500+ curated historical incidents** across seven categories: dark events, STS transfers, port probes, flag flips, ownership pivots, pre-attack staging, sanctions-evasion runs. (See §5 for curation pipeline.)
2. **Featurization with 24+ engineered features per entity:** heading volatility, owner-history depth, distance-to-chokepoint, time-since-last-port, prior gap frequency, flag-change recency, AIS message quality (timestamp jitter, position quantization), kinematic plausibility margin, sanctions-network proximity (graph hops), draft-vs-cargo-declaration consistency, port-rotation entropy, identity-mutation history, peer-vessel co-location patterns, weather-route plausibility, etc.
3. **Multi-model ensemble:**
   - **Nearest-neighbor retrieval** over the pattern library (cosine + scaled-Euclidean) — fast, fully explainable, surfaces matching incidents as receipts.
   - **Small temporal transformer** trained offline on the historical AIS dump, predicting next-state distributions over the next N minutes — captures dynamics the NN misses.
   - **Disagreement between the two** is itself a signal surfaced to the operator.
4. **Confidence calibration UI** — every prediction shows not just confidence but historical accuracy: *"Forecaster is 87% accurate on dark-event predictions in the last 90 days (n=47)."* Operators trust calibrated confidence; uncalibrated is a red flag and a Q&A trap.
5. **Per-prediction provenance** — every forecast surfaces matching historical cases with one-click drill-down: source URL, full incident timeline, feature-by-feature comparison.
6. **Global Fishing Watch (GFW) signal layer** — GFW pioneered dark-vessel detection methods (loitering, encounters, port-state matching) and publishes both data and methodology. We ingest their public dataset and reuse their feature definitions for the Forecaster, weighted alongside our own.

**Why max version:** explainability + calibration + ensemble + best-in-class external signals = four independent axes of credibility. Each alone is good; together they're what a real intel product looks like, not a hackathon demo.

**Demo moments:**
- Countdown timer ticking down to a vessel's predicted dark event.
- Matching historical case popping up next to the live entity, side-by-side feature comparison.
- Calibration sidebar updating in real time as predictions resolve on the time scrubber.
- Ensemble disagreement signal: *"NN says dark in 23 min (high conf). Transformer says no dark event likely. Operator review."*

### 3.2 Unmasker — detects active deception

**Goal:** detect *active* deception, not just signal absence.

**Invariant suite — 14 invariants (vs. v1's 6):**

Maritime:
1. Kinematic plausibility (position-velocity consistency over time)
2. Identity persistence (MMSI/IMO/name change detection across voyages)
3. Flag-of-convenience switch tracking with predictive lookahead
4. STS transfer signatures (co-location + AIS-off + non-port)
5. Sensor-truth disagreement (AIS vs. Danti satellite vs. drone splats)
6. Owner-network disagreement (registered owner vs. beneficial-owner trail vs. OpenSanctions)
7. AIS message-quality forensics (timestamp jitter, position quantization, NMEA checksum oddities)
8. Cargo-declaration vs. vessel-behavior consistency (laden tanker speed profile, draft-vs-declaration)
9. **Schedule-vs-physics** — declared route, ETA, port-rotation, and cargo against actual kinematics, weather plausibility, and chokepoint timing. Flags vessels whose declared trip doesn't match what physics permits.

Aviation:
10. ADS-B kinematic plausibility
11. Callsign reuse / spoofing detection

Multi-domain:
12. Temporal-anomaly correlation (multiple invariants tripping simultaneously on the same entity)
13. Adversary-playbook fingerprint match (set of broken invariants matching a known deception pattern from the historical library)
14. **RF-geolocation invariant** (Hawkeye-360-style) — when AIS claims a vessel is dark or far away but RF emissions geolocate it elsewhere, flag the contradiction. *"You can go dark on AIS, but you can't go dark on physics."* Mock-data acceptable for v1; integrates with real Hawkeye / Spire / KSAT feeds when available.

Each invariant breakage produces a structured contradiction event with severity, evidence, source attribution, and a "fix or ignore" routing suggestion to the operator.

**Stretch (post-hackathon):** acoustic/MASINT signature checks, full Hawkeye-360 / Spire RF API integration, space-domain proximity-ops invariants, InSAR sub-mm deformation checks for fixed sites.

**Demo moments:**
- *Claims vs. Reality* split panel — left: AIS-claimed position, right: drone-splat-grounded actual position with the vessel rendered in 3D.
- Fingerprint-match invariant firing: *"This combination of kinematic + identity + flag invariants matches the deception pattern of M/V Helena (incident #047). Confidence 0.91."*

### 3.3 Synthesizer — connects across domains, surfaces intent

**Goal:** when scattered cross-domain events are part of one operation, surface the unified narrative — with strict guardrails against confabulation.

**Architecture (max version):**

1. **Sliding temporal window** (configurable: 15min/1hr/6hr/24hr) across all feeds.
2. **Entity-resolved event clustering** by time, geography, and actor — entities pre-resolved against the knowledge graph.
3. **Knowledge graph backbone** (GraphRAG-style) — every ingested event creates/updates nodes (entities, locations, organizations, persons) and edges (ownership, co-location, communication, incident-history). Graph queryable for multi-hop reasoning: *"vessel A's owner shares a director with vessel B's owner who was sanctioned by OFAC in 2024."*
4. **Multi-model narrative ensemble** — Codex and Claude both propose narratives independently from the same evidence cluster. Agreement → high-confidence alert. Disagreement → either suppressed or surfaced as itself a signal (*"the models disagree on what this means — operator review recommended"*).
5. **Strict no-confab discipline** — both models prompted with structured-output schemas and forced to return `{"narrative": null, "reason": "evidence insufficient"}` when the cluster doesn't support a story. Confabulation is a fireable offense; we'd rather miss a real story than invent one.
6. **Per-narrative provenance graph** — every claim in every narrative traceable back to a specific source event with one click; the entire reasoning chain is auditable.
7. **Satellite-overpass correlator** — for every alert, surface which (and *whose*) satellites were overhead at the time, using NORAD TLEs (Celestrak / N2YO). *"China's Gaofen-12 passed 4 minutes before this event."* Forces the narrative to consider attribution.
8. **Capture-before-cache-clears agent** — when Forecaster confidence crosses a threshold, an autonomous capture agent immediately snapshots all volatile evidence (AIS gaps, ADS-B drops, Telegram channel state, Sentinel-1 tasking schedule, news article DOM, X/Twitter posts). Adversaries delete; we freeze. Every capture is timestamped + hashed + signed for chain-of-custody.
9. **Transit-count ground-truth metric** — per chokepoint, count actual transits per hour and compare to declared schedules / historical baselines / official narratives. Surface deltas as a numeric signal (e.g., *"Hormuz transits down 92.2% in the last 6h"*). Bilawal's Hormuz-replay demo proved this number alone tells the story.
10. **Deep entity resolution stack** — every entity ingested gets resolved against GLEIF (Global Legal Entity Identifier Foundation), OpenCorporates (130+ jurisdictions), and OpenSanctions in a single canonical-ID lookup. Eliminates the "Helena vs MV Helena vs Helena Marina Ltd" problem; gives the knowledge graph stable nodes.
11. **GDELT GKG integration** — pull pre-extracted entities + relationships from GDELT's Global Knowledge Graph (already done at scale, free) into our knowledge graph as a base layer. We add the cross-domain reasoning on top.
12. **Live commodity / market correlator** — overlay Brent / WTI / LNG futures (Yahoo Finance / Alpha Vantage free APIs) on the event timeline. When a maritime event correlates with an oil-price move, surface the correlation. Bilawal's Hormuz demo proved this is the single most legible signal for non-military audiences.

**Demo moments:**
- The "lone alerts become coordinated probe" beat with three contributing events expanding into a knowledge graph view.
- The disagreement signal: *"Codex says probe (0.74). Claude says coincidence (0.31). Operator review recommended."* — judges love this because it shows we know LLMs are fallible.
- Multi-hop graph query: *"Why is this vessel suspicious?"* → graph walk → *"owner-of-owner sanctioned 2024."*
- Satellite-overpass correlation: *"This event happened 4 min after Gaofen-12 (CN) passed overhead. Coincidence rated low."*
- Transit-count surfaced as a single hero metric: *"Hormuz: 14 transits/hr → 1 transit/hr in 6h. 92.8% drop. Brent up 7.2%."*

### 3.4 Translator — explains what matters, to whom

**Goal:** same alert, every audience that matters.

**Persona library (max version):**

Native audiences (4):
1. Tactical operator (terse, callsign-heavy, ROE-aware)
2. Theater commander (strategic context, pattern-of-life)
3. Cabinet-level (one paragraph, dollar amounts, named adversaries)
4. Public-facing (neutral, source-attributed, no operational specifics)

Coalition audiences (4):
5. UK Royal Navy / Five Eyes (locale, units, time zones)
6. Australian Border Force / RAN
7. Japanese Maritime Self-Defense Force
8. Philippine Coast Guard

Foreign-language outputs (4):
- Arabic, Mandarin, Russian, Tagalog — Codex-translated, marked as machine-translated, ready for human-in-loop review by a linguist before partner release.

> **Defended minimum:** we cap *the dropdown* at 4 native audiences in the demo UI. More dropdown options dilutes the "judge flips through and watches the same alert reframe four times" beat. Coalition + foreign-language outputs are accessed via a secondary expand panel, not the main dropdown. Quantity in the persona library; clarity in the demo surface.

**Demo moments:**
- Judge flips through all four native audiences live (the original beat).
- Coalition-mode toggle: *"show this to Australia."* Output reframes vessel names, time zones, units.
- Translation toggle: *"show this in Mandarin."* Output appears with a "machine-translated, human-review pending" banner.
- Cabinet-tier overlay: live oil-futures chart appears alongside the alert summary. *"Iran is moving sanctioned crude through the Strait. ~$80M shipment. Brent up 1.4% in the last hour."*

---

## 4. Reactive UX

VANTAGE is **never passive.** Every surface is operator-driven.

### 4.1 Investigate-on-anything
Click any vessel, aircraft, event, location, alert, or knowledge-graph node → full swarm pivot, live reasoning streamed in the swarm panel. 3D globe zooms; spatiotemporal context loads (splat scene if available, time scrubber positioned).

### 4.2 Natural-language query bar
Powered by the knowledge graph + event store + Synthesizer. Examples:
- *"Anything weird in the Red Sea in the last 6 hours?"*
- *"Show me Iranian-linked tankers near a Chinese-operated port."*
- *"Has anything matched the Helena pre-dark pattern this week?"*
- *"Which vessels have flipped flags more than twice in 2026?"*
- *"Give me a knowledge-graph view of M/V Helena's ownership chain."*
- *"Compare the Bandar Abbas dock today vs. last Tuesday."* (splat change detection)

### 4.3 Sandbox / Replay mode
- Replay any past 24h+ of data with the swarm running fresh — Forecaster predictions are scored against actual outcomes as time advances (live calibration in action).
- Inject a counterfactual: *"what would the swarm do if AIS dropped for 30 minutes in CENTCOM?"*
- Run training drills against historical incidents with the operator stepping into the seat.

### 4.4 Human gate (everywhere, audited, signed)
For any synthesized alert: **accept · reject · escalate · annotate.** Every action timestamped, cryptographically signed (operator key), exportable as evidence package. Tiered authorization: operator can accept; only commander-tier user can authorize escalation to ATAK push or partner notification. Full chain-of-custody.

### 4.5 Multimodal upload
Operator drops in a satellite image, screenshot of a Telegram channel, PDF report, or drone clip → system OCRs/parses/extracts entities, indexes into the event store, and starts tracking referenced entities. Each upload becomes a typed event with provenance.

### 4.6 Briefing generator
*"Give me my morning brief"* → Translator synthesizes the last 12h of high-priority alerts into a one-page brief tailored to the selected persona. Exportable as a properly-formatted PDF. Ready to walk into a SCIF with.

### 4.7 Voice command (stretch — defended)
> **Defended skip:** voice control sounds cool but is a demo failure mode (mic noise in a hackathon room kills it). We support keyboard shortcuts for power users instead — every reactive action has a hotkey, logged in `?` overlay.

---

## 4.5 Spatiotemporal Context Layer

The world model the swarm reasons against. **Not "a 3D viewer."** Three integrated components:

### 3D globe
Cesium-rendered globe with terrain elevation. Entities (vessels, aircraft, sensors, alerts) rendered as 3D billboards or models. Camera flies smoothly between viewpoints. Day/night terminator, weather overlay (NOAA marine), AIS density heatmap. Default view; 2D Deck.gl as fallback.

### Time scrubber
Continuous timeline over the hero region's last 7 days (Hormuz primary; Taiwan and Black Sea pre-loaded for backup demos). Scrub to any point and the world re-renders to that moment: entity positions, alert states, agent reasoning at the time. Operator can rewind to "before the Helena dark event" and watch the Forecaster's countdown play forward against the timeline.

### Splat library
**~5+ pre-baked Gaussian splats of hero scenes** processed ahead of the demo from public OSINT drone footage:
- Bandar Abbas oil terminal, Iran
- Houthi launch site at Saada, Yemen
- Mischief Reef, South China Sea (Chinese reclaimed island)
- Sevastopol naval base, Crimea (Russian Black Sea fleet)
- Strait of Malacca pilot station

Each geo-anchored. Surfaced via Investigate when the operator clicks a location with a matching splat. Operator can fly the camera through the scene in real time. **The Unmasker uses the splat as the "reality" reference for its Claims-vs-Reality panel — vessels rendered into the splat at their AIS-claimed and ground-truth positions side-by-side.**

**Architectural framing for the pitch:** this is not "a 3D viewer." It is the spatiotemporal substrate the agents reason against.
- The Forecaster validates predictions against the time scrubber's playback.
- The Unmasker uses splats as reality-truth.
- The Synthesizer's knowledge-graph nodes are spatially grounded.
- The 3D globe is just where everything lives.

**Stretch (§15):** live splat training from streaming drones, splat change detection (T1 vs. T2 diffing), splat-derived feature extraction (count vehicles, measure dock occupancy).

### Visual treatment — the "spy aesthetic" shader pack

A Bilawal-grade visual layer that runs over the 3D globe and entity layers. Demo-polish per hour is the highest in the project.

- **CRT scanline shader preset** — instant operations-center vibe.
- **NVG / night-vision shader preset** — green tint, bloom, edge enhancement.
- **FLIR / thermal shader preset** — heat-coded entity highlights; pairs with the Unmasker ("thermal signature inconsistent with declared cargo").
- **Configurable post-FX panel** — bloom, sharpening, vignette, chromatic aberration. Operator-tunable; demo defaults to "cinematic."
- **Sparse-vs-full detection toggle** — show only Forecaster-flagged entities, or every blip on Earth.
- **Cinematic camera arcs** — programmable smooth zooms from globe → region → entity for every alert. Don't cut, *arc*.
- **GPS-jamming tile renderer** — colored hex grid overlaying jammed regions, pulled from ADSBExchange GPS-interference tiles. Bilawal's signature feature in the Iran replay.
- **No-fly-zone propagation animation** — watch zones spread over time during a crisis (cascading lockdowns), tied to the time scrubber.
- **Particle-system traffic on OSM road network** — animated flow density driven by inferred activity. Pure cinematic eye-candy.
- **NORAD-ID-on-hover** — hover any vessel/aircraft/satellite, popup shows ID, recent track, and ownership trail.
- **Pipeline / undersea-cable overlay** — 3D ribbons on the globe; sets up the Baltic-cable demo pack.
- **Cascading event visualization** — when one event triggers downstream events (e.g., maritime probe → no-fly zone → cyber probe), draw animated edges between them.

**Defended skip:** projected live CCTV onto buildings (cool but bandwidth-heavy and brittle on stage). Pre-bake one or two hero-scene CCTV stills as splat overlays instead.

---

## 5. The Historical Pattern Library

**Target: 500+ curated historical incidents at v1, growing.**

**Categories (with ~v1 case counts):**
- Dark events (~150)
- STS transfers (~80)
- Port / cyber probes (~50)
- Flag-of-convenience flips (~60)
- Ownership pivots (~40)
- Pre-attack staging (~70)
- Sanctions-evasion runs (~50)

**Sources:**
- TankerTrackers public reports
- Lloyd's List Intelligence (open snippets)
- EU sanctions enforcement notices
- OFAC SDN designations + accompanying reports
- US Navy / Coast Guard public press
- Maritime Executive, gCaptain, FreightWaves
- GDELT events + linked news articles
- Bellingcat investigations
- Marinecadastre AIS history dumps
- Academic papers on shadow-fleet behavior
- ACLED conflict events database (for pre-attack staging)
- Atlantic Council DFRLab reports

**Curation pipeline (semi-automated):**
1. Source ingest → raw incident records (Codex-assisted parsing)
2. Manual normalization → structured incident schema (human review)
3. Featurization → vector + metadata
4. **Validation against held-out behavior** — does the live entity matcher reproduce the labeled outcome on a 20% held-out subset? Iterate until precision >0.85 at 0.7 confidence threshold.
5. **Semi-supervised expansion** — use v1 library to bootstrap discovery of similar patterns in the historical AIS dump; human-review the candidates; promote validated cases to v2.

**Per-case provenance:** every case in the library carries source URL, ingest date, curator initials, validation status, and a per-feature "how was this measured" trail. Auditable end-to-end.

---

## 6. Architecture

```
                     ┌────────────────────────────────────────┐
   Live data feeds → │   INGEST LAYER (Python async)          │
                     │   AIS · ADS-B · GDELT · NewsAPI ·      │
                     │   OpenSanctions · OFAC · EU sanctions ·│
                     │   Wikidata · ACLED · Danti · NOAA ·    │
                     │   Shodan · Censys · Telegram OSINT ·   │
                     │   pre-recorded drone OSINT             │
                     └───────────────────┬────────────────────┘
                                         │ event stream
                                         ▼
                     ┌────────────────────────────────────────┐
                     │   STORAGE LAYER                        │
                     │   • Postgres + TimescaleDB (events)    │
                     │   • Qdrant (entity / pattern vectors)  │
                     │   • Knowledge graph (Postgres + AGE,   │
                     │     or Neo4j if needed)                │
                     │   • Splat asset store (S3-compatible)  │
                     │   • Redis (hot alert cache, sessions)  │
                     └───────────────────┬────────────────────┘
                                         │
                     ┌───────────────────▼────────────────────┐
                     │   AGENT SWARM (Codex + Claude ensemble)│
                     │                                        │
                     │   FORECASTER ─┐  (NN + transformer)    │
                     │   UNMASKER ───┼─→ alert queue          │
                     │   SYNTHESIZER ┘  (Codex + Claude)      │
                     │                                        │
                     │   TRANSLATOR ← (per-audience, cached)  │
                     │                                        │
                     │   All MCP-tool-callable, Pydantic out, │
                     │   8s hard timeout, fallback paths      │
                     └───────────────────┬────────────────────┘
                                         │ structured alerts
                                         ▼
                     ┌────────────────────────────────────────┐
                     │   API LAYER (FastAPI + SSE + WS)       │
                     │   • alerts stream                      │
                     │   • investigate(entity_id)             │
                     │   • query(nl)                          │
                     │   • sandbox / replay                   │
                     │   • accept/reject/escalate (signed)    │
                     │   • upload (multimodal)                │
                     │   • brief                              │
                     │   OpenAPI 3.1 spec, generated client   │
                     └───────────────────┬────────────────────┘
                                         │
                     ┌───────────────────▼────────────────────┐
                     │   VANTAGE CONSOLE (React + TS)         │
                     │  • Cesium 3D globe (default view)      │
                     │  • Time scrubber (7-day hero region)   │
                     │  • Splat scene viewer (gsplat.js)      │
                     │  • Knowledge-graph view (Cytoscape)    │
                     │  • Swarm activity panel (live trace)   │
                     │  • Audience dropdown + coalition panel │
                     │  • Evidence drill-down                 │
                     │  • NL query bar                        │
                     │  • Investigate button                  │
                     │  • Live / Demo / Sandbox toggle        │
                     │  • Human gate (signed accept/reject)   │
                     │  • Audit trail viewer                  │
                     │  • Briefing generator                  │
                     │  • Multimodal upload                   │
                     └────────────────────────────────────────┘

         ┌────────────────────────────────────────────────────┐
         │   OBSERVABILITY (cross-cutting)                    │
         │   • OpenTelemetry traces across agents + API       │
         │   • Structured logging (JSON + event correlation)  │
         │   • Metrics (Prometheus-compatible)                │
         │   • Audit log (append-only, signed)                │
         └────────────────────────────────────────────────────┘
```

**Agent invariants:**
- Pydantic structured-output schemas; anything that doesn't validate is rejected.
- 8s hard timeout per agent, fallback to last-known-good or `null` narrative. *(Defended minimum: timeout stays tight. Slower agents = worse demo, regardless of compute available.)*
- All tool calls (Danti, OpenSanctions, AIS history, satellite, Shodan, knowledge graph, splat lookup) wrapped as **MCP servers** so any agent can call any tool.
- Every alert carries a full evidence trail (event IDs, source URLs, confidence math, matching historical cases, knowledge-graph paths). **Nothing is unsourced.**
- Every agent decision traced via OpenTelemetry, viewable in the audit trail.

---

## 7. Tech Stack — Production-Grade

**Backend**
- Python 3.12 async (FastAPI + Server-Sent Events + WebSockets)
- OpenAI Agents SDK for swarm orchestration
- Anthropic SDK for Claude ensemble agents
- MCP Python SDK for tool wrappers
- Pydantic v2 for schemas
- **Postgres 16 + TimescaleDB** for the event store *(upgraded from SQLite — proper time-series queries, hypertables, continuous aggregates)*
- **Postgres + Apache AGE** for the knowledge graph (cleaner ops than Neo4j for our scale)
- Qdrant for vector memory + pattern library
- Redis for hot alert cache and session state
- `sentence-transformers` (all-MiniLM-L6-v2) for embeddings
- `scipy.spatial` + custom kNN for nearest-neighbor matching
- PyTorch for the small temporal transformer (offline training)
- `pyais` for AIS parsing
- `httpx` async for source ingest
- OpenTelemetry SDK for tracing

**Frontend**
- React 18 + TypeScript (Vite)
- Tailwind + shadcn/ui (consistent design system)
- **CesiumJS** for the 3D globe (default view); Google Photorealistic 3D Tiles for terrain
- Deck.gl for 2D fallback + density heatmaps; Kepler.gl as emergency fallback if Cesium dies on stage
- **In-browser splat rendering:** `gsplat.js` or `mkkellogg/GaussianSplats3D` (lighter, MIT, fork-ready)
- **Splat training pipeline:** Reality Capture (Epic) for photogrammetry posing → Postshot (NVIDIA GPU) or Brush (Apple Silicon) for production splats. For custom training pre-event: `nerfstudio-project/gsplat` (Apache 2.0, PyTorch reference impl). Output to SPZ/glTF for browser delivery.
- Custom GLSL shader pack (CRT / NVG / FLIR / post-FX) wired into Cesium PostProcessStage
- `skyfield` (Python) + `satellite.js` (browser) for NORAD TLE propagation
- **`uber/h3-py` + `uber/h3-js`** for hex-grid spatial index — chokepoint clustering, GPS-jamming tile renderer, AIS-density bucketing
- Cytoscape.js for knowledge-graph view
- TanStack Query for alert stream + cache
- Zustand for client state
- Framer Motion for state transitions
- `milsymbol` for TAK-flavored alert glyphs

**Models**
- OpenAI Codex / GPT-class via the partner workspace (primary)
- Anthropic Claude (ensemble narrative + second opinion)
- `sentence-transformers` (local) for embeddings
- Custom temporal transformer (PyTorch, offline-trained on historical AIS)

**Infra & Ops**
- `docker-compose` brings up the entire stack locally with one command
- `Makefile` with `make demo`, `make dev`, `make test`, `make lint`
- GitHub Actions CI: type checks (mypy), lint (ruff), tests (pytest), frontend type check + build, smoke test
- OpenAPI 3.1 spec auto-generated from FastAPI; Swagger UI hosted at `/docs`
- Env management: `.env.example` with every key, `pydantic-settings` for typed config
- Vercel for the public frontend (if we want a hosted demo)
- Local laptop for the backend on stage (one less moving part)

**Build harness (for the build itself, not the product)**
- **Aider** (`Aider-AI/aider`, Apache 2.0) as the multi-LLM CLI — supports parallel Claude/Codex/Gemini sessions, in-repo edits, auto-test loops
- tmux layout with one Aider window per agent (backend / frontend / data ingest / docs / pattern library curation)
- Shared `WORKING.md` scratchpad for agent coordination
- Auto-commit-on-test-pass via pre-push hook

---

## 8. Data Sources — Maximal Ingest Breadth

| Source | Use |
|---|---|
| aishub.net + MarineTraffic + VT Explorer | Live AIS (multi-provider redundancy) |
| MarineCadastre historical dump | Historical AIS for pattern library + temporal model training |
| OpenSky Network | Civilian ADS-B flight tracking |
| **ADSBExchange** | Military flight tracking (filters out by other providers) + GPS-jamming interference tiles |
| **NORAD TLEs (Celestrak / N2YO)** | Live satellite tracking — every alert correlates with overhead sats, attribution by satellite operator |
| **Hawkeye 360 / Spire RF** | RF geolocation of dark vessels — physics-grounded Unmasker invariant ("can't go dark on physics") |
| **USGS earthquake feed** | Live ground events; gives the globe a "the earth is alive" baseline |
| **OpenStreetMap (Overpass API)** | Landmark POIs, port locations, military base outlines, road network for particle traffic |
| **Public CCTV streams** (port cams, city feeds) | 1 frame/min projected onto 3D geometry for hero scenes |
| **Global Fishing Watch API** | Dark-vessel detection signals (loitering, encounters, port-state matching) — Forecaster signal layer |
| **GLEIF (Global Legal Entity Identifier)** | Authoritative corporate identifiers — entity-resolution backbone |
| **OpenCorporates API** | Corporate ownership across 130+ jurisdictions — beneficial-ownership graph |
| **GDELT GKG (Global Knowledge Graph)** | Pre-extracted entities + relationships from global news, free; base layer for our knowledge graph |
| **OCCRP Aleph (`pudo/aleph`)** | Investigation-platform beneficial-ownership graph extraction |
| **Equasis** | Canonical vessel ownership database (free with registration) |
| **Yahoo Finance / Alpha Vantage** | Live commodity futures (Brent, WTI, LNG) for cabinet-tier correlation |
| **NASA EONET** | Earth observation events (storms, wildfires, volcanoes) — globe baseline |
| **NOAA HF coastal radar** | Over-the-horizon vessel detection |
| GDELT 2.0 streaming + GDELT 1.0 historical | News-derived events with geo + actor |
| NewsAPI / RSS aggregators (multi-language) | Fast news cross-reference |
| OpenSanctions JSON | Sanctioned entities, beneficial ownership |
| OFAC SDN JSON direct | Latest US sanctions |
| EU sanctions JSON | Latest EU sanctions |
| Wikidata SPARQL | Entity grounding (vessels, companies, persons) |
| Danti API | Satellite imagery + geospatial intel for the Unmasker |
| Planet Labs OSINT (free tier) | Additional commercial satellite imagery |
| Sentinel Hub (free tier) | ESA Copernicus data |
| NOAA marine weather | Vessel route plausibility |
| Shodan + Censys | Cyber-side probes for the Synthesizer |
| Telegram public channels (via API) | OSINT social signals |
| ACLED conflict events | Pre-attack staging context |
| TankerTrackers / Lloyd's List | Historical incident curation |
| Public OSINT drone footage | Splat library inputs |

**Defended max:** ingesting from many sources doesn't mean *displaying* from many. The console aggregates, dedupes, and entity-resolves before surfacing. Breadth in the back, focus in the front.

---

## 9. Demo Strategy

### Three pitches, three demo packs

**60-second submission video** (required) — the canonical demo arc, edited for camera. Pre-recorded so we don't depend on live data.

**3-minute round-1 pitch** — full demo arc, live console, judge engagement.

**5-7 minute final-round pitch (top six)** — extended demo with a judge-driven Investigate moment, knowledge-graph walkthrough, and a Battle Staff teaser.

### Three demo packs (judge picks the region)

Each pack has fully pre-cached scenarios, splat scenes, narrated talk track, and a known-good run timing.

1. **Strait of Hormuz (default)** — Iranian shadow-fleet dark event, Bandar Abbas splat, Fujairah cyber probe, Xinhua narrative coordination.
2. **Taiwan Strait** — Chinese maritime militia at Mischief Reef, ADS-B drop near Pratas, Global Times narrative coordination.
3. **Black Sea** — Russian shadow-tanker re-flagging, Sevastopol splat, Wagner-linked OSINT social signals.

> "Pick a region" framing on stage is a massive credibility move. Judges who know the AOR get to test us in their own.

### The 60-second arc (canonical)

1. **Open** — 3D globe spinning, vessels and aircraft moving in real time. *"Real public data, right now."*
2. **Forecaster ticks** — countdown next to a Hormuz tanker: *"predicted dark event in 23 min."* Calibration sidebar shows Forecaster's recent track record.
3. **It happens** — vessel goes dark. Forecaster confidence ratchets. Matching historical case (M/V Helena, 12APR25) pops up side-by-side.
4. **Unmasker overlays** — *Claims vs. Reality* split, drone-splat-grounded reality on the right. *"Vessel claims 80km away. Splat shows it at the dock."*
5. **Synthesizer connects** — Fujairah port-system probe + Xinhua release join the maritime alert. Knowledge-graph view briefly opens. *"Likely coordinated probe — 0.74. Codex and Claude agree."*
6. **Translator** — judge picks "cabinet secretary." Same alert becomes one paragraph the SecDef would actually read.
7. **Human gate** — operator signs the accept. Audit log scrolls. *"Nothing happens without human authorization. Full chain-of-custody."*
8. **Reactive moment** — invite the judge: *"click any other vessel."* Swarm pivots, splat loads, swarm trace streams.
9. **Close** — *"Real data. Real ships. Three regions ready. Open source."*

Three "holy shit" moments + one interactive moment + one closing flex (three regions).

---

## 10. Audiences & Translation

(Covered in §3.4 — persona library + coalition + foreign-language outputs.)

---

## 11. Human-in-the-Loop · DoD 3000.09 · Chain of Custody

The product is **decision support, not weapons employment.** Every claim has receipts, every action has a human gate, every interaction is audit-logged with cryptographic signatures.

**Surfaces of the policy posture:**
- Human-gate overlay on every cross-domain alert (`accept · reject · escalate · annotate`).
- Per-recommendation explainability: confidence score decomposed into its inputs (NN match cases, transformer prediction, ensemble agreement).
- Audit trail viewer: every operator action with timestamp, signed signature, and reason. Exportable as evidence package (JSON + signed PDF).
- Tiered authorization: operator-tier can accept/reject; commander-tier required for escalation to ATAK push or partner notification.
- "System never engages" footer disclaimer (unironic, true).

**Stage Q&A talk track:**
> *"VANTAGE is fully aligned with DoD 3000.09. We do not engage targets. The system is decision support — it surfaces patterns, recommends interpretations, and routes alerts. Every recommendation has an evidence trail, every action has a tiered human authorization gate, and every operator action is cryptographically signed and audit-logged. You can export any decision as an evidence package for downstream legal review."*

### Pitch-line library

Battle-tested phrasings (some original, some lifted from Bilawal's channel where they land harder than anything we'd write fresh). Use the relevant line in pitch and Q&A.

| Line | When to use |
|---|---|
| *"The only piece that doesn't exist commercially is the fusion layer. That's what we built."* | Any "how is this different from Palantir / Lattice / Maven?" Q&A. Lifted from Bilawal's Maven breakdown — lands hardest when the questioner already knows him. |
| *"You can go dark on AIS, but you can't go dark on physics."* | Unmasker beat — when introducing the RF-geolocation invariant. |
| *"S-2 at 0600 — not a spy movie."* | Counter-framing when judges accuse us of being demo-flashy. The S-2 archetype is who the product serves. |
| *"Built for the sensors of 2028, not 2018."* | When asked about future-proofing or how this scales to GMTI / next-gen SAR. |
| *"This is the kind of evidence that survives a courtroom."* | Chain-of-custody / 3000.09 talk. |
| *"Lattice fuses what's visible. We find what's hidden."* | Anduril positioning. |
| *"Maven targets what it sees. We predict what's coming."* | Palantir Maven positioning. |
| *"Same OSINT a creator uses on YouTube — but with chain-of-custody, signed actions, and cross-domain agents on top."* | Direct positioning vs. Bilawal's WorldView if a judge brings him up. |
| *"OSINT proves the supply chain."* | When introducing financial / sanctions / adtech-derived signals. |
| *"We get the staff inside the adversary's OODA loop."* | OODA framing — open the README and the round-1 pitch with this. |

---

## 12. Competitive Landscape

| System | What it does well | Where VANTAGE lives |
|---|---|---|
| **Palantir Gotham** | Ontology-driven link analysis, classified intel | We're an OSINT-first synthesizer that emits to Gotham, not a replacement |
| **Palantir Maven SmartSystem** | AI-enabled targeting + fusion | We predict and contextualize; Maven targets what we surface |
| **Anduril Lattice** | Mesh-network C2, sensor fusion | Lattice fuses what's visible; we find what's hidden |
| **Vannevar Decrypt** | Foreign-language intel analysis | Complementary — we can ingest Vannevar outputs as a feed |
| **Shield AI / Hivemind** | Autonomy SDK | Downstream of us — we don't fly anything |
| **ATAK / TAK Server** | Tactical-edge COP | We emit Cursor-on-Target events into ATAK |
| **CJADC2** | DoD's umbrella unification program | We're the awareness layer that feeds it |

**One-line positioning:**
> *"Lattice fuses what's visible and Maven targets what it sees. VANTAGE finds what's actively being hidden, predicts what's coming, connects the dots across domains, and renders the world in 3D so the operator can see it the way the adversary does."*

---

## 13. Adversary Playbook

### Maritime gray zone
AIS spoofing, dark periods, STS transfers, flag-of-convenience switches, MMSI/IMO/name changes, shadow-fleet operations, sanctions-evasion runs.

### Aviation gray zone
ADS-B drop-offs near sensitive airspace, callsign reuse, civil-aircraft surveillance overflights, dual-use drone proliferation.

### Information operations
State-affiliated media coordinated with operational tempo, social astroturfing, disinfo injection into OSINT feeds.

### Cyber
DDoS timed with operations, port/logistics IT probes, pre-positioning malware (Volt-Typhoon-style).

### Space domain (added in max scope)
Satellite proximity ops (rendezvous and proximity operations / RPO), RF jamming, GPS spoofing of regional users, anti-satellite signaling.

### Subsurface / undersea (added in max scope)
USV swarms (Ukrainian Black Sea playbook), undersea cable threats (Baltic anchor-drag attribution), submarine activity inference from surface AIS exclusion zones.

### Hybrid
Combinations of the above as one operation — the Synthesizer's whole reason for existing.

**Recent demo-ready events:** Houthi Red Sea attacks, Russian Black Sea fleet vs. Ukrainian USVs, Iranian shadow-fleet Hormuz incidents, Chinese maritime militia at Second Thomas Shoal, severed Baltic undersea cables.

---

## 14. Strategic Geography — Three Demo Packs

> **Defended minimum:** **one** primary demo region (Hormuz). The other two (Taiwan, Black Sea) are insurance, not parallel narratives. We rehearse Hormuz to perfection and run the others only if a judge asks. Splitting rehearsal time three ways guarantees three mediocre demos.

### Pack 1 — Strait of Hormuz (primary)
- Hero entity: Iranian-linked tanker M/V Helena (or fresh equivalent).
- Splat: Bandar Abbas oil terminal.
- Cyber probe: Fujairah port systems.
- Narrative coordination: Xinhua "freedom of navigation."

### Pack 2 — Taiwan Strait (backup)
- Hero entity: Chinese maritime militia vessel near Mischief Reef.
- Splat: Mischief Reef reclaimed island.
- Cyber probe: Philippine telecom infrastructure.
- Narrative coordination: Global Times.

### Pack 3 — Black Sea (backup)
- Hero entity: Russian shadow tanker re-flagging mid-voyage.
- Splat: Sevastopol naval base.
- Cyber probe: Ukrainian port logistics IT.
- Narrative coordination: TASS.

Architecture extends to Bab-el-Mandeb, South China Sea, Baltic, Bering Strait without code changes — mention as "ready to onboard" on stage.

---

## 15. Roadmap & Stretch (post-hackathon)

**Promoted into v1 core (not stretch anymore):**
- Cyber feed integration (Shodan/Censys)
- Knowledge graph backbone
- Multi-model narrative ensemble (Codex + Claude)
- Confidence calibration UI
- Provenance graph per alert
- Audit trail viewer with cryptographic signing
- Three demo packs
- Tiered authorization
- Multimodal upload
- Briefing generator
- Spatiotemporal context layer (3D globe + time scrubber + splat library)
- Coalition + foreign-language Translator personas
- 12-invariant Unmasker

**True stretch (post-hackathon):**
- Live drone-video ingestion + on-demand splat training
- Splat change detection (T1 vs. T2 diffing) for site-monitoring use case
- Splat-derived feature extraction (vehicle counts, dock occupancy)
- CoT emission to a real TAK Server (we'll simulate for the demo)
- Vannevar Decrypt API ingestion (real foreign-language intel)
- Mobile / TAK companion view (read-only)
- Multi-operator collaboration with handoff
- Acoustic/MASINT invariants
- Space-domain proximity-ops invariants
- Crypto-rail sanctions evasion detection
- **Operator + commander shared-AR briefing room** — adapt `bilawalsidhu/see-through-walls` (MIT, MultiSet VPS + Meta Ray-Bans + iPhone) so two analysts can stand in the same physical space and see VANTAGE alerts pinned in 3D around them. Wall-occlusion handled. Unity + Swift bolt-on; not on the React/Python critical path.
- **WiFi RTT / RSSI indoor positioning** — Bilawal's "your WiFi can see you" angle. Indoor target localization for SCIF / port / facility monitoring use cases. Adds a new sensor modality (RF presence) to the Unmasker. ~8hr stretch.
- **Browser-based gsplat training** (nerfstudio gsplat compiled to WASM) — show "we could train splats from a phone" live on stage.
- **AI red-team agent** — Codex/Claude playing the adversary given current alert state, suggesting what the adversary would do next. Gated behind sandbox mode; never auto-fires on live data.
- **Adtech-derived crew geolocation** (MAID resale / ad-network data as shadow-fleet crew tracker) — Bilawal's Candy Crush trick. Ethically gray; flag explicitly in the demo.
- **Sub-acoustic / seismic detection layer** (USGS + NOAA) — submarine surface events inferred from ground vibration.
- **AI Battle Staff** — full implementation of S-2/S-3/S-4/S-5 planning agents consuming VANTAGE alerts and producing ranked COAs (the headline post-hackathon roadmap)

---

## 16. Build Plan — Sequenced Phases

Phases are sequenced, not time-boxed. AI agents handle the implementation grind; humans handle the judgment, curation, and rehearsal.

**Phase 0 — Pre-build (before doors open if possible)**
- Pattern library curation kicks off (target 500 cases)
- Splat preprocessing of 5 hero scenes
- Demo-pack data pre-cached
- Codex + Danti + Anthropic access verified

**Phase 1 — Foundation**
- Repo scaffold, env, CI green
- **Multi-LLM CLI build harness:** tmux layout with parallel Claude / Codex / Gemini agents, shared `WORKING.md` scratchpad, auto-commit-on-test-pass. Lifted from Bilawal's vibe-coding pattern. Set up first; everything else benefits.
- Postgres + TimescaleDB + Qdrant + Redis up via docker-compose
- Ingest layer: AIS + ADS-B + GDELT + OpenSanctions + Wikidata + NORAD TLEs live
- Cesium 3D globe shell with live entity rendering + base shader pack
- FastAPI scaffold + OpenAPI generation
- SSE alert stream wired

**Phase 2 — Agent vertical slices (parallel)**
- Forecaster: NN matcher + temporal transformer + calibration UI
- Unmasker: 14 invariants + Claims-vs-Reality panel + splat integration
- Synthesizer: clustering + knowledge graph + Codex/Claude ensemble + provenance graph + satellite-overpass correlator + capture-before-cache agent + transit-count metric
- Translator: 4 native + 4 coalition personas + foreign-language outputs

**Phase 3 — Reactive surfaces**
- Investigate-on-anything end-to-end
- NL query bar (graph + event store routing)
- Sandbox / replay mode with live Forecaster scoring
- Multimodal upload
- Briefing generator
- Human gate UI with cryptographic signing
- Audit trail viewer

**Phase 4 — Spatiotemporal layer integration**
- Time scrubber wired into Cesium + agents
- Splat library loaded, geo-anchored, surfaced via Investigate
- Knowledge-graph view (Cytoscape) with multi-hop walks
- Three demo packs fully cached and tested

**Phase 5 — Polish & rehearsal**
- Demo script written for 60s / 3min / 5-7min versions
- Three full dry runs against a cold console
- 1-min submission video recorded and edited
- README + ARCHITECTURE.md + quickstart polish
- Public repo polish (badges, screenshots, demo GIF)
- Final type-check, lint, test pass

---

## 17. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Live data goes quiet during demo | Three pre-cached demo packs; Live/Demo/Sandbox toggle |
| LLM hallucinates a narrative | Ensemble disagreement signal; strict no-confab schemas; receipts on every claim |
| Agent latency stalls demo | 8s hard timeout; fallback to last-known-good; pre-warmed contexts |
| Unmasker false positive on stage | Use historically-validated cases for the canonical demo path |
| Looks like "ChatGPT for generals" | Visible swarm reasoning panel, evidence trail on every claim, knowledge-graph view, no chat-only UI |
| Pattern library too small to be credible | 500-case minimum at v1, with full per-case provenance |
| Reactive surfaces add demo failure modes | Cap interactivity at 3-4 well-rehearsed gestures; sandbox mode as escape hatch |
| 3000.09 challenge in Q&A | Locked talk track + cryptographic chain-of-custody as hard evidence |
| Splat fails to render on stage | Pre-compiled assets; 2D Deck.gl fallback toggle; one tested rendering path |
| Codex / partner API rate limits | Local response cache with prompt-cache awareness; Claude as fallback |
| Knowledge graph slow at query time | Materialized common queries; Postgres-AGE pre-warmed; query-cap for stage |
| Scope creep in the final 6 hours | **Feature freeze 6h before submission**; no new features added, only polish + bug fixes |
| Time-zone confusion on the time scrubber | UTC always-on toggle; demo runs in UTC by default |
| Multiple regions dilute rehearsal | Hormuz is *the* demo; Taiwan/Black Sea are only run if asked |
| Postgres + TimescaleDB unfamiliar to team | Pre-built docker-compose with seed data; quickstart works on clean clone |

---

## 18. Decisions (formerly Open Questions)

Decisions made:
- **Cyber feed:** in for v1.
- **Knowledge graph:** in for v1, Postgres + AGE.
- **Multi-model ensemble:** in for v1, Codex + Claude.
- **Confidence calibration UI:** in for v1.
- **CoT emission:** simulated for v1; real TAK Server is post-hackathon.
- **Three demo packs:** Hormuz primary, Taiwan + Black Sea as backup. *Rehearse Hormuz; only run others if asked.*
- **Battle Staff teaser:** out of v1; named in roadmap slide only.
- **License-holder name:** "VANTAGE Project Contributors" until team commits to a name list at submission.

Still open:
- **Team composition + ownership** — who owns frontend / backend / data curation / demo direction?
- **Hosting** — local laptop for demo (recommended) or hosted? Need to decide before phase 5.
- **Submission video format** — screen recording with voiceover (recommended for control) vs. live talking head.

---

## 19. Future Direction (post-hackathon)

VANTAGE is the awareness layer. The natural extension is **AI Battle Staff** — layer the Army's MDMP on top with specialized planning agents per staff section (S-2 intel, S-3 ops, S-4 logistics, S-5 plans) that consume VANTAGE alerts and produce courses of action with risk profiles. The commander gets *what's happening · why · what it means · here are three ways to respond, ranked.*

Mention as a roadmap slide. Don't try to build it.

---

## 20. Professional Polish & Production Quality

Things that separate a hackathon prototype from a defense product. We do all of these.

### Code quality
- Type hints everywhere (Python: full mypy; TS: strict mode)
- Ruff + mypy in CI; both must be green to merge
- Pytest suite covering core agent logic + invariant checkers + API contract tests
- Eslint + Prettier on frontend; Tailwind class sorting via plugin
- Pre-commit hooks for lint + type check
- Conventional Commits for commit messages

### Repo hygiene
- README with badges (CI, license, version), one-screenshot demo, demo GIF, quickstart
- ARCHITECTURE.md (in `context/`) with component diagrams + design decisions
- CONTRIBUTING.md with dev setup + style guide
- AGENTS.md describing each agent's role, schema, and tool access
- MIT LICENSE
- `.env.example` with every env var documented
- `Makefile` with `make demo`, `make dev`, `make test`, `make lint`
- One-command quickstart: `git clone && make demo` works on a clean Mac/Linux box

### Reliability
- Graceful degradation when any source feed is down (Forecaster reports "feed: degraded" rather than crashing)
- Health-check endpoints for every service
- Structured JSON logging with correlation IDs across agents
- OpenTelemetry traces viewable in the audit log
- Per-agent error budgets visible in the swarm panel

### Security
- No secrets in repo (gitleaks in CI)
- All API endpoints input-validated via Pydantic
- CORS configured for the demo origin only
- Audit log append-only with cryptographic signatures
- SBOM (CycloneDX) generated as a CI artifact

### Operator UX polish
- Keyboard shortcuts for every reactive action; `?` overlay shows the map
- Dark mode default (operator console aesthetic), light mode supported
- Accessibility: WCAG AA on the console (judge demos in any lighting)
- Consistent visual language: shadcn/ui design system, one font, one color palette
- Subtle motion on state changes (Framer Motion); no gratuitous animation
- Copy-edit pass on every string

### Branding
- Logo (simple wordmark + glyph)
- One color palette (defense-coded but not generic — maybe deep navy + amber accent)
- Consistent tagline placement on every surface
- Demo deck (if needed for round 1) follows the same palette

### Pitch quality
- Every "Talk like a pro" line from the Operator's Manual rehearsed
- Stage Q&A prep: 20 most likely questions with crisp answers
- Dry-run feedback loop with at least one mock judge

---

## 21. Repo & Open-Source Discipline

The judges *will* look at our GitHub. Most won't run the code, but the repo itself signals seriousness.

- Public from the first commit (already true)
- Tagged release (`v0.1.0-hackathon-submission`) at submission
- README that someone can read in 60 seconds and understand what this is
- Demo video linked in the README, not just the submission form
- `context/` folder with all the supporting docs (Operator's Manual, Hackathon Resources, Scope, Architecture)
- Per-component README in each subpackage (`backend/`, `frontend/`, `agents/`, `pattern_library/`)
- Inline comments only where the *why* is non-obvious (per project style)
- License + Contributors clear
- No leaked credentials, no large binary blobs (splats hosted externally if too big)

---

## 22. Glossary & Background Reading

For military terminology, organizational structure, doctrine, intelligence tradecraft, the C2 stack we're competing with, the adversary playbook, and the strategic geography we operate in — see `context/operators_manual.md`. It's the team's shared primer; read it once before pitching.

For the hackathon's operational details (schedule, partner access, judging process, rules) — see `context/hackathon_resources.md`.

---

*This doc is alive. Update it as decisions get made; prune sections as they get folded into the README or implemented in code. The bar is "professional defense product, on a hackathon timeline, with AI-assisted engineering" — not "hackathon demo."*
