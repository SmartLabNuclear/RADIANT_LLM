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
- **KB Condition**: 5-source KB (`5s`)
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
Shared operational functions across safety, security, and safeguards
Within the discussion of safetyâ€“securityâ€“safeguards interfaces, the operational functions identified as being shared across all three domains (i.e., common to safety, security, and safeguards simultaneously) are:
-    Access control
-    Detection
-    Monitoring
-    Alarms
-    Surveillance
-    MAAs (Material Access Areas)
-    VAs (Vital Areas)
-    Locks & keys
These items are explicitly shown as the central â€œtriple-overlapâ€ set in the interface diagram. (1167010.pdf, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€, p. 24)
How this is represented in the domain-interface schematic
The associated schematic is a three-circle Venn diagram labeled Safety, Security, and Safeguards. The functions listed above appear in the center region where all three circles overlap, indicating they are operational functions/interfaces that must be managed in a coordinated way across the three S3 domains. (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Lists Access control/Alarms/Surveillance as triple-shared; GT triple-overlap is Detection, Monitoring, MAAs, VAs, Operational Safety, Locks & Keys (no Access/Alarms/Surveillance there). Misses Operational Safety.
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
How the roles are distinguished in the domain-interface schematic
The roles of Safety, Security, and Safeguards are distinguished visually by depicting them as three separate (but overlapping) domains in a three-circle Venn-style schematic. Each circle is explicitly labeled with its domain name and includes accompanying text that states that domainâ€™s overarching purpose; the overlaps indicate interfaces/commonalities among the domains. (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€; p. 24 text introducing Figure 1)
Primary objective associated with each domain (as conveyed by labels)
From the schematicâ€™s in-circle/adjacent labels, the primary objectives are:
-    Safety: â€œProtection of Health, Safety of the Public and Environmentâ€ (1167010.pdf, p. 24, Figure 1)
-    Security: â€œProtect Against Sabotage, Malicious Acts and External Attacksâ€ (1167010.pdf, p. 24, Figure 1)
-    Safeguards: â€œDeter, Theft, Misuseâ€; and â€œDiversionâ€ (i.e., deterrence of theft/misuse and prevention/detection of diversion of nuclear material). (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Objectives match Figure 1 labels closely; Venn/overlap distinction correct. Minor interpretive gloss on Safeguards.
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
Safeguardsâ€“Security interaction: systems / operational functions
The interfaces (overlaps) between the safeguards and security domains are described as being primarily in:
-    Access control
-    Detection, surveillance, and monitoring (including associated alarms)
This is stated directly in the discussion of interfaces/overlaps and reinforced by the interface figure. (1167010.pdf, pp. 7 and 20, discussion of safeguardsâ€“security overlap)
How these are presented in interface schematics as supporting both objectives
In the associated domain-interface schematic (a three-domain Venn-style diagram), these functions are presented as shared/overlapping capabilities between the Security and Safeguards domainsâ€”i.e., shown in the overlap region as common operational elements that simultaneously:
-    support security objectives (protection against sabotage/malicious acts), and
-    support safeguards objectives (deterrence/detection of theft, misuse, diversion of nuclear material).
In Figure 1, the shared-function callout includes items such as â€œAccess Control, Detection, Monitoring, Alarms, Surveillance â€¦â€ indicating these are cross-domain features supporting both safeguards and security. (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
```

- Scores

```text
Metric Work
- Notes: Safeguards–Security overlap narrative correct but omits explicit MAAs/VAs/Locks & keys list; cites pp.7,20 + Fig.1 callout paraphrase.
- CoP
  - CoP_S: 0.75
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- CiP: 0.95
- CiH: 1
- HR: 0.08
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
Within the used nuclear fuel storage facility (UNFSF) design-integration discussion, the governing U.S. regulatory frameworks identified are:
-    Physical protection (security): 10 CFR Part 73 (including the safety/security interface provision 10 CFR 73.58, with associated guidance such as Regulatory Guide (RG) 5.73).
Citation: (1167010.pdf, p. 6; p. 9)
-    Material control & accounting (MC&A): 10 CFR Part 74, â€œMaterial Control and Accounting of Special Nuclear Material.â€
Citation: (1167010.pdf, p. 6; p. 9)
(For context, the discussion also situates these within the spent fuel storage licensing framework of 10 CFR Part 72 for ISFSIs/UNFSFs, but Part 72 is the licensing context rather than the core MC&A/physical protection rule sets.)
Citation: (1167010.pdf, p. 6â€“7)
```

- Scores

```text
Metric Work
- Notes: 10 CFR 73/74 correct; extra Part 72 licensing context beyond GT condensed.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0.12
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.95
- CiH: 1
- HR: 0.12
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
Within the used nuclear fuel storage facility (UNFSF) â€œsecurity and safeguards by designâ€ discussion, the document associates the following performance goal/objective with each framework:
-    Physical protection â€” 10 CFR Part 73:
The objective is to analyze and establish physical protection (security) design features early in the design process so as to minimize reliance on operational/programmatic measures while ensuring the facility can protect against DBT-level threats, including theft/diversion of strategic SNM and radiological sabotage.
Citation: (1167010.pdf, p. 13, discussion of Part 73/physical protection design objectives in the UNFSF context)
-    Material control & accounting (MC&A) â€” 10 CFR Part 74:
The objective is to analyze and establish safeguards/MC&A design features early in the design process to minimize reliance on operational programs, and to deter, prevent, and detect the loss/theft/sabotage, unlawful diversion, or unauthorized production of special nuclear material (SNM).
Citation: (1167010.pdf, p. 13, discussion of Part 74/MC&A design objectives in the UNFSF context)
```

- Scores

```text
Metric Work
- Notes: Performance objectives for Parts 73/74 align with GT; cites Sec. discussion p.13.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.06
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.06
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
The facility system identified as having dual safeguards and security functions suitable for early integration into the design of a used nuclear fuel storage facility (UNFSF) is the:
-    Exit and Entry Control System for Protected Areas
This is explicitly described as serving both safeguards and security roles (i.e., supporting both domainsâ€™ objectives) in the UNFSF design-integration discussion.
Citation: (1167010.pdf, p. 7, discussion of integrating safeguards and security into UNFSF design)
```

- Scores

```text
Metric Work
- Notes: Correct dual-function system; omits GT detail that it serves PAs, VAs, and MAAs.
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
A facility system is justified as having dual safeguards and security functions for early design integration when the applicable regulatory requirements and guidance for both domains drive overlapping functional design criteriaâ€”i.e., the same system can credibly satisfy key elements of physical protection (security) and material control & accounting / safeguards without being treated as two completely separate design features.
In the UNFSF discussion, the document explains that the Exit and Entry Control / Access Control System for Protected Areas (PAs) (also referenced with VAs and MAAs) was selected specifically because:
1.    Regulatory-guidance review identifies it as a common (shared-function) system
The system is selected after reviewing safeguards/security guidance documents and is explicitly described as a system that â€œshares safeguards and security function,â€ making it a prime candidate for early â€œbuilt-inâ€ integration rather than late add-on features.
Citation: (1167010.pdf, p. 13)
2.    It is directly tied to a core physical protection requirement for preventing/ detecting unauthorized SNM removal
The Access Control System is stated to be provided to meet 10 CFR 73.45(b), which requires entry/exit techniques with the capability to â€œdetect, assess, and communicateâ€ an attempted unauthorized removal of SNMâ€”a security requirement that also aligns with safeguards goals (controlling and detecting movement of nuclear material). The document also describes the system as consisting of radiation detection plus metal and explosive detection components (supporting both material-related and adversary-related concerns).
Citation: (1167010.pdf, p. 14)
3.    Early integration is justified by the stated performance goal of minimizing reliance on operational programs
The rationale for early integration is framed as establishing security and safeguards design features early so the facility achieves â€œminimal reliance on the operational programâ€ while still addressing key threats (e.g., theft/diversion and sabotage-related concerns). A dual-function system supports this objective because one engineered system can satisfy multiple requirements simultaneously.
Citation: (1167010.pdf, p. 13)
4.    It is developed by deriving functional design criteria from the governing security and safeguards frameworks
The discussion anchors the design-criteria derivation to the governing regulatory structure for physical protection (10 CFR Part 73) and MC&A/safeguards (10 CFR Part 74), supported by NRC regulatory guidance referenced in the same design-integration discussion. This regulatory â€œmappingâ€ is presented as the basis for selecting and defining requirements for a dual-function system.
Citations: (1167010.pdf, p. 6; p. 9; p. 13â€“14)
```

- Scores

```text
Metric Work
- Notes: Strong dual-function justification (overlap, 73.45 example, early integration); RG 5.53 from GT not named explicitly.
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
The scope of application of the framework for integrating safeguards and security into the design of a Used Nuclear Fuel Storage Facility (UNFSF) is defined by four elements:
1.    Develop the performance goals, functional design criteria, and design requirements for a system with dual safeguards and security functions (including identifying the specific requirements for that system and addressing early integration of those requirements).
2.    Identify applicable methods and trade studies.
3.    Describe the performance assessment process.
4.    Highlight the benefits of early-stage integration into the design.
Citation: (1167010.pdf, p. 13, â€œScope of the applicationâ€)
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
For SNM doorway monitors in the UNFSF design requirements, the monitor must be able to detect:
-    Minimum Pu-239 quantity: 0.5 g of plutonium 239
-    Shielding condition: encased in at least 3 mm of brass
-    Confidence level: 90% confidence limit
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 16)
```

- Scores

```text
Metric Work
- Notes: Pu-239 mass, shielding, 90% confidence match GT; omits <0.1% false-alarm clause in condensed answer.
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
The UNFSF design requirements specify that SNM doorway monitors should have a maximum false alarm rate of less than 0.1%.
Citation: (1167010.pdf, p. 15â€“16, design requirements for SNM doorway monitors)
```

- Scores

```text
Metric Work
- Notes: <0.1% false alarm rate stated as required.
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
Per the UNFSF design requirements for SNM doorway monitors, the doorway monitor must be capable of detecting:
-    Minimum U 233 quantity: 1 gram of U 233 (containing 7â€“10 ppm U 232)
-    Time window: within 4 hours of removal of all decay products
-    Shielding condition: encased in at least 3 mm of brass
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 16, design requirements for SNM doorway monitors)
```

- Scores

```text
Metric Work
- Notes: U-233 1 g, 4 h decay-product window, 3 mm brass match GT; U-232 ppm detail adds minor HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.12
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.12
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
The UNFSF design requirements specify the following minimum detection effectiveness and false alarm thresholds for metal (firearms/nonferrous metal) detectors and explosive detectors:
Metal / firearm detector
-    Minimum detection effectiveness: â‰¥ 85% effective detection rate
-    False alarm threshold: â‰¤ 10% (with sensitivity adjusted to achieve the 85% detection level)
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 17)
Explosive detector
-    Minimum detection effectiveness / required detection probability: â‰¥ 90% effective detection rate (detection probability)
-    Minimum detectable explosive mass: 200 g of dynamite, TNT, or similar nitrogen-containing compounds (at the 90% detection effectiveness level)
-    False alarm threshold: â‰¤ 1% (with sensitivity adjusted to achieve this detection level)
Citations: (1167010.pdf, p. 17â€“18)
```

- Scores

```text
Metric Work
- Notes: Metal and explosive thresholds match GT.
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
In Figure 4 (UNFSF design flow), after the â€œPerformance Assessmentâ€ decision node:

