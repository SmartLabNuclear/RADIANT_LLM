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
- **KB Condition**: 1-source KB (`1s`)
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
  Operational functions described as shared across Safety, Security, and Safeguards
  Within the safety–security–safeguards interface discussion, the functions identified as common to all three domains are:
  •    Detection
  •    Monitoring
  •    MAAs
  •    VAs
  •    Operational Safety
  •    Locks & Keys
  (1167010.pdf, p. 24, Figure 1; 1167010.pdf, p. 7)
  How the shared responsibility is visually represented in the schematic
  The associated domain-interface schematic depicts Safety, Security, and Safeguards as a three-circle Venn diagram. The shared operational functions are shown as items placed in/associated with the overlap regions of the circles—indicating these responsibilities are not owned by a single domain but instead sit at the interfaces (including the triple-overlap conceptually representing “shared by all three”).
  (1167010.pdf, p. 24, Figure 1 “Safety, Security, and Safeguards Interfaces”)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Lists all six shared functions; Venn/triple-overlap representation matches GT. Extra p.7 cite is auxiliary.
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
  (2026-01-08; Winter)
  How the roles are distinguished in the domain-interface schematic
  The schematic distinguishes Safety, Security, and Safeguards using a three-circle Venn diagram, where:
  •    Each circle is explicitly labeled with the domain name (Safety / Security / Safeguards).
  •    The overlap regions visually indicate areas of interface/shared measures across domains (i.e., functions/controls that support more than one domain).
  (1167010.pdf, p. 24, Figure 1 “Safety, Security, and Safeguards Interfaces”)
  Primary objective associated with each domain (from the visual + labels)
  From the labels within/associated with each domain in the figure:
  •    Safety: primary objective is protection of people/public health and the environment.
  (1167010.pdf, p. 24, Figure 1)
  •    Security: primary objective is protection against sabotage / malicious acts (including external attack).
  (1167010.pdf, p. 24, Figure 1)
  •    Safeguards: primary objective is preventing theft/diversion/misuse of nuclear material and addressing proliferation concerns.
  (1167010.pdf, p. 24, Figure 1)
  In short: the schematic separates the domains by distinct labeled circles and domain-specific concerns/objectives, while showing integration via the overlapping regions that represent shared/interface responsibilities.
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Safeguards objective adds proliferation framing beyond GT; security wording slightly compressed vs verbatim labels.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.06
- ViR: 0.75
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.06
- ViR: 0.75
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
  (2026-01-08; Winter)
  Systems / operational functions facilitating Safeguards ↔ Security interaction
  In the safeguards–security interface, the document identifies the interaction as occurring primarily through:
  •    Access control
  •    Detection / surveillance / monitoring (i.e., monitoring and detection functions, including surveillance)
  (1167010.pdf, p. 7)
  In the associated interface schematic (Figure 1), the safeguards–security overlap is populated with specific operational elements that support these interaction mechanisms, including:
  •    Access control
  •    Detection / monitoring (including surveillance)
  •    Alarms
  •    MAAs and VAs
  •    Locks & keys
  (1167010.pdf, p. 24, Figure 1 “Safety, Security, and Safeguards Interfaces”)
  How the schematic presents these as supporting both objectives
  The interface schematic uses a three-circle Venn diagram (Safety / Security / Safeguards). The functions listed above are shown in a callout associated with the Safeguards–Security overlap region, visually indicating that these same systems are intended to simultaneously:
  •    support safeguards objectives (e.g., deterrence/detection of diversion or theft of nuclear material via monitoring, verification-related activities), and
  •    support security objectives (e.g., preventing/detecting malicious acts via access restriction, alarms, and detection/monitoring systems).
  (1167010.pdf, p. 24, Figure 1; 1167010.pdf, p. 7)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Safeguards–Security functions and overlap placement match; minor interpretive bullets (e.g., proliferation) add HR.
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
  (2026-01-08; Winter)
  Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility, the report identifies U.S. NRC regulations as the governing regulatory frameworks for:
  •    Physical protection (security): 10 CFR Part 73 (“Physical Protection of Plants and Materials”).
  (1167010.pdf, p. 6; see also discussion referencing 10 CFR 73.58 / RG 5.73 in the same security integration context: 1167010.pdf, p. 9–10)
  •    Material Control & Accounting (MC&A) / safeguards: 10 CFR Part 74 (“Material Control and Accounting of Special Nuclear Materials”).
  (1167010.pdf, p. 10)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Parts 73/74 correctly identified; extra cross-refs (RG 5.73, pp.9–10) beyond GT condensed.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.92
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.92
- CiH: 1
- HR: 0.08
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
  (2026-01-08; Winter)
  Within the used nuclear fuel storage facility design-integration discussion, the report assigns the following distinct performance goals/objectives to the two cited NRC regulatory frameworks:
  Regulatory framework    Domain    Distinct performance goal/objective (verbatim from report)
  10 CFR Part 73 (“Physical Protection of Plants and Materials”)    Physical protection / security    “The performance goal/objective of the physical security rule is to analyze and establish the security design features that provide minimal reliance on operational program to protect against the design basis threats of theft or diversion of strategic special nuclear materials and radiological sabotage at an early stage.” (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, Badwan & Demuth, p. 6, Sec. 3.1.1)
  10 CFR Part 74 (“Material Control and Accounting of Special Nuclear Materials”)    MC&A / safeguards    “The performance goal/objective of the Safeguards/MC&A rules is to analyze and establish, at early stage, safeguard features that provide minimal reliance on operational programs to deter, prevent, detect loss or theft or sabotage, or unlawful diversion or unauthorized production of special nuclear materials.” (1167010.pdf, Badwan & Demuth, p. 10, Sec. 1.2)
  Key distinction conveyed by these objectives (as written):
  •    Part 73 emphasizes security design features to protect against DBT theft/diversion of strategic SNM and radiological sabotage, with minimal reliance on operational programs, established early. (1167010.pdf, Badwan & Demuth, p. 6, Sec. 3.1.1)
  •    Part 74 emphasizes safeguards/MC&A features to deter, prevent, and detect SNM loss/theft/sabotage and unlawful diversion/unauthorized production, also with minimal reliance on operational programs, established early. (1167010.pdf, Badwan & Demuth, p. 10, Sec. 1.2)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Both performance objectives align with GT; long table + distinction bullets add slight HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.08
