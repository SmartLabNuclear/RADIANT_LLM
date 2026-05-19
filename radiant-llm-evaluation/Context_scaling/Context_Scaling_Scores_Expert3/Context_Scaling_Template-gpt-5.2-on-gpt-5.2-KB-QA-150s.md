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
- **KB Condition**: 150-source KB (`150s`)
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
Operational functions shared across Safety, Security, and Safeguards
In the discussion of the 3S interfaces, the operational functions shown as shared across all three domains are (verbatim from the schematic callout):
â€¢    Access Control
â€¢    Detection
â€¢    Monitoring
â€¢    Alarms
â€¢    Surveillance
â€¢    MAAs
â€¢    VAs
â€¢    Locks & Keys
Citation: (1167010.pdf, p. 24, Figure â€œdomain-interface schematicâ€)
How this is represented in the domain-interface schematic
The associated schematic is depicted as a three-circle Venn diagram with circles labeled Safety, Security, and Safeguards. The central triple-overlap region (where all three circles intersect) is highlighted by a callout pointing into that central overlap, and the callout text lists the shared operational functions above.
Citation: (1167010.pdf, p. 24, Figure â€œdomain-interface schematicâ€)
```

- Scores

```text
Metric Work
- Notes: Wrong triple-overlap inventory vs GT (adds Access control/Alarms/Surveillance; omits Operational safety); center-Venn claim follows wrong list.
- CoP
  - CoP_S: 0.5
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.35
- ViR: 0.71
Scores
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- CiP: 1
- CiH: 1
- HR: 0.35
- ViR: 0.71
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
How the schematics distinguish the roles (Safety vs. Security vs. Safeguards)
In the domain-interface schematics, the three domains are visually separated as three labeled regions (often a Venn-style diagram)â€”each domain has its own labeled â€œpurpose/protectionâ€ statement, while the overlaps indicate interface/shared measures and the center indicates integrated â€œ3S.â€
â€¢    In one schematic, each domain label is paired with a short â€œprotect/prevent/deterâ€ phrase inside/adjacent to its region.
â€¢    In another schematic, the three circles are labeled Safety, Security, and Safeguards, with additional text in overlap regions and a central â€œ3Sâ€ label to emphasize integration.
Citations: (1167010.pdf, p. 24, Figure â€œSafety, Security, and Safeguards Interfacesâ€); (1984826.pdf, p. 7, Figure (3S Venn diagram))
Primary objective associated with each domain (as conveyed by the labels)
Safety â€” primary objective: protect public health and the environment (i.e., protection of the public and environment from harmful radiological consequences).
Citations: (1167010.pdf, p. 24, Figure â€œSafety, Security, and Safeguards Interfacesâ€); (1984826.pdf, p. 7, Figure (3S Venn diagram))
Security â€” primary objective: protect against sabotage, malicious acts, and external attacks (i.e., prevent/mitigate intentional adversary actions).
Citation: (1167010.pdf, p. 24, Figure â€œSafety, Security, and Safeguards Interfacesâ€)
Safeguards â€” primary objective: deter theft/misuse and prevent diversion of nuclear material (nonproliferation/material-accountability intent reflected directly in the labels).
Citation: (1167010.pdf, p. 24, Figure â€œSafety, Security, and Safeguards Interfacesâ€)
How the interface is conveyed
The overlap regions in these schematics communicate that the domains are distinct in objective but interdependent in implementation, with shared/interface functions depicted in the intersections and an integrated 3S region at the center.
Citations: (1167010.pdf, p. 24, Figure â€œSafety, Security, and Safeguards Interfacesâ€); (1984826.pdf, p. 7, Figure (3S Venn diagram))
```

- Scores

```text
Metric Work
- Notes: 1167010 Figure 1 objectives well aligned; additional citations to 1984826.pdf not in E* for this item → CiP < 1 and HR for cross-document material.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 0.6
- CiH: 1
- HR: 0.18
- ViR: 0.9
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 0.6
- CiH: 1
- HR: 0.18
- ViR: 0.9
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
Systems / operational functions enabling Safeguardsâ€“Security interaction
The interface schematics identify the following operational functions as facilitating interaction between the Safeguards and Security domains:
â€¢    Access Control
â€¢    Detection
â€¢    Monitoring
â€¢    Alarms
â€¢    Surveillance
â€¢    MAAs
â€¢    VAs
â€¢    Locks & Keys
Citation: (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
How the schematics show these functions supporting both objectives
In the domain-interface schematic, these functions are placed in the shared interface area between the â€œSecurityâ€ and â€œSafeguardsâ€ domains (i.e., the overlap/interface region rather than being exclusive to only one domain). This visual placement conveys that the same measures simultaneously support:
â€¢    Security objectives (protecting against sabotage/malicious acts/external attacks), and
â€¢    Safeguards objectives (deterring theft/misuse/diversion of nuclear material),
by functioning as common controls usable for both domains.
Citation: (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
```

- Scores

```text
Metric Work
- Notes: Safeguards–Security function list and overlap explanation match GT.
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
Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility, the governing U.S. regulatory frameworks identified are:
â€¢    Physical protection: NRC 10 CFR Part 73 (â€œPhysical Protection of Plants and Materialsâ€).
â€¢    Material control and accounting (MC&A): NRC 10 CFR Part 74 (â€œMaterial Control and Accounting of Special Nuclear Materialâ€).
Citations: (1167010.pdf, p. 13, discussion referencing 10 CFR Parts 73 and 74); (1167010.pdf, p. 22, discussion of safeguards/security regulatory basis including Parts 73 and 74)
```

- Scores

```text
Metric Work
- Notes: Parts 73/74 correct; cites p.13 and p.22 vs E* p.13 sections (acceptable drift).
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
Within the used nuclear fuel storage facility (UNFSF) design-integration discussion, the report associates the following performance goal/objective statements with each regulatory framework:
1) Physical protection â€” 10 CFR Part 73
Performance goal/objective (as stated): to â€œanalyze and establish the security design features that provide minimal reliance on operational program to protect against the design basis threats of theft or diversion of strategic special nuclear materials and radiological sabotage at an early stage.â€
Citation: (1167010.pdf, p. 13, Sec. 3.1.1, â€œPhysical Protection of Plants and Materials (10 CFR Part 73) Performance Goal/objectiveâ€)
2) Material control & accounting (MC&A) â€” 10 CFR Part 74
Performance goal/objective (as stated in the report): â€œThe performance goal/objective of the physical security rule is to analyze and establish the security design features that provide minimal reliance on operational program to protect against the design basis threats of theft or diversion of strategic special nuclear materials and radiological sabotage at an early stage.â€
Citation: (1167010.pdf, p. 13, Sec. 1.2, â€œMaterial Control and Accounting of Special Nuclear Materials (10 CFR Part 74) Performance Goal/objectiveâ€)
```

- Scores

```text
Metric Work
- Notes: Part 73 objective quoted correctly; Part 74 block mistakenly repeats the Part 73 performance-goal sentence — major factual error for half the question.
- CoP
  - CoP_S: 0.5
  - CoP_N:
