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
- **KB Condition**: 200-source KB (`200s`)
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
Shared operational functions across safety, security, and safeguards (3S):
Within the 3S interface discussion, the operational functions explicitly shown as common to all three domains are:
â€¢    Access control
â€¢    Detection
â€¢    Monitoring
â€¢    Alarms
â€¢    Surveillance
â€¢    MAAs
â€¢    VAs
â€¢    Locks & keys
This set is presented together as the functions shared across the three domains in the central overlap of the interface schematic.
(1167010.pdf, â€œFigure 1. Safety, Security, and Safeguards Interfaces.â€, p. 24, Figure 1 callout list)
How this is represented in the domain-interface schematic:
The associated schematic is a Venn diagram labeled â€œFigure 1. Safety, Security, and Safeguards Interfaces.â€ The functions listed above appear together in the diagramâ€™s central intersection (the overlap of safety, security, and safeguards), indicating they are shared/common operational functions spanning all three domains.
(1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Wrong triple-overlap inventory vs GT (adds Access control/Alarms/Surveillance; omits Operational safety); claims that list sits in the three-way center.
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
In the domain-interface schematics, safety, security, and safeguards are distinguished as three separate (but overlapping) domains, each shown as its own labeled region (typically a three-circle/Venn-style interface figure). The labels inside/adjacent to each domain explicitly state the primary objective for that domain, making the roles visually unambiguous. (1167010.pdf, p. 24, Figure 1. Safety, Security, and Safeguards Interfaces)
How each domainâ€™s role is distinguished + its primary objective (as labeled)
â€¢    Safety is presented as the domain focused on:
â€œProtection of Health, Safety of the Public and Environment.â€
This objective is attached directly to the Safety region in the schematic.
(1167010.pdf, p. 24, Figure 1)
â€¢    Security is presented as the domain focused on:
â€œProtect Against, Sabotage, Malicious Acts and External Attacks.â€
This objective is attached directly to the Security region in the schematic.
(1167010.pdf, p. 24, Figure 1)
â€¢    Safeguards is presented as the domain focused on:
â€œDeter, Theft, Misuseâ€ and â€œDiversion.â€
These objectives are attached directly to the Safeguards region in the schematic (often as short phrases capturing the nonproliferation/material-diversion emphasis).
(1167010.pdf, p. 24, Figure 1)
Visual logic conveyed by the schematic
â€¢    The separation into three labeled regions communicates that each domain has a distinct top-level mission.
â€¢    The overlaps communicate that some functions/interfaces are shared or tightly coupled across domains, but the primary objective statements remain domain-specific and are communicated through the domain labels themselves.
(1167010.pdf, p. 24, Figure 1)
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
Systems / operational functions that facilitate Safeguardsâ€“Security interaction
In the Security âˆ© Safeguards interface region of the domain-interface schematic, the following systems/operational functions are listed as facilitating interaction between the safeguards and security domains:
â€¢    Access Control
â€¢    Detection
â€¢    Monitoring
â€¢    Alarms
â€¢    Surveillance
â€¢    MAAs (Material Access Areas)
â€¢    VAs (Vital Areas)
â€¢    Locks & keys
These are the functions explicitly placed in the overlap between Security and Safeguards in the schematic. (1167010.pdf, p. 24, Figure 1: â€œSafety, Security, and Safeguards Interfacesâ€)
How the schematic presents them as supporting both objectives
The interface schematic depicts Safety, Security, and Safeguards as overlapping domains (Venn-style). The functions above are written in the shared overlap region between Security and Safeguards, visually indicating they are jointly relevantâ€”i.e., they support security objectives (e.g., prevention/detection of malicious acts, access restriction) while also supporting safeguards objectives (e.g., deterrence/detection of theft/misuse/diversion through monitoring, surveillance, alarms, controlled access, and protected areas). (1167010.pdf, p. 24, Figure 1)
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
Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility (UNFSF), the regulatory frameworks identified are:
â€¢    Physical protection (security): U.S. NRC, 10 CFR Part 73 â€” â€œPhysical Protection of Plants and Materialsâ€
â€¢    Material control and accounting (MC&A): U.S. NRC, 10 CFR Part 74 â€” â€œMaterial Control and Accounting of Special Nuclear Materialâ€
This is stated directly in the design-integration discussion as the starting point for safeguards/security system design being based on regulatory requirements, with Part 73 governing physical protection and Part 74 governing MC&A. (1834341.pdf, p. 6, discussion text on safeguards/security system design and regulatory requirements)
```

- Scores

```text
Metric Work
- Notes: Part 73 / Part 74 correct but evidence is 1834341 only, not 1167010 Section 3 E*.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 0
- CiH: 0
- HR: 0.05
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
10 CFR Part 73 (Physical protection / physical security)    Ensure the facilityâ€™s physical protection system can defend against the Design Basis Threat (DBT) and includes measures to protect against radiological sabotage and prevent theft or diversion of special nuclear material (SNM). (1897829.pdf, p. 29; 1897829.pdf, p. 87; 1906501.pdf, p. 66)
10 CFR Part 74 (Material Control & Accountingâ€”MC&A)    Detect diversion of fissile (special nuclear) material through MC&A (with the discussion noting the MC&A objective is centered on diversion detection, e.g., via item accounting approaches for discrete items). (1886489.pdf, p. 18â€“19; 1896981.pdf, p. 40)
Notes/limits from the local knowledge base
â€¢    The retrieved local excerpts clearly link Part 73 to DBT-based protection against radiological sabotage and theft/diversion, and link Part 74 to diversion detection via MC&A. However, the available excerpts did not provide more granular, numeric â€œperformance goalsâ€ (e.g., specific detection timeliness thresholds) for a used fuel storage facility beyond those stated objectives. (1897829.pdf, p. 29 & p. 87; 1886489.pdf, p. 18â€“19)
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
The facility system identified as suitable for early integration because it can serve dual safeguards and security functions is the Exit and Entry Control System for Protected Areas (i.e., the protected-area access control/entryâ€“exit control system).
This system is presented in the safeguards/security integration framework as a â€œcommon facility systemâ€ that can be selected specifically because it supports overlapping safeguardsâ€“security needs (notably access control and related detection/monitoring functions). (1834341.pdf, p. 6)
```

- Scores

```text
Metric Work
- Notes: Correct Exit and Entry Control System; citation only 1834341 not E* 1167010.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0
- CiH: 0
- HR: 0.05
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
A system is justified as having dual safeguards and security functions (and therefore being a good candidate for early integration into a used nuclear fuel storage facility design) when the applicable regulatory requirements and guidance for both domains drive overlapping functional requirements for that same system.
1) The selection is justified by explicitly starting from NRC regulatory requirements for both domains
The design-selection process is described as beginning with regulatory requirements, specifically:
â€¢    10 CFR Part 73 as the basis for physical protection (security), and
â€¢    10 CFR Part 74 as the basis for material control and accounting (MC&A) (safeguards).
These frameworks define the obligations that the facility design must satisfy, and they motivate identifying systems that can satisfy requirements in both regimes. (1834341.pdf, p. 6)
2) A â€œdual-functionâ€ system is selected by assessing applicable regulatory guides to derive functional design criteria and design requirements for both safeguards and security
The documents describe identifying applicable regulatory guides for an ISFSI/UNFSF context and then assessing those guides to define functional design criteria and design requirementsâ€”specifically to facilitate selecting a facility system with dual safeguards/security functions. In other words, the â€œdual functionâ€ designation is not ad hoc; it is justified by a structured review that maps regulatory expectations into system functions. (1167010.pdf, p. 13)
3) The selected system is justified because it supports overlapping operational objectives (i.e., common functions)
Based on this guidance review, the Exit and Entry Control System for Protected Areas (including applicability to Protected Areas / Vital Areas / Material Access Areas) is identified as a system that â€œshares safeguards and security function,â€ making it suitable for early integration. (1167010.pdf, p. 13)
How this relates to the â€œcriteriaâ€ question (what makes it qualify as dual-function)
Putting the above together, the criteria/regulatory considerations are essentially:
1.    Regulatory coverage in both domains (security under Part 73; MC&A/safeguards under Part 74). (1834341.pdf, p. 6)
2.    Demonstrable overlap in required functions when NRC guidance is translated into functional/design requirements (i.e., the system supports both domainsâ€™ objectives). (1167010.pdf, p. 13)
3.    Selection supported by review of applicable regulatory guides for ISFSI/UNFSF design/licensing/operation, explicitly done to enable identification of a â€œcommonâ€ (dual-function) system. (1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Overlapping requirements, guide-driven criteria, and protected-area dual-function example match GT; NRC Regulatory Guide 5.53 (E* ref) not named explicitly.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 0.75
- CiH: 1
- HR: 0.15
- ViR: 0.92
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 0.75
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
The scope of application of the framework for integrating safeguards and security into the design of a Used Nuclear Fuel Storage Facility (UNFSF) is defined by four elements:
1.    Develop the performance goals, functional design criteria, and design requirements for a system with dual safeguards and security functions, and identify/address the specific requirements early in the integration process.
2.    Identify methods and trade studies.
3.    Describe the performance assessment process.
4.    Highlight the benefits of integrating safeguards and security at the early stage of design.
Citations: (1167010.pdf, p. 13, discussion of â€œscope of the applicationâ€ of the framework for integrating safeguards and security into UNFSF design)
```

- Scores

```text
Metric Work
- Notes: Four scope elements match GT list on 1167010 p13.
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
According to the UNFSF design requirements for SNM doorway monitors, the monitor must be able to detect:
â€¢    Minimum Pu-239 quantity: 0.5 g of Pu 239
â€¢    Shielding condition: encased in a minimum of 3 mm of brass
â€¢    Confidence level: 90% confidence limit
Citation: (1167010.pdf, p. 16, design requirements text for SNM doorway monitors)
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
The maximum false alarm rate specified for SNM doorway monitors (for detecting special nuclear material) in the UNFSF design requirements is:
â€¢    False alarm rate: < 0.1%
Citation: (1167010.pdf, â€œApplication of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facilityâ€, Badwan & Demuth, p. 16, design requirements for SNM doorway monitors)
```

- Scores

```text
Metric Work
- Notes: <0.1% false alarm matches GT Section 3.3.2.
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
According to the UNFSF SNM doorway monitor design requirements, the doorway monitor must be capable of detecting:
â€¢    Minimum quantity: 1 g of U 233 (containing 7â€“10 ppm of U 232)
â€¢    Time window / timing condition: within 4 hours of removal of all decay products
â€¢    Shielding condition: encased in a minimum of 3 mm of brass
Citations: (1167010.pdf, p. 16, design requirements for SNM doorway monitorsâ€”U 233 detection requirement and shielding condition)
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
Metal detectors (firearms/metal detection)
â€¢    Minimum detection effectiveness: â‰¥ 85% effective detection rate
â€¢    Maximum false alarm threshold: â‰¤ 10% false alarm rate (with sensitivity set to achieve the 85% detection level)
Citation: (1167010.pdf, â€œApplication of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facilityâ€, Badwan & Demuth, p. 17â€“18, design requirements text citing typical requirements per RG 5.7)
Explosive detectors
â€¢    Minimum detectable explosive mass: 200 grams (for dynamite, TNT, and similar nitrogen-containing compounds)
â€¢    Required detection probability / effectiveness: â‰¥ 90% effective detection rate
â€¢    Maximum false alarm threshold: â‰¤ 1% false alarm rate (with sensitivity set to achieve the 90% detection level)
Citation: (1167010.pdf, Badwan & Demuth, p. 17â€“18, design requirements text for explosive detector performance; referenced as typical requirements per RG 5.7)
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
In Figure 4 (the UNFSF design/integration framework), after the â€œPerformance Assessmentâ€ decision node:

- YES path: goes to â€œFinal Design Optimized and Harmonized.â€
- NO path(s): loops back to â€œFinal Designâ€ (i.e., iterate/revise the final design and reassess).

PDF source: (1167010.pdf, p. 27, Figure 4: â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
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
In Figure 1 (UNFSF 3S interface schematic), the text â€œAccess Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keysâ€ is in the bottom-center red callout box. Its arrow points upward into the Safeguardsâ€“Security overlap region (i.e., the Safeguards âˆ© Security interface area of the Venn diagram).

Source: (1167010.pdf, p. 24, Figure 1 â€œUNFSF 3S interface schematicâ€)
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
- Orange box feeding into â€œDesign Security Systemâ€:
â€œ-High Assurance â€“DBTâ€ and â€œ-Mitigation Measuresâ€ (in the same orange callout box).

- Green â€œDesign Certificationâ€ oval (emphasis):
â€œEmphasis on: Delayâ€.

Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (UNFSF design and regulatory process schematic), the decision step that appears immediately after â€œDesign Security Systemâ€ is:

- â€œ(Evaluation) Objectives Metâ€

Source: (1167010.pdf, p. 26, Figure 2)
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
In Figure 2 (UNFSF design and regulatory process schematic), the two inputs listed inside the orange box feeding into â€œDesign Security Systemâ€ are:

1. High Assurance â€“ DBT
2. Mitigation Measures

Source: (1167010.pdf, p. 26, Figure 2)
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
In Figure 2 of the UNFSF design and regulatory process schematic:

- Inside the â€œDesign Certificationâ€ oval, the emphasized text is: â€œEmphasis on: Delayâ€.
- Inside the â€œCOL Applicationâ€ oval, the emphasized text is: â€œEmphasis on: Detection, Delay, Response Assessmentâ€.

Source: (1167010.pdf, p. 26, Figure 2; also appears across the Figure 2 rendering on p. 25)
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
In Figure 2 (UNFSF design and regulatory process schematic), the central workflow shows 3 main sequential stages:

1. Characterize Facility Design
2. Design Security System
3. (Evaluation) Objectives Met

Source: (1167010.pdf, p. 25, Figure 2; also shown on p. 26, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Three central stages Characterize Facility Design → Design Security System → (Evaluation) Objectives Met match GT (not counting upstream Define Objectives).
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
- â€œDesign Security Systemâ€ appears in Figure 2 (*Regulatory Framework for Designing Security Systems*).
Source: (1167010.pdf, p. 26, Figure 2)

- â€œDesign Safeguards Systemâ€ appears in Figure 3 (*Regulatory Framework for Designing Safeguard Systems*).
Source: (1167010.pdf, p. 27, Figure 3)
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
- Figure 2 (security system schematic) â€” inside the â€œDesign Certificationâ€ oval, the emphasis is: â€œEmphasis on: Delay.â€
Source: (1167010.pdf, p. 26, *Figure 2* â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (safeguards system schematic) â€” inside the â€œDesign Certificationâ€ oval, the emphasis is: â€œEmphasis on: Deter, Prevent Theft, Diversion.â€
Source: (1167010.pdf, p. 26, *Figure 3* â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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
- Figure 2 (security system schematic): the â€œCOL Applicationâ€ oval emphasizes â€œDetection, Delay, Response Assessment.â€
Source: (1167010.pdf, p. 26, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (safeguards system schematic): the â€œCOL Applicationâ€ oval emphasizes â€œDetection, Recovery, Response Assessment.â€
Source: (1167010.pdf, p. 27, Figure 3 â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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
- Figure 2 (Security system schematic): the top-center source feeding into â€œDesign Certificationâ€ is â€œStandard Set of Site and Security Characteristics.â€
Source: (1167010.pdf, p. 26, *Figure 2* â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (Safeguards system schematic): the top-center source feeding into â€œDesign Certificationâ€ is â€œSNM Form, Enrichment, Quantity, Process Units.â€
Source: (1167010.pdf, p. 27, *Figure 3* â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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

1. Identify the safeguards and security regulationsâ€™ performance goals.
2. Identify functional design criteria and develop specific design requirements from the applicable regulatory guides, guidance, codes, and standards.

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 11, framework application text)
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

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
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
In Figure 4 of the UNFSF design integration workflow, both the Physical Security (10 CFR 73) branch and the Safeguards (MC&A) (10 CFR 74) branch follow the same sequence of design-development boxes (before they come together for integration):

1. Performance Goal
2. Functional Design Criteria
3. Design Requirements

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
```

- Scores

```text
Metric Work
- Notes: Parallel sequence Performance Goal → Functional Design Criteria → Design Requirements matches GT.
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
- Exact label of the central integration box (Figure 4):
â€œIntegration of Design Requirements (Dual Function)â€

- What dual-role concept it represents:
It represents integrating safeguards and physical security design requirements for systems/components that have a â€œdual functionâ€â€”i.e., common systems that serve both safeguards and security purposes in the facility design.

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
```

- Scores

```text
Metric Work
- Notes: Label and dual-function concept (common systems serving both domains) align with GT.
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
- The assessment step that follows it (later in the workflow sequence) is â€œPerformance Assessment.â€

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
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
In Figure 4 (UNFSF design integration workflow), the supporting analysis activities shown alongside the main design stages are:

1. Security Assessment Methods and Safeguards Assessment Methods
- These appear alongside / feeding into the Conceptual Design stage.

2. Trade Studies (shown for both the security and safeguards sides)
- These appear alongside / feeding into the Preliminary Design stage.

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€)
```

- Scores

```text
Metric Work
- Notes: Security/Safeguards assessment methods at Conceptual Design and Trade Studies at Preliminary Design match GT; no spurious extra branch.
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
