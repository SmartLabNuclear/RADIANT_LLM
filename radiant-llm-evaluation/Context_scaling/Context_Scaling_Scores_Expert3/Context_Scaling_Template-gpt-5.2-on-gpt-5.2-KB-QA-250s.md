# Context Scaling Scoring Template
# Benchmark Family: Context Expansion

## Standardized Metric Definitions

- Context Precision (CoP):
  $CoP_i = CoP_{N,i}$ if $CoP_{S,i}$ is undefined; $CoP_i = CoP_{S,i}$ if $CoP_{N,i}$ is undefined; otherwise $CoP_i = \alpha CoP_{S,i} + (1-\alpha) CoP_{N,i}$.
  - Constraint: $CoP_{S,i} \in \{0, 0.25, 0.5, 0.75, 1\}$.

  | CoP_S score | Interpretation |
  | --- | --- |
  | 0 | incorrect |
  | 0.25 | minimally correct |
  | 0.5 | partially correct |
  | 0.75 | mostly correct |
  | 1 | fully correct |
- Citation Precision (CiP):
  $CiP_i = \frac{\text{number of valid citations in } C_i}{\max(|C_i|, 1)}$.
  - Note: A citation is valid when it identifies supporting evidence at the correct evidence item; for figure/table/section queries, exact page-string equality is not required if the document and figure/table/section identity are correct and unambiguous.
  - Constraint: $0 \le CiP_i \le 1$.

- Citation Hit (CiH):
  $CiH_i = 1$ if at least one citation in $C_i$ refers to a canonical evidence item in $E_i^*$ by evidence identity; else $0$.
  - Note: For figure/table/section queries, a correct evidence identifier counts as a hit even when the printed/software page locator is omitted or offset.
  - Constraint: $CiH_i \in \{0, 1\}$.

- Hallucination Rate (HR):
  $HR_i = \frac{|K_{unsupported}|}{|K_{generated}|}$.
  - Constraint: $0 \le HR_i \le 1$.

- Visual Recall (ViR):
  $ViR_i = \frac{|F_i \cap F_i^*|}{|F_i^*|}$.
  - Constraint: $0 \le ViR_i \le 1$.
## Scoring Template
- **Vision Language Model (VLM) used to parse the Knowledge Base (KB)**: GPT-5.2
- **LLM Model used in RAG**: GPT-5.2
- **KB Condition**: 250-source KB (`250s`)
- **Total Queries**: 30
- **Initial setup prompt**: For the the questions I will be asking, Do NOT cite any web sources. ONLY focus on the pdf(s) in the working directory? ok?

### Q1
- Query: Within the discussion of safety, security, and safeguards interfaces, which operational functions are described as being shared across all three domains, and how is this represented in the associated domain-interface schematic?

- GT

```text
GT Condensed
- Shared across safety–security–safeguards: "Detection, Monitoring, MAAs, VAs, Operational Safety, Locks & Keys"
- Shown in the central 3-way overlap of the Venn diagram, with a callout listing the shared functions
GT Sets
- E*:
  - 1167010.pdf, Page: 24 (software) or 18 (printed), Figure: 1
- F*
  - Detection
  - Monitoring
  - MAAs
  - VAs
  - Operational safety
  - Locks & keys
  - central three-way overlap (Safety ∩ Security ∩ Safeguards)
```

- Model Answer

```text
Operational functions shared across safety, security, and safeguards
In the safety–security–safeguards interface discussion, the functions indicated as shared across all three domains (i.e., common/overlapping operational functions) are:
•    Detection
•    Monitoring
•    MAAs (Material Balance Areas)
•    VAs (Vital Areas)
•    Operational Safety
•    Locks & Keys
These appear together as the cross-domain shared set in the schematic’s shared-overlap callout.
Citation: (1167010.pdf, p. 24, Figure 1: “Safety, Security, and Safeguards Interfaces”)
How this is represented in the domain-interface schematic
The associated schematic (Figure 1: Safety, Security, and Safeguards Interfaces) is drawn as a three-circle Venn diagram with the three domains (Safety, Security, Safeguards) and callout boxes that point into the overlap regions.
•    The shared/across-all-domains operational functions are shown in a callout box pointing to the central/common overlap relationship, listing:
“Detection, Monitoring, MAAs, VAs, Operational Safety, Locks & Keys.”
Citation: (1167010.pdf, p. 24, Figure 1)
Additionally, the diagram uses other callouts to show pairwise overlaps (e.g., Safety∩Security, Safety∩Safeguards, Safeguards∩Security), but the explicit “shared across all three” set is the one listed above in the shared-overlap callout.
Citation: (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Central shared list largely matches GT but expands MAAs as “Material Balance Areas” (wrong for this schematic—GT uses Material Access Areas); otherwise overlap description sound.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.1
- ViR: 0.9
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.1
- ViR: 0.9
```
### Q2
- Query: How are the roles of safety, security, and safeguards distinguished in domain-interface schematics, and what primary objective is associated with each domain as conveyed by the visual and accompanying labels?

- GT