- YES path: proceeds to â€œFinal Design Optimized and Harmonized.â€
  - Citation: (1167010.pdf, p. 27, Figure 4)

- NO path(s): loop back to â€œFinal Designâ€ for further revision/iteration, and then the design is reassessed.
  - Citation: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: YES/NO paths after Performance Assessment match GT; minor extra ‘reassessed’ wording.
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
In Figure 1 (UNFSF 3S interface schematic), the phrase â€œAccess Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keysâ€ is in the bottom-center red rounded-rectangle callout box. The arrow from that box points upward into the lower central overlap region, i.e., the Safeguards âˆ© Security overlap (below the Safety circle).

Citation: (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Callout location and Safeguards∩Security overlap match GT.
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

1) Orange box feeding into â€œDesign Security Systemâ€ contains:
- â€œ-High Assurance â€“DBTâ€
- â€œ-Mitigation Measuresâ€

2) Inside the green â€œDesign Certificationâ€ oval, the emphasized text is:
- â€œEmphasis on: Delayâ€

Citation: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Orange box lines and ovals (Delay; COL emphasis text) match GT; page p25 vs E* acceptable.
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
In Figure 2 (UNFSF design and regulatory process schematic), the decision/evaluation step that appears immediately after â€œDesign Security Systemâ€ is:

- â€œ(Evaluation) Objectives Met?â€

Citation: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Next step after Design Security System matches GT.
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

Citation: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (â€œRegulatory Framework for Designing Security Systemsâ€), the two items listed under â€œDefine Objectivesâ€ are:

1. Identify Threats
2. Select Set of Scenarios

Citation: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Define Objectives sub-items match GT.
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

- Inside the â€œDesign Certificationâ€ oval, the emphasized text is: â€œEmphasis on: Delayâ€.
  Citation: (1167010.pdf, p. 25, Figure 2)

- Inside the â€œCOL Applicationâ€ oval, the emphasized text is: â€œDetection, Delay, Response Assessmentâ€.
  Citation: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Design Certification and COL Application emphases match GT (COL text matches condensed without ‘Emphasis on’ prefix).
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
In Figure 2 (â€œUNFSF design and regulatory process schematicâ€), the central workflow shows 3 main sequential stages:

1. Characterize Facility Design
2. Design Security System
3. (Evaluation) Objectives Met?

Citation: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)
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
- â€œDesign Security Systemâ€ appears in Figure 2 (the security regulatory framework schematic).
  Citation: (1167010.pdf, p. 25, Figure 2)

- â€œDesign Safeguards Systemâ€ appears in Figure 3 (the safeguards regulatory framework schematic).
  Citation: (1167010.pdf, p. 26, Figure 3)
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
In the UNFSF design and regulatory process schematics:

- Figure 2 (Security framework): the green â€œDesign Certificationâ€ oval emphasizes â€œEmphasis on: Delay.â€
  *(1167010.pdf, p. 25, Figure 2)*

- Figure 3 (Safeguards framework): the green â€œDesign Certificationâ€ oval emphasizes deterring and preventing theft/diversion (of SNM).
  *(1167010.pdf, p. 26, Figure 3)*
```

- Scores

```text
Metric Work
- Notes: Design Certification emphases for Figures 2 vs 3 match GT.
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
In the UNFSF design and regulatory process schematics, the â€œCOL Applicationâ€ oval emphasizes:

- Figure 2 (Security framework): â€œDetection, Delay, Response Assessment.â€
  *(1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)*

- Figure 3 (Safeguards framework): â€œDetection, Recovery, Response Assessment.â€
  *(1167010.pdf, p. 26, Figure 3 â€” â€œRegulatory Framework for Designing Safeguard Systemsâ€)*
```

- Scores

```text
Metric Work
- Notes: COL oval emphases for both figures match GT.
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
- Figure 2 (Security framework): The top-center source feeding into â€œDesign Certificationâ€ is â€œStandard Set of Site and Security Characteristics.â€
  Citation: (1167010.pdf, p. 25, Figure 2 â€” â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (Safeguards framework): The top-center source feeding into â€œDesign Certificationâ€ is â€œSNM Form, Enrichment, Quantity, Process Units.â€
  Citation: (1167010.pdf, p. 26, Figure 3 â€” â€œRegulatory Framework for Designing Safeguard Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Top-center sources into Design Certification match GT.
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
According to the UNFSF framework application text, the first two steps in integrating safeguards and security into the facility design are:

1. Identification of applicable regulatory requirements
2. Selection of a common system that shares dual safeguards and security functions

Citation: (1167010.pdf, p. 13, UNFSF framework application text)
```

- Scores

```text
Metric Work
- Notes: Steps do not match GT Section 2 (performance goals; then criteria/requirements from RGs). p.13 citation ≠ E* Section 2 → CiP 0.
- CoP
  - CoP_S: 0.5
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.35
- ViR: 1
Scores
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- CiP: 0
- CiH: 0
- HR: 0.35
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
In Figure 4 of the UNFSF design integration workflow, the two top-level regulatory branches and their explicit CFR citations are:

1. Physical Security â€” â€œ10CFR73â€
2. Safeguards (MC&A) â€” â€œ10CFR74â€

Citation: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Branches and CFR labels match GT; Figure 4 p.27 citation OK.
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
In Figure 4 (UNFSF design integration workflow), both the Physical Security (10 CFR 73) branch and the Safeguards (MC&A) (10 CFR 74) branch share the same pre-integration sequence of design-development boxes:

1. Performance Goal
2. Functional Design Criteria
3. Design Requirements

These then feed into â€œIntegration of Design Requirements (Dual Function)â€.

Citation: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Pre-integration sequence matches GT/F*.
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
  *(1167010.pdf, p. 27, Figure 4)*

- Dual-role concept it represents:
  It represents harmonizing/integrating design requirements that serve a dual function across both regulatory branchesâ€”i.e., requirements that simultaneously support Physical Security (10 CFR 73) and Safeguards/MC&A (10 CFR 74) before proceeding to the unified â€œFinal Designâ€ and subsequent assessment steps.
  *(1167010.pdf, p. 27, Figure 4)*
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
- The assessment step that follows the downstream design progression is â€œPerformance Assessmentâ€ (appearing after â€œFinal Designâ€).

Citation: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design then Performance Assessment match GT; ‘downstream’ wording mildly imprecise vs ‘follows’.
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

- At the Conceptual Design stage:
  - â€œSecurity Assessment Methodsâ€ (feeds into Conceptual Design)
  - â€œSafeguards Assessment Methodsâ€ (feeds into Conceptual Design)
  Citation: (1167010.pdf, p. 27, Figure 4)

- At the Preliminary Design stage:
  - â€œTrade Studiesâ€ (shown feeding into Preliminary Design)
  Citation: (1167010.pdf, p. 27, Figure 4)

- After the Final Design stage (as the iterative check):
  - â€œPerformance Assessmentâ€ (occurs after Final Design, with the NO/YES decision loop)
  Citation: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Assessment methods at Conceptual Design and Trade Studies at Preliminary match GT; extra Performance Assessment after Final not in GT condensed.
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
