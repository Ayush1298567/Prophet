# 3rd Annual NatSec Hackathon — Hacker Resources

> Source packet shared with all hackers. Mirrored here so the VANTAGE team has every operational detail in one place.

---

## 1. Discord

Join the **National Security Hackathon (by Army xTech)** Discord:
https://discord.com/invite/xgEaYSfZ2x

---

## 2. Location

**Shack15** · 1 Ferry Building, Suite 201, San Francisco, CA 94111

- **Venue access:** 2nd floor of the Ferry Building. Take the Ferry Building elevator up, turn left, and you'll see the Shack15 main entrance. Overnight access is allowed.
- **Parking:** very limited near the Ferry Building. Park farther out and take Uber, Lyft, or public transit.

---

## 6. Wifi

- **SSID:** `SHACK15_Members`
- **Password:** `M3mb3r$4L!f3`

---

## 7. Kickoff Happy Hour

Stanford, **5pm PT on May 1st**. Registration was required to meet fellow hackers, partners, and officials.

---

## 8. Schedule

### Saturday, May 2nd — Day 1
| Time | Event |
|---|---|
| 0900 | Doors open, team formation |
| 1100 | Welcome kickoff + presentations |
| 1145 | **Hacking starts** |
| 1300 | Lunch |
| 1900 | Dinner |
| 2200 | Doors close (overnight stays OK, no reentry) |

### Sunday, May 3rd — Day 2
| Time | Event |
|---|---|
| 0900 | Doors open |
| 1200 | **Hacking stops, submissions due** |
| 1215 | Round-1 judging starts |
| 1300 | Lunch |
| 1400 | Round-1 concludes |
| 1410 | Finalists announced, on-stage demos begin |
| 1445 | Final-round judge deliberation |
| 1515 | Winners announced + closing |
| 1600 | Doors close |

---

## 9. Rules

- **Open source:** GitHub repository must be public at submission.
- **New work only:** every project must be started from scratch during the hackathon. No prior work.
- **Tool usage:** any AI tool or material is fair game, provided it's openly accessible to all attendees.
- **Problem statements:** all projects must fit one of the five problem statements below.
- **Team size:** up to 4 members.

---

## 10. Problem Statements

### 🚨 PS1 · Sensor Analysis and Integration
Fuse data from many sensor types (EO, IR, RF, radar, etc.) into one actionable picture. Consolidate detections across modalities, optimize sensor search strategies, and maintain custody of targets in contested environments.

Example projects:
- Optimize sensor search across multiple modalities to maximize probability of reacquiring a lost target while minimizing search time, accounting for last-known state, maneuverability, and sensor constraints.
- Auto-fuse multi-sensor detection messages into a single correlated event, refining confidence/time/location iteratively.
- Pipeline that analyzes uncorrelated tracks to identify candidate paths of evading objects (debris vs. separation vs. threat).

### ✈️ PS2 · Edge Deployments and Drone Operation
Front-line operators commanding autonomous systems from austere, disconnected environments — sometimes from a backpack. Push computation and control to the tactical edge, balancing power, latency, and mission complexity.

Example projects:
- Lightweight edge architecture for drone C2 + onboard inference from a portable, battery-powered kit.
- Single operator tasking a small swarm of autonomous vehicles from an edge device under intermittent or denied connectivity.
- Real-time sensor pipeline on edge hardware that ingests video and RF from drones, performs local target detection, and pushes prioritized alerts without cloud reliance.

### 🪖 PS3 · Mission Command and Control  ← **VANTAGE's primary track**
Synthesize information from across the battlespace into a coherent picture and act on it faster than the adversary. Integrate sensor feeds, intel, and unit positions into a unified interface that accelerates the kill chain and decision-making.

Example projects:
- Battlefield command dashboard with live multi-source feeds (sensor tracks, unit positions, vehicle locations, comms, intel) into one operational picture with intuitive viz and natural-language querying.
- Automate kill-chain steps from detection through identification to engagement recommendation, with human-in-the-loop oversight and explainable rationale.
- Tool that ingests operational reports, links entities (people, units, locations, events) into a knowledge graph, and surfaces emerging patterns in real time.