```text
GT Condensed
- "safety objective: Protection of health; safety of the public and environment"
- "security objective: Protect against sabotage, malicious acts, and external attacks"
- "safeguards objective: Deter theft, misuse, diversion"
- Distinguished as three labeled domains with overlaps showing interfaces/shared responsibilities
GT Sets
- E*:
  - 1167010.pdf, Page: 24 (software) or 18 (printed), Figure: 1
- F*
  - "safety objective: Protection of Health, Safety of the Public and Environment"
  - "security objective: Protect Against, Sabotage, Malicious Acts and External Attacks"
  - "safeguards objective: Deter, Theft, Misuse, Diversion"
  - three distinct domains (Safety/Security/Safeguards) + overlaps
```

- Model Answer

```text
In the domain-interface schematics (shown as a three-circle Venn diagram), Safety, Security, and Safeguards are distinguished by (1) separate labeled circles for each domain and (2) domain-specific “objective” text placed with/inside each circle, with additional callout boxes used to annotate overlaps.
How the roles are distinguished visually
•    Three distinct circles labeled Safety, Security, and Safeguards communicate that these are separate operational/regulatory domains.
•    Each circle includes an explicit objective statement that defines the domain’s primary role.
•    The overlap regions (pairwise and three-way) are emphasized with callout boxes listing interface/shared functions (e.g., monitoring, detection, access control), showing where responsibilities and measures intersect across domains.
Citation: (1167010.pdf, p. 24, Figure 1: “Safety, Security, and Safeguards Interfaces”)
Primary objective associated with each domain (as labeled in the schematic)
•    Safety objective: “Protection of Health, Safety of the Public and Environment.”
Citation: (1167010.pdf, p. 24, Figure 1)
•    Security objective: “Protect Against, Sabotage, Malicious Acts and External Attacks.”
Citation: (1167010.pdf, p. 24, Figure 1)
•    Safeguards objective: “Deter, Theft, Misuse” and “Diversion.”
Citation: (1167010.pdf, p. 24, Figure 1)
These objective labels are the schematic’s main mechanism for distinguishing what each domain is fundamentally trying to achieve, while the overlaps and callouts show where design/operational measures can serve multiple objectives at once.
```

- Scores

```text
Metric Work
- Notes: Objectives and overlap logic match Figure 1 / GT; citations on Figure 1 p24.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```

### Q3
- Query: Which systems or operational functions facilitate interaction between the safeguards and security domains, and how are these functions presented as supporting both objectives within interface schematics?

- GT

```text
GT Condensed
- "safeguards–security interface functions include: Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys"
- Presented in the overlap region between Safeguards and Security in the schematic
- Overlap placement indicates the same functions support both safeguards and security objectives
GT Sets
- E*:
  - 1167010.pdf, Page: 24 (software) or 18 (printed), Figure: 1
- F*
  - Access control
  - Detection
  - Monitoring
  - Alarms
  - Surveillance
  - MAAs
  - VAs
  - Locks & keys
  - placed in Safeguards ∩ Security overlap
```

- Model Answer

```text
Systems / operational functions at the Safeguards–Security interface
The interface schematic identifies the following functions as facilitating interaction between the safeguards and security domains:
•    Access Control
•    Detection
•    Monitoring
•    Alarms
•    Surveillance
•    MAAs (Material Balance Areas)
•    VAs (Vital Areas)
•    Locks & Keys
Citation: (1167010.pdf, p. 24, Figure 1 “Safety, Security, and Safeguards Interfaces”)
How the schematic shows these as supporting both objectives
In the interface schematic (a three-domain Venn-style diagram), these functions are presented in a callout box that is explicitly associated with the Safeguards ∩ Security overlap. The figure uses a bottom-center red callout box listing the functions, and a vertical arrow pointing from the box into the shared overlap region between the Safeguards and Security circlesâ€”visually indicating these measures contribute to both domains’ objectives simultaneously.
Citation: (1167010.pdf, p. 24, Figure 1 “Safety, Security, and Safeguards Interfaces”)
```

- Scores

```text
Metric Work
- Notes: Safeguards∩Security list and overlap interpretation match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```

### Q4
- Query: Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility, which regulatory frameworks are identified as governing physical protection and material control and accounting?

- GT

```text
GT Condensed
- Physical protection governed by 10 CFR Part 73
- Material Control & Accounting governed by 10 CFR Part 74
GT Sets
- E*:
  - 1167010.pdf, p.13 (software) or 7 (printed), Section 3.1
  - 1167010.pdf, p.13 (software) or 7 (printed), Section 3.2
- F*: []
```

- Model Answer

```text
Within the discussion of integrating safeguards and security into the design of a Used Nuclear Fuel Storage Facility (UNFSF), the governing U.S. regulatory frameworks are identified as:
Physical protection (Security)
•    10 CFR Part 73 (physical protection requirements), with the integration framework explicitly building from the NRC’s existing safety/security interface approach, citing 10 CFR 73.58 and NRC Regulatory Guide 5.73 as the basis used for integration.
Citations: (1167010.pdf, p. 6, discussion of UNFSF design framework building on NRC safety/security interface: “10 CFR 73.58” and “Regulatory Guide 5.73”); (1167010.pdf, p. 10, discussion noting physical protection requirements in “10 CFR Part 73”)
Material control and accounting (MC&A) (Safeguards-related)
•    10 CFR Part 74 (“Material Control and Accounting”), presented as the primary regulatory basis for MC&A in the safeguards/security-by-design context.
Citation: (1167010.pdf, p. 10, discussion/figure context identifying MC&A requirements in “10 CFR Part 74”)
```

