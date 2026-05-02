# VANTAGE Operator's Manual

> A modular military primer for someone who's about to pitch a defense product to a room full of people who do this for a living.

**How to read this:** Each of the eight sections is self-contained. Skim what you already know, deep-read what's new. Every section ends with **"Why this matters for VANTAGE"** (so it grounds back to the project) and **"Talk like a pro"** (a one-liner you can drop into your pitch).

A glossary of must-know acronyms is at the end. Bookmark it.

**Estimated read time:** 45 minutes for a full pass, ~5 minutes per section.

---

## Section 1 · STRUCTURE — How the U.S. military is organized

### TL;DR
The military is structured along three axes at once: **service** (Army, Navy, Air Force, Marines, Space Force, Coast Guard), **geography** (combatant commands like CENTCOM and INDOPACOM), and **echelon** (units that nest from squad up through corps). Most of your conversations about VANTAGE will involve a battalion-or-above commander supported by a staff of 4-12 officers, each of whom owns one slice of the picture.

### The branches and what they do
- **Army** — ground force, the biggest by headcount. Battalions, brigades, divisions.
- **Navy** — ships, carriers, submarines, naval aviation. Owns the global maritime picture.
- **Air Force** — aircraft, missiles, the bulk of intelligence platforms.
- **Marines** — light, fast, expeditionary; technically under the Navy department.
- **Space Force** — newest branch, owns satellites and orbital domain.
- **Coast Guard** — under DHS in peacetime, Navy in wartime; matters a lot for the maritime gray zone.

### Combatant commands (the geographic ones)
The world is carved up into "AORs" (areas of responsibility), each owned by a four-star combatant commander:
- **CENTCOM** — Middle East and Central Asia (Iran, Iraq, Syria, Afghanistan area). The Hormuz scenario in your demo is CENTCOM's lane.
- **INDOPACOM** — Indo-Pacific (China, Taiwan, Korea, South China Sea). The biggest, the most strategically loaded.
- **EUCOM** — Europe (Russia, Ukraine, NATO).
- **AFRICOM** — Africa.
- **NORTHCOM** — North America (homeland defense).
- **SOUTHCOM** — Latin America.
Plus functional ones: **SOCOM** (special ops), **STRATCOM** (nuclear, strategic), **CYBERCOM** (cyber), **TRANSCOM** (logistics), **SPACECOM** (space).

### Unit hierarchy (use Army terms — they're the lingua franca)
A **squad** (~10 troops) → **platoon** (~30) → **company** (~100) → **battalion** (~600) → **brigade** (~3-5k) → **division** (~15k) → **corps** (~50k+).
The level you'll most often address with VANTAGE is **battalion** or **brigade** — that's where commanders need synthesized decision support and where staff-officer roles become a thing.

### Ranks — the simplified version
There are two ladders, **enlisted** (E-1 to E-9, the people who do the work) and **officer** (O-1 to O-10, the people who decide). For your purposes:
- **NCOs** (sergeants, E-5 through E-9) — the experienced backbone.
- **Junior officers** (lieutenants, captains — O-1 to O-3) — first leadership roles.
- **Field grades** (major, lieutenant colonel, colonel — O-4 to O-6) — battalion and brigade commanders. *This is your primary "user" archetype.*
- **Flag officers** (general, admiral — O-7 to O-10) — theater commanders, joint chiefs. *This is your "pitch to the secretary" archetype.*
Navy/Coast Guard use different rank names but the structure is parallel.

### The staff sections — *very important for VANTAGE*
Every commander above company level has a staff. The staff is divided by function and numbered. Use **S-** at battalion/brigade, **G-** at higher Army echelons, **N-** in the Navy, **A-** in the Air Force, **J-** for joint.

| Section | Owns |
|---|---|
| **S-1** | Personnel, admin |
| **S-2** | **Intelligence** — enemy, terrain, weather. *This is where VANTAGE lives.* |
| **S-3** | **Operations** — current fight, course-of-action development |
| **S-4** | Logistics, sustainment |
| **S-5** | Plans (longer horizon) |
| **S-6** | Communications, signals, cyber |

The future-direction "Battle Staff" version of VANTAGE literally builds an AI agent for each of these sections.

