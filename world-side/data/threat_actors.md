# Threat Actors Reference Catalog

**Project:** Prophet — Threat-Timing Forecaster
**Layer:** World Layer / "Who" Reference Data
**Last Updated:** 2026-05-02
**Purpose:** Reference catalog of named state-affiliated APTs and major organized cyber-criminal groups, organized by sponsor. Each entry follows a consistent structure so downstream pattern-matchers can parse the file and align historical actor-behavior triggers with current geopolitical context.

**Naming-taxonomy note:** Microsoft transitioned to a weather-based taxonomy in April 2023 (Blizzard = Russia, Typhoon = China, Sleet = North Korea, Sandstorm = Iran, Tempest = financial cybercrime, Storm-#### = developing/unattributed). In June 2025, Microsoft, CrowdStrike, Google/Mandiant, and Palo Alto Unit 42 announced a strategic collaboration to publish a unified mapping across taxonomies. This catalog uses the most-common public name as the primary heading, with full alias lists per entry.

---

## RUSSIA

Russia's offensive cyber capability is split across three intelligence services with overlapping but distinguishable mandates: the **GRU** (military intelligence; disruptive and destructive operations, influence), the **SVR** (foreign intelligence; long-dwell strategic espionage), and the **FSB** (domestic security; political targeting, near-abroad, and protect-the-criminals tolerance). Microsoft's Blizzard suffix tracks all three.

### Sandworm

- **Common name(s) and aliases.** Sandworm / Voodoo Bear (CrowdStrike) / Telebots / IRIDIUM (legacy MS) / Seashell Blizzard (Microsoft, current) / BlackEnergy Group / ELECTRUM (Dragos) / IRON VIKING (SecureWorks).
- **Suspected sponsor / unit.** Russian GRU Main Center for Special Technologies (GTsST), military Unit 74455. Attributed by US DOJ indictment (October 2020) and UK NCSC.
- **Active years.** ~2009–present; first publicly named by iSIGHT Partners in 2014.
- **Typical target sectors.** Electric grids, ICS/SCADA, government, telecommunications, transportation/logistics, media, sporting events. Strong Ukraine focus.
- **Signature TTPs.** Destructive wipers and ICS-targeting malware (BlackEnergy, Industroyer/CrashOverride, NotPetya, Olympic Destroyer, Industroyer2, AcidRain, CaddyWiper). Heavy use of supply-chain compromise and living-off-the-land (T1485 Data Destruction, T1561 Disk Wipe).
- **Historical activation triggers.** Major Russian geopolitical inflection points: Ukraine pre-invasion preparation (BlackEnergy 2015 grid attack, Dec 23 2015), Russian doping ban (Olympic Destroyer, Feb 2018 PyeongChang opening), expansion of Western sanctions (NotPetya, June 27 2017 — pre-Constitution-Day Ukraine), and full-scale invasion windows (AcidRain wiped Viasat KA-SAT modems on Feb 24 2022, the morning of the invasion).
- **Notable named campaigns.** BlackEnergy / Ukraine grid blackout (2015); Industroyer / Kyiv blackout (2016); NotPetya (2017, ~$10B global damage); Olympic Destroyer (2018); AcidRain / Viasat (2022); Industroyer2 / Ukrenergo (2022); Prestige ransomware on Polish/Ukrainian logistics (Oct 2022).
- **Authoritative reference.** MITRE ATT&CK G0034 — https://attack.mitre.org/groups/G0034/ ; Mandiant — https://www.mandiant.com/resources/blog/sandworm-disrupts-power-ukraine-operational-technology

### APT28 / Fancy Bear

- **Common name(s) and aliases.** APT28 (Mandiant) / Fancy Bear (CrowdStrike) / Sofacy / Pawn Storm (Trend Micro) / Sednit (ESET) / STRONTIUM (legacy MS) / Forest Blizzard (Microsoft) / IRON TWILIGHT (SecureWorks) / Group 74.
- **Suspected sponsor / unit.** GRU 85th Main Special Service Center, military Unit 26165. Named in DOJ indictments (July 2018, Oct 2018) and DOJ/UK joint statement.
- **Active years.** ~2004–present.
- **Typical target sectors.** Government, military, defense industrial base, political organizations, journalists, anti-doping bodies, aerospace, NATO members and partners.
- **Signature TTPs.** Credential phishing at scale, zero-day exploitation (CVE-2017-0263, CVE-2023-23397 Outlook), custom implants (X-Agent, Sofacy, Zebrocy, GooseEgg), router compromise (T1133 External Remote Services), hack-and-leak operations.
- **Historical activation triggers.** Election cycles in NATO countries (US 2016, France 2017, US 2024); WADA/IOC actions against Russian athletes (2016 WADA hack post-McLaren report); NATO summits and exercises; Bundestag plenary periods (2015 Bundestag breach).
- **Notable named campaigns.** German Bundestag (2015); DNC / DCCC / Podesta hack-and-leak (2016); WADA/TAS leak (2016); MacronLeaks (May 2017); IOC PyeongChang reconnaissance (2018); Outlook NTLM-relay campaign exploiting CVE-2023-23397 (2022–2023); GooseEgg post-exploitation tooling exposed by Microsoft (2024).
- **Authoritative reference.** MITRE ATT&CK G0007 — https://attack.mitre.org/groups/G0007/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2024/04/22/analyzing-forest-blizzards-custom-post-compromise-tool-for-exploiting-cve-2022-38028-to-obtain-credentials/

### APT29 / Cozy Bear

- **Common name(s) and aliases.** APT29 / Cozy Bear (CrowdStrike) / The Dukes (F-Secure) / NOBELIUM (legacy MS) / Midnight Blizzard (Microsoft) / UNC2452 / IRON RITUAL / YTTRIUM / BlueBravo (Recorded Future).
- **Suspected sponsor / unit.** Russian Foreign Intelligence Service (SVR). Attributed jointly by NSA, CISA, FBI, and UK NCSC in April 2021 SolarWinds attribution statement.
- **Active years.** ~2008–present.
- **Typical target sectors.** Western foreign-policy ministries, diplomatic missions, think tanks, COVID-19 vaccine research (2020), cloud and identity-platform vendors, IT supply chain.
- **Signature TTPs.** Stealthy long-dwell operations, supply-chain compromise (SolarWinds), abuse of OAuth/identity (Golden SAML, T1606 Forge Web Credentials), password spray + MFA fatigue, cloud-native lateral movement (T1078.004 Cloud Accounts).
- **Historical activation triggers.** Strategic policy moments where forecasting Western intent is high-value: NATO/EU summits, sanctions-package drafting, vaccine-development races, US administration transitions (DNC 2015 prior to election; SolarWinds active during US-Russia diplomatic transition in 2020).
- **Notable named campaigns.** DNC intrusion (2015–2016, parallel to APT28); COVID-19 vaccine targeting (2020, UK/US/Canada joint advisory); SolarWinds / SUNBURST supply-chain (Dec 2020, ~18,000 customers); Microsoft corporate email breach via legacy OAuth app (Jan 2024); HPE corporate email breach (May 2023, disclosed Jan 2024); TeamViewer corporate intrusion (June 2024).
- **Authoritative reference.** MITRE ATT&CK G0016 — https://attack.mitre.org/groups/G0016/ ; Mandiant — https://cloud.google.com/blog/topics/threat-intelligence/unc2452-merged-into-apt29

### Turla

- **Common name(s) and aliases.** Turla / Snake / Uroburos / Venomous Bear (CrowdStrike) / Waterbug (Symantec) / Krypton / SECRET BLIZZARD (Microsoft) / IRON HUNTER.
- **Suspected sponsor / unit.** Russian FSB Center 16 (Center for Information Security). Named in May 2023 joint advisory (FBI / NSA / CISA / Five Eyes) tied to Operation MEDUSA Snake-malware takedown.
- **Active years.** ~1996–present (one of the longest-running APTs; lineage to "Moonlight Maze" 1996–1999).
- **Typical target sectors.** Foreign ministries, embassies, defense, research institutions, OPEC, NATO members and partners; very Western-Europe heavy.
- **Signature TTPs.** Bespoke implants (Snake/Uroburos, Carbon, Mosquito, Kazuar), satellite-link C2 hijacking (T1583.005), abuse of compromised infrastructure of other actors (notably riding atop Iranian APT34 infrastructure as exposed by NCSC/NSA in 2019), strong OPSEC and stealth.
- **Historical activation triggers.** Long-cycle strategic intelligence; spikes correlated with NATO/EU foreign-policy formation periods and post-sanctions retaliation phases. Notable bursts after the 2014 Crimea annexation and around the 2022 Ukraine invasion.
- **Notable named campaigns.** RUAG (Swiss defense, 2014); German Foreign Office (2017–2018); "Neuron"/"Nautilus" hijacking Iranian infrastructure (2017–2018, exposed 2019); Kazuar backdoor reuse with SUNBURST (analyzed 2021); Operation MEDUSA Snake takedown by FBI (May 2023).
- **Authoritative reference.** MITRE ATT&CK G0010 — https://attack.mitre.org/groups/G0010/ ; CISA AA23-129A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-129a

### Gamaredon

- **Common name(s) and aliases.** Gamaredon / Primitive Bear (CrowdStrike) / ACTINIUM (legacy MS) / Aqua Blizzard (Microsoft) / Armageddon (SSU of Ukraine) / Shuckworm (Symantec) / Trident Ursa (Unit 42) / IRON TILDEN.
- **Suspected sponsor / unit.** FSB officers operating from occupied Crimea (FSB 18th Center, Sevastopol office). Officially attributed by Ukraine's SSU in November 2021 with named officers indicted.
- **Active years.** 2013–present (post-Crimea annexation).
- **Typical target sectors.** Almost exclusively Ukrainian — government, military, defense, law enforcement, diplomatic. Highest-volume Russian operator against Ukraine.
- **Signature TTPs.** Spear-phishing with weaponized Office documents (T1566.001), VBScript/PowerShell loaders, custom tooling (PteroLogin, Pterodo, GammaLoad, GammaSteel). Volume over stealth — described as "noisy" and tactical-tempo.
- **Historical activation triggers.** Russian military preparations and active operations against Ukraine. Activity surges precede kinetic phases: pre-invasion ramp Q4 2021–Feb 2022; sustained high tempo throughout the war; bursts before major Ukrainian counteroffensives.
- **Notable named campaigns.** Continuous "Armageddon" campaign tracking (2014–present per SSU); pre-invasion 2022 surge documented by Symantec/Talos; ongoing PowerShell-based operations against Ukrainian government 2023–2025.
- **Authoritative reference.** MITRE ATT&CK G0047 — https://attack.mitre.org/groups/G0047/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2022/02/04/actinium-targets-ukrainian-organizations/

### Star Blizzard / Callisto

- **Common name(s) and aliases.** Star Blizzard (Microsoft) / Callisto Group / SEABORGIUM / COLDRIVER / TA446 (Proofpoint) / BlueCharlie (Recorded Future) / Iron Frontier.
- **Suspected sponsor / unit.** UK NCSC assesses "almost certainly" subordinate to FSB Centre 18. Two officers — Ruslan Peretyatko (FSB Centre 18) and Andrey Korinets — indicted by US DOJ in December 2023.
- **Active years.** ~2015–present.
- **Typical target sectors.** Defense/foreign-policy think tanks, academia, journalists, NGOs, current and former government officials, US Department of Energy nuclear-research staff, Ukraine-related advocacy.
- **Signature TTPs.** Long-form social-engineering and credential phishing (T1566.002), evilginx-style adversary-in-the-middle phishing kits, persistent reconnaissance against named individuals, hack-and-leak (e.g., 2019 UK trade-document leak before general election).
- **Historical activation triggers.** UK and US election windows; Western policy debates on Ukraine support, sanctions, and energy; nuclear-policy negotiations. Activity intensified after the 2022 Ukraine invasion and again ahead of the 2024 US election.
- **Notable named campaigns.** Pre-2019 UK general election trade-document leak; sustained targeting of US national labs (2020–2022); 2023 NCSC/CISA joint advisory on parliamentary and academic targeting; Microsoft/DOJ takedown of 100+ domains (October 2024).
- **Authoritative reference.** MITRE ATT&CK G1003 (Note: COLDRIVER tracked separately) — https://attack.mitre.org/groups/G1003/ ; CISA AA23-341A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-341a

### Berserk Bear / Energetic Bear

- **Common name(s) and aliases.** Berserk Bear (CrowdStrike) / Energetic Bear / Dragonfly / Crouching Yeti (Kaspersky) / TEMP.Isotope / DYMALLOY (Dragos) / IRON LIBERTY / Ghost Blizzard (Microsoft, recent).
- **Suspected sponsor / unit.** Russian FSB Center 16 — Russian nationals Pavel Akulov, Mikhail Gavrilov, and Marat Tyukov of FSB Military Unit 71330 indicted by DOJ in March 2022.
- **Active years.** ~2010–present.
- **Typical target sectors.** Energy (electricity, oil/gas), water, nuclear, aviation, critical-manufacturing OT/ICS networks; primarily US, Western Europe, Turkey.
- **Signature TTPs.** Watering-hole attacks against industry-specific sites, supply-chain compromise of ICS vendor websites, Havex/Karagany malware, Outlook web-form persistence, long-dwell reconnaissance of OT networks (rarely destructive — focus on prepositioning and tradecraft refinement, T1190).
- **Historical activation triggers.** Critical-infrastructure targeting cycles correlate with US-Russia tensions and energy-policy moments. 2017–2018 wave coincided with intensifying sanctions debate; 2020 US state/local government targeting was disclosed weeks before the November 2020 election.
- **Notable named campaigns.** "Dragonfly" energy-sector campaigns (2013–2014); "Dragonfly 2.0" / Palmetto Fusion (2017, US/UK/Turkey energy and nuclear); US state, local, territorial, tribal (SLTT) government access campaign (Oct 2020 CISA advisory); March 2022 DOJ indictment unsealed for global energy targeting including Wolf Creek nuclear plant.
- **Authoritative reference.** MITRE ATT&CK G0035 (Dragonfly) — https://attack.mitre.org/groups/G0035/ ; CISA AA20-296A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-296a

### Cadet Blizzard / Ember Bear

- **Common name(s) and aliases.** Cadet Blizzard (Microsoft) / Ember Bear (CrowdStrike) / Saint Bear (ThreatBook) / FROZENVISTA (Google TAG) / Nodaria (Symantec) / TA471 (Proofpoint) / UAC-0056 (CERT-UA) / UNC2589 (Mandiant) / DEV-0586 (legacy MS) / Bleeding Bear.
- **Suspected sponsor / unit.** GRU 161st Specialist Training Center, Unit 29155. Officially attributed by US, UK, and 9-country coalition in September 2024 with $10M reward offered.
- **Active years.** ~2020–present.
- **Typical target sectors.** Ukraine government and critical infrastructure; NATO-member governments and critical infrastructure (Czechia, Poland, Estonia, Latvia documented); aid/logistics organizations supporting Ukraine.
- **Signature TTPs.** Destructive disk wipers disguised as ransomware, web-server defacement, leak-site mockups for psychological effect, exploitation of public-facing applications (T1190). Unit 29155 historically conducted GRU sabotage and assassination — cyber arm reflects that culture.
- **Historical activation triggers.** Pre-kinetic phases of Russian aggression. WhisperGate hit Ukrainian government on January 13–14, 2022 — exactly five weeks before the full-scale invasion — alongside diplomatic negotiations breaking down. Activity tracks Russian pressure cycles on NATO-eastern-flank states.
- **Notable named campaigns.** WhisperGate destructive wiper (Jan 13–14, 2022); Ukrainian government website defacement campaign (Jan 2022); critical-infrastructure targeting across 26+ NATO countries documented in Sept 2024 joint advisory; transportation-sector reconnaissance in Eastern Europe (2023–2024).
- **Authoritative reference.** MITRE ATT&CK G1003 — https://attack.mitre.org/groups/G1003/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2023/06/14/cadet-blizzard-emerges-as-a-novel-and-distinct-russian-threat-actor/

### RomCom / Storm-0978

- **Common name(s) and aliases.** RomCom / Storm-0978 (Microsoft) / Tropical Scorpius (Unit 42) / Void Rabisu (Trend Micro) / UAC-0180 (CERT-UA).
- **Suspected sponsor / unit.** Russia-aligned; Microsoft assesses dual-purpose financial-crime + Russian-state-aligned espionage. Connections to Cuba ransomface affiliation; targeting selection strongly aligned with GRU priorities (Ukraine support / NATO summits).
- **Active years.** 2022–present.
- **Typical target sectors.** Defense, government, Ukraine-aid organizations, energy, pharmaceutical, NATO summit attendees, Western politicians.
- **Signature TTPs.** Trojanized installers of legitimate software, zero-day exploitation (CVE-2023-36884 Office/Windows Search), RomCom RAT family, occasional ransomware deployment as cover. Hybrid criminal/state operating model.
- **Historical activation triggers.** NATO summits and Ukraine-policy moments. CVE-2023-36884 zero-day was used against attendees of the July 2023 Vilnius NATO Summit and the Ukrainian World Congress. Pattern: surge before publicly announced multilateral events.
- **Notable named campaigns.** Ukrainian-military-themed lures (2022); CVE-2023-36884 Vilnius NATO Summit campaign (June–July 2023); UNC4895 / "Industrial Spy" affiliations (2022); 2024 Firefox/Windows zero-day chain (CVE-2024-9680 + CVE-2024-49039) reported by ESET.
- **Authoritative reference.** MITRE ATT&CK G1024 — https://attack.mitre.org/groups/G1024/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2023/07/11/storm-0978-attacks-reveal-financial-and-espionage-motives/

---

## CHINA

China's offensive cyber posture is now dominated by the **Ministry of State Security (MSS)** civilian intelligence service operating through provincial bureaus and contractor companies (notably exposed in the 2024 i-Soon leak), plus **PLA Strategic Support Force / Cyberspace Force** units. MSS has progressively absorbed missions formerly run by PLA Unit 61398. Microsoft tracks Chinese actors with the Typhoon suffix.

### APT1

- **Common name(s) and aliases.** APT1 / Comment Crew / Comment Panda / GIF89a / Byzantine Candor / Brown Fox / Shanghai Group.
- **Suspected sponsor / unit.** PLA General Staff Department 3rd Department, 2nd Bureau, Unit 61398 (Pudong, Shanghai). Five officers indicted by US DOJ in May 2014 — first-ever US criminal charges against state actors for hacking.
- **Active years.** ~2006–2014 (post-indictment, mission migrated to MSS-aligned groups).
- **Typical target sectors.** US/Western intellectual-property-rich industries: aerospace, energy, telecom, IT, satellite/transport, scientific R&D, manufacturing.
- **Signature TTPs.** High-volume IP theft, custom backdoors (WEBC2, BISCUIT, GLOOXMAIL), simple but persistent spear-phishing, long dwell times (often years).
- **Historical activation triggers.** Five-Year-Plan-aligned industrial-policy priorities. Activity correlated with the 12th Five-Year Plan (2011–2015) sectors. APT1's public exposure was itself triggered by accumulated US frustration over IP theft pre-2014 indictment.
- **Notable named campaigns.** Mandiant documented at least 141 victims across 20 industries in the Feb 2013 APT1 report; targeting of Telvent (energy SCADA, 2012); NYT and WSJ reporter compromises (2013); QinetiQ defense compromise (multi-year, ~2007–2010).
- **Authoritative reference.** MITRE ATT&CK G0006 — https://attack.mitre.org/groups/G0006/ ; Mandiant APT1 Report — https://www.mandiant.com/sites/default/files/2021-09/mandiant-apt1-report.pdf

### APT10 / Stone Panda

- **Common name(s) and aliases.** APT10 / Stone Panda (CrowdStrike) / menuPass / POTASSIUM (legacy MS) / Granite Typhoon (Microsoft) / Cicada / CVNX / HOGFISH / Red Apollo / BRONZE RIVERSIDE.
- **Suspected sponsor / unit.** MSS Tianjin State Security Bureau, with operational use of contractor company Huaying Haitai. Two MSS officers indicted by US DOJ in December 2018.
- **Active years.** ~2009–present.
- **Typical target sectors.** Managed Service Providers (MSPs) — used as supply-chain pivot to client networks across aerospace, healthcare, government, biotech, mining, finance.
- **Signature TTPs.** "Cloud Hopper" supply-chain through MSPs (T1199 Trusted Relationship), credential theft and re-use across federated environments, custom backdoors (PlugX, Quasar, RedLeaves, ChChes).
- **Historical activation triggers.** Industrial-policy priorities and Made-in-China-2025 sectors; M&A and trade-negotiation cycles. Operation Cloud Hopper (2014–2017) ran throughout the Made-in-China-2025 rollout window.
- **Notable named campaigns.** Operation Cloud Hopper (2014–2017, MSP supply-chain); IBM and HPE breaches (disclosed 2018); A-LIST / NTT Data (2020); ongoing operations against Japanese government and defense contractors documented by JPCERT and NPA (2021–2024).
- **Authoritative reference.** MITRE ATT&CK G0045 — https://attack.mitre.org/groups/G0045/ ; CrowdStrike — https://www.crowdstrike.com/adversaries/stone-panda/

### APT41 / Wicked Panda

- **Common name(s) and aliases.** APT41 / Wicked Panda (CrowdStrike) / Barium / Winnti (overlapping cluster) / Brass Typhoon (Microsoft, current) / BARIUM (legacy MS) / Double Dragon (Mandiant report title) / TG-2633.
- **Suspected sponsor / unit.** MSS contractors (Chengdu 404 Network Technology). Five Chinese nationals indicted by US DOJ in September 2020.
- **Active years.** ~2012–present.
- **Typical target sectors.** Dual-use: state espionage targeting (healthcare, telecom, government) **and** financially motivated targeting (online gaming, cryptocurrency, software supply chain). Globally distributed.
- **Signature TTPs.** Software supply-chain compromise (CCleaner 2017, ASUS Live Update 2019, NetSarang 2017), gaming-industry virtual-currency theft, custom modular implants (HIGHNOON, PIPEMON, MESSAGETAP). Frequently uses code-signing certificates stolen from gaming firms.
- **Historical activation triggers.** Dual cycle — espionage tasking aligns with Chinese strategic priorities (Belt-and-Road, Made-in-China-2025); financial activity is opportunistic. Notable surge against state and local US governments in May–Feb 2022 during early COVID-19 federal-relief disbursement window.
- **Notable named campaigns.** ShadowPad (NetSarang) supply chain (2017); CCleaner backdoor (2017); ASUS Live Update / Operation ShadowHammer (2019); MESSAGETAP telecom-CDR theft (2019); US state-government compromises across at least six states using Log4Shell and USAHerds vulnerabilities (May 2021–Feb 2022, per Mandiant).
- **Authoritative reference.** MITRE ATT&CK G0096 — https://attack.mitre.org/groups/G0096/ ; Mandiant — https://www.mandiant.com/resources/insights/apt41-dual-espionage-and-cyber-crime-operation

### APT40 / Leviathan

- **Common name(s) and aliases.** APT40 / Leviathan (Proofpoint) / Bronze Mohawk (SecureWorks) / GADOLINIUM (legacy MS) / Gingham Typhoon (Microsoft) / Kryptonite Panda (CrowdStrike) / TEMP.Periscope / TEMP.Jumper / MUDCARP.
- **Suspected sponsor / unit.** MSS Hainan State Security Department, operating through front company Hainan Xiandun Technology Development Co. Four Chinese nationals (3 MSS officers + 1 Hainan Xiandun employee) indicted by US DOJ in July 2021.
- **Active years.** ~2013–present.
- **Typical target sectors.** Maritime industries, naval defense contractors, universities (especially with Navy research links), engineering, transportation, healthcare/biomedical, governments around the South China Sea littoral, plus countries with Belt-and-Road initiatives.
- **Signature TTPs.** Rapid weaponization of newly disclosed N-day vulnerabilities (often within days), targeting of edge devices (SOHO routers, VPN appliances) for ORB infrastructure, custom implants (Murkytop, Homefry, Scanbox web profiler), heavy use of Australian-government-hosted infrastructure for proxying.
- **Historical activation triggers.** South China Sea diplomatic and military events; AUKUS announcement (Sept 2021) preceded sustained Australian-government targeting; freedom-of-navigation operations; Belt-and-Road negotiation cycles.
- **Notable named campaigns.** US Navy submarine-warfare contractor compromises (2018); Cambodian election infrastructure (2018); July 2021 indictment campaign (multi-year, multi-country); ongoing Australian government targeting summarized in joint ASD/CISA advisory (July 2024); compromised SOHO router ORB networks documented by Mandiant (2024).
- **Authoritative reference.** MITRE ATT&CK G0065 — https://attack.mitre.org/groups/G0065/ ; ASD/CISA Joint Advisory — https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/apt40-advisory

### Volt Typhoon

- **Common name(s) and aliases.** Volt Typhoon (Microsoft) / VANGUARD PANDA (CrowdStrike) / BRONZE SILHOUETTE (SecureWorks) / Voltzite (Dragos) / DEV-0391 (legacy MS) / Insidious Taurus (Unit 42).
- **Suspected sponsor / unit.** PRC state-sponsored actor; FBI Director Wray (Jan 2024 House testimony) and CISA Director Easterly publicly attributed pre-positioning intent to PLA-aligned mission. Joint CISA/NSA/FBI advisory Feb 2024.
- **Active years.** Public discovery May 2023; activity dating to mid-2021.
- **Typical target sectors.** US critical infrastructure — water/wastewater, electricity, transportation, communications, ports — plus Guam (logistics-relevant to Taiwan contingency). Pacific allies' infrastructure.
- **Signature TTPs.** Living-off-the-land binaries (LOLBins) almost exclusively; near-zero malware footprint; SOHO-router compromise (KV-Botnet) for last-mile obfuscation; theft of valid credentials for years-long persistence; explicit operational-preparation-of-the-environment posture rather than collection.
- **Historical activation triggers.** Strategic prepositioning rather than reactive — but discovery and disclosure surged ahead of the January 2024 Taiwan presidential election and the 2024 US election cycle. The KV-Botnet disruption (Dec 2023) and the unprecedented public attribution were timed with US administration messaging on Taiwan deterrence.
- **Notable named campaigns.** Initial Microsoft disclosure on Guam communications infrastructure (May 2023); KV-Botnet SOHO-router infrastructure exposed and disrupted by US DOJ court order (Dec 2023, announced Jan 2024); ongoing reporting of US water-utility intrusions through 2024 (CISA AA24-038A and follow-ons).
- **Authoritative reference.** MITRE ATT&CK G1017 — https://attack.mitre.org/groups/G1017/ ; CISA AA24-038A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a

### Salt Typhoon

- **Common name(s) and aliases.** Salt Typhoon (Microsoft) / GhostEmperor (Kaspersky) / FamousSparrow (ESET) / Earth Estries (Trend Micro) / UNC5807 (Mandiant) / RedMike (Recorded Future) / OPERATOR PANDA (CrowdStrike).
- **Suspected sponsor / unit.** PRC state-sponsored. CISA/NSA/FBI joint advisory (August 2025, AA25-239A) and 12-country coalition statement; activity attributed to MSS-aligned operations targeting global telecommunications.
- **Active years.** Discovery 2024 (likely active 2022 or earlier); cluster overlaps go back further.
- **Typical target sectors.** Telecommunications providers (US carriers including Verizon, AT&T, T-Mobile, Lumen, Spectrum, Consolidated, Windstream); government and lawful-intercept systems; ISP edge equipment globally (Cisco IOS XE, Fortinet).
- **Signature TTPs.** Compromise of telecommunications routing/lawful-intercept infrastructure, rootkits (Demodex), credential and configuration theft enabling targeted call and SMS metadata access, edge-device persistence on Cisco and Fortinet appliances, on-keyboard tradecraft.
- **Historical activation triggers.** Pre-positioning ahead of high-stakes US political and policy events. Salt Typhoon's targeting of US presidential and senior-administration phones was disclosed in October–December 2024 — directly during and after the US presidential campaign. The August 2025 CISA advisory was timed with renewed Taiwan-policy debate.
- **Notable named campaigns.** US telecom intrusion campaign disclosed Sept–Dec 2024 (lawful-intercept platforms, communications of senior US political figures); August 2025 joint advisory documenting global telecom, government, transportation, and lodging targeting; 2025 Global Cyber Alliance "Salt Typhoon Across the Internet" mapping.
- **Authoritative reference.** CISA AA25-239A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-239a ; Microsoft Threat Intelligence — https://www.microsoft.com/en-us/security/blog (Salt Typhoon coverage)

### Mustang Panda

- **Common name(s) and aliases.** Mustang Panda (CrowdStrike) / TA416 (Proofpoint) / RedDelta (Recorded Future) / BRONZE PRESIDENT (SecureWorks) / HoneyMyte (Kaspersky) / Earth Preta (Trend Micro) / Twill Typhoon (Microsoft) / Camaro Dragon (Check Point).
- **Suspected sponsor / unit.** PRC state-sponsored; CrowdStrike and Mandiant assess MSS-aligned with significant tasking on diaspora/policy targets aligned with United Front Work Department interests.
- **Active years.** ~2014–present.
- **Typical target sectors.** Asia-Pacific governments, ASEAN secretariats, Catholic Church / Vatican (Tibetan and Vatican-China dialogue context), NGOs in Mongolia and Taiwan, European foreign ministries, telecom in SE Asia.
- **Signature TTPs.** Lure documents tied to active geopolitical events, PlugX variants (notably the "USB-spreading" PlugX revealed by FBI takedown 2025), DLL side-loading (T1574.002), router firmware implants ("Horse Shell" by Camaro Dragon cluster).
- **Historical activation triggers.** Vatican–China diplomatic-recognition negotiations (RedDelta surge 2020 ahead of the September 2020 provisional agreement renewal); Russian invasion of Ukraine (Mar 2022 surge against EU foreign ministries with Ukraine-themed lures); ASEAN summits.
- **Notable named campaigns.** RedDelta Vatican / Hong Kong Catholic Diocese campaign (2020); EU diplomatic targeting with Ukraine-themed lures (2022); USB-spreading PlugX disrupted by FBI court order (Jan 2025, ~4,000 US machines cleaned); Earth Preta SE Asia government campaigns (2022–2025).
- **Authoritative reference.** MITRE ATT&CK G0129 — https://attack.mitre.org/groups/G0129/ ; Recorded Future RedDelta — https://www.recordedfuture.com/research/reddelta-targets-european-government-organizations

### Storm-0558

- **Common name(s) and aliases.** Storm-0558 (Microsoft developing-cluster designation, retained).
- **Suspected sponsor / unit.** PRC state-sponsored, attributed by US intelligence to China's Ministry of State Security (MSS). Microsoft and CISA Cyber Safety Review Board Mar 2024 report.
- **Active years.** Confirmed 2021–present.
- **Typical target sectors.** Foreign-ministry and senior-government email accounts in Western countries focused on China-policy formation (US State Department, Department of Commerce, Congressional staff dealing with China).
- **Signature TTPs.** Forged authentication tokens — used a stolen Microsoft consumer signing key (MSA key, vintage 2016) to mint tokens accepted by Exchange Online (T1606 Forge Web Credentials). Identity-layer attack rather than endpoint malware.
- **Historical activation triggers.** US-China senior-policy events. Discovery-window access (May 15 – Jun 16, 2023) coincided directly with Secretary Blinken's June 2023 Beijing visit, the first by a US Secretary of State to China since 2018. Targeting of Commerce Secretary Raimondo's emails preceded her August 2023 China trip.
- **Notable named campaigns.** Single named campaign — the Summer 2023 Microsoft Exchange Online intrusion (May–June 2023); ~25 organizations affected; ~60,000 State Department emails exfiltrated. Reviewed by US Cyber Safety Review Board (March 2024).
- **Authoritative reference.** Microsoft — https://www.microsoft.com/en-us/security/blog/2023/07/14/analysis-of-storm-0558-techniques-for-unauthorized-email-access/ ; CSRB Report — https://www.cisa.gov/sites/default/files/2025-03/CSRBReviewOfTheSummer2023MEOIntrusion508.pdf

### Flax Typhoon

- **Common name(s) and aliases.** Flax Typhoon (Microsoft) / Ethereal Panda (CrowdStrike) / Storm-0919 (legacy MS) / RedJuliett (Recorded Future, partial overlap).
- **Suspected sponsor / unit.** PRC state-sponsored; US DOJ/FBI tied operations to Integrity Technology Group (Beijing) — a PRC-government-linked contractor — in indictment and Raptor Train botnet takedown (September 2024). Treasury Department sanctioned Integrity Tech in January 2025.
- **Active years.** ~2021–present.
- **Typical target sectors.** Taiwanese government agencies, education, IT, manufacturing; expanded to global IoT and SOHO devices via the Raptor Train botnet for ORB infrastructure used against Western targets.
- **Signature TTPs.** Compromise of edge devices and IoT (cameras, NVRs, routers) to build botnet infrastructure (T1584 Compromise Infrastructure); minimal post-compromise malware; living-off-the-land techniques on Windows targets.
- **Historical activation triggers.** Taiwanese election and cross-Strait tension cycles. Microsoft public disclosure (August 2023) coincided with intensifying PLA exercises post-Pelosi visit; Raptor Train takedown (Sep 2024) was timed against PRC pressure on Taiwan around the 2024 election.
- **Notable named campaigns.** Sustained Taiwanese-government campaign documented by Microsoft (2023); Raptor Train IoT botnet (260,000+ devices, disrupted by US DOJ Sep 2024); pre-Taiwan-election ORB activity tracked through Q4 2023.
- **Authoritative reference.** Microsoft — https://www.microsoft.com/en-us/security/blog/2023/08/24/flax-typhoon-using-legitimate-software-to-quietly-access-taiwanese-organizations/ ; FBI Raptor Train announcement — https://www.fbi.gov/news/press-releases/court-authorized-operation-disrupts-worldwide-botnet-used-by-peoples-republic-of-china-prc-state-sponsored-hackers

---

## IRAN

Iran's offensive cyber capability splits across the **Islamic Revolutionary Guard Corps (IRGC)** — particularly the IRGC Intelligence Organization (IRGC-IO) and IRGC Electronic Warfare Cyber Defense Organization — and the civilian **Ministry of Intelligence and Security (MOIS / VAJA)**. Microsoft tracks Iranian actors with the Sandstorm suffix.

### APT33 / Elfin

- **Common name(s) and aliases.** APT33 / Elfin (Symantec) / Refined Kitten (CrowdStrike) / HOLMIUM (legacy MS) / Peach Sandstorm (Microsoft) / Magnallium (Dragos).
- **Suspected sponsor / unit.** IRGC-aligned. Mandiant attributes to Iran with high confidence; Recorded Future links to IRGC Intelligence Organization. No US indictment yet, but extensive overlap with IRGC-cleared Iranian contractors.
- **Active years.** ~2013–present.
- **Typical target sectors.** Aviation, defense, petrochemical, energy (especially Saudi and US energy firms), and increasingly satellite communications and defense industrial base.
- **Signature TTPs.** Password spraying at scale (T1110.003), spear-phishing with aviation/energy lures, custom backdoors (TURNEDUP, FalseFont), recent shift to FalseFont implant against US defense industrial base (Microsoft, Dec 2023).
- **Historical activation triggers.** US-Iran sanctions cycles and military events. Activity surged after the 2018 US withdrawal from JCPOA; Soleimani killing (Jan 3, 2020) preceded retaliatory targeting of US defense and government; sanctions snapbacks repeatedly correlate with new campaign waves.
- **Notable named campaigns.** Saudi/petrochemical targeting (2016–2017); ShapeShift cryptocurrency-exchange compromise (2018); Persistent password-spray campaign against energy and defense (2019–2020 Microsoft disclosure); FalseFont US defense industrial base (Dec 2023).
- **Authoritative reference.** MITRE ATT&CK G0064 — https://attack.mitre.org/groups/G0064/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2023/09/14/peach-sandstorm-password-spray-campaigns-enable-intelligence-collection-at-high-value-targets/

### APT34 / OilRig

- **Common name(s) and aliases.** APT34 / OilRig (Palo Alto Unit 42) / Helix Kitten (CrowdStrike) / IRN2 / Crambus (Symantec) / Hazel Sandstorm (Microsoft) / EUROPIUM (legacy MS) / Cobalt Gypsy.
- **Suspected sponsor / unit.** Iranian Ministry of Intelligence and Security (MOIS / VAJA). Internal MOIS tooling exposed in the "Lab Dookhtegan" Telegram leaks (2019).
- **Active years.** ~2014–present.
- **Typical target sectors.** Middle East energy, financial services, telecommunications, government — particularly Gulf states (Saudi Arabia, UAE, Qatar, Kuwait), Israel, plus extensions to Western firms with regional exposure.
- **Signature TTPs.** DNS-tunneling C2 (Helminth, ALMA Communicator), credential theft and re-use across Microsoft Exchange and IIS web shells (TwoFace), Outlook Web Access password capture, lateral movement via stolen credentials. Tooling famously hijacked-and-reused by Russia's Turla in 2017–2018.
- **Historical activation triggers.** Saudi-Iran tensions and Gulf maritime incidents. Surge after the September 2019 Abqaiq–Khurais Saudi Aramco facility attack; activity tracking US Iran-policy decisions (sanctions, JCPOA).
- **Notable named campaigns.** Operation Cleaver (early activity attributed by Cylance); Saudi Aramco targeting (2017); Bahrain government (2019); Lab Dookhtegan tool leaks exposing Glimpse, PoisonFrog, HyperShell (March 2019); Albanian government attack (July 2022, attributed to MOIS — caused Albania to sever diplomatic relations with Iran).
- **Authoritative reference.** MITRE ATT&CK G0049 — https://attack.mitre.org/groups/G0049/ ; Mandiant — https://cloud.google.com/blog/topics/threat-intelligence/apt34-targets-jordan-government

### APT35 / Charming Kitten

- **Common name(s) and aliases.** APT35 / Charming Kitten (CrowdStrike) / Phosphorus (legacy MS) / Mint Sandstorm (Microsoft) / Newscaster / Ajax Security Team / TA453 (Proofpoint) / Magic Hound / Cobalt Illusion / Yellow Garuda.
- **Suspected sponsor / unit.** IRGC Intelligence Organization (IRGC-IO). FBI cyber-most-wanted listing of Charming-Kitten-affiliated operators; US Treasury sanctions on the IRGC-IO.
- **Active years.** ~2014–present.
- **Typical target sectors.** Journalists, dissidents, academics, think-tank researchers focused on Iran policy, US/Israeli political campaigns, US nuclear-deal negotiators, Israeli civilian targets, COVID-19 research (2020).
- **Signature TTPs.** Long-form social-engineering personas (fake journalists, fake conference invites — "POWERSTAR" / "GhostEcho"), credential-phishing kits with MFA capture, account-takeover and email-thread injection, custom implants (POWERSTAR/CharmPower, BellaCiao).
- **Historical activation triggers.** US presidential campaign cycles (targeted Trump campaign 2020, Microsoft disclosure October 2020; targeted Trump and Biden campaigns 2024 per FBI/CISA/ODNI joint statement August 2024); JCPOA negotiations; Israel–Iran kinetic exchanges (April and October 2024 missile exchanges preceded by phishing surges).
- **Notable named campaigns.** HBO breach precursor activity (2017); 2020 US presidential campaign targeting; Israel-Hamas war academic-researcher targeting (Oct 2023 onward); August 2024 Trump-campaign hack-and-leak attributed by ODNI; ongoing TA453 academic-researcher impersonation through 2025.
- **Authoritative reference.** MITRE ATT&CK G0059 — https://attack.mitre.org/groups/G0059/ ; Microsoft — https://www.microsoft.com/en-us/security/blog/2023/04/18/nation-state-threat-actor-mint-sandstorm-refines-tradecraft-to-attack-high-value-targets/

### MuddyWater

- **Common name(s) and aliases.** MuddyWater / MERCURY (legacy MS) / Mango Sandstorm (Microsoft) / Static Kitten (CrowdStrike) / TEMP.Zagros / Boggy Serpens / Earth Vetala / Cobalt Ulster / Yellow Nix.
- **Suspected sponsor / unit.** Iranian MOIS (subordinate); January 2022 US Cyber Command attribution naming MOIS as the sponsor and publishing samples to VirusTotal.
- **Active years.** ~2017–present.
- **Typical target sectors.** Middle East government, telecom, oil, defense — Israel, Saudi Arabia, Turkey, Iraq, Jordan, UAE; expanded to North America and Europe.
- **Signature TTPs.** Spear-phishing with malicious archives, PowerShell-based loaders (POWERSTATS), legitimate remote-management tools (ScreenConnect, Atera, AnyDesk) for persistence and C2 (T1219 Remote Access Software), credential theft and lateral movement to MFA-relay attacks.
- **Historical activation triggers.** Israel-Iran tensions and regional proxy events. Sustained activity surge after Oct 7, 2023 Hamas attacks and through 2024 Israel-Iran exchanges. Earlier surges followed the Iran-Saudi 2017 diplomatic crisis.
- **Notable named campaigns.** Continuous Israeli/Saudi/Turkish targeting (2017–present); MERCURY destructive attacks against Israeli organizations using disguised ransomware "DEV-1084" partner activity (2022); Atera/ScreenConnect campaigns (2023–2024); pre-Albania-attack reconnaissance (overlap with APT34 cluster, 2022).
- **Authoritative reference.** MITRE ATT&CK G0069 — https://attack.mitre.org/groups/G0069/ ; CISA AA22-055A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-055a

### CyberAv3ngers

- **Common name(s) and aliases.** CyberAv3ngers / Soldiers of Solomon (claimed persona) / Cyber Avengers / IRGC-CEC.
- **Suspected sponsor / unit.** IRGC-affiliated; US Treasury OFAC designated six IRGC-CEC (Cyber-Electronic Command) officials in February 2024 specifically tied to CyberAv3ngers operations.
- **Active years.** Public emergence 2020; major activity 2023–present.
- **Typical target sectors.** Water and wastewater utilities, programmable logic controllers (especially Israeli-made Unitronics Vision PLCs), industrial control systems with default or weak credentials.
- **Signature TTPs.** Direct internet-exposed PLC compromise via default credentials (T1078.001 Default Accounts), defacement of HMI screens with anti-Israel messaging (T1491 Defacement), opportunistic targeting based on supplier-country (Israeli-made equipment).
- **Historical activation triggers.** Direct response to Israel-Hamas conflict. CyberAv3ngers' Unitronics campaign began on November 25, 2023 — seven weeks after the October 7, 2023 Hamas attacks — explicitly framed as retaliation for Israeli operations in Gaza. Hits on US water utilities (Aliquippa, PA, Nov 25, 2023) selected because they used Israeli equipment.
- **Notable named campaigns.** November–December 2023 Unitronics PLC defacement campaign across multiple US water utilities; ongoing claimed disruption activities throughout 2024 against Israeli-supplier infrastructure globally.
- **Authoritative reference.** CISA AA23-335A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a ; US Treasury — https://home.treasury.gov/news/press-releases/jy2072

---

## NORTH KOREA

DPRK's offensive cyber capability is consolidated under the **Reconnaissance General Bureau (RGB)** of the Korean People's Army, with major sub-clusters Bureau 121 and Lab 110 lineage. Mission set is unique among state actors: heavy financially motivated component (sanctions evasion / regime financing) alongside espionage and disruptive operations. Microsoft uses the Sleet suffix.

### Lazarus Group

- **Common name(s) and aliases.** Lazarus Group / Hidden Cobra (US Government) / Guardians of Peace (2014 persona) / ZINC (legacy MS) / Diamond Sleet (Microsoft) / Labyrinth Chollima (CrowdStrike) / APT38 (financial sub-cluster, Mandiant).
- **Suspected sponsor / unit.** DPRK Reconnaissance General Bureau (RGB), Lab 110 / Bureau 121. US DOJ indictments of Park Jin Hyok (Sept 2018), Jon Chang Hyok and Kim Il (Feb 2021).
- **Active years.** ~2009–present.
- **Typical target sectors.** Banks (SWIFT-network targets), cryptocurrency exchanges and DeFi protocols, defense, entertainment, aerospace, journalists, cryptocurrency engineers via fake recruitment.
- **Signature TTPs.** Strategic destructive wipers, SWIFT-message manipulation, Operation Dream Job fake-recruiter LinkedIn campaigns, cryptocurrency-exchange compromise via supply chain and trading-software trojans, custom implants (Manuscrypt, BLINDINGCAN, COPPERHEDGE).
- **Historical activation triggers.** Symbolic political events (Sony hack tied to "The Interview" theatrical release Dec 2014); regime financing pressure cycles correlated with sanctions; major cryptocurrency price moves trigger waves of exchange targeting. Bybit $1.5B theft (Feb 2025) followed sanctions tightening in late 2024.
- **Notable named campaigns.** Sony Pictures (Nov 2014); Bangladesh Bank SWIFT heist (Feb 2016, $81M); WannaCry (May 2017); Ronin Bridge / Axie Infinity ($625M, March 2022); Harmony Horizon Bridge ($100M, June 2022); Atomic Wallet (June 2023); Bybit ($1.5B, February 2025 — largest crypto theft on record).
- **Authoritative reference.** MITRE ATT&CK G0032 — https://attack.mitre.org/groups/G0032/ ; CISA Hidden Cobra — https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-239a

### Kimsuky / APT43

- **Common name(s) and aliases.** Kimsuky (Kaspersky) / APT43 (Mandiant) / Thallium (legacy MS) / Emerald Sleet (Microsoft) / Velvet Chollima (CrowdStrike) / Black Banshee / Sparkling Pisces / TA406 (Proofpoint).
- **Suspected sponsor / unit.** RGB foreign-intelligence mission. Mandiant moderate-confidence assessment (March 2023); FBI/CISA/NSA/Korean NIS joint advisory (June 2023, AA23-158A).
- **Active years.** ~2012–present.
- **Typical target sectors.** South Korean and US/Japanese think tanks, academia, journalists, government foreign-policy and nuclear-policy staff, cryptocurrency exchanges (cybercrime arm funds operations).
- **Signature TTPs.** Spear-phishing impersonating journalists/academics, credential-phishing kits, custom implants (BabyShark, AppleSeed, ReconShark), self-funding through cryptocurrency theft (juche-aligned operational model), abuse of free email/cloud services for low-cost C2.
- **Historical activation triggers.** US-South Korea-Japan trilateral meetings, North-South Korea diplomatic events, US presidential transitions (2020 transition team targeted), nuclear-policy debates. Diehl Defence (German air-defense supplier to ROK) targeted in 2024 amid Korean IRIS-T sales.
- **Notable named campaigns.** South Korean nuclear-research compromises (2014–present); 2020 US presidential transition targeting; Diehl Defence (Germany, 2024); long-running TA406 academic-impersonation operations against US/UK/EU policy researchers (2020–2025).
- **Authoritative reference.** MITRE ATT&CK G0094 — https://attack.mitre.org/groups/G0094/ ; Mandiant — https://cloud.google.com/blog/topics/threat-intelligence/apt43-north-korea-cybercrime-espionage

### Andariel

- **Common name(s) and aliases.** Andariel / Silent Chollima (CrowdStrike) / PLUTONIUM (legacy MS) / Onyx Sleet (Microsoft) / DarkSeoul / Stonefly / APT45 (Mandiant) / Operation GoldenAxe.
- **Suspected sponsor / unit.** RGB sub-organization. US DOJ indictment of Rim Jong Hyok (July 2024) named him as an Andariel/RGB hacker; US Treasury sanctions on associated entities.
- **Active years.** ~2009–present.
- **Typical target sectors.** Defense industrial base (US, ROK, India, UK, Japan), nuclear power and energy, aerospace, healthcare (ransomware against US hospitals to fund espionage); particular focus on advanced military technology including uranium-enrichment, missile, and submarine R&D.
- **Signature TTPs.** Maui ransomware (Aug 2022 advisory) used against healthcare to fund operations, custom backdoors (TigerRAT, Dtrack, Volgmer), exploitation of public-facing apps including Log4Shell and ManageEngine vulnerabilities, weaponizing access for IP theft of weapons-systems data.
- **Historical activation triggers.** DPRK weapons-program priorities and US sanctions cycles. Maui ransomware against US healthcare began at the same period as accelerated DPRK missile-test calendar (2021–2022). Andariel surge against defense contractors increased after 2022 ROK conventional-deterrence announcements.
- **Notable named campaigns.** DarkSeoul (2013, ROK banks/broadcasters); Maui ransomware against US healthcare (2021–2022); NASA, Boeing, Lockheed Martin targeting per July 2024 DOJ indictment; Operation Dream Magic against Korean defense (2023); ongoing 2024–2025 campaigns against UK/Japan defense.
- **Authoritative reference.** MITRE ATT&CK G0138 — https://attack.mitre.org/groups/G0138/ ; CISA AA22-187A (Maui) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-187a

### BlueNoroff

- **Common name(s) and aliases.** BlueNoroff (Kaspersky) / APT38 sub-cluster (Mandiant) / Stardust Chollima (CrowdStrike) / Sapphire Sleet (Microsoft) / CryptoCore / TA444 (Proofpoint) / COPERNICIUM.
- **Suspected sponsor / unit.** RGB; financial-targeting sub-cluster of broader Lazarus organization.
- **Active years.** ~2014–present.
- **Typical target sectors.** SWIFT-connected banks (early activity), cryptocurrency venture funds, DeFi protocols, NFT projects, blockchain engineers, ATM networks, foreign-currency clearing systems.
- **Signature TTPs.** Long social-engineering buildup posing as VCs/investors/recruiters, malicious investment-themed documents, custom implants (RustBucket on macOS, ObjCShellz, KANDYKORN), targeting of cryptocurrency-firm engineers' macOS workstations specifically (T1566.002).
- **Historical activation triggers.** Sanctions enforcement waves and major regime-financing pressure points. Cryptocurrency-targeting tempo accelerated after each round of US Treasury sanctions on DPRK financial conduits (notably post-2022 Tornado Cash sanctions).
- **Notable named campaigns.** Bangladesh Bank heist preparation (2015–2016, jointly with Lazarus core); Banco de Chile / NIC Asia Bank / Cosmos Bank ATM heists (2017–2018); CryptoCore exchange hits (2018–2020); 3CX supply-chain compromise (March 2023); RustBucket macOS campaign (2023); KANDYKORN against blockchain engineers (Nov 2023).
- **Authoritative reference.** MITRE ATT&CK G0082 — https://attack.mitre.org/groups/G0082/ ; Kaspersky — https://securelist.com/the-bluenoroff-cryptocurrency-hunt-is-still-on/105488/

---

## OTHER STATE SPONSORS

### APT32 / OceanLotus (Vietnam)

- **Common name(s) and aliases.** APT32 / OceanLotus (Mandiant) / Cobalt Kitty / SeaLotus / TIN WOODLAWN (SecureWorks) / BISMUTH (legacy MS) / Canvas Cyclone (Microsoft, Vietnam-suffix Cyclone).
- **Suspected sponsor / unit.** Vietnamese government-aligned, with Volexity and Mandiant assessing operational ties to Vietnam Ministry of Public Security or affiliated front companies.
- **Active years.** ~2014–present.
- **Typical target sectors.** Foreign investors in Vietnam, automotive (BMW, Hyundai targeted 2019), governments in Southeast Asia (Cambodia, Laos, Philippines), Vietnamese dissidents and journalists abroad, COVID-19 research (China, 2020).
- **Signature TTPs.** Sophisticated lure documents, custom backdoors (KerrDown, Cobalt Strike, Ratankba), watering-hole attacks on Vietnamese-language news sites, mobile-spyware activity against dissidents (overlap with Predator/Pegasus customer reporting).
- **Historical activation triggers.** Foreign-direct-investment negotiations, ASEAN summits, dissident-network mapping campaigns. Spike against Chinese government bodies during COVID-19 emergence (Jan–April 2020).
- **Notable named campaigns.** ASEAN diplomatic targeting (2017); BMW / Hyundai automotive-IP (2019); China Ministry of Emergency Management COVID-19 targeting (Q1 2020); ongoing dissident surveillance documented by Amnesty International (2020–2024).
- **Authoritative reference.** MITRE ATT&CK G0050 — https://attack.mitre.org/groups/G0050/ ; Mandiant — https://www.mandiant.com/resources/blog/cyber-espionage-apt32

### APT36 / Transparent Tribe (Pakistan)

- **Common name(s) and aliases.** APT36 / Transparent Tribe (Proofpoint) / Mythic Leopard (CrowdStrike) / ProjectM / C-Major / Earth Karkaddan (Trend Micro) / Copper Fieldstone.
- **Suspected sponsor / unit.** Pakistan-aligned; Indian CERT and multiple researchers attribute to actors operating from Pakistan with mission alignment to ISI interests.
- **Active years.** ~2013–present.
- **Typical target sectors.** Indian military, Indian government, Indian education-sector researchers with defense ties, Indian critical infrastructure, Afghan government (pre-2021).
- **Signature TTPs.** Cross-platform malware (Crimson RAT for Windows, CapraRAT for Android), spear-phishing with India-military-themed documents, spoofed Indian government web portals, watering-hole compromises.
- **Historical activation triggers.** India-Pakistan kinetic and diplomatic events. Surges before/after Pulwama-Balakot crisis (Feb 2019); Article 370 abrogation (Aug 2019); Galwan Valley clash (June 2020 — Crimson RAT activity surge documented by Cisco Talos).
- **Notable named campaigns.** Operation C-Major (2016 Indian military targeting); Operation Honey Trap fake-romance / dating-app social engineering against Indian soldiers (2018–ongoing); CapraRAT Android trojanized YouTube apps targeting India (2023); ongoing campaigns against Indian government and education sectors (2024–2025).
- **Authoritative reference.** MITRE ATT&CK G0134 — https://attack.mitre.org/groups/G0134/ ; Proofpoint — https://www.proofpoint.com/us/threat-insight/post/operation-transparent-tribe

### SideWinder (India)

- **Common name(s) and aliases.** SideWinder / Razor Tiger (CrowdStrike) / RattleSnake / T-APT-04 / APT-C-17.
- **Suspected sponsor / unit.** Indian-state-aligned; Kaspersky and Group-IB assess India-aligned with high confidence based on targeting and infrastructure overlap.
- **Active years.** ~2012–present.
- **Typical target sectors.** Pakistani military and government, Chinese government and military, Nepalese, Sri Lankan, Bangladeshi, Maldivian government targets; expanded to maritime / port / energy in Africa and SE Asia (2024).
- **Signature TTPs.** Spear-phishing with weaponized Office documents abusing template-injection (T1221) and CVE-2017-11882 equation-editor exploits, custom JavaScript stagers, nation-state-themed lures, very high operational tempo (one of the most prolific APTs by sample count).
- **Historical activation triggers.** South-Asia border events, especially LoC incidents and PRC-PAK CPEC milestones. Activity tracked closely with India-Pakistan border tensions and the 2020 Galwan India-China clash.
- **Notable named campaigns.** Continuous Pakistani-military-targeted operations (2012–present); 2020–2021 surge against Chinese military post-Galwan; expansion to maritime/nuclear targets in SE Asia and Middle East documented by Kaspersky (Oct 2024).
- **Authoritative reference.** MITRE ATT&CK G0121 — https://attack.mitre.org/groups/G0121/ ; Kaspersky — https://securelist.com/sidewinder-apt-the-never-ending-mission/114849/

### Ghostwriter / UNC1151 (Belarus)

- **Common name(s) and aliases.** Ghostwriter (Mandiant influence-operation label) / UNC1151 (Mandiant cyber cluster) / Storm-0257 (legacy MS) / TA445 (Proofpoint) / Moonscape.
- **Suspected sponsor / unit.** Belarusian government; EU Council formal attribution (Sept 2021) named UNC1151 as Belarusian-government-affiliated. US Treasury OFAC sanctioned associated entities.
- **Active years.** ~2016–present.
- **Typical target sectors.** Polish, Lithuanian, Latvian, Ukrainian, German government, military, journalists, opposition political figures; influence-operation arm pushes anti-NATO and anti-Ukraine narratives via compromised media accounts.
- **Signature TTPs.** Hybrid cyber+influence — credential phishing of journalists and politicians (T1566.002), publication of fabricated "leaks" via compromised legitimate media accounts, spear-phishing with custom HTML-smuggling stagers.
- **Historical activation triggers.** Belarusian and Russian regional pressure events. Activity surge before the 2020 Belarusian election, the 2021 Belarus-Poland border crisis (instrumentalized migration), and continuously throughout the Russian invasion of Ukraine to support Russian narratives.
- **Notable named campaigns.** Polish/Lithuanian/Latvian government targeting (2016–present); fabricated-leaks campaigns against German and Polish military officials (2020–2021); 2022 surge against Ukrainian military email accounts; continuous 2023–2025 disinformation pushed via compromised Eastern European media accounts.
- **Authoritative reference.** MITRE ATT&CK G1008 — https://attack.mitre.org/groups/G1008/ ; Mandiant — https://www.mandiant.com/resources/blog/unc1151-linked-to-belarus-government

---

## MAJOR CYBERCRIME CREWS RELEVANT TO STATE-ALIGNED ACTIVITY

These groups are not formally state-tasked but operate with permissive jurisdictions and either coordinate with, are tolerated by, or have been observed pivoting in alignment with state interests. The Russia-tolerated cluster is most consequential for Prophet's threat-timing model because Russian government enforcement against these crews tracks Russia's diplomatic posture toward the West.

### Cl0p / TA505

- **Common name(s) and aliases.** Cl0p (also stylized CL0P) / TA505 (Proofpoint) / FIN11 (Mandiant) / Lace Tempest (Microsoft) / GRACEFUL SPIDER (CrowdStrike) / Hive0065.
- **Suspected sponsor / unit.** Russian-affiliated criminal enterprise. CISA/FBI assessment in AA23-158A: "Russia-affiliated cyber gang" with no evidence of state tasking but operating from permissive jurisdiction. Six Ukrainian nationals arrested in Ukraine (June 2021) — only partial disruption.
- **Active years.** ~2014–present (TA505 lineage); Cl0p ransomware brand from 2019.
- **Typical target sectors.** Indiscriminate by sector; selects victims by exploitable managed-file-transfer (MFT) vendor exposure: Accellion FTA (2020), GoAnywhere MFT (2023), MOVEit Transfer (2023), Cleo Harmony/VLTrader (2024).
- **Signature TTPs.** Mass-exploitation of zero-day MFT vulnerabilities (T1190), exfiltration-only "data-extortion" (often without encryption deployment), LEMURLOOT and DEWMODE web shells, name-and-shame leak site.
- **Historical activation triggers.** Vendor-vulnerability discovery cycles (operates on its own zero-day pipeline rather than geopolitical events). However, the targeting impact-distribution skews heavily toward US and Western victims, consistent with Russian-tolerated criminal posture.
- **Notable named campaigns.** Accellion FTA mass-exploitation (Dec 2020–Jan 2021); GoAnywhere MFT (CVE-2023-0669, Feb 2023); MOVEit Transfer (CVE-2023-34362, May–June 2023, ~2,500+ organizations affected); Cleo MFT (CVE-2024-50623, Dec 2024).
- **Authoritative reference.** MITRE ATT&CK G0092 (TA505) — https://attack.mitre.org/groups/G0092/ ; CISA AA23-158A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a

### LockBit

- **Common name(s) and aliases.** LockBit / LockBit 2.0 / LockBit 3.0 (Black) / LockBit Green / Bitwise Spider (CrowdStrike).
- **Suspected sponsor / unit.** Russia-tolerated criminal RaaS; primary administrator "LockBitSupp" identified by US/UK/Australia in May 2024 as Dmitry Khoroshev (Russian national) — sanctioned and indicted but not extradited.
- **Active years.** September 2019–present (substantially disrupted; rebuild ongoing).
- **Typical target sectors.** Indiscriminate — accounted for ~25% of global ransomware attacks 2022–2023; affiliates targeted manufacturing, healthcare, government, education, financial services, professional services across all geographies.
- **Signature TTPs.** Ransomware-as-a-Service affiliate model with self-spreading lockers, double-extortion leak site, exploitation of Citrix Bleed and other edge-device vulnerabilities (T1190), competitive recruitment offering highest affiliate commission share.
- **Historical activation triggers.** Operates continuously; attack tempo is more affiliate-driven than geopolitical. However, Russian internal enforcement against LockBit visibly absent — consistent with Russia-tolerated criminal posture used as deniable pressure.
- **Notable named campaigns.** Royal Mail UK (Jan 2023); ICBC Financial Services (Nov 2023); Boeing (Oct–Nov 2023); UK Ministry of Defence payroll contractor (May 2024); Operation Cronos disruption by NCA / FBI / Europol / 10-country task force (Feb 19–20, 2024) — 34 servers seized, 200+ crypto wallets frozen, 1,000+ decryption keys recovered. Group rebuilt within days but at significantly reduced operational capacity through 2025.
- **Authoritative reference.** CISA AA23-165A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-165a ; NCA Operation Cronos — https://www.nationalcrimeagency.gov.uk/the-nca-announces-the-disruption-of-lockbit-with-operation-cronos

### Conti / TrickBot Remnants

- **Common name(s) and aliases.** Conti / WIZARD SPIDER (CrowdStrike) / TrickBot operators / Ryuk lineage / GOLD ULRICK / ITG23 (IBM X-Force) / FIN12 (related cluster).
- **Suspected sponsor / unit.** Russian-tolerated criminal organization with documented FSB liaison ties exposed in the February 2022 "ContiLeaks" Jabber chat dump. US Treasury sanctioned seven Trickbot/Conti members in February 2023 and an additional 11 in September 2023 in coordination with UK NCA.
- **Active years.** Conti brand 2020–May 2022 (formal shutdown); members rebadged into Black Basta, BlackByte, Karakurt, Royal/Blacksuit, Quantum.
- **Typical target sectors.** Healthcare (notable Ireland HSE attack, May 2021), local governments, manufacturing, professional services. Internal Conti policy explicitly excluded targeting Russia and CIS countries.
- **Signature TTPs.** TrickBot/BazarLoader email-loader access broker pipeline, Cobalt Strike post-exploitation, Conti ransomware double-extortion. Internal corporate-style structure (HR, payroll, R&D) revealed by ContiLeaks.
- **Historical activation triggers.** Russia-aligned political stance — Conti issued a public statement supporting the Russian government within days of the February 2022 invasion of Ukraine; this triggered the ContiLeaks insider dump and accelerated the brand's wind-down. The brand's dissolution was strategic (avoid sanctions) rather than disruption-induced.
- **Notable named campaigns.** Ireland Health Service Executive (May 2021, ~$100M recovery cost); Costa Rica government (April 2022, declared national emergency); Conti shutdown announcement (May 2022); Trickbot/Conti sanctions and indictments (Feb 2023, Sep 2023).
- **Authoritative reference.** MITRE ATT&CK G0102 (Wizard Spider) — https://attack.mitre.org/groups/G0102/ ; CISA AA21-265A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-265a

### Black Basta

- **Common name(s) and aliases.** Black Basta / BlackBasta / Storm-0506 (legacy MS) / UNC4393 (Mandiant).
- **Suspected sponsor / unit.** Russian-tolerated criminal RaaS; Conti-lineage successor. Trellix and Intel 471 analysis of February 2025 internal-chat leak identified leader "GG"/"Tramp"/"AA" as Russian national Oleg Nefedov, with the leak suggesting Russian authority facilitation (June 2024 Armenia detention followed by "green corridor" exfiltration to Russia).
- **Active years.** April 2022 – approximately January 2025 (operations ceased; EU Most Wanted listing of leader added January 2026).
- **Typical target sectors.** Healthcare (US hospitals), critical manufacturing, financial services, construction, MSPs. Frequently selected high-impact-on-services US targets.
- **Signature TTPs.** Initial access via Qakbot / DarkGate / phishing-as-a-service, Cobalt Strike + Brute Ratel post-exploitation, ESXi-targeting Linux variant, double-extortion. Internal chats showed development goals to rebuild on Conti source code.
- **Historical activation triggers.** Operated continuously through Russia-Ukraine war period; chat leaks indicated leadership coordinated with Russian authorities for member protection. Activity tempo correlated with Conti-alumni resource flow rather than geopolitical events.
- **Notable named campaigns.** Ascension Health (May 2024, ~140 hospitals affected); Capita UK (March 2023); ABB industrial automation (May 2023); Synlab Italia (April 2024). Operations-effective end January 11, 2025; INTERPOL Red Notice and EU Most Wanted on leader Jan 2026.
- **Authoritative reference.** CISA AA24-131A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-131a ; Trellix Black Basta chat leak analysis — https://www.trellix.com/blogs/research/analysis-of-black-basta-ransomware-chat-leaks/

### Scattered Spider / 0ktapus

- **Common name(s) and aliases.** Scattered Spider (CrowdStrike) / 0ktapus (Group-IB) / UNC3944 (Mandiant) / Octo Tempest (Microsoft) / Scatter Swine (Okta) / Muddled Libra (Unit 42) / Star Fraud / Roasted 0ktapus.
- **Suspected sponsor / unit.** Anglophone (US/UK) cybercriminal collective from "The Com" loose-affiliate ecosystem; not state-affiliated. Five US/UK arrests in November 2024 (DOJ unsealed indictment of California, Florida, Texas, North Carolina, and UK defendants).
- **Active years.** ~2022–present.
- **Typical target sectors.** SaaS-heavy enterprises — telecommunications, BPO, financial services, hospitality (casino/hotel operators), retail, technology. Pivoted to BlackCat/ALPHV and then Akira/RansomHub ransomware affiliations.
- **Signature TTPs.** Help-desk social engineering for MFA reset (T1556), SIM swapping, identity-provider abuse (especially Okta), legitimate remote-access tools, native English speakers conducting voice phishing — distinguishing them from Russian-speaking criminal crews.
- **Historical activation triggers.** Opportunity-driven (vulnerable SaaS configurations); not geopolitically activated. However, the November 2024 arrests have not curtailed activity from remaining members and adjacent Com-ecosystem actors.
- **Notable named campaigns.** Twilio / Okta supply-chain phishing (Aug 2022, ~130 organizations); MGM Resorts (Sept 2023); Caesars Entertainment (Sept 2023, $15M ransom paid); Clorox (Aug 2023); Transport for London (Sept 2024); Snowflake-customer extortion campaign (May–July 2024, including Ticketmaster, AT&T, Santander).
- **Authoritative reference.** MITRE ATT&CK G1015 — https://attack.mitre.org/groups/G1015/ ; CISA AA23-320A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a

### Akira

- **Common name(s) and aliases.** Akira / Storm-1567 (legacy MS) / Howling Scorpius (Unit 42) / Punk Spider (operating partner overlap with Scattered Spider).
- **Suspected sponsor / unit.** Russian-tolerated criminal RaaS with operational ties to former Conti members (per Arctic Wolf and Chainalysis blockchain analysis showing wallet overlaps with Conti).
- **Active years.** March 2023–present.
- **Typical target sectors.** Mid-market enterprises across manufacturing, education, financial services, real estate, healthcare, professional services; strong SonicWall and Cisco ASA SSL-VPN exploitation pattern targeting victims with weak MFA on edge devices.
- **Signature TTPs.** Initial access via vulnerable VPN appliances (CVE-2023-20269 Cisco, CVE-2024-40766 SonicWall, CVE-2024-37085 ESXi), double-extortion with retro 1980s-style leak site, Linux/ESXi encryption variant, occasionally negotiates substantially in chat.
- **Historical activation triggers.** Vendor-vulnerability cycles; Akira tempo is highly correlated with disclosure of new VPN-appliance N-days. Surge in late 2024 after CVE-2024-40766 SonicWall MFA-bypass disclosure.
- **Notable named campaigns.** Stanford University (2023); Nissan Australia (Dec 2023); Hitachi Vantara (Apr 2024); BL Companies / various engineering firms (2024); ongoing high-volume mid-market campaign through 2025 targeting SonicWall-VPN-exposed organizations.
- **Authoritative reference.** CISA AA24-109A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-109a ; Arctic Wolf Akira — https://arcticwolf.com/resources/blog/conti-and-akira-chained-together/

---

## Notes for downstream pattern-matching

- **Sponsor-attribution citations.** Every group above has at least one US-government, allied-government, or major-vendor primary attribution source. For prediction purposes, treat MITRE ATT&CK G-numbers as the primary key; alias mappings live in the "aliases" line of each entry.
- **Triggering-event ontology.** Recurring trigger categories observed across this catalog: (1) sanctions packages, (2) elections in target countries, (3) military operations or kinetic exchanges, (4) diplomatic summits (especially when adversary leader is meeting with target government), (5) indictments of named officers, (6) infrastructure-takedown / disruption events, (7) symbolic political dates (anniversary attacks), (8) major sporting events with state-political weight, (9) vendor-vulnerability disclosure for the cybercrime crews. Prophet's pattern-matcher should treat these nine categories as the primary feature-space dimensions when scoring "who would activate now."
- **Attribution confidence levels.** Russia GRU and DPRK RGB groups have the strongest formal-indictment attribution. China MSS attribution is increasingly formalized (i-Soon leak 2024, Salt Typhoon multi-country statement 2025). Iran groups have somewhat lower public-evidence density. Cybercrime-group "tolerance by state" attributions are inferential — based on enforcement absence rather than positive evidence.