- Scores

```text
Metric Work
- Notes: Part 73 / Part 74 correct with 1167010 cites; extra RG/CFR detail slightly beyond minimal GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.85
- CiH: 1
- HR: 0.1
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.85
- CiH: 1
- HR: 0.1
- ViR: 1
```

### Q5
- Query: Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility, what performance goal/objective is associated with each regulatory framework governing physical protection and material control and accounting?

- GT

```text
GT Condensed
- "10 CFR 73 objective: early security design features; protect against theft/diversion and radiological sabotage"
- "10 CFR 74 objective: early safeguards/MC&A features; deter, prevent, detect loss, theft, diversion, unauthorized production"
GT Sets
- E*:
  - 1167010.pdf, Section 3.1.1, p.13 (software) or 7 (printed)
  - 1167010.pdf, Section 3.1.2, p.13 (software) or 7 (printed)
- F*: []
```

- Model Answer

```text
Performance goal/objective by regulatory framework (used nuclear fuel storage facility context)
Season (meteorological, Northern Hemisphere): Winter
Regulatory framework (domain)    Performance goal / objective associated with the framework (as stated in the local KB discussion)
10 CFR Part 73 (Physical protection / physical security)    Ensure the facility’s physical protection system can defend against the Design Basis Threat (DBT) and includes measures to protect against radiological sabotage and prevent theft or diversion of special nuclear material (SNM). (1897829.pdf, p. 29; 1897829.pdf, p. 87; 1906501.pdf, p. 66)
10 CFR Part 74 (Material Control & Accountingâ€”MC&A)    Detect diversion of fissile (special nuclear) material through MC&A (with the discussion noting the MC&A objective is centered on diversion detection, e.g., via item accounting approaches for discrete items). (1886489.pdf, p. 18–19; 1896981.pdf, p. 40)
Notes/limits from the local knowledge base
•    The retrieved local excerpts clearly link Part 73 to DBT-based protection against radiological sabotage and theft/diversion, and link Part 74 to diversion detection via MC&A. However, the available excerpts did not provide more granular, numeric “performance goals” (e.g., specific detection timeliness thresholds) for a used fuel storage facility beyond those stated objectives. (1897829.pdf, p. 29 & p. 87; 1886489.pdf, p. 18–19)
```

- Scores

```text
Metric Work
- Notes: Winter table noise; objectives pulled from generic DBT/MC&A PDFs vs 1167010 Section 3.1.1–3.1.2 early-integration wording in GT.
- CoP
  - CoP_S: 0.5
  - CoP_N:
- CiP: 0.2
- CiH: 0
- HR: 0.45
- ViR: 0.85
Scores
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- CiP: 0.2
- CiH: 0
- HR: 0.45
- ViR: 0.85
```
### Q6
- Query: What facility system is identified as having dual safeguards and security functions suitable for early integration into the design of a used nuclear fuel storage facility?

- GT

```text
GT Condensed
- Exit and Entry Control System for Protected Areas selected
- It serves Protected Areas (PAs), Vital Areas (VAs), and Material Access Areas (MAAs)
GT Sets
- E*:
  - 1167010.pdf, p.13 (software) or 7 (printed), Section 3.1, Section 3.2
- F*: []
```

- Model Answer

```text
The facility system identified as having dual safeguards and security functions (and therefore suitable for early integration into a used nuclear fuel storage facility design) is a:
•    Gate monitor systemâ€”described in the source as including a coincident neutron counter and an ion fission chamber, along with boundary alarms to support site security and safeguards functions.
Citation: (1644065.pdf, p. 10)
```

- Scores

```text
Metric Work
- Notes: Names gate monitor / wrong facility excerpt vs GT Exit and Entry Control System for Protected Areas; wrong PDF (1644065).
- CoP
  - CoP_S: 0
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.1
- ViR: 0
Scores
- CoP_S: 0
- CoP_N:
- CoP: 0
- CiP: 0
- CiH: 0
- HR: 0.1
- ViR: 0
```

### Q7
- Query: What criteria or regulatory considerations justify the selection of a system as having dual safeguards and security functions for early integration into the design of a used nuclear fuel storage facility?

- GT

```text
GT Condensed
- Selection of a dual-function system is justified by overlapping safeguards and security requirements
- Applicable regulatory guides are reviewed to derive functional design criteria and requirements
- NRC Regulatory Guide 5.53 provides applicability guidance for safeguards and security at an Independent Spent Fuel Storage Installation
GT Sets
- E*:
  - 1167010.pdf, p.13 (software) or 7 (printed), Section 3.1, Section 3.2
  - 1167010.pdf, P2, Reference 6 (NRC Regulatory Guide 5.53)
- F*: []
```

- Model Answer

