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
- **KB Condition**: 20-source KB (`20s`)
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
Within the safetyâ€“securityâ€“safeguards interface discussion, the operational functions shown as common to all three domains (i.e., in the triple-overlap) are:
â€¢    Detection
â€¢    Monitoring
â€¢    MAAs (Material Access Areas)
â€¢    VAs (Vital Areas)
â€¢    Operational safety
â€¢    Locks & keys
These are explicitly depicted as shared/common elements in the schematic. (1167010.pdf, p. 24, Figure 1: â€œSafety, Security, and Safeguards Interfacesâ€)
How this is represented in the domain-interface schematic
The associated schematic is a three-domain interface/overlap diagram (a Venn-style interface figure). The items listed above are placed in the central intersection region where Safety, Security, and Safeguards all overlapâ€”visually indicating these functions are jointly relevant and must be coordinated across all three domains. (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Triple-overlap function list matches GT (Detection, Monitoring, MAAs, VAs, Operational safety, Locks & keys); Venn/center representation correct.
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
How the roles are distinguished in the domain-interface schematics
In the domain-interface schematics, Safety, Security, and Safeguards are shown as three distinct labeled domains (depicted as separate regionsâ€”typically a three-set overlap/â€œVennâ€ style figure). Each domain is explicitly differentiated by its own title and a short descriptive label that states what that domain is trying to protect against or achieve. (1167010.pdf, p. 24, Figure 1: â€œSafety, Security, and Safeguards Interfacesâ€; see also the domain-label text on p. 23)
Primary objective associated with each domain (as conveyed by the visual + labels)
The schematicâ€™s labels associate the following primary objectives with each domain:
â€¢    Safety: Protection of health and safety of the public and the environment.
(1167010.pdf, p. 23; p. 24, Figure 1)
â€¢    Security: Protection against sabotage, malicious acts, and external attacks.
(1167010.pdf, p. 23; p. 24, Figure 1)
â€¢    Safeguards: Deterrence of theft/misuse and prevention/detection of diversion (i.e., ensuring nuclear material is not diverted from peaceful use).
(1167010.pdf, p. 23; p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Venn distinction and three objectives match Figure 1; slight paraphrase on Safeguards + extra p.23 cites.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0.06
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.95
- CiH: 1
- HR: 0.06
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
Systems / operational functions that facilitate Safeguards â†” Security interaction
In the safeguardsâ€“security interface, the operational functions presented as supporting both domains are:
â€¢    Access control
â€¢    Detection
â€¢    Monitoring
â€¢    Surveillance
â€¢    Alarms
â€¢    MAAs (Material Access Areas)
â€¢    VAs (Vital Areas)
â€¢    Locks & keys
These are identified as interface elements linking safeguards objectives (e.g., control/knowledge of nuclear material and its movement) with security objectives (e.g., preventing/detecting unauthorized access or malicious acts). (1167010.pdf, p. 24, Figure 1; see also discussion surrounding the interface elements: 1167010.pdf, p. 7)
How the schematic presents them as supporting both objectives
In the domain-interface schematic (a three-domain overlap diagram), these functions are placed in the overlap region between the â€œSafeguardsâ€ and â€œSecurityâ€ domains (i.e., the shared/interface area), visually indicating they are jointly leveraged to meet both safeguards and security aims rather than belonging uniquely to only one domain. (1167010.pdf, p. 24, Figure 1: â€œSafety, Security, and Safeguards Interfacesâ€)
```

- Scores

```text
Metric Work
- Notes: Full safeguards–security interface list and overlap-region explanation match GT.
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
Within the discussion of integrating safeguards and security into the design of a used nuclear fuel storage facility, the governing regulatory frameworks identified are the U.S. NRC regulations in Title 10 CFR:
â€¢    Physical protection (security): 10 CFR Part 73, â€œPhysical Protection of Plants and Materialsâ€
â€¢    Material control and accounting (MC&A): 10 CFR Part 74, â€œMaterial Control and Accounting of Special Nuclear Materialâ€
Citations: (1167010.pdf, p. 6; 1167010.pdf, p. 7)
```

- Scores

```text
Metric Work
- Notes: Parts 73/74 correctly identified; citations p.6–7 vs E* p.13 sections (same document, acceptable locator drift).
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.9
- CiH: 1
- HR: 0.06
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.9
- CiH: 1
- HR: 0.06
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
Within the used nuclear fuel storage facility design discussion, the document associates the following performance goal/objective with each regulatory framework:
1) Physical protection (Security) â€” 10 CFR Part 73
â€¢    Performance goal/objective:
â€œThe performance goal/objective of the physical security rule is to analyze and establish the security design features that provide minimal reliance on operational program to protect against the design basis threats of theft or diversion of strategic special nuclear materials and radiological sabotage at an early stage.â€
Citation: (1167010.pdf, p. 13)
2) Material control & accounting (Safeguards/MC&A) â€” 10 CFR Part 74
â€¢    Performance goal/objective:
â€œThe performance goal/objective of the Safeguards/MC&A rules is to analyze and establish, at early stage, safeguard features that provide minimal reliance on operational programs to deter, prevent, detect loss or theft or sabotage, or unlawful diversion or unauthorized production of special nuclear materials.â€
Citation: (1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Quoted performance objectives for Parts 73/74 match GT; cites p.13.
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
The facility system identified as having dual safeguards and security functionsâ€”and therefore suitable for early integration into the design of a used nuclear fuel storage facilityâ€”is the:
â€¢    Exit and Entry Control System for Protected Areas
Citation: (1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Correct dual-function system; omits GT sentence that it serves PAs, VAs, and MAAs.
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
A facility system is justified as having dual safeguards and security functions (and thus suitable for early integration into a used nuclear fuel storage facility design) when it is shownâ€”based on applicable regulatory requirements and guidanceâ€”to satisfy both:
1) Physical protection (security) design needs under the NRC physical security rule (10 CFR Part 73), and
2) Material control & accounting (MC&A)/safeguards design needs under the NRC MC&A rules (10 CFR Part 74).
(1167010.pdf, p. 6; 1167010.pdf, p. 7)
Regulatory/selection criteria emphasized in the document
The discussion frames the selection criteria around an early-stage design analysis that:
â€¢    Identifies and assesses applicable regulatory guides and requirements for ISFSI/used-fuel storage facility design, licensing, and operation, and then uses those to
â€¢    Define functional design criteria and design requirements for safeguards and security systemsâ€”supporting selection of systems that can serve both domains.
(1167010.pdf, p. 13)
Why â€œearly integrationâ€ is justified (performance objective basis)
The document ties â€œearly integrationâ€ to the stated performance goal/objective that design features should be established at an early stage with minimal reliance on operational programs:
â€¢    For 10 CFR Part 73 (physical security): early-stage analysis and establishment of security design features to protect against design basis threats, including theft/diversion of strategic SNM and radiological sabotage, with minimal reliance on operations.
â€¢    For 10 CFR Part 74 (Safeguards/MC&A): early-stage analysis and establishment of safeguards features to deter/prevent/detect loss, theft, sabotage, unlawful diversion, or unauthorized production of SNM, with minimal reliance on operations.
(1167010.pdf, p. 13)
How this justifies a â€œdual-functionâ€ system choice
Using those criteria, a system like the Exit and Entry Control System for Protected Areas is justified as â€œdual-functionâ€ because controlled entry/exit/access management is inherently central to meeting security (physical protection) objectives while also supporting safeguards/MC&A (controlled access and accountability-related controls)â€”making it a strong candidate for integration early in facility layout and design.
(1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Overlapping requirements, guidance review, 73.45 example, and early-integration rationale match spirit of GT; NRC RG 5.53 from GT not named explicitly.
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
The scope of application of the framework for integrating safeguards and security into the design of the UNFSF is defined by four elements:
1.    Develop performance goals, functional design criteria, and design requirements for a dual safeguards-and-security systemâ€”including identifying specific requirements and addressing early integration of those requirements.
2.    Identify methods and trade studies.
3.    Describe the performance assessment process.
4.    Highlight the benefits of early-stage integration in the design process.
Citation: (1167010.pdf, p. 13)
```

- Scores

```text
Metric Work
- Notes: Four scope-of-application elements match GT.
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
According to the UNFSF design requirements for SNM doorway monitors (citing the requirements drawn from Regulatory Guide 5.27), the monitors must be able to detect, at minimum:
â€¢    Quantity: 0.5 g of plutonium-239 (Pu-239)
â€¢    Shielding condition: encased in at least 3 mm of brass
â€¢    Confidence level: 90% confidence limit
Citation: (1167010.pdf, p. 16, design requirements discussion for SNM doorway monitors / Regulatory Guide 5.27)
```

- Scores

```text
Metric Work
- Notes: 0.5 g Pu-239, 3 mm brass, 90% confidence match GT; omits <0.1% false-alarm clause; cites RG 5.27 (verify vs source).
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
The maximum false alarm rate specified for SNM doorway monitors in the UNFSF design requirements is:
â€¢    Less than 0.1%.
Citation: (1167010.pdf, p. 15â€“16, design requirements for SNM doorway monitors / discussion drawing from Regulatory Guide 5.27)
```

- Scores

```text
Metric Work
- Notes: <0.1% false alarm rate stated as required; citation grounded to design-requirements pages.
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
According to the UNFSF design requirements for SNM doorway monitors (as discussed in the UNFSF safeguards/security-by-design framework), a doorway monitor must be capable of detecting:
â€¢    Minimum U 233 quantity: 1 gram of U 233 (containing 7â€“10 ppm of U 232)
â€¢    Time window: within 4 hours of removal of all decay products
â€¢    Shielding condition: encased in at least 3 mm of brass
(and installed in locations with minimal background; if installed in high-background areas, sufficient shielding should be provided to maintain sensitivity)
Citations: (1167010.pdf, p. 16, design requirements for SNM doorway monitorsâ€”U 233 requirement; also see background/shielding placement guidance on pp. 16â€“17)
```

- Scores

```text
Metric Work
- Notes: U-233 bundle matches GT; extra background/shielding placement sentence adds HR.
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
Within the UNFSF design requirements (drawing on the cited Regulatory Guide 5.7), the specified minimum detection effectiveness and false alarm thresholds are:
Metal / firearm detectors (handheld or portal)
â€¢    Minimum detection effectiveness: â‰¥ 85% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 10% (when sensitivity is adjusted to achieve the detection effectiveness above)
Citation: (1167010.pdf, p. 17â€“18, design requirements discussion citing Regulatory Guide 5.7)
Explosive detectors
â€¢    Minimum detectable explosive mass: 200 g (for dynamite, TNT, and similar nitrogen-containing compounds)
â€¢    Required detection probability (effectiveness): â‰¥ 90% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 1% (when sensitivity is adjusted to achieve the detection effectiveness above)
Citation: (1167010.pdf, p. 17â€“18, design requirements discussion citing Regulatory Guide 5.7)
```

- Scores

```text
Metric Work
- Notes: Metal/explosive thresholds match GT; ‘Regulatory Guide 5.7’ attribution may be inaccurate vs E* (minor HR/CiP).
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.95
- CiH: 1
- HR: 0.08
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.95
- CiH: 1
- HR: 0.08
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
In Figure 4 (UNFSF design process), after the â€œPerformance Assessmentâ€ decision node:

- YES path: proceeds to â€œFinal Design Optimized and Harmonized.â€
- NO path(s): loop back to â€œFinal Design.â€ (The figure shows two â€œNOâ€ branches, but both feed back to the â€œFinal Designâ€ step.)

PDF evidence: (974767.pdf, p. 20, Figure 4)
```

- Scores

```text
Metric Work
- Notes: YES/NO semantics match GT, but citation is 974767.pdf instead of canonical 1167010.pdf in E* → CiH 0, CiP 0; path content otherwise correct.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0
- CiH: 0
- HR: 0.25
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0
- CiH: 0
- HR: 0.25
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
In Figure 1 (UNFSF 3S interface schematic), the text â€œAccess Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keysâ€ appears in the Safeguardsâ€“Security interface callout box, and its arrow points to the overlap region between the â€œSafeguardsâ€ and â€œSecurityâ€ circles (i.e., the Safeguards/Security overlap).

Source: (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
```

- Scores

```text
Metric Work
- Notes: Callout location correct; Safeguards–Security overlap described (acceptable vs ‘bottom-center’ wording in GT).
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

Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (UNFSF design and regulatory process schematic), the decision step immediately after â€œDesign Security Systemâ€ is:

- â€œ(Evaluation) Objectives Met?â€

Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (UNFSF design and regulatory process schematic), the orange box feeding into â€œDesign Security Systemâ€ lists these two inputs:

1. â€œ-High Assurance â€“DBTâ€
2. â€œ-Mitigation Measuresâ€

Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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

Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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

- Inside the â€œDesign Certificationâ€ oval, the emphasized text is: â€œEmphasis on: Delayâ€
- Inside the â€œCOL Applicationâ€ oval, the emphasized text is: â€œDetection, Delay, Response Assessmentâ€

Source: (1167010.pdf, p. 25â€“26, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (UNFSF design and regulatory process schematic), the central workflow shows 3 main sequential stages:

1. Characterize Facility Design
2. Design Security System
3. (Evaluation) Objectives Met?

Source: (1167010.pdf, p. 25â€“26, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Three central stages match GT.
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
  Source: (1167010.pdf, p. 25, Figure 2)

- â€œDesign Safeguards Systemâ€ appears in Figure 3 (*Regulatory Framework for Designing Safeguard Systems*).
  Source: (1167010.pdf, p. 26, Figure 3)
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

- Figure 2 (security systems): the â€œDesign Certificationâ€ oval emphasizes â€œDelay.â€
  Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (safeguards systems): the â€œDesign Certificationâ€ oval emphasizes â€œDeter, Prevent Theft, Diversion.â€
  Source: (1167010.pdf, p. 26, Figure 3 â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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
In the UNFSF design and regulatory process schematics:

- Figure 2 (Security Systems): the â€œCOL Applicationâ€ oval emphasizes â€œDetection, Delay, Response Assessment.â€
  Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (Safeguards Systems): the â€œCOL Applicationâ€ oval emphasizes â€œDetection, Recovery, Response Assessment.â€
  Source: (1167010.pdf, p. 26, Figure 3 â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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
- Figure 2 (Security systems schematic): the top-center source feeding into â€œDesign Certificationâ€ is â€œStandard Set of Site and Security Characteristics.â€
  Source: (1167010.pdf, p. 25, Figure 2 â€œRegulatory Framework for Designing Security Systemsâ€)

- Figure 3 (Safeguards systems schematic): the top-center source feeding into â€œDesign Certificationâ€ is â€œSNM Form, Enrichment, Quantity, Process Units.â€
  Source: (1167010.pdf, p. 26, Figure 3 â€œRegulatory Framework for Designing Safeguard Systemsâ€)
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
The UNFSF framework application text states that the first two steps for integrating safeguards and security into the facility design are:

1. Identification of applicable regulatory requirements
2. Selection of a common system that shares dual safeguards and security functions

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 6)
```

- Scores

```text
Metric Work
- Notes: Answer lists generic ‘identify requirements / select dual-function system’ vs GT Section 2 steps (performance goals; then criteria/requirements from RGs). Citation p.6 not E* Section 2 → CiP 0, CiH 0.
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
In Figure 4 of the UNFSF design integration workflow, the two top-level regulatory branches are:

1. Physical Security â€” 10 CFR 73
2. Safeguards (MC&A) â€” 10 CFR 74

Source: (1167010.pdf, p. 27, Figure 4 â€œFramework for Integrating Safeguards into Design of Nuclear Facilityâ€; see also p. 23 list of figures referencing 10 CFR 73 for Figure 2 and 10 CFR 74 for Figure 3, which are carried into the Figure 4 integration framework)
```

- Scores

```text
Metric Work
- Notes: Branches and CFR labels match GT; extra cross-refs to pp.23 add minor HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.92
- CiH: 1
- HR: 0.1
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.92
- CiH: 1
- HR: 0.1
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
In Figure 4 (UNFSF design integration workflow), the common sequence of design-development boxes that appears under both the Physical Security (10 CFR 73) branch and the Safeguards (MC&A) (10 CFR 74) branch before integration is:

1. Performance Goal
2. Functional Design Criteria
3. Design Requirements
4. Trade Studies

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Adds ‘Trade Studies’ as a fourth box in the pre-integration sequence; GT condensed lists only Performance Goal → Functional Design Criteria → Design Requirements before integration.
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

This represents the dual-role (dual-function) concept that some design requirements can be integrated because they simultaneously support both:
- Physical security functions, and
- Safeguards / MC&A functions (i.e., â€œdual safeguards and security functionsâ€).

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4; see also p. 6 re: â€œdual safeguards and security functionsâ€)
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
- The assessment step that follows is â€œPerformance Assessment.â€

Source: (1167010.pdf, *Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility*, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design then Performance Assessment match GT.
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
In Figure 4 (UNFSF design integration workflow), the supporting analysis activities shown alongside the design stages are:

- Security Assessment Methods â€” shown feeding into the Conceptual Design stage.
- Safeguards Assessment Methods â€” shown feeding into the Conceptual Design stage.
- Trade Studies (shown on both the Physical Security and the Safeguards/MC&A sides) â€” appear before integration, and feed into the integration that then proceeds to Conceptual Design.
- Performance Assessment â€” appears after Final Design as the assessment/decision step (with YES/NO outcomes).

Source: (1167010.pdf, Badwan & Demuth, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual/Preliminary supporting activities match GT; extra Performance Assessment after Final not in GT condensed.
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