- CiP: 0.85
- CiH: 1
- HR: 0.25
- ViR: 1
Scores
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- CiP: 0.85
- CiH: 1
- HR: 0.25
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
The facility system identified as having dual safeguards and security functionsâ€”and therefore suitable for early integration into the design of a used nuclear fuel storage facilityâ€”is the:
â€¢    Exit and Entry Control System for Protected Areas
Citation: (1167010.pdf, p. 13, discussion of early design integration of safeguards/security functions for a UNFSF)
```

- Scores

```text
Metric Work
- Notes: Correct dual-function system named; omits explicit PA/VA/MAA serving sentence from GT.
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
A facility system is justified as having dual safeguards and security functions (and therefore a candidate for early design integration in a used nuclear fuel storage facility / ISFSI context) based on regulatory-driven functional design criteria derived from reviewing the applicable design/licensing/operational regulatory guidance for both domains and selecting systems that can satisfy both sets of objectives with minimal reliance on operational programs.
1) Regulatory-basis criterion: derive functional design criteria/requirements from applicable guidance
The report states that the selection is grounded in an assessment of applicable regulatory guides for design, licensing, and operation, which are used to define functional design criteria and design requirements for safeguards and security systems. This regulatory review provides the justification for identifying systems whose functions inherently serve both safeguards and security needs (i.e., are â€œdual-functionâ€ by requirements mapping).
Citation: (1167010.pdf, p. 13, discussion of assessing applicable regulatory guides to define functional design criteria/requirements for safeguards and security systems)
2) Performance objective criterion: â€œearlyâ€ safeguards/security features that minimize reliance on operations programs
As a key selection criterion for what to integrate early, the report emphasizes a performance objective of establishing safeguards/security design features at an early stage that provide minimal reliance on operational programs while supporting core protective outcomes (e.g., deterrence/prevention/detection related to theft/diversion/sabotage/unlawful diversion/unauthorized production). This is used to justify choosing systems that are intrinsic design features and not primarily procedural/administrative controls.
Citations: (1167010.pdf, p. 13, performance-goal/objective discussion); (1167010.pdf, p. 6, discussion of safeguards performance objectives)
3) Why this supports â€œdual-functionâ€ selection (safeguards + security)
Under these regulatory and performance considerations, a system qualifies as â€œdual-functionâ€ when its required functions (e.g., controlled entry/exit to protected areas) simultaneously support:
â€¢    Security: physical protection against adversary actions (intrusion, sabotage, theft attempts), and
â€¢    Safeguards/MC&A support: controlled access consistent with preventing/limiting opportunities for diversion or unauthorized actions involving nuclear material.
This is the logic used to justify selecting the Exit and Entry Control System for Protected Areas as suitable for early integration as a dual safeguards-and-security system.
Citation: (1167010.pdf, p. 13, identification and justification context for early integration of a dual-function system)
```

- Scores

```text
Metric Work
- Notes: Dual-function criteria largely match GT; RG 5.53 not explicit by number.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 1
- CiH: 1
- HR: 0.08
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
Within the UNFSF discussion, the scope of application of the framework for integrating safeguards and security into design is defined by four elements:
1.    Developing the performance goals, functional design criteria, and design requirements for a system with dual safeguards and security functions (including identifying specific requirements and addressing early integration of those requirements).
2.    Identifying methods and trade studies.
3.    Describing the performance assessment process.
4.    Highlighting the benefits of integrating safeguards and security at the early stage of design.
Citation: (1167010.pdf, â€œIntegrating Safeguards and Security into the Design of a Used Nuclear Fuel Storage Facility,â€ p. 13, discussion of framework scope)
```

- Scores

```text
Metric Work
- Notes: Four scope elements match GT.
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
According to the UNFSF design requirements for SNM doorway monitors, the monitor must be capable of detecting:
â€¢    Minimum quantity: 0.5 g of plutonium-239 (Pu 239)
â€¢    Shielding condition: encased in at least 3 mm of brass
â€¢    Confidence level: 90% confidence limit
Citation: (1167010.pdf, p. 16, design requirements discussion for SNM doorway monitors)
```

- Scores

```text
Metric Work
- Notes: Pu-239, brass, 90% confidence match GT; omits <0.1% false-alarm clause.
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
A numeric maximum false alarm rate is not specified in the UNFSF design requirements for SNM doorway monitors. The requirement is expressed qualitatively as maintaining a â€œlow false alarm rate.â€
Citation: (1167010.pdf, p. 15, discussion of SNM doorway monitor performance: â€œâ€¦while maintaining a low false alarm rate.â€)
```

- Scores

```text
Metric Work
- Notes: Claims no numeric false-alarm cap; GT specifies <0.1% — incorrect.
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
Per the UNFSF doorway-monitor design requirements, the doorway monitor must be capable of detecting:
â€¢    Minimum quantity: 1 g of uranium 233 (U 233) (specified as containing 7â€“10 ppm of U 232)
â€¢    Time window: within 4 hours of removal of all decay products
â€¢    Shielding condition: encased in at least 3 mm of brass
â€¢    Confidence level (also specified in the same requirement): 90% confidence limit
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, Badwan & Demuth, p. 16, design requirements for doorway monitors detecting U 233)
```

- Scores

```text
Metric Work
- Notes: U-233 bundle matches GT; extra confidence bullet adds minor HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.1
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.1
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
Within the UNFSF design requirements, the specified minimum detection effectiveness and false alarm thresholds for metal (firearm) detectors and explosive detectors are:
Metal / firearm (walk-through portal or handheld) detectors
â€¢    Minimum detection effectiveness: â‰¥ 85% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 10%, when sensitivity is adjusted to achieve the required detection effectiveness
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 17, design requirements for firearm/metal detectors)
Explosive detectors
â€¢    Minimum detectable explosive mass: 200 grams (for â€œdynamite, TNT, and similar nitrogen-containing compoundsâ€)
â€¢    Required detection probability / effectiveness: â‰¥ 90% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 1%, when sensitivity is adjusted to the required detection level
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 18, design requirements for explosive detectors)
```

- Scores

```text
Metric Work
- Notes: Detector thresholds match GT; clean citations.
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
In Figure 4 of the UNFSF design framework, after the â€œPerformance Assessmentâ€ decision node:

- YES path: the process proceeds to â€œFinal Design Optimized and Harmonized.â€
Source: *(1167010.pdf, p. 27, Figure 4)*

- NO paths: the process loops back to â€œFinal Designâ€ (iteration/redo of the design) before reassessing performance.
Source: *(1167010.pdf, p. 27, Figure 4)*
```

- Scores

```text
Metric Work
- Notes: YES/NO paths match GT; minor iteration gloss.
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
In Figure 1 (UNFSF 3S interface schematic), the text â€œAccess Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keysâ€ appears in the bottom-center red callout box. Its arrow points upward into the Safeguardsâ€“Security overlap region (i.e., the intersection of Safeguards and Security, near the lower central overlap of the Venn diagram).

Source: (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Bottom-center callout and Safeguards∩Security overlap match GT.
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

1. Orange box feeding into â€œDesign Security Systemâ€
 The orange callout box contains:
 - â€œHigh Assurance â€“DBTâ€
 - â€œMitigation Measuresâ€
 (Its arrow feeds upward into â€œDesign Security Systemâ€.)
 Source: (1167010.pdf, p. 25, Figure 2)

2. Emphasis inside the green â€œDesign Certificationâ€ oval
 Inside the green oval labeled â€œDesign Certificationâ€, the emphasized text is:
 - â€œEmphasis on: Delayâ€
 Source: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Orange box and Design Certification emphasis match GT.
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
In Figure 2 (UNFSF design and regulatory process schematic), the decision step that appears immediately after â€œDesign Security Systemâ€ is:

- â€œ(Evaluation) Objectives Metâ€

Source: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Decision step after Design Security System matches GT.
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
In Figure 2 (UNFSF design and regulatory process schematic), the orange box feeding into â€œDesign Security Systemâ€ lists two inputs:

1. High Assurance â€“ DBT
2. Mitigation Measures

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
In Figure 2 (UNFSF design and regulatory process schematic), the two items listed under â€œDefine Objectivesâ€ are:

1. Identify Threats
2. Select Set of Scenarios

Source: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Define Objectives items match GT.
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

- Inside the â€œDesign Certificationâ€ oval, the emphasis is â€œDelay.â€
- Inside the â€œCOL Applicationâ€ oval, the emphasis is â€œDetection, Delay, and Response Assessment.â€

Source: *(1167010.pdf, p. 25, Figure 2)*
```

- Scores

```text
Metric Work
- Notes: Delay and COL emphasis content match GT (minor ‘and’ in COL list).
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
In Figure 2, the central workflow (the three gray boxes inside the dashed orange oval, connected left-to-right) contains 3 main sequential stages:

1. Characterize Facility Design
2. Design Security System
3. (Evaluation) Objectives Met

Source: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Three-stage central workflow matches GT.
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
- â€œDesign Security Systemâ€ appears in Figure 2 (UNFSF design and regulatory process schematic).
Source: *(1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)*

- â€œDesign Safeguards Systemâ€ appears in Figure 3 (UNFSF design and regulatory process schematic).
Source: *(1167010.pdf, p. 26, Figure 3 â€” â€œRegulatory Framework for Designing Safeguard Systemsâ€)*
```

- Scores

```text
Metric Work
- Notes: Figure 2 / Figure 3 mapping matches GT.
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
- Figure 2 (â€œDesign Certificationâ€ oval): emphasized text is â€œEmphasis on: Delay.â€
Source: *(1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)*

- Figure 3 (â€œDesign Certificationâ€ oval): emphasized text is â€œEmphasis on: Deter, Prevent Theft, Diversion.â€
Source: *(1167010.pdf, p. 26, Figure 3 â€” â€œRegulatory Framework for Designing Safeguard Systemsâ€)*
```

- Scores

```text
Metric Work
- Notes: Design Certification emphases with ‘Emphasis on:’ phrasing match GT substance.
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

- Figure 2 (â€œCOL Applicationâ€ oval) emphasizes: â€œDetection, Delay, Response Assessment.â€
Source: (1167010.pdf, p. 25, Figure 2)

- Figure 3 (â€œCOL Applicationâ€ oval) emphasizes: â€œDetection, Recovery, Response Assessment.â€
Source: (1167010.pdf, p. 26, Figure 3)
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
- Figure 2: The top-center source feeding into â€œDesign Certificationâ€ is â€œStandard Set of Site and Security Characteristics.â€
Source: (1167010.pdf, p. 25, Figure 2)

- Figure 3: The top-center source feeding into â€œDesign Certificationâ€ is â€œSNM Form, Enrichment, Quantity, Process Units.â€
Source: (1167010.pdf, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: Top-center Design Certification sources match GT.
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
According to the UNFSF framework application text, the first two steps for integrating safeguards and security into the facility design are:

1. Identify the safeguards and security regulatory performance goals.
2. Identify functional design criteria and develop specific design requirements based on the applicable regulatory guides, guidance, codes, and standards.

Source: (1167010.pdf, p. 9 and p. 11, UNFSF framework application text)
```

- Scores

```text
Metric Work
- Notes: First two steps align well with GT Section 2 condensed (performance goals; then criteria/requirements from guides); cites p.9 and p.11 near E* Section 2.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.9
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.9
- CiH: 1
- HR: 0.08
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
In Figure 4 (UNFSF design integration workflow), the two top-level regulatory branches and their explicitly attached CFR citations are:

- Physical Security â€” 10 CFR 73
- Safeguards (MC&A) â€” 10 CFR 74

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Figure 4 branches and CFR labels match GT.
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
In Figure 4 (UNFSF design integration workflow), both the Physical Security and Safeguards (MC&A) branches show the same sequence of design-development boxes (before the integration step):

1. Performance Goal
2. Functional Design Criteria
3. Design Requirements

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Pre-integration three-box sequence matches GT.
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

- â€œIntegration of Design Requirements (Dual Function)â€

This represents the dual-role concept that certain design requirements/features can serve both:
- Physical Security functions, and
- Safeguards (MC&A) functions
(i.e., requirements are integrated so they provide dual-function/dual-benefit performance across both regulatory branches).

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Integration box label and dual-role concept match GT.
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

- The design stage immediately after â€œIntegration of Design Requirements (Dual Function)â€ is â€œConceptual Design.â€
- The assessment step that follows (after the downstream design progression) is â€œPerformance Assessment.â€

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design and Performance Assessment match GT; ‘downstream’ wording mild imprecision.
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
In Figure 4 (UNFSF design integration workflow), the supporting analysis activities shown alongside the design stages are:

- At the â€œConceptual Designâ€ stage:
- Security Assessment Methods
- Safeguards Assessment Methods
*(both shown feeding into/supporting Conceptual Design)*

- At the â€œPreliminary Designâ€ stage:
- Trade Studies
*(shown supporting Preliminary Design on both the Physical Security and Safeguards (MC&A) sides)*

- After the â€œFinal Designâ€ stage:
- Performance Assessment *(shown as the decision/assessment step after Final Design, prior to reaching â€œFinal Design Optimized and Harmonizedâ€ on the YES path)*

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual/Preliminary supporting activities match GT; Performance Assessment after Final is extra vs GT condensed.
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