- ViR: 1
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
  (2026-01-08; Winter)
  The facility system identified as having dual safeguards and security functions, suitable for early integration into the design of a used nuclear fuel storage facility, is the Exit and Entry Control System for Protected Areas.
  Source: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, Badwan & Demuth, p. 6; see also discussion p. 13)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Correct dual-function system named; omits GT detail that it serves PAs, VAs, and MAAs.
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
  Criteria / regulatory considerations used to justify selecting a dual-function (safeguards + security) system for early UNFSF design integration
  In the UNFSF design-integration discussion, a facility system is justified as “dual safeguards and security” when it can be derived from, and shown to satisfy, overlapping functional requirements and performance objectives from both of the governing regulatory frameworks:
  1) Physical protection / security framework — 10 CFR Part 73
  The selection is justified when the system is needed to meet Part 73 physical protection requirements and objectives (e.g., protecting against theft/diversion and radiological sabotage), and can be defined via functional design criteria and design requirements extracted from the applicable security regulations/guidance.
  Regulatory anchor: 10 CFR Part 73 (see also the document’s example tying access control to 10 CFR 73.45(b)).
  Source (local KB): (1167010.pdf, p. 13–14; p. 18)
  2) Safeguards / MC&A framework — 10 CFR Part 74
  The selection is justified when the same system also supports the Part 74 MC&A performance intent—i.e., establishing safeguards features early in design to deter/prevent/detect loss/theft/diversion (and related adversarial outcomes).
  Source (local KB): (1167010.pdf, p. 6–7; p. 13)
  How the document operationalizes this “dual-function” selection logic (what makes a system a good candidate)
  The document’s integration approach explicitly describes:
  •    assessing applicable regulatory guides/requirements (from Parts 73 and 74),
  •    using them to define functional design criteria and design requirements for safeguards and security systems, and
  •    thereby selecting a facility system that has dual safeguards and security functions—with the Exit and Entry Control System for Protected Areas identified as such a candidate.
  Source (local KB): (1167010.pdf, p. 13)
  Concrete example of the regulatory basis for “dual-function”
  A key justification example is access / entry-exit control: the document notes the Access Control System is “provided specifically to meet” 10 CFR 73.45(b) using “specific entry and exit techniques” to detect/assess/communicate attempted unauthorized removal of SNM (implemented with radiation detection plus metal/explosive detection). These same capabilities also support safeguards goals by helping detect unauthorized removal/diversion pathways—hence the “dual” role.
  Source (local KB): (1167010.pdf, p. 18)
  ________________________________________
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Overlapping requirements and 73.45 example match spirit of GT; does not explicitly name RG 5.53 as in GT.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.1
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.1
- ViR: 1
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
  (2026-01-07; Winter)
  Within the application scope discussion for integrating Safeguards and Security into the design of a Used Nuclear Fuel Storage Facility (UNFSF), the framework’s application is defined by four elements/objectives:
  1.    Develop performance goals, functional design criteria, and design requirements for a dual safeguards-and-security system; identify the specific requirements for that system; and address early integration of these requirements.
  2.    Identify methods and trade studies.
  3.    Describe the performance assessment process.
  4.    Highlight the benefits of integrating safeguards and security early in the design stage.
  Source (local KB): (1167010.pdf, p. 13, application scope/objectives list)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Four scope elements match GT (first item expanded but same substance).
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
  (2026-01-07; Winter)
  According to the design requirements for SNM doorway monitors, the monitor must be able to detect at least:
  •    Minimum quantity: 0.5 g of plutonium-239 (Pu 239)
  •    Shielding condition: encased in at least 3 mm of brass
  •    Confidence level: 90% confidence limit (noted alongside a false alarm rate < 0.1%)
  Grounding (local KB): (1167010.pdf, p. 16–17, SNM doorway monitor design requirements)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: 0.5 g Pu-239, 3 mm brass, 90% / <0.1% false alarms match GT; page span slightly off E* but same section.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.95
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
  Maximum specified false alarm rate (SNM doorway monitors)
  The design requirements specify a maximum false alarm rate of less than 0.1% for SNM doorway monitors used to detect special nuclear material.
  Grounding (local KB): (1167010.pdf, p. 15–17, SNM doorway monitor design requirements)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: States <0.1% false alarm rate as required; no unsupported extras.
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
  U 233 doorway monitor detectability requirement (minimum quantity, time window, shielding)
  According to the specified doorway monitor design requirements, the monitor must be able to detect:
  •    Minimum quantity: 1 gram of uranium 233 (U 233)
  •    Time window/condition: within 4 hours of removal of all decay products
  •    Shielding condition: U 233 (noted as containing 7–10 ppm U 232) encased in at least 3 mm of brass
  •    (Also specified in the same requirement statement: detection is at a 90% confidence limit.)
  Source: (1167010.pdf, p. 16, doorway monitor design requirements for U 233)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: 1 g U-233, 4 h after decay-product removal, 3 mm brass match GT; extra U-232 ppm + confidence bullet add HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.15
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.15
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
  Metal and explosive detector performance requirements (thresholds)
  1) Metal (firearm) detectors (handheld or portal)
  •    Minimum detection effectiveness: ≥ 85% effective detection rate
  •    Maximum false alarm rate: ≤ 10% (when set to achieve the stated detection effectiveness)
  Source: (1167010.pdf, pp. 17–18, metal/firearm detector performance requirements in the entry/exit control system discussion)
  2) Explosive detectors
  •    Minimum detectable explosive mass: 200 grams of dynamite, TNT, and similar nitrogen-containing compounds
  •    Required detection probability/effectiveness: ≥ 90% effective detection rate at that minimum mass
  •    Maximum false alarm rate: ≤ 1% (when sensitivity is set to achieve the stated detection effectiveness)
  Source: (1167010.pdf, pp. 17–18, explosive detector performance requirements in the entry/exit control system discussion)
  ________________________________________
