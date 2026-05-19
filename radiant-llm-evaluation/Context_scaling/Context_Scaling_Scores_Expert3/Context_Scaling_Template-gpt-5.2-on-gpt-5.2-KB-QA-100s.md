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
- **KB Condition**: 100-source KB (`100s_R2`)
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
Operational functions shared across safety, security, and safeguards (all three)
In the safetyâ€“securityâ€“safeguards interface discussion, the operational functions shown as shared across all three domains are:
â€¢    Detection
â€¢    Monitoring
â€¢    MAAs (Material Access Areas)
â€¢    VAs (Vital Areas)
â€¢    Operational Safety
â€¢    Locks & Keys
Citations: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 7; p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
How this is represented in the domain-interface schematic
The associated schematic is a three-circle (Venn-style) domain-interface diagram for Safety, Security, and Safeguards. The functions listed above are depicted as the central, triple-overlap set (common to all three domains) and are presented via a callout box connected to that center overlap by an arrow/leader line.
Citation: (1167010.pdf, p. 24, Figure 1)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Triple-overlap list matches GT (six functions); schematic/callout description correct; trailing season line is irrelevant HR.
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
The schematic distinguishes Safety, Security, and Safeguards by presenting them as three separately labeled domains arranged as an overlapping, three-circle (Venn-type) interface diagram. Each circle represents one domain, and the overlaps visually indicate where functions/interfaces can be shared or coordinated across domains. (1167010.pdf, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
Primary objective associated with each domain (as conveyed by the labels)
From the figureâ€™s labels, the primary objective associated with each domain is:
â€¢    Safety: â€œProtection of Health, Safety of the Public and Environmentâ€ (1167010.pdf, p. 24, Figure 1)
â€¢    Security: â€œProtect Against Sabotage, Malicious Acts and External Attacksâ€ (1167010.pdf, p. 24, Figure 1)
â€¢    Safeguards: â€œDeter, Theft, Misuseâ€ and â€œDiversionâ€ (i.e., deterrence of theft/misuse and diversion). (1167010.pdf, p. 24, Figure 1)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Venn layout and three domain objectives match Figure 1; minor interpretive gloss on Safeguards; season line HR.
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
In the safetyâ€“securityâ€“safeguards interface discussion and associated schematic, the operational functions presented as facilitating interaction between the Safeguards and Security domains are:
â€¢    Access Control
â€¢    Detection
â€¢    Monitoring
â€¢    Alarms
â€¢    Surveillance
â€¢    MAAs (Material Access Areas)
â€¢    VAs (Vital Areas)
â€¢    Locks & Keys
Source: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 24, Figure 1 â€œSafety, Security, and Safeguards Interfacesâ€)
How the schematics present these functions as supporting both objectives
In Figure 1, these functions are shown in a callout box connected by an arrow into the overlap region between the â€œSafeguardsâ€ and â€œSecurityâ€ circles of the Venn-style interface schematicâ€”indicating they are shared interface functions that simultaneously support:
â€¢    Security objectives (protection against sabotage/malicious acts/external attacks), and
â€¢    Safeguards objectives (deterrence/detection related to theft/misuse/diversion).
Source: (1167010.pdf, p. 24, Figure 1)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Full safeguards–security function list and overlap placement match GT; season line HR.
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
Within the UNFSF design-integration discussion, the regulatory frameworks identified are:
â€¢    Physical protection (security): 10 CFR Part 73 (Physical Protection of Plants and Materials).
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 13)
â€¢    Material control & accounting (MC&A): 10 CFR Part 74 (Material Control and Accounting of Special Nuclear Material).
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 13; p. 23)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Parts 73/74 correct; cites p.13 plus auxiliary p.23.
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
Within the UNFSF design-integration discussion, the report associates the following performance goals/objectives with the two key regulatory frameworks:
1.    Physical protection â€” 10 CFR Part 73 (Security)
o    Performance goal/objective: to analyze and establish security design features at an early stage that provide minimal reliance on the operational program, in order to protect against design basis threats involving theft or diversion of strategic SNM and radiological sabotage.
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 13, â€œPhysical Protection (10 CFR Part 73)â€)
2.    Material control & accounting â€” 10 CFR Part 74 (Safeguards/MC&A)
o    Performance goal/objective: to analyze and establish safeguards features at an early stage that provide minimal reliance on operational programs, to deter, prevent, and detect the loss/theft, sabotage, unlawful diversion, or unauthorized production of special nuclear material.
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 23, â€œMaterial Control and Accounting / Safeguards/MC&A (10 CFR Part 74)â€)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Performance objectives for Parts 73/74 match GT; Part 74 block cites p.23 (acceptable).
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 0.92
- CiH: 1
- HR: 0.05
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 0.92
- CiH: 1
- HR: 0.05
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
The facility system identified as having dual safeguards and security functionsâ€”and therefore suitable for early integration into the design of a used nuclear fuel storage facility (UNFSF)â€”is the:
â€¢    Exit and Entry Control System for Protected Areas (PAs) (discussed in the context of PAs and also referenced alongside VAs and MAAs).
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 13)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Exit/Entry Control system correct; explicitly ties PAs/VAs/MAAs in prose → satisfies GT detail.
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
A facility system is justified as having dual safeguards and security functions (and thus a strong candidate for early integration in a Used Nuclear Fuel Storage Facility (UNFSF) design) when regulatory requirements and guidance show that the same engineered system can satisfy both:
â€¢    physical protection (security) requirements, and
â€¢    material control & accounting / safeguards (MC&A)-related objectives,
using shared functional design criteria.
Criteria / regulatory considerations cited in the UNFSF framework discussion
1.    It is traceable to both regulatory frameworks (security + safeguards).
The framework explicitly grounds design integration in the two governing rule sets: 10 CFR Part 73 (physical protection) and 10 CFR Part 74 (MC&A/safeguards). A â€œdual-functionâ€ system is one whose requirements can be derived from both sets and integrated early in design.
Citations: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 6; p. 9)
2.    Its selection is supported by review of applicable regulatory guidance used to derive functional design criteria/design requirements.
The document describes selecting a â€œcommon system that shares safeguards and security functionâ€ after reviewing applicable guidance, and then developing performance goals, functional design criteria, and design requirements for that system.
Citation: (1167010.pdf, p. 13, discussion of selecting a common dual-function system and deriving criteria/requirements)
3.    It satisfies explicit physical protection entry/exit performance requirements tied to SNM removal (a security requirement that overlaps safeguards intent).
For the chosen example system (protected-area exit/entry control), the basis includes 10 CFR 73.45(b), which requires entry/exit techniques able to detect, assess, and communicate attempts at unauthorized removal of special nuclear material (SNM)â€”linking access control directly to material-related outcomes central to safeguards.
Citation: (1167010.pdf, p. 14, Access Control System provided to meet 10 CFR 73.45(b))
4.    It combines subsystems that directly serve both domainsâ€™ objectives (material detection + adversary interdiction).
The selected Access Control / Exit-Entry Control System is described as including both radiation/SNM detection and metal/explosive detection, supporting safeguards-relevant material monitoring and security-relevant threat/interdiction functions in one integrated system.
Citation: (1167010.pdf, p. 14, description of system components)
Season (Northern Hemisphere, meteorological): Winter________________________________________
```

- Scores

```text
Metric Work
- Notes: Dual-function justification strong; GT’s RG 5.53 not named explicitly; season/underscore artifact HR.
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
The scope of the application of the framework for integrating safeguards and security into the design of the UNFSF is defined by four elements:
1.    Develop the performance goals, functional design criteria, and design requirements for a system with dual safeguards and security functions (including identifying the specific requirements for that system and addressing early integration of those requirements).
2.    Identify applicable methods and trade studies.
3.    Describe the performance assessment process.
4.    Highlight the benefits of early-stage integration into the design.
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 13, â€œScope of the applicationâ€)
Season (Northern Hemisphere, meteorological): Winter
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
Per the UNFSF design requirements for SNM doorway monitors (plutonium detection), the monitor must be capable of detecting:
â€¢    Minimum quantity: 0.5 g of Pu 239
â€¢    Shielding condition: encased in a minimum of 3 mm of brass
â€¢    Confidence level: 90% confidence limit
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 16, SNM doorway monitor design requirements)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Pu-239, brass, 90% confidence match GT; omits <0.1% false-alarm clause in condensed answer.
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
The UNFSF design requirements specify that SNM doorway monitors should have a false alarm rate less than 0.1%.
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 15â€“16, SNM doorway monitor design requirements)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: States <0.1% false alarm rate; season line minor HR.
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
â€¢    Minimum U 233 quantity: 1 gram of U 233 (containing 7â€“10 ppm U 232)
â€¢    Time window: within 4 hours of removal of all decay products
â€¢    Shielding condition: encased in at least 3 mm of brass
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 16, SNM doorway monitor design requirements)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: U-233 bundle matches GT; season line HR.
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
Metal (firearm) detectors â€” minimum performance requirements
â€¢    Minimum detection effectiveness: â‰¥ 85% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 10% (with sensitivity adjusted to achieve the 85% detection level)
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, p. 17, metal/firearm detector requirements)
Explosive detectors â€” minimum performance requirements
â€¢    Minimum detectable explosive mass: 200 g of dynamite, TNT, or similar nitrogen-containing compounds
â€¢    Required detection probability (effectiveness): â‰¥ 90% effective detection rate
â€¢    Maximum false alarm rate: â‰¤ 1% (with sensitivity adjusted to achieve the 90% detection level)
Citation: (1167010.pdf, Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility, pp. 17â€“18, explosive detector requirements)
Season (Northern Hemisphere, meteorological): Winter
```

- Scores

```text
Metric Work
- Notes: Metal/explosive thresholds match GT; season line HR.
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
In Figure 4 (UNFSF design/integration framework), after the â€œPerformance Assessmentâ€ decision node:

- YES path: proceeds to â€œFinal Design Optimized and Harmonizedâ€.
- NO path(s): loop back to â€œFinal Designâ€ (i.e., the NO branches return to the â€œFinal Designâ€ box for revision before reassessment).

Source: (1167010.pdf, p. 27, Figure 4).
```

- Scores

```text
Metric Work
- Notes: YES/NO paths after Performance Assessment match GT; minor reassessment wording.
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
In Figure 1 (UNFSF 3S interface schematic), the text â€œAccess Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keysâ€ is contained in the bottom-center red callout box. The arrow from this box points upward into the lower central overlap region of the Venn diagramâ€”i.e., the lower portion of the triple-overlap (Safetyâ€“Securityâ€“Safeguards) region.

Source: (1167010.pdf, p. 24, Figure 1)
```

- Scores

```text
Metric Work
- Notes: Callout box correct; arrow described as lower triple-overlap (Safety∩Security∩Safeguards) vs GT Safeguards∩Security for this callout.
- CoP
  - CoP_S: 0.25
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 0.5
Scores
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- CiP: 1
- CiH: 1
- HR: 0
- ViR: 0.5
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

- Orange box feeding into â€œDesign Security Systemâ€:
â€œ-High Assurance â€“DBTâ€ and â€œ-Mitigation Measuresâ€