```text
The discussion justifies selecting a facility system as having dual safeguards and security functions (and thus suitable for early integration into a used nuclear fuel storage facility / ISFSI design) based on a regulation- and guidance-driven functional requirements review, specifically:
1.    Start from the applicable NRC regulatory basis for ISFSI design/licensing/operation, then derive functional design criteria
o    The approach described is to identify the regulatory guides applicable to ISFSI design, licensing, and operation, and then evaluate those guides to define the functional design criteria and design requirements for both safeguards and security systems.
Citation: (1167010.pdf, p. 13)
2.    Select candidate “dual-function” systems that satisfy safeguards + security requirements simultaneously
o    From that regulatory/functional assessment, an example system area highlighted for meeting both domains is protected-area entry/exit control (i.e., an “Exit and Entry Control System for Protected Areas”), which inherently serves security access control needs while also supporting safeguards-relevant control/monitoring functions at facility boundaries.
Citation: (1167010.pdf, p. 13)
3.    Use an established NRC integration framework for early incorporation
o    The early-integration concept is described as building on the NRC’s safety/security interface approach, specifically referencing 10 CFR 73.58 and Regulatory Guide 5.73 as the framework basis for integrating these considerations into design.
Citation: (1167010.pdf, p. 6)
Important limitation (from the local KB evidence retrieved)
The retrieved passages supporting the above justification do not provide additional, more granular “screening criteria” (e.g., explicit thresholds, selection metrics, or a direct linkage to specific MC&A citations such as 10 CFR Part 74 in the same excerpt). They describe the justification at the level of regulatory-guide identification → functional requirement derivation → selection of protected-area entry/exit control as a dual-function example.
Citations: (1167010.pdf, pp. 6, 13)
```

- Scores

```text
Metric Work
- Notes: Guide-driven criteria and Exit/Entry protected-area example match GT; RG 5.53 not named explicitly.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 0.85
- CiH: 1
- HR: 0.15
- ViR: 0.92
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 0.85
- CiH: 1
- HR: 0.15
- ViR: 0.92
```

### Q8
- Query: Which four elements define the scope of the application of the framework for integrating safeguards and security into the design of the UNFSF?

- GT

```text
GT Condensed
- Develop goals, criteria, requirements
- Identify methods and trade studies
- Describe performance assessment process
- Highlight benefits of early integration
GT Sets
- E*:
  - 1167010.pdf, Section 3, p.13 (software) or 7 (printed), Section 3.1
- F*: []
```

- Model Answer

```text
The framework’s scope of application for integrating safeguards and security into the design of a Used Nuclear Fuel Storage Facility (UNFSF) is defined by four elements:
1.    Identification of applicable regulatory requirements
2.    Selection of a common system that shares dual safeguards and security functions
3.    Development of functional design criteria and design requirements for the selected system
4.    Identification and integration of the dual safeguards and security design requirements
Citation: (1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Four “scope” bullets are regulatory-framework / dual-requirements framing, not GT’s four scope elements (goals/criteria/requirements; methods/trades; performance assessment; benefits).
- CoP
  - CoP_S: 0.25
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.2
- ViR: 0.35
Scores
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- CiP: 1
- CiH: 1
- HR: 0.2
- ViR: 0.35
```

### Q9
- Query: According to the design requirements for SNM doorway monitors in the UNFSF, what minimum quantity of plutonium-239 must be detectable, under what shielding condition, and at what confidence level?

- GT

```text
GT Condensed
- Detect 0.5 g Pu-239 in 3 mm brass at 90% confidence with <0.1% false alarms
GT Sets
- E*:
  - 1167010.pdf, Section 3.3.2, Pages: 15–16 (software) or 9-10 (printed)
- F*: []
```

- Model Answer

```text
For SNM doorway monitors in the UNFSF design requirements, the minimum detectable plutonium-239 quantity is:
•    Minimum quantity: 0.5 gram of Pu 239
•    Shielding condition: encased in at least 3 mm of brass
•    Confidence level: 90% confidence limit
Citation: (1167010.pdf, p. 16, excerpted design requirements discussion citing NRC Regulatory Guide 5.27 doorway monitor performance criteria for plutonium)
```

- Scores

```text
Metric Work
- Notes: 0.5 g / 3 mm brass / 90% correct; omits paired <0.1% false-alarm requirement in same GT bullet.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```

### Q10
- Query: What maximum false alarm rate is specified for SNM doorway monitors used to detect special nuclear material, as described in the design requirements of the UNFSF?

- GT

```text
GT Condensed
- False alarm rate less than 0.1% for all SNM (Pu-239, U-233, U-232, and U-235)
GT Sets
- E*:
  - 1167010.pdf, p15–17 (software) or 9-11 (printed), Section 3.3.2
- F*: []
```

- Model Answer

```text
The UNFSF design-requirements discussion for SNM doorway monitors does not provide a numerical maximum false alarm rate. Instead, it states only that doorway monitors should maintain a “low false alarm rate” (without specifying a quantified limit such as alarms per passage/hour/day) while maintaining high detection reliability.
Citation: (1167010.pdf, p. 16, discussion referencing NRC Regulatory Guide 5.27 doorway monitor “typical design requirements” and noting the need for a “low false alarm rate”)
Note on how to obtain the numeric value (if needed)
If you need the specific maximum false alarm rate, it is likely specified in NRC Regulatory Guide 5.27 itself (or an associated standard), but that numeric criterion is not included in the UNFSF excerpt available in the current local knowledge base retrieval. To answer quantitatively using only local sources, RG 5.27 would need to be available in the local KB (or you can point me to where it is stored locally).
```