```

- Scores

```text
Metric Work
- Notes: Metal ≥85%/≤10% FA and explosive 200 g / ≥90% / ≤1% FA match GT.
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
  In **Figure 4 (UNFSF design flow)**, after the **“Performance Assessment”** decision node:

  - **YES path:** proceeds to **“Final Design Optimized and Harmonized.”**
  - **NO path:** **loops back to “Final Design”** (i.e., iterates the design rather than finalizing it).

  **Citation:** (1167010.pdf, p. 13, Figure 4 — flowchart showing “Performance Assessment” with YES → “Final Design Optimized and Harmonized” and NO → “Final Design”)
```

- Scores

```text
Metric Work
- Notes: YES/NO paths after Performance Assessment match GT and F*; printed/software page offset allowed for Figure 4.
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
  In **Figure 1 (UNFSF 3S interface schematic)**, the text **“Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys”** appears in the **bottom-center red rounded-rectangle callout box**. The **arrow from this box points into the overlap region between “Safeguards” and “Security”** (the lower central overlap of those two circles in the Venn diagram).

  **Citation:** (1167010.pdf, p. 24, **Figure 1** — UNFSF 3S interface schematic)
```

- Scores

```text
Metric Work
- Notes: Callout location and Safeguards∩Security overlap match GT/F*.
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
  - **Orange box feeding into “Design Security System”:**
    “**-High Assurance –DBT**” and “**-Mitigation Measures**”

  - **Emphasized inside the green “Design Certification” oval:**
    “**Emphasis on: Delay**”

  **Citation:** (1167010.pdf, *Regulatory Framework for Designing Security Systems*, p. 26, **Figure 2**)