- Green â€œDesign Certificationâ€ oval (emphasis inside):
â€œEmphasis on: Delayâ€

Source: (1167010.pdf, p. 25, Figure 2: â€œRegulatory Framework for Designing Security Systemsâ€)
```

- Scores

```text
Metric Work
- Notes: Orange box and Design Certification / COL emphases match GT.
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

- â€œ(Evaluation) Objectives Metâ€

Source: (1167010.pdf, p. 25, Figure 2)
```

- Scores

```text
Metric Work
- Notes: Next decision after Design Security System matches GT.
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
In Figure 2 (UNFSF design and regulatory process schematic), the orange input box feeding into â€œDesign Security Systemâ€ lists these two inputs:

1. High Assurance â€“ DBT
2. Mitigation Measures

Source: (1167010.pdf, p. 25, Figure 2, â€œRegulatory Framework for Designing Security Systemsâ€)
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
In Figure 2 (UNFSF design and regulatory process schematic), under â€œDefine Objectivesâ€ the two listed items are:

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

- Design Certification oval: â€œEmphasis on: Delayâ€
- COL Application oval: â€œEmphasis on: Detection, Delay, Response Assessmentâ€

Source: (1167010.pdf, p. 25â€“26, Figure 2)
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
3. (Evaluation) Objectives Met

Source: (1167010.pdf, p. 25â€“26, Figure 2)
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
- â€œDesign Security Systemâ€ appears in Figure 2 (â€œRegulatory Framework for Designing Security Systemsâ€).
Source: (1167010.pdf, p. 25, Figure 2)

