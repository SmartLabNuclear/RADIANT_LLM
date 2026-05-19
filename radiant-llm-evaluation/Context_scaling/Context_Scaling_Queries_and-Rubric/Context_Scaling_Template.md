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
- **Vision Language Model (VLM) used to parse the Knowledge Base (KB)**:
- **LLM Model used in RAG**:
- **KB Condition**:
- **Total Queries**: 30
- **Initial setup prompt**:

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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
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
Model Condensed
- 
Extracted Sets
- C
  - 
- F
  - 
K Generated
- 
K Unsupported
- 
```

- Scores

```text
Metric Work
- CoP
  - CoP_S:
  - CoP_N:
- CiP:
- CiH:
- HR:
- ViR:
Scores
- CoP_S:
- CoP_N:
- CoP:
- CiP:
- CiH:
- HR:
- ViR:
```