```

- Scores

```text
Metric Work
- Notes: Orange box lines and Design Certification emphasis (Delay) match GT; minor dash/spacing vs verbatim.
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
  In **Figure 2** (UNFSF design and regulatory process schematic), the decision step immediately after **“Design Security System”** is:

  - **“(Evaluation) Objectives Met?”**

  **Citation:** (1167010.pdf, p. 26, **Figure 2** — UNFSF design and regulatory process schematic)
```

- Scores

```text
Metric Work
- Notes: Next decision after Design Security System matches GT (optional ? on label).
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
  In **Figure 2** (UNFSF design and regulatory process schematic), the **orange box feeding into “Design Security System”** lists these two inputs:

  1. **High Assurance – DBT**
  2. **Mitigation Measures**

  **Citation:** (1167010.pdf, p. 26, **Figure 2** — “Regulatory Framework for Designing Security Systems”)
```

- Scores

```text
Metric Work
- Notes: Two orange-box inputs match GT (spacing/DBT hyphen cosmetic).
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
  In **Figure 2 (UNFSF design and regulatory process schematic)**, under **“Define Objectives”** the two listed items are:

  1. **Identify threats**
  2. **Select set of scenarios**

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 26, **Figure 2**)
```

- Scores

```text
Metric Work
- Notes: Identify threats + select scenarios under Define Objectives match GT.
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
  In **Figure 2** (UNFSF design and regulatory process schematic):

  - Inside the **“Design Certification”** oval, the emphasized text is: **“Emphasis on: Delay”**
  - Inside the **“COL Application”** oval, the emphasized text is: **“Emphasis on: Detection, Delay, Response Assessment”**

  **Citation:** (1167010.pdf, p. 26, **Figure 2** — UNFSF design and regulatory process schematic)
```

- Scores

```text
Metric Work
- Notes: Design Certification and COL Application emphases match GT.
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
  In **Figure 2 (UNFSF design and regulatory process schematic)**, the **central workflow** shows **three** main sequential stages:

  1. **Characterize Facility Design**
  2. **Design Security System**
  3. **(Evaluation) Objectives Met?** (decision step)

  **Citation:** (1167010.pdf, p. 26, **Figure 2** — UNFSF design and regulatory process schematic)
```

- Scores

```text
Metric Work
- Notes: Three central stages and labels match GT.
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
  - **“Design Security System”** appears in **Figure 2** (*Regulatory Framework for Designing Security Systems*).
    **Citation:** (1167010.pdf, p. 26, **Figure 2**)

  - **“Design Safeguards System”** appears in **Figure 3** (*Regulatory Framework for Designing Safeguard Systems*).
    **Citation:** (1167010.pdf, p. 27, **Figure 3**)
```

- Scores

```text
Metric Work
- Notes: Figure 2 / Figure 3 mapping for the two design boxes matches GT.
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
  - **Figure 2 (“Regulatory Framework for Designing Security Systems”) — Design Certification oval:**
    **“Emphasis on: Delay”**
    **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 26, **Figure 2**)

  - **Figure 3 (“Regulatory Framework for Designing Safeguard Systems”) — Design Certification oval:**
    **“Emphasis on: Deter, Prevent Theft, Diversion”**
    **Citation:** (1167010.pdf, Badwan & Demuth, p. 27, **Figure 3**)
```

- Scores

```text
Metric Work
- Notes: Figure 2 vs Figure 3 Design Certification emphases match GT.
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
  In the UNFSF design and regulatory process schematics, the **“COL Application”** oval emphasizes:

  - **Figure 2 (Security systems schematic):** **“Emphasis on: Detection, Delay, Response Assessment”**
    **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 26, **Figure 2**)

  - **Figure 3 (Safeguards systems schematic):** **“Emphasis on: Detection, Recovery, Response Assessment”**
    **Citation:** (1167010.pdf, Badwan & Demuth, p. 27, **Figure 3**)