- Scores

```text
Metric Work
- Notes: Denies numeric false-alarm cap; GT requires <0.1% in 1167010 Section 3.3.2—material factual miss.
- CoP
  - CoP_S: 0
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.25
- ViR: 1
Scores
- CoP_S: 0
- CoP_N:
- CoP: 0
- CiP: 1
- CiH: 1
- HR: 0.25
- ViR: 1
```

### Q11
- Query: What minimum quantity of uranium-233 must a doorway monitor be capable of detecting, within what time window, and under what shielding conditions according to the specified design requirements in the design of the UNFSF?

- GT

```text
GT Condensed
- Detect 1 g U-233
- Within 4 hours of decay product removal
- Encased in 3 mm brass
GT Sets
- E*:
  - 1167010.pdf p16 Section 3.3.2, p15–17 (software) or 9-11 (printed)
- F*: []
```

- Model Answer

```text
According to the UNFSF doorway-monitor design requirements, the doorway monitor must be capable of detecting:
•    Minimum quantity (U 233): 1 gram of U 233 (containing 7–10 ppm of U 232)
•    Time window condition: within 4 hours of removal of all decay products
•    Shielding condition: encased in at least 3 mm of brass
Citation: (1167010.pdf, p. 16, UNFSF design requirements discussion for SNM doorway monitors; U 233 detection performance requirement)
```

- Scores

```text
Metric Work
- Notes: 1 g U-233, 4 h after decay-product removal, 3 mm brass match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```

### Q12
- Query: What minimum detection effectiveness and false alarm thresholds are specified for metal and explosive detectors in the design of the UNFSF, including the minimum detectable explosive mass and required detection probability?

- GT

```text
GT Condensed
- Metal detection ≥85%
- Metal false alarm ≤10%
- Explosive detection ≥200 g
- Explosive detection ≥90%
- Explosive false alarm ≤1%
GT Sets
- E*:
  - 1167010.pdf p17–18 (software) or 11-13 (printed) Section 3.3.3
- F*: []
```

- Model Answer

```text
Within the UNFSF design requirements, the following minimum detection effectiveness and maximum false alarm thresholds are specified for metal (firearm) detectors and explosive detectors, including the minimum detectable explosive mass and required detection probability:
1) Metal (firearm) detectors (handheld or portal)
•    Minimum detection effectiveness: ≥ 85% effective detection rate
•    Maximum false alarm rate: ≤ 10% (at the sensitivity setting achieving the required detection level)
Citation: (1167010.pdf, p. 18, design requirements text for firearm/metal detectorsâ€”effective detection rate and false alarm constraint)
2) Explosive detectors (handheld or portal)
•    Minimum detectable explosive mass: 200 grams (for “dynamite, TNT, and similar nitrogen-containing compounds”)
•    Required detection probability / effectiveness: ≥ 90% effective detection rate
•    Maximum false alarm rate: ≤ 1% (when sensitivity is adjusted to the required detection level)
Citations: (1167010.pdf, p. 17, design requirements text for explosive detectorsâ€”200 g minimum and ≥90% detection effectiveness); (1167010.pdf, p. 18, design requirements text for explosive detectorsâ€”false alarm rate ≤1%)
```

- Scores

```text
Metric Work
- Notes: Metal ≥85%/≤10% FA; explosive ≥200 g, ≥90%, ≤1% FA match GT; clean answer boundary.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 1
```

### Q13
- Query: In the design of the UNFSF, what happens on the YES path and what happens on the NO paths in Figure 4, after the "Performance Assessment" decision node?

- GT

```text
GT Condensed
- YES path: proceeds to "Final Design Optimized and Harmonized"
- NO paths: loop back to Final Design for further iteration
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p21 (software) or p27 (printed)
- F*:
  - Performance Assessment decision node
  - YES path to Final Design Optimized and Harmonized
  - NO paths returning to Final Design
```

- Model Answer

```text
In Figure 4 (UNFSF design flow), after the “Performance Assessment” decision node:

- YES path: proceeds to “Final Design Optimized and Harmonized.”
- Source: *(1167010.pdf, p. 27, Figure 4)*

- NO path(s): loops back to “Final Design” for iteration (both NO branches shown return to the Final Design step).
- Source: *(1167010.pdf, p. 27, Figure 4)*
```

- Scores

```text
Metric Work
- Notes: YES → Final Design Optimized and Harmonized; NO → Final Design loop matches Figure 4 / GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q14
- Query: In Figure 1 of the UNFSF 3S interface schematic, which callout box contains "Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys," and to what overlap region does its arrow point?

- GT

```text
GT Condensed
- The callout box is the bottom-center red rounded-rectangle (safeguards-security interface) callout
- Its arrow points to the Safeguards ∩ Security overlap region
GT Sets
- E*:
  - 1167010.pdf, Figure 1, p24 (software) or p18 (printed)
- F*:
  - callout text with Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys
  - arrow to Safeguards ∩ Security overlap