- â€œDesign Safeguards Systemâ€ appears in Figure 3 (â€œRegulatory Framework for Designing Safeguard Systemsâ€ / â€œRegulatory Framework for Designing Safeguards System (10 CFR 74)â€).
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
- Figure 2 (Security system schematic) â€” inside the â€œDesign Certificationâ€ oval, the emphasized text is: â€œEmphasis on: Delayâ€.
Source: (1167010.pdf, p. 25, Figure 2)

- Figure 3 (Safeguards system schematic) â€” inside the â€œDesign Certificationâ€ oval, the emphasized text is: â€œEmphasis on: Deter, Prevent Theft, Diversionâ€.
Source: (1167010.pdf, p. 26, Figure 3)
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
In the UNFSF design and regulatory process schematics, the ?COL Application? oval highlights different assessment emphases:

- Figure 2 (Security systems framework): emphasizes Detection, Delay, and Response Assessment.
Source: (1167010.pdf, p. 25, Figure 2)

- Figure 3 (Safeguards systems framework): emphasizes Detection, Recovery, and Response Assessment.
Source: (1167010.pdf, p. 26, Figure 3)
```

- Scores

```text
Metric Work
- Notes: COL emphases match GT; typographic ‘?COL?’ noise negligible HR.
- CoP
  - CoP_S: 1
  - CoP_N:
- CiP: 1
- CiH: 1
- HR: 0.03
- ViR: 1
Scores
- CoP_S: 1
- CoP_N:
- CoP: 1
- CiP: 1
- CiH: 1
- HR: 0.03
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
- Figure 2 (Security system schematic): the top-center source feeding into â€œDesign Certificationâ€ is
â€œStandard Set of Site and Security Characteristics.â€

- Figure 3 (Safeguards system schematic): the top-center source feeding into â€œDesign Certificationâ€ is
â€œSNM Form, Enrichment, Quantity, Process Units.â€

Source: (1167010.pdf, p. 25, Figure 2; p. 26, Figure 3)
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

1. Identification of applicable regulatory requirements
2. Selection of a common system that shares dual safeguards and security functions

Source: (1167010.pdf, p. 13, UNFSF framework application text)
```

- Scores

```text
Metric Work
- Notes: Generic two steps vs GT Section 2 wording; p.13 citation not E* Section 2 → CiP 0, CiH 0.
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
In Figure 4 (UNFSF design integration workflow), the two top-level regulatory branches are:

1. Physical Security â€” explicitly tied to 10 CFR 73 (Physical Protection of Plants and Materials).
2. Safeguards (MC&A) â€” explicitly tied to 10 CFR 74 (Material Control and Accounting of Special Nuclear Material).

Sources: (1167010.pdf, p. 27, Figure 4; 1167010.pdf, p. 13, Safeguards and Security Rules and Regulations)
```

- Scores

```text
Metric Work
- Notes: Figure 4 branches and CFR labels match GT; extra p.13 cite minor HR.
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
In Figure 4 (UNFSF design integration workflow), both the Physical Security branch and the Safeguards (MC&A) branch show the same pre-integration sequence of design-development boxes:

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
In Figure 4 (UNFSF design integration workflow), the central integration box is labeled:

- â€œIntegration of Design Requirements (Dual Function)â€

It represents the dual-role concept of integrating physical security and safeguards (MC&A) design requirements into a single, unified set of dual-function design requirements that can be carried forward into the facility design process.

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

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual Design and Performance Assessment match GT.
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
In Figure 4 (UNFSF design integration workflow), the supporting analysis activities shown alongside the design stagesâ€”and where they appearâ€”are:

- Security Assessment Methods â†’ feed into the Conceptual Design stage.
- Safeguards Assessment Methods â†’ feed into the Conceptual Design stage.
- Trade Studies (shown on both the Physical Security and Safeguards sides) â†’ feed into the Preliminary Design stage.
- Performance Assessment (decision node) â†’ occurs after Final Design (NO loops back to Final Design; YES proceeds to Final Design Optimized and Harmonized).

Source: (1167010.pdf, p. 27, Figure 4)
```

- Scores

```text
Metric Work
- Notes: Conceptual/Preliminary supporting boxes match GT; Performance Assessment after Final is extra vs GT condensed.
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