```

- Scores

```text
Metric Work
- Notes: COL oval emphases for Figures 2 and 3 match GT.
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
  In the UNFSF design and regulatory process schematics:

  - **Figure 2 (Security systems schematic):** the **top-center source** feeding into **“Design Certification”** is **“Standard Set of Site and Security Characteristics.”**
    **Citation:** (1167010.pdf, p. 26, **Figure 2**)

  - **Figure 3 (Safeguards systems schematic):** the **top-center source** feeding into **“Design Certification”** is **“SNM Form, Enrichment, Quantity, Process Units.”**
    **Citation:** (1167010.pdf, p. 27, **Figure 3**)
```

- Scores

```text
Metric Work
- Notes: Top-center sources into Design Certification for Figures 2 and 3 match GT.
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
  According to the **UNFSF framework application** text, the first two steps for integrating **safeguards and security** into the facility design are:

  1. **Identify and analyze applicable regulations and regulatory guidance** needed to develop a framework for designing safeguards and security systems that meet regulatory objectives and functional performance.
  2. **Implement and integrate that regulatory framework** for designing **Safeguards/MC&A** and **security systems** into the overall design and operation of the facility.

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 13)
```

- Scores

```text
Metric Work
- Notes: Does not state GT’s first two integration steps (performance goals; then criteria/requirements from RGs). One citation (p.13) does not identify E* Section 2 evidence → CiP=0 by definition; CiH=0.
- CoP
  - CoP_S: 0.5
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.4
- ViR: 1
Scores
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- CiP: 0
- CiH: 0
- HR: 0.4
- ViR: 1
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
  In **Figure 4 (UNFSF design integration workflow)**, the two **top-level regulatory branches** at the top of the workflow are:

  1. **Physical Security** — explicitly labeled **“10CFR73”**
  2. **Safeguards (MC&A)** — explicitly labeled **“10CFR74”**

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 13, **Figure 4**)
```

- Scores

```text
Metric Work
- Notes: Branches and CFR labels match GT; Figure 4 page offset vs E* acceptable under rubric.
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
  In **Figure 4 (UNFSF design integration workflow)**, the **common sequence of design-development boxes** that appears under **both** the **Physical Security (10CFR73)** branch and the **Safeguards (MC&A) (10CFR74)** branch **before integration** is:

  **Performance Goal → Functional Design Criteria → Design Requirements**

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 13, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Pre-integration box sequence matches GT/F*.
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
  - **Exact label of the central integration box (Figure 4):**
    **“Integration of Design Requirements (Dual Function)”**
    *(1167010.pdf, “Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility”, Badwan & Demuth, p. 13, Figure 4)*

  - **Dual-role concept it represents:**
    It represents **design requirements that serve a dual function across both regulatory branches**—i.e., requirements developed under **Physical Security (10 CFR 73)** and **Safeguards/MC&A (10 CFR 74)** that can be **combined/leveraged as shared (dual-purpose) design features** during integration into the overall UNFSF facility design.
    *(1167010.pdf, Badwan & Demuth, p. 13, Figure 4)*
```

- Scores

```text
Metric Work
- Notes: Exact integration box label matches; dual-role explanation consistent with GT (extra CFR color adds minor HR).
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.9
- CiH: 1
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.9
- CiH: 1
- HR: 0.05
- ViR: 1
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
  In **Figure 4 (UNFSF design integration workflow)**:

  - The design stage immediately after **“Integration of Design Requirements (Dual Function)”** is **“Conceptual Design.”**
  - The assessment step that follows is **“Performance Assessment.”**

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, **Figure 4**)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design then Performance Assessment after integration match GT.
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
  In **Figure 4 (UNFSF design integration workflow)**, the **supporting analysis activities** shown alongside the design stages (and where they appear) are:

  1. **Security Assessment Methods** and **Safeguards Assessment Methods** — shown as supporting inputs alongside the **Conceptual Design** stage.
  2. **Trade Studies** (for both the security and safeguards sides) — shown as supporting inputs alongside the **Preliminary Design** stage.
  3. **Performance Assessment** — shown following the **Final Design** stage (with the decision logic branching afterward).

  **Citation:** (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, **Figure 4**)
```

- Scores

```text
Metric Work
- Notes: Assessment methods at Conceptual Design and Trade Studies at Preliminary match GT; extra Performance-after-Final item not in GT condensed.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.25
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.25
- ViR: 1
```