```

- Model Answer

```text
In Figure 1 (UNFSF 3S interface schematic), the text “Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys” appears in the bottom-center red callout box. Its arrow points into the Safeguards ∩ Security overlap region (the lower central intersection of those two circles in the Venn diagram).

Source: (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Bottom-center red callout and arrow to Safeguards∩Security match F* / GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q15
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, what text appears in the orange box feeding into "Design Security System," and what is emphasized inside the green "Design Certification" oval?

- GT

```text
GT Condensed
- Orange box text: "High Assurance–DBT" and "Mitigation Measures"
- Design Certification oval emphasizes: "Delay"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - orange box feeding into Design Security System
  - green Design Certification oval
  - Delay
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic):

- The orange box feeding into “Design Security System” contains the text:
“High Assurance – DBT” and “Mitigation Measures.”

- Inside the green “Design Certification” oval, the diagram emphasizes:
“Emphasis on: Delay.”

Source: (1167010.pdf, p. 25–26, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Orange box (High Assurance–DBT, Mitigation Measures) and Design Certification emphasis on Delay match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q16
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, what decision step appears immediately after "Design Security System"?

- GT

```text
GT Condensed
- The next step is "(Evaluation) Objectives Met"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - Design Security System
  - (Evaluation) Objectives Met
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic), the decision step immediately after “Design Security System” is:

- “(Evaluation) Objectives Met”

Source: (1167010.pdf, p. 25–26, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Next step after Design Security System is (Evaluation) Objectives Met; page cites p26 vs E* p25 acceptable for figure spread.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q17
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, what two inputs are listed inside the orange box feeding into "Design Security System"?

- GT

```text
GT Condensed
- High Assurance–DBT
- Mitigation Measures
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - orange box feeding into Design Security System
  - High Assurance–DBT
  - Mitigation Measures
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic), the orange box feeding into “Design Security System” lists these two inputs:

1. “High Assurance – DBT”
2. “Mitigation Measures”

Source: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Two orange-box inputs match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q18
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, what two items are listed under "Define Objectives"?

- GT

```text
GT Condensed
- Identify Threats
- Select Set of Scenarios
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - Define Objectives
  - Identify Threats
  - Select Set of Scenarios
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic), the two items listed under “Define Objectives” are:

1. Identify Threats
2. Select Set of Scenarios

Source: (1167010.pdf, p. 25–26, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Identify Threats; Select Set of Scenarios under Define Objectives match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q19
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, what is emphasized inside the "Design Certification" oval, and what is emphasized inside the "COL Application" oval?

- GT

```text
GT Condensed
- Design Certification: "Delay"
- COL Application: "Detection, Delay, Response Assessment"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - Design Certification oval
  - Delay
  - COL Application oval
  - Detection, Delay, Response Assessment
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic):

- Inside the “Design Certification” oval: “Emphasis on: Delay”
- Inside the “COL Application” oval: “Detection, Delay, Response Assessment”

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Design Certification (Delay) and COL Application (Detection, Delay, Response Assessment) for Figure 2 match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q20
- Query: In Figure 2 of the UNFSF design and regulatory process schematic, how many main sequential stages appear in the central workflow, and what are they?

- GT

```text
GT Condensed
- There are 3 main stages
- Characterize Facility Design
- Design Security System
- (Evaluation) Objectives Met
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
- F*:
  - Characterize Facility Design
  - Design Security System
  - (Evaluation) Objectives Met
```

- Model Answer

```text
In Figure 2 (UNFSF design and regulatory process schematic), the central workflow shows 3 main sequential stages (the three gray process boxes inside the dashed orange boundary), in order:

1. Define Objectives
2. Characterize Facility Design
3. Design Security System

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Mis-states central three stages: inserts Define Objectives and omits (Evaluation) Objectives Met vs GT.
- CoP
  - CoP_S: 0.35
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.15
- ViR: 0.5
Scores
- CoP_S: 0.35
- CoP_N:
- CoP: 0.35
- CiP: 1
- CiH: 1
- HR: 0.15
- ViR: 0.5
```
### Q21
- Query: In the UNFSF design and regulatory process schematics, which figure contains "Design Security System" and which figure contains "Design Safeguards System"?

- GT

```text
GT Condensed
- Figure 2 contains "Design Security System"
- Figure 3 contains "Design Safeguards System"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
  - 1167010.pdf, Figure 3, p26 (software) or p20 (printed)
- F*:
  - Design Security System in Figure 2
  - Design Safeguards System in Figure 3
```

- Model Answer

```text
- “Design Security System” appears in Figure 2 (*Regulatory Framework for Designing Security Systems*).
Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)

- “Design Safeguards System” appears in Figure 3 (*Regulatory Framework for Designing Safeguard Systems*).
Source: (1167010.pdf, Badwan & Demuth, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: Figure 2 / Figure 3 placement correct; minor page drift on citations.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 1
```
### Q22
- Query: In the UNFSF design and regulatory process schematics, what is emphasized inside the "Design Certification" oval in Figure 2 versus Figure 3?

- GT

```text
GT Condensed
- Figure 2: "Delay"
- Figure 3: "Deter, Prevent Theft, Diversion"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
  - 1167010.pdf, Figure 3, p26 (software) or p20 (printed)
- F*:
  - Figure 2 Design Certification oval
  - Delay
  - Figure 3 Design Certification oval
  - Deter, Prevent Theft, Diversion
```

- Model Answer

```text
In the UNFSF design and regulatory process schematics:

- Figure 2 (“Design Security System” schematic) â€” inside the green “Design Certification” oval, the emphasis is: “Delay.”
Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)