### What a commander actually does on a Tuesday
- Receives briefings from S-2 and S-3
- Makes a decision (the only thing they can't delegate)
- Approves orders, signs off on lethal action
- Talks to higher headquarters and to subordinate commanders
- Does *not* spend their day staring at sensor feeds — that's what the staff is for. **VANTAGE serves the staff who serve the commander.**

### Why this matters for VANTAGE
You're not building a tool that a private operates. You're building a tool that a battalion S-2 (an intelligence captain or major) uses to prepare a briefing that informs a battalion commander's decision. Every demo should make clear *which person you're helping* and *what decision they're making*.

### Talk like a pro
> *"VANTAGE is built for the S-2 to give the commander a synthesized intelligence picture before the morning brief — not for the operator to stare at a screen."*

---

## Section 2 · DOCTRINE — How they plan and fight

### TL;DR
Three concepts cover 80% of what you'll hear: the **OODA loop** (the basic decision cycle), the **kill chain** (the canonical sequence from "we see something" to "we hit it and assess"), and **MDMP** (the formal staff process for planning operations). Modern doctrine obsesses over **tempo** — being faster than the adversary's loop. VANTAGE's whole pitch is *we compress the loop.*

### The OODA loop (Boyd, 1970s)
Observe → Orient → Decide → Act. Then repeat. Originally about fighter pilots; now used everywhere. The strategic insight: the side that completes the loop faster — and *gets inside* the other side's loop — wins. Modern doctrine talks about **tempo** (rate and rhythm of action *relative* to the enemy), not just raw speed.

### The kill chain (F2T2EA)
Find → Fix → Track → Target → Engage → Assess. The canonical sequence for striking a target.
- **Find** — detect that something is there
- **Fix** — pin down where it is
- **Track** — keep custody of it as it moves
- **Target** — decide it's worth hitting and prepare the engagement
- **Engage** — actually use force
- **Assess** — battle damage assessment, did it work?

The Special Operations variant is **F3EAD** (find, fix, finish, exploit, analyze, disseminate) — adds the intel-exploitation loop after the strike.

The modern story is "kill chain compression": shrinking time from Find to Engage from hours/days to minutes/seconds. **Maven Smart System exists to do this.**

### MDMP — the Military Decision Making Process
The Army's seven-step planning ritual:
1. Receipt of mission
2. Mission analysis
3. Course-of-action (COA) development
4. COA wargaming
5. COA comparison
6. COA approval
7. Orders production

Real staffs run this in 8-72 hours depending on time pressure. The "AI Battle Staff" extension of VANTAGE automates this. For now, it's enough to know the framework exists and that "COA" is what you call a course of action.

### Rules of Engagement (ROE)
The legal/policy guardrails on when you can use force, against whom, and how much. **Standing ROE** is peacetime baseline; **Supplemental ROE** is mission-specific. Every engagement decision has to be ROE-compliant. ROE is *the* reason "human in the loop" matters: AI can recommend, but a human (often with a JAG officer alongside) has to confirm ROE compliance before fire is opened.

### Concepts of operation (CONOPS) and operations orders (OPORDs)
- **CONOPS** — the high-level plan: what the unit is going to do, why, and how.
- **OPORD** — the formal, structured order with five paragraphs: Situation, Mission, Execution, Service Support, Command & Signal. Every unit briefing follows this format.

### Why this matters for VANTAGE
VANTAGE compresses the OODA loop *for the commander's staff.* The Forecaster and Synthesizer collapse "Observe" and "Orient" from hours to seconds. The Translator collapses "brief the commander" from minutes to one paragraph. The Unmasker resists adversary attempts to corrupt your "Observe" step. You hand off "Decide" to the human (3000.09 compliance), and "Act" is downstream of VANTAGE. **Your pitch line is "we get the staff inside the adversary's OODA loop."**

### Talk like a pro
> *"We're not replacing the kill chain. We're compressing the early steps — find, fix, track — so the commander's decision happens inside the adversary's loop."*

---

## Section 3 · INTELLIGENCE — How they know what they know

### TL;DR
Intelligence is divided by collection method (the "INTs"), processed through a five-step **intelligence cycle**, and the holy grail is **all-source** fusion — combining INTs into a single picture. The most important conceptual distinction for VANTAGE is **track vs. identity**: a sensor blip says "something is here," but knowing *what* it is requires correlation. Most C2 systems are great at tracks and weak at identity.

### The INTs
| Acronym | What it is | Example |
|---|---|---|
| **HUMINT** | Human intelligence — spies, debriefs, informants | Source in a foreign port reports a sanctioned shipment |
| **SIGINT** | Signals intelligence — communications and electronic emissions | Intercepted radio between adversary ships |
| **IMINT** | Imagery — satellite, aerial, drone | Satellite photo of a tank column |
| **GEOINT** | Geospatial — maps, terrain, geographic patterns | Heatmap of incidents along a route |
| **OSINT** | Open source — news, social media, public databases | Bellingcat-style investigation |
| **MASINT** | Measurement & signature — radar returns, acoustic, IR signatures | Submarine acoustic fingerprint |
| **FININT** | Financial intelligence — banking, sanctions, ownership | OpenSanctions hit on a vessel owner |
| **CYBINT** | Cyber intelligence — network telemetry, malware analysis | Detection of a port-system intrusion |

The first six are "classical." FININT and CYBINT are modern adds.

### The intelligence cycle
Tasking → Collection → Processing → Analysis → Dissemination → Feedback. Each step has different people and tools. VANTAGE accelerates the **processing → analysis → dissemination** legs by automating fusion and producing operator-ready briefs.

### "All-source"
The aspirational state where you fuse every INT into one coherent picture. Palantir Gotham and Maven exist to chase this. **VANTAGE is an all-source synthesizer that emphasizes OSINT-leaning sources** (because that's what's available to a hackathon team) but the architecture extends to classified INTs trivially.

### Track vs. identity (the critical distinction)
- A **track** is a sensor blip — a contact, a signal return, a position fix. It just means *something is at these coordinates*.
- An **identity** is the answer to *what is it?* — a specific vessel, a known unit, a particular person.
- The hardest problem in modern C2 is **identity assignment**: an operator drowning in tracks but unable to confidently identify which ones matter.
- VANTAGE's Unmasker doesn't just confirm tracks — it disputes them. *"You think this is vessel X. Sensor truth says it's not."*

### Indications and Warnings (I&W)
The intelligence discipline of detecting precursors of adversary action. *Has the unit started rehearsals? Are reservists being mobilized? Did the troop transports leave port?* I&W is inherently predictive. **Your Forecaster pillar is essentially an automated I&W system.**

### Why this matters for VANTAGE
You are an OSINT-heavy all-source synthesizer that produces I&W-grade outputs. Each of your data sources maps to an INT — AIS/ADS-B (OSINT/MASINT-flavored), news/GDELT (OSINT), Danti satellite imagery (IMINT/GEOINT), OpenSanctions (FININT). This vocabulary lets a judge place you on the existing intelligence map immediately.

### Talk like a pro
> *"VANTAGE is OSINT-leaning all-source fusion that delivers indications and warnings without waiting for classified collection."*

---

## Section 4 · SYSTEMS IN THE FIELD — The C2 stack you're competing with

### TL;DR
Five names cover 90% of what you need to know: **Palantir** (Gotham/Foundry/AIP/Maven), **Anduril** (Lattice), **ATAK/TAK** (the tactical edge), **Vannevar** (foreign-language intel analysis), and **Shield AI** (autonomy). Each owns part of the picture. **VANTAGE lives in the gaps between them** — predictive, contextualizing, deception-detecting, cross-domain.

### Palantir — the data and AI giant of defense
- **Gotham** — the original intelligence platform. Ontology-driven (everything is a typed entity with relationships). Used by intel community since post-9/11. Strong at link analysis, weak at natural-language query.
- **Foundry** — the broader data platform. Used in commercial too.
- **AIP (AI Platform)** — the LLM-integration layer added in 2023. Got DIA / classified-network accreditation for GPT-class models in late 2024 — *this is genuinely new*.
- **Maven Smart System (MSS)** — Palantir-built AI-enabled targeting/fusion engine. Originally a DoD program ("Project Maven"), now a Palantir product running on the AIP stack. Recently designated as the cornerstone of CJADC2 and is becoming a formal program of record.

### Anduril — the rising AI-native defense prime
- **Lattice for C2** — mesh-networked, AI-first command and control. Fuses thousands of sensors and effectors into one operational picture, recommends courses of action, supports counter-UAS at scale.
- Recently won a multi-billion-dollar Army enterprise contract consolidating dozens of procurement pathways. Anduril/Lattice is now strategically dominant for new C2 acquisition.
- Designed for "mosaic warfare" — distributed, composable kill webs.
- The big assumption: persistent connectivity. In contested spectrum (jamming, denial), this assumption breaks.

### ATAK / WinTAK / CivTAK + TAK Server — the tactical edge
- **ATAK** — the Android Tactical Assault Kit. Runs on a phone, gives a ground unit a real-time COP with friendly positions, sensor tracks, and chat.
- **WinTAK** — the Windows desktop equivalent.
- **CivTAK** — the civilian-released version (used by police, fire, search-and-rescue).
- **TAK Server** — the federated comms/data backend.
- **Cursor on Target (CoT)** — the open XML schema TAK uses for "what/when/where" events. Lightweight enough for austere networks. *If VANTAGE emits CoT, our alerts appear natively in any ATAK device on the network.*

### Vannevar Labs — gen-AI for intel analysis
- **Decrypt** — Gen-AI platform for foreign-language intelligence (open-source, intercepts, etc.). Deployed across many DoD sites. Reports 10x analyst throughput.
- The lesson Vannevar proves: **domain-finetuned models beat generic LLMs** on military analysis. Don't over-rely on raw GPT for serious work.

### Shield AI / Hivemind — autonomy SDK
- Powers autonomous swarms (UAVs, jets) without GPS or comms. Operates in degraded environments — a unique value prop.
- Lives at the platform-control layer, *downstream* of C2. Doesn't generate C2 decisions; it executes them on unmanned systems.

### CJADC2 — the umbrella program
**Combined Joint All-Domain Command and Control** is the DoD's modernization push to unify C2 across services and coalition partners. CENTCOM has a deployed minimum viable capability since spring 2024. Open DAGIR (the open data repository) went live shortly after. Most modern AI defense programs justify themselves under CJADC2.

### Where VANTAGE fits in this stack
- **Lattice** fuses what's visible. **VANTAGE** finds what's hidden.
- **Maven** detects targets. **VANTAGE** predicts adversary moves and surfaces intent.
- **Vannevar** analyzes intel after the fact. **VANTAGE** synthesizes intent in real time.
- **ATAK** is the operator's window. **VANTAGE** can emit alerts as CoT into that window.
- **CJADC2** is the umbrella. VANTAGE is the awareness layer that feeds it.

### Why this matters for VANTAGE
You will be asked, on stage, *"how is this different from Lattice?"* and *"why doesn't Palantir do this?"* You should be able to name Lattice, Maven, and Gotham without hesitation, place VANTAGE in the gap between them, and demonstrate you've thought about why no incumbent has built it yet (answer: incumbents optimize for what's visible; you optimize for what's hidden, predicted, and cross-domain).

### Talk like a pro
> *"Lattice fuses what's visible and Maven targets what it sees. VANTAGE finds what's actively being hidden, predicts what's coming, and connects the dots across domains."*

---

## Section 5 · ADVERSARY PLAYBOOK — How they actually operate

### TL;DR
Modern adversaries (state and non-state) operate in the **"gray zone"** — actions short of war, designed to achieve strategic effects without triggering a kinetic response. The toolkit includes **AIS spoofing**, **GPS jamming**, **flag-of-convenience switches**, **shell-company ownership**, **shadow fleets**, **influence operations**, **cyber probes**, and **proxy violence**. VANTAGE is purpose-built to detect these specifically because incumbents optimize for visible kinetic threats.

### Gray zone — the dominant operating space
"Gray zone" describes activities that are aggressive but stay below the threshold of armed conflict. Examples: Russian "little green men" in Crimea, Chinese maritime militia in the South China Sea, Iranian use of proxy militias, ransomware attacks attributed to state actors. The strategic logic: chip away at the adversary's position without giving them a clean *casus belli*.

### Hybrid warfare
A coordinated mix of military, cyber, information, economic, and proxy operations. The Russia-Ukraine conflict is the textbook example — kinetic combat layered with cyber attacks on infrastructure, info ops, proxy mercenaries (Wagner), economic coercion (energy), and sabotage in third countries. **The Synthesizer pillar of VANTAGE exists because hybrid warfare is multi-domain by design.**

### Maritime gray zone — the VANTAGE sweet spot
- **Sanctions evasion** — moving cargo (oil, weapons, dual-use goods) past Western sanctions.
- **The "shadow fleet"** — aging tankers operating with opaque ownership, used by Iran, Russia, North Korea, Venezuela. The number of identifiable shadow-fleet vessels has grown into the hundreds, possibly more than a thousand, since 2022.
- **AIS spoofing** — broadcasting a false position to make a vessel appear elsewhere.
- **AIS dark periods** — turning off the transponder entirely. Common before ship-to-ship transfers.
- **STS (ship-to-ship) transfers** — meeting another vessel at sea to transfer cargo, often with both AIS off.
- **Flag-of-convenience switches** — re-flagging vessels in lax-jurisdiction registries (Liberia, Panama, Cook Islands) to obscure ownership.
- **MMSI / IMO / name changes** — quietly altering a vessel's identifiers between voyages.

### Aviation gray zone
- ADS-B spoofing (rarer but documented)
- Dropping off radar near sensitive airspace
- Civil aircraft used for surveillance overflights
- Dual-use drone proliferation (commercial DJI gear used for ISR or strike)

### Information operations
- State-affiliated media coordinated with operational tempo (e.g., Xinhua statement timed with a maritime probe)
- Social-media astroturfing
- Disinformation injected into adversary OSINT feeds (a real concern for systems like VANTAGE)

### Cyber probes against military and civil infrastructure
- DDoS against government sites timed with operations
- Probes against port and logistics IT
- Pre-positioning malware in critical infrastructure (the "Volt Typhoon"-style activity)

### Concrete recent examples to know (and use in your demo)
- **Houthi attacks in the Red Sea / Bab-el-Mandeb** (2023-ongoing) — civilian shipping under missile and drone attack, coalition (Operation Prosperity Guardian) response.
- **Russian Black Sea fleet** — Ukrainian USVs (uncrewed surface vessels) attacking Russian warships, classic asymmetric maritime conflict.
- **Iranian shadow fleet** — sanctions-evading oil exports, Strait of Hormuz incidents, occasional vessel seizures by IRGC Navy.
- **Chinese maritime militia in the South China Sea** — fishing fleets used as a paramilitary tool, swarming Philippine resupply missions at Second Thomas Shoal.
- **Severed undersea cables in the Baltic** (2023-ongoing) — attributed to Russian/Chinese vessels with deliberate anchor drags.

### Why this matters for VANTAGE
**Every demo example you give should pull from this world.** Maritime gray zone is the sweet spot because public data (AIS, OpenSanctions, news) is rich, adversaries are named, and incidents are fresh in the news cycle. Use real ship names, real chokepoints, real sanctioning regimes. Specificity is credibility.

### Talk like a pro
> *"The fight isn't kinetic — it's gray zone. Adversaries spoof, lie, switch flags, and time their cyber and info ops to maritime moves. VANTAGE is built to see all of that as one operation, not five disconnected events."*

---

## Section 6 · STRATEGIC GEOGRAPHY — Where things happen

### TL;DR
The world has a small number of strategically loaded places where most of what you'll demo actually occurs. Know the **theaters** (regions owned by combatant commands), the **chokepoints** (narrow passages where shipping concentrates), and the **adversary forward areas**. For VANTAGE's hero demo, pick **one** region (probably Hormuz) and stay there.

### The major theaters and what's contested in each
- **Indo-Pacific (INDOPACOM)** — China rising, Taiwan flashpoint, North Korea unstable, South China Sea contested island-building, Philippines-China standoffs. *The single biggest US strategic concern of the next decade.*
- **Middle East (CENTCOM)** — Iran nuclear and conventional pressure, Iranian proxies (Houthis, Hezbollah, Iraqi militias), Israel ongoing conflicts, Syria fragmented, Iraq fragile.
- **Europe (EUCOM)** — Russia-Ukraine war, NATO eastern flank, Baltic and Black Sea incidents, Arctic militarization.
- **Africa (AFRICOM)** — multiple coups (Sahel especially), Russian/Wagner footprint, terrorism in the Horn of Africa, China port investments.
- **Latin America (SOUTHCOM)** — narcotics flows, Venezuelan instability, Cuban/Chinese intelligence presence.
- **Arctic** — accelerating Russian and Chinese activity, ice-route opening, new chokepoints emerging.

### Maritime chokepoints — memorize these
About 80% of world trade by volume moves by sea, and a startling fraction passes through fewer than ten narrow places. Chokepoint disruption is the highest-leverage adversary move.

| Chokepoint | Why it matters | Adversary angle |
|---|---|---|
| **Strait of Hormuz** | ~20-30% of global oil trade | Iran can mine / harass; *primary VANTAGE demo zone* |
| **Bab-el-Mandeb** | Suez approaches; Red Sea entry | Houthi attacks, Iranian-backed |
| **Suez Canal** | Europe-Asia shortcut | Egyptian sovereignty; recall *Ever Given* 2021 |
| **Strait of Malacca** | China's main oil import route; ~25% of global trade | Chinese chokepoint anxiety drives Belt & Road logic |
| **Taiwan Strait** | TSMC, China-Taiwan | The most strategically loaded body of water on earth right now |
| **South China Sea** | Disputed islands, $3T+ annual trade | Chinese island-building, Philippine standoffs |
| **Bosphorus / Dardanelles** | Russian Black Sea access | Turkish control under Montreux Convention |
| **English Channel** | NATO/UK lifeline | Russian shadow shipping, undersea cable risk |
| **Bering Strait** | Arctic gateway | Russia/China Arctic posture |

### Key US base footprint (just enough to know)
- **Diego Garcia** (Indian Ocean) — strategic bomber/sub base
- **Guam** (Pacific) — power projection into INDOPACOM
- **Bahrain** — 5th Fleet HQ (CENTCOM maritime)
- **Ramstein** (Germany) — air ops hub for EUCOM/AFRICOM
- **Yokosuka / Sasebo** (Japan) — 7th Fleet
- **Camp Humphreys** (Korea) — biggest US base overseas

### Why this matters for VANTAGE
Pick **one** region for your hero demo. **Strongly recommend Hormuz / Bab-el-Mandeb**: data is public, incidents are recent, adversaries are named (Iran, Houthi forces), the news cycle gives you fresh material every week. Mention in your pitch that VANTAGE extends naturally to South China Sea, Black Sea, Baltic.

Avoid demos that involve invented countries or hypothetical scenarios. Real ship + real chokepoint + real ownership trail = irrefutable credibility.

### Talk like a pro
> *"Our hero demo runs over the Strait of Hormuz because that's where the gray-zone playbook is most active right now. The architecture extends to the Taiwan Strait and the Black Sea without code changes."*

---

## Section 7 · THE RED LINES — DoD Directive 3000.09 and human-in-the-loop

### TL;DR
The most important policy document for any AI defense product is **DoD Directive 3000.09 (Autonomy in Weapon Systems)**, originally issued 2012 and updated January 2023. It defines three regimes of human involvement: **in-the-loop**, **on-the-loop**, and **out-of-the-loop**, and effectively requires "appropriate levels of human judgment" for any use of force. The 2023 update actually *loosened* some constraints to allow human-on-loop for time-critical defensive systems. **The line between getting deployed and getting killed by reviewers is whether you respect this doctrine.**

### The three regimes
| Regime | What it means | Where it's allowed |
|---|---|---|
| **Human-in-the-loop** | AI recommends; human authorizes each action | Default for lethal force, especially against humans |
| **Human-on-the-loop** | AI selects and engages; human can override in real time | Allowed for time-critical defense (counter-UAS, point defense) |
| **Human-out-of-the-loop** | AI selects and engages with no human intervention | Heavily restricted; not authorized for strategic targets |

### Why "human-in-the-loop" is a religion
Three reasons stack:
1. **Ethics** — broad consensus that machines must not autonomously decide to kill humans. International humanitarian law (LOAC), a wide range of NGO advocacy, and DoD's own ethical AI principles all converge here.
2. **Legality** — every engagement has to be ROE-compliant and Law-of-Armed-Conflict-compliant. Humans (often with a JAG officer alongside) verify this. AI cannot be held legally accountable; commanders can.
3. **Practicality** — AI is wrong sometimes. The cost of a wrong target is asymmetric (a destroyed school vs. a delayed strike). The human is the failsafe.

### What the 2023 update changed
The revision *streamlined* the senior-leader review process and explicitly allowed human-on-the-loop for defensive systems where "system speed exceeds human cognitive speed." This is why counter-UAS systems can engage incoming drones autonomously *as long as a human can override*. It does not relax constraints on offensive lethal autonomy.

### Where the JAG officer fits
A **Judge Advocate General officer** is the legal officer attached to commands that conduct operations. They review targeting packages for ROE/LOAC compliance. The whisper-secret bottleneck in modern kill chains is often *not* technical — it's waiting for the JAG to approve the engagement. **A VANTAGE that compresses *technical* fusion but ignores the legal review gate is solving the wrong half of the problem.**

### Other red lines worth knowing
- **Civilian harm** — every engagement must consider proportionality and discrimination (LOAC principles). AI systems that cannot reason about proportionality are non-starters for lethal use.
- **Bias and hallucination** — AI that makes confident wrong claims can get a commander charged with a war crime. Vannevar's whole pitch is "we finetune for accuracy" precisely because of this.
- **Audit trail** — every AI-assisted decision must be logged and explainable. *This is exactly what VANTAGE's evidence-trail design supports.*

### Why this matters for VANTAGE
- **Never claim autonomy.** Always show the human gate.
- Frame the AI as **augmentation**, not replacement.
- Build in **explainable rationale** for every recommendation (your demo's "why" pane).
- Show the **audit trail** — every alert has receipts.
- If anyone asks "is this 3000.09-compliant?" the answer is **"yes, we're a human-in-the-loop decision-support system; we do not engage targets."**

### Talk like a pro
> *"VANTAGE is fully aligned with DoD 3000.09 — the system is decision support, not weapons employment. Every recommendation has an evidence trail and a human authorization gate."*

---

## Section 8 · CULTURE & LANGUAGE — How to sound like you belong

### TL;DR
Military culture rewards **brevity, directness, and respect for hierarchy.** Acronym density is high but you only need to know ~30 of them. Time and date formats are different. The biggest cultural sin is overclaiming experience or expertise you don't have; the biggest cultural win is acknowledging what you don't know while showing you've done the homework on what matters.

### How they talk
- **Laconic.** Short sentences, no fluff. "Roger." "Wilco." "Negative." Not "Yeah I'll take care of that."
- **Direct.** "Here's the situation, here's what I need." Not buried in qualifiers.
- **Hierarchical address.** Sir/ma'am is universal in formal contexts. Use rank or position when known ("Colonel," "Commander," "Chief").
- **End with a comm-check phrase.** "How copy?" "Over." "Out." (Don't say both — "over" means continue, "out" means done.)

### Time and date formats
- **Time:** 24-hour clock, no colon. *1430* not *14:30* and not *2:30 PM*. "Fourteen thirty" or "fourteen-thirty hours."
- **Date:** Day-Month(abbrev)-Year. *02MAY26* not *5/2/2026*. The month is always the abbreviation.
- **Time zone:** Often expressed as a single letter — *Z* for Zulu (UTC), *L* for local. *1430Z* = 14:30 UTC.

### The cardinal sins (don't commit these on stage)
- **Calling a Marine a "soldier."** Soldiers are Army. Marines are Marines. Mistake = visible cringe.
- **"The Pentagon decided X."** The Pentagon is a building. The decision was made by the Secretary of Defense, OSD (Office of the Secretary of Defense), the Joint Chiefs, or a specific service. Specificity matters.
- **Calling AI "autonomous"** without qualification. Triggers 3000.09 alarm bells. Always say "AI-augmented decision support" or "human-in-the-loop AI."
- **Overclaiming you've worked with the military.** If you haven't, don't pretend. Officers hire for honesty.
- **Using "killchain" as a casual verb.** It's a serious term tied to lethal force; using it loosely makes you sound like a *Call of Duty* enthusiast, not a defense person.

### The fast credibility wins
- **Name a real adversary system or platform.** "We're not trying to clone Lattice." "This complements Maven." Instant recognition.
- **Use a chokepoint correctly in context.** "Hormuz" not "the Iran area."
- **Distinguish strategic / operational / tactical.** Strategic = national, years; operational = theater, months; tactical = unit, hours-days. Mixing levels reveals greenness.
- **Reference DoD 3000.09 by number.** Marks you as someone who's read the actual policy.
- **Acknowledge what you don't know.** "I'm not a military operator, so I'd want to validate this assumption with someone who is" lands extremely well.

### Acronym density management
You don't need to know every acronym. You need to recognize the ones you'll see and use the ones that signal homework. Refer to the glossary below.

### Dress code
For the hackathon, normal hacker attire is fine. If you ever pitch to a colonel later, lean conservative — collared shirt, no logos. Don't wear military-coded gear (camo pattern, "Operator" t-shirts) unless you've earned it; it reads as costume.

### What to do if you don't know something on stage
"That's a great question. I don't know the precise answer, but here's how I'd think about it — and I'd want to validate with the operator community before deploying." This response wins. Bullshitting loses.

### Why this matters for VANTAGE
You will be in a room with people who genuinely speak this language. Your goal is not to *be* one of them — it's to *respect* them, communicate clearly, and make obvious that you've done the homework. Officers love builders who try to learn. They despise builders who pretend.

### Talk like a pro
> *"I'm a builder, not an operator — I built VANTAGE by talking to people who do this for a living and reading enough doctrine to know what I don't know. Here's what we built and why."*

---

## Glossary — the ~30 acronyms you'll actually hear

| Acronym | Meaning |
|---|---|
| AIS | Automatic Identification System (maritime transponder) |
| ADS-B | Automatic Dependent Surveillance-Broadcast (aviation transponder) |
| AOR | Area of Responsibility |
| ATAK | Android Tactical Assault Kit |
| BDA | Battle Damage Assessment |
| C2 | Command and Control |
| CJADC2 | Combined Joint All-Domain Command and Control |
| COA | Course of Action |
| COP | Common Operational Picture |
| CoT | Cursor on Target (data schema) |
| CONOPS | Concept of Operations |
| ELINT | Electronic Intelligence |
| F2T2EA | Find, Fix, Track, Target, Engage, Assess |
| GEOINT | Geospatial Intelligence |
| HUMINT | Human Intelligence |
| IMINT | Imagery Intelligence |
| ISR | Intelligence, Surveillance, Reconnaissance |
| I&W | Indications and Warnings |
| JAG | Judge Advocate General (legal officer) |
| LOAC | Law of Armed Conflict |
| MASINT | Measurement and Signature Intelligence |
| MDMP | Military Decision Making Process |
| OODA | Observe, Orient, Decide, Act |
| OPORD | Operations Order |
| OSD | Office of the Secretary of Defense |
| OSINT | Open-Source Intelligence |
| RF | Radio Frequency |
| ROE | Rules of Engagement |
| SIGINT | Signals Intelligence |
| SOCOM | Special Operations Command |
| SOF | Special Operations Forces |
| STS | Ship-to-Ship (transfer) |
| TAK | Tactical Assault Kit (the broader ecosystem) |
| TOC | Tactical Operations Center |
| UAS / UAV | Unmanned Aerial System / Vehicle |

---

## What to do with this manual

1. **Read it once tonight,** end-to-end, before the kickoff happy hour. ~45 minutes.
2. **Tomorrow morning, before doors open,** re-skim sections 4 (Systems), 5 (Adversary), and 7 (Red Lines). Those are the ones that will come up most in judge questions.
3. **Keep it open in a tab during the build.** When someone on the team says "what's an S-2 again?", point them at section 1.
4. **Crib the "Talk like a pro" lines** for your pitch deck and your README. They are battle-tested phrasings.
5. **The glossary is a survival kit.** When someone uses an acronym you don't recognize, ctrl-F it.

You don't need to become a military expert. You need to be a builder who clearly **respects** the people you're building for, has done **enough** homework to ask intelligent questions, and stays **honest** about the limits of what you know.

That's the entire game.

---

*Sister docs: `../README.md` (project spec), `PS3_brainstorm_brief.md` (research, TBD), `repo_explore.md` (curated repos, TBD).*