### 💻 PS4 · Digital Defense and Cybersecurity
Networked, software-defined military and AI systems are prime targets. Auto-detect and mitigate attacks on mission-critical infra, protect AI deployments and comms links, and harden the digital backbone.

Example projects:
- Auto-detect and mitigate DDoS on ground-based sensor and comms assets, maintaining mission continuity during active cyber engagement.
- Anomaly detection on RF transmissions (frequency, power, modulation shifts) that may indicate tampering.
- Deployable security scanning toolkit validating containerized AI model deployments against known-good baselines.

### 🎖️ PS5 · General National Security
Anything else benefiting national security. **Talk to a mentor before building** to validate fit.

---

## 11. Partner-Provided Resources

### Palantir
- Full access to a Palantir AIP instance for the duration. On-site Palantir staff add users via email.
- Free developer-tier signup for ramp-up before the event and continued personal use after.
- **Hardware:** Connected Adaptive Sensor Kit (CASK) is available for PS1 and PS2 — Palantir's edge product for using the ontology on small hardware in austere/intermittent-connectivity environments. Stripped-down kits provided.
- Hardware overview: https://docs.google.com/document/d/1Hy_YT56Qp5JmBZaYY4H32wrjdWPcueAETVzmY3Qtm3Y/edit?usp=sharing

### OpenAI
- **Codex access** provisioned in a dedicated workspace.
- Pre-work doc (complete before the event): https://docs.google.com/document/d/109o8nE77qAQgatabferZuV6eJaIYmfGe7F1Sqjpbn0s/edit?usp=sharing
- Codex access request form: https://docs.google.com/forms/d/e/1FAIpQLSeT5AtwJeDbRNWCyVTRs5fAeT9RopGge_9RqWkRy7isyvIOrQ/viewform?usp=send_form

### Danti
- User accounts on Danti's geospatial intelligence platform.
- Account request form: https://docs.google.com/forms/d/e/1FAIpQLSfEGuvJXsZW31eG-kgK4-1fiCGTvmTVfdmLYTbJ-jqg4IZKng/viewform?usp=send_form

---

## 12. OSINT Resources

| Resource | URL |
|---|---|
| Sample DEFCON projects (2025 scrape) | https://defcon-inspiration.cerebralvalley.ai/ |
| Network/internet monitoring search | https://shodan.io |
| OSINT framework | https://osintframework.com/ |
| AI-powered OSINT search | https://exa.ai |
| AIS shipping data | https://www.aishub.net |
| Historical AIS API | https://developer.barentswatch.no/docs/AIS/historic-ais-api/ |
| Vessel-traffic data dump | https://hub.marinecadastre.gov/pages/vesseltraffic |
| Vessel-traffic dataset (Kaggle) | https://www.kaggle.com/datasets/eminserkanerdonmez/ais-dataset/data |
| Flight tracking | https://www.flightradar24.com |
| Geo data viz | https://kepler.gl · https://deck.gl |
| Simulated hardware environment | https://wokwi.com |

---

## 13. Judging & Submissions

Judging happens **Sunday, May 3rd**. Judges evaluate **technical demos** — do not present slides, demo what you built.

Submit via the form when hacking is complete. Submission requires a **1-minute demo video** uploaded to YouTube, Loom, or similar.

### Criteria
| Weight | Criterion | What it measures |
|---|---|---|
| 35% | Technical Demo | Quality of demo, engineering quality, working state |
| 30% | Military Impact Potential | Real-world military pain point addressed |
| 25% | Solution Creativity | Novelty of approach |
| 10% | Presentation & Pitch | How well it was presented |

### Process
1. **Round 1 (group judging):** ~3 min pitch + 1–2 min Q&A in assigned judging groups.
2. **Round 2 (top six on stage):** ~3 min pitch + 2–3 min Q&A in front of full panel.

---

## 14. Prizes

Provided by the United States Army.

| Place | Prize |
|---|---|
| 1st | $20,000 |
| 2nd | $12,000 |
| 3rd | $8,000 |
| 4th | $6,000 |
| 5th | $4,000 |

---

## Contact

- Email: ray@cerebralvalley.ai
- Discord: https://discord.com/invite/xgEaYSfZ2x
- Submission form: https://cerebralvalley.ai/e/3rd-annual-natsec-hackathon/submit