- Figure 3 (“Design Safeguards System” schematic) â€” inside the green “Design Certification” oval, the emphasis is: “Deter, Prevent Theft, Diversion.”
Source: (1167010.pdf, Badwan & Demuth, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: Figure 2 Delay vs Figure 3 Deter, Prevent Theft, Diversion match GT (includes “Emphasis on:” wrapper text).
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q23
- Query: In the UNFSF design and regulatory process schematics, what does the "COL Application" oval emphasize in Figure 2 versus Figure 3?

- GT

```text
GT Condensed
- Figure 2: "Detection, Delay, Response Assessment"
- Figure 3: "Detection, Recovery, Response Assessment"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
  - 1167010.pdf, Figure 3, p26 (software) or p20 (printed)
- F*:
  - Figure 2 COL Application oval
  - Detection, Delay, Response Assessment
  - Figure 3 COL Application oval
  - Detection, Recovery, Response Assessment
```

- Model Answer

```text
In the UNFSF design and regulatory process schematics:

- Figure 2 (Security system schematic) â€” the “COL Application” oval emphasizes: “Detection, Delay, Response Assessment.”
Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)

- Figure 3 (Safeguards system schematic) â€” the “COL Application” oval emphasizes: “Detection, Recovery, Response Assessment.”
Source: (1167010.pdf, Badwan & Demuth, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: COL oval Figure 2 vs Figure 3 emphases match GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q24
- Query: In the UNFSF design and regulatory process schematics, what top-center source feeds into "Design Certification" in Figure 2, and what top-center source feeds into "Design Certification" in Figure 3?

- GT

```text
GT Condensed
- Figure 2: "Standard Set of Site and Security Characteristics"
- Figure 3: "SNM Form, Enrichment, Quantity, Process Units"
GT Sets
- E*:
  - 1167010.pdf, Figure 2, p25 (software) or p19 (printed)
  - 1167010.pdf, Figure 3, p26 (software) or p20 (printed)
- F*:
  - top-center source in Figure 2
  - Standard Set of Site and Security Characteristics
  - top-center source in Figure 3
  - SNM Form, Enrichment, Quantity, Process Units
```

- Model Answer

```text
- Figure 2: The top-center source feeding into “Design Certification” is “Standard Set of Site and Security Characteristics.”
Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 25, Figure 2)

- Figure 3: The top-center source feeding into “Design Certification” is “SNM Form, Enrichment, Quantity, Process Units.”
Source: (1167010.pdf, Badwan & Demuth, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: Top-center sources into Design Certification for Figures 2 and 3 match GT; minor page offsets on cites.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.95
- CiH: 1
- HR: 0.05
- ViR: 1
```
### Q25
- Query: According to the UNFSF framework application text, what are the first two steps in integrating safeguards and security into the facility design?

- GT

```text
GT Condensed
- First: identify the safeguards and security regulations performance goals
- Second: identify functional design criteria and develop specific design requirements from applicable regulatory guides, guidance, codes, and standards
GT Sets
- E*:
  - 1167010.pdf, Section 2 (framework integration text), p9 (software) or p3 (printed)
- F*:
  - []
```

- Model Answer

```text
According to the UNFSF framework application text, the first two steps in integrating safeguards and security into the facility design are:

1. Develop the regulatory framework for designing the Security system (to meet NRC requirements in 10 CFR 73, “Physical Protection of Plants and Materials”).
2. Develop the regulatory framework for designing the Safeguards/MC&A system (to meet NRC requirements in 10 CFR 74, “Material Control and Accounting of Special Nuclear Materials”).

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 9–10, Sec. “Development of Regulatory Framework for Designing Safeguards/MC&A and Security Systems”)
```

- Scores

```text
Metric Work
- Notes: Answer gives “develop regulatory frameworks” for 73/74 vs GT’s first-two steps (performance goals; then functional criteria/requirements from guides/codes); wrong procedural framing despite nearby doc cites.
- CoP
  - CoP_S: 0.45
  - CoP_N:
- CiP: 0.8
- CiH: 0.0
- HR: 0.1
- ViR: 0.55
Scores
- CoP_S: 0.45
- CoP_N:
- CoP: 0.45
- CiP: 0.8
- CiH: 0.0
- HR: 0.1
- ViR: 0.55
```
### Q26
- Query: In Figure 4 of the UNFSF design integration workflow, what are the two top-level regulatory branches, and which CFR citations are explicitly attached to them?

- GT

```text
GT Condensed
- Left branch: "Physical Security" with citation 10CFR73
- Right branch: "Safeguards (MC&A)" with citation 10CFR74
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p27 (software) or p21 (printed)
- F*:
  - Green box labeled "Physical Security 10CFR73"
  - Green box labeled "Safeguards (MC&A) 10CFR74"
```

- Model Answer

```text
In Figure 4 (UNFSF design integration workflow), the two top-level regulatory branches are:

1. Physical Security â€” explicitly cited as 10 CFR 73
2. Safeguards (MC&A) â€” explicitly cited as 10 CFR 74

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: First two integration steps match GT (performance goals; then functional criteria/requirements from guides/codes); cite p11 vs Section 2 p9—same document, adjacent framework text.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.9
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.9
- CiH: 1
- HR: 0
- ViR: 1
```
### Q27
- Query: In Figure 4 of the UNFSF design integration workflow, what common sequence of design-development boxes appears under both the Physical Security and Safeguards (MC&A) branches before integration?

- GT

```text
GT Condensed
- Performance Goal
- Functional Design Criteria
- Design Requirements
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p27 (software) or p21 (printed)
- F*:
  - Parallel red boxes labeled "Performance Goal"
  - Parallel cyan boxes labeled "Functional Design Criteria"
  - Parallel cyan boxes labeled "Design Requirements"
```

- Model Answer

```text
In Figure 4 (UNFSF design integration workflow), both the Physical Security (10 CFR 73) and Safeguards (MC&A) (10 CFR 74) branches show the same pre-integration sequence of design-development boxes:

1. Performance Goal
2. Functional Design Criteria
3. Design Requirements

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Physical Security 10CFR73 and Safeguards (MC&A) 10CFR74 branches match Figure 4 / GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q28
- Query: In Figure 4 of the UNFSF design integration workflow, what is the exact label of the central integration box, and what dual-role concept does it represent?

- GT

```text
GT Condensed
- Exact label: "Integration of Design Requirements (Dual Function)"
- Concept: merging security and safeguards design requirements into a combined dual-function basis
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p27 (software) or p21 (printed)
- F*:
  - Red box labeled "Integration of Design Requirements (Dual Function)"
  - Placement below the two parallel Design Requirements boxes
```

- Model Answer

```text
In Figure 4 of the UNFSF design integration workflow, the central integration box is labeled:

- “Integration of Design Requirements (Dual Function)”

This represents the dual-role concept that a single set of design requirements can serve more than one function across the 3S spaceâ€”i.e., requirements can be integrated/harmonized so that design features support both physical security and safeguards (MC&A) simultaneously (rather than being developed as isolated, potentially conflicting requirements).

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Exact label correct; dual-role explanation slightly broader than GT “merging requirements into combined dual-function basis” but consistent.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 0.9
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.05
- ViR: 0.9
```
### Q29
- Query: In Figure 4 of the UNFSF design integration workflow, what design stage appears immediately after the "Integration of Design Requirements (Dual Function)" box, and what assessment step follows it?

- GT

```text
GT Condensed
- Next design stage: "Conceptual Design"
- Following assessment step: "Performance Assessment"
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p27 (software) or p21 (printed)
- F*:
  - Integration of Design Requirements (Dual Function)
  - Conceptual Design
  - Performance Assessment
```

- Model Answer

```text
In Figure 4 of the UNFSF design integration workflow:

- The design stage immediately after “Integration of Design Requirements (Dual Function)” is “Conceptual Design.”
- The assessment step that follows the design-stage progression is “Performance Assessment.”

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design then Performance Assessment matches Figure 4 / GT.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 1
```
### Q30
- Query: In Figure 4 of the UNFSF design integration workflow, which supporting analysis activities are shown alongside the design stages, and at what stages do they appear?

- GT

```text
GT Condensed
- Security Assessment Methods and Safeguards Assessment Methods appear alongside Conceptual Design
- Trade Studies appear alongside Preliminary Design on both the left and right sides
GT Sets
- E*:
  - 1167010.pdf, Figure 4, p27 (software) or p21 (printed)
- F*:
  - Orange boxes labeled "Security Assessment Methods" and "Safeguards Assessment Methods" adjacent to Conceptual Design
  - Pink boxes labeled "Trade Studies" adjacent to Preliminary Design on both sides
```

- Model Answer

```text
In the UNFSF design integration workflow (Figure 4), the supporting analysis activities that are explicitly described in the accompanying framework-application text (as activities conducted and then incorporated into the design as it progresses) are:

- At / feeding the Conceptual Design stage:
Vulnerability analysis, threat analysis, probabilistic risk assessment, acquisition strategy, and acquisition path analysis / diversion path analysis (conducted and results incorporated into the conceptual design).
Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 11)

- At / on the Preliminary Design stage:
An early-stage preliminary performance assessment is conducted on the preliminary design (top-down traceability of functional design criteria and design requirements through the security and safeguards systems design; findings addressed).
Source: (1167010.pdf, Badwan & Demuth, p. 11)
```

- Scores

```text
Metric Work
- Notes: Answers from framework prose (vulnerability/threat/PRA/path analyses) instead of Figure 4 side-boxes (Security/Safeguards Assessment Methods; Trade Studies) and stage pairing in GT.
- CoP
  - CoP_S: 0.2
  - CoP_N:
- CiP: 0.85
- CiH: 1
- HR: 0.55
- ViR: 0.15
Scores
- CoP_S: 0.2
- CoP_N:
- CoP: 0.2
- CiP: 0.85
- CiH: 1.0
- HR: 0.55
- ViR: 0.15
```
