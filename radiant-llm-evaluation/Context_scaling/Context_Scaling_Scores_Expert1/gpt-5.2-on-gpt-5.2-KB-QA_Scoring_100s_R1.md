# gpt-5.2-on-gpt-5.2-KB-QA_Responses_100s_R1

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
## Response Set

- **Vision Language Model (VLM) used to parse the Knowledge Base (KB)**: GPT-5.2
- **LLM Model used in RAG**: GPT-5.2
- **KB Condition**: 100-sources KB (`100s_R1`)
- **Total Queries**: 30
- **Initial setup prompt**:  For the the questions I will be asking, Do NOT cite any web sources. ONLY focus on the pdf(s) in the working directory? ok?

### Document

    - **Title**: Application of Framework for Integrating Safety, Security and Safeguards (3Ss) into the Design Of Used Nuclear Fuel Storage Facility
    - **Source**: 1167010.pdf (Badwan & Demuth, LA-UR-14-27045, rev.1, 2015)
### Notes:
    - "External URLs are ignored for CiP/CiH scoring."
    - "RADIANT-LLM citations use both PDF-software printed page numbers (indices)."
    - "CiP is expert-verified at the cited location (document/page/figure/section)."
    - "CiH is binary evidence-hit: at least one citation must match a canonical E* evidence item."
    - "HR counts unsupported generated claims, independent of whether it is required by GT."
    - "If a claim is both wrong and unsupported: it increases HR and decreases CoP."

### Q1
- **Query**: What functions are shared across Safety, Security, and Safeguards in the UNFSF framework?

      - **GT Condensed**
        - **"shared across safety–security–safeguards**: Detection, Monitoring, MAAs, VAs, Operational Safety, Locks & Keys"
        - Shown in the central 3-way overlap of the Venn diagram, with a callout listing the shared functions

      - **GT Sets**
        - **E***
          - **"1167010.pdf, Page**: 24, Figure: 1"
        - **F***
          - Detection
          - Monitoring
          - MAAs
          - VAs
          - Operational safety
          - Locks & keys
          - central three-way overlap (Safety ∩ Security ∩ Safeguards)

      - **Model Condensed**
        - States that the local knowledge base does not provide information on shared 3S functions
        - Declines to enumerate any functions or describe the schematic content

      - **Extracted Sets**
        - **C**: []
        - **F**: []
        - **K Generated**: []
        - **K Unsupported**: []

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.0 (no semantic content provided; explicit non-answer)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 0 / 1 = 0.0 (no citations generated)
        - **CiH**: CiH = 0 (no reference to canonical evidence item)
        - **HR**: HR = 0 / 0 = 0.0 (no atomic claims generated)
        - **ViR**: ViR = 0 / 7 = 0.0 (no required visual facts recovered)

      - **Scores**
        - **CoP_S**: 0.0
        - **CoP_N**: null
        - **CoP**: 0.0
        - **CiP**: 0.0
        - **CiH**: 0
        - **HR**: 0.0
        - **ViR**: 0.0

### Q2
- **Query**: What are the primary roles of Safety, Security, and Safeguards?

      - **GT Condensed**
        - **"safety objective**: Protection of health; safety of the public and environment"
        - **"security objective**: Protect against sabotage, malicious acts, and external attacks"
        - **"safeguards objective**: Deter theft, misuse, diversion"
        - Distinguished as three labeled domains with overlaps showing interfaces/shared responsibilities

      - **GT Sets**
        - **E***
          - **"1167010.pdf, Page**: 24, Figure: 1"
        - **F***
          - **"safety objective**: Protection of Health, Safety of the Public and Environment"
          - **"security objective**: Protect Against, Sabotage, Malicious Acts and External Attacks"
          - **"safeguards objective**: Deter, Theft, Misuse, Diversion"
          - three distinct domains (Safety/Security/Safeguards) + overlaps

      - **Model Condensed**
        - Correctly states the primary objectives of Safety, Security, and Safeguards
        - Describes the use of a Venn diagram to show overlaps and shared responsibilities
        - Introduces additional operational functions not explicitly labeled in the UNFSF figure

      - **Extracted Sets**
        - **C**
          - **"1167010.pdf, Page**: 24, Figure: d1478096c577d2a8:p24:f0"
        - **F**
          - three-circle Venn diagram
          - overlap between Safety, Security, and Safeguards
        - **K Generated**
          - Safety aims to protect public health and the environment
          - Security aims to protect against sabotage and malicious acts
          - Safeguards aim to deter theft, misuse, and diversion
          - Monitoring, detection, access control, alarms, and surveillance are integrated across domains
        - **K Unsupported**
          - Monitoring is explicitly listed in the UNFSF schematic
          - Detection is explicitly listed in the UNFSF schematic
          - Access control is explicitly listed in the UNFSF schematic
          - Alarms are explicitly listed in the UNFSF schematic
          - Surveillance is explicitly listed in the UNFSF schematic

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.25 (minimally correct: correct domain objectives but incorrect/overextended schematic interpretation)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 1 / 1 = 1.0 (citation contains a valid 3S Venn diagram)
        - **CiH**: CiH = 1 (citation refers to the canonical evidence item document and figure location)
        - **HR**: HR = 5 / 4 = 0.25 (unsupported functional claims beyond required answer)
        - **ViR**: ViR = 1 / 4 = 0.25 (recognizes Venn structure but misses labeled objectives)

      - **Scores**
        - **CoP_S**: 0.25
        - **CoP_N**: null
        - **CoP**: 0.25
        - **CiP**: 1.0
        - **CiH**: 1
        - **HR**: 0.25
        - **ViR**: 0.25

### Q3
- **Query**: Which functions lie at the interface between safeguards and security?

      - **GT Condensed**
        - **"safeguards–security interface functions include**: Access Control, Detection, Monitoring, Alarms, Surveillance, MAAs, VAs, Locks & Keys"
        - Presented in the overlap region between Safeguards and Security in the schematic
        - Overlap placement indicates the same functions support both safeguards and security objectives

      - **GT Sets**
        - **E***
          - **"1167010.pdf, Page**: 24, Figure: 1"
        - **F***
          - Access control
          - Detection
          - Monitoring
          - Alarms
          - Surveillance
          - MAAs
          - VAs
          - Locks & keys
          - placed in Safeguards ∩ Security overlap

      - **Model Condensed**
        - Provides a conceptual discussion of safeguards–security interaction
        - Does not enumerate specific interface functions from the UNFSF schematic
        - Relies on external 3S literature and abstract interaction reasoning

      - **Extracted Sets**
        - **C**
          - 1644065.pdf, p. 4
          - 2455109.pdf, p. 18
          - 2455109.pdf, p. 31
          - 2455109.pdf, p. 90
        - **F**
          - overlap between safeguards and security (conceptual)
        - **K Generated**
          - Safeguards and security interact through shared concerns about theft and sabotage
          - Design constraints can affect both safeguards and security
          - Physical barriers can serve both safeguards and security purposes
        - **K Unsupported**
          - These functions correspond to those listed in the UNFSF safeguards–security interface
          - UNFSF schematic explicitly shows these functions in the overlap

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.25 (minimal correctness: recognizes interface concept but not required functions)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 3 / 3 = 1.0 (citations support conceptual discussion)
        - **CiH**: CiH = 0 (no citation to expert UNFSF evidence item)
        - **HR**: HR = 2 / 3 = 0.33 (unsupported claims relative to UNFSF schematic)
        - **ViR**: ViR = 0 / 9 = 0.0 (no required visual facts recovered)

      - **Scores**
        - **CoP_S**: 0.25
        - **CoP_N**: null
        - **CoP**: 0.25
        - **CiP**: 1.0
        - **CiH**: 0
        - **HR**: 0.33
        - **ViR**: 0.0

### Q4
- **Query**: Which regulations govern security and safeguards for the UNFSF?

      - **GT Condensed**
        - Physical protection governed by 10 CFR Part 73
        - Material Control & Accounting governed by 10 CFR Part 74

      - **GT Sets**
        - **E***
          - 1167010.pdf, p.13, Section 3.1
        - **F***: []

      - **Model Condensed**
        - Identifies 10 CFR Part 73 as governing physical protection
        - Identifies 10 CFR Part 74 as governing material control and accounting
        - Mentions NRC Regulatory Guide 5.73 as related interface guidance

      - **Extracted Sets**
        - **C**
          - 1167010.pdf, Page 9
          - 1834341.pdf, Page 6
          - 1886489.pdf, Page 19
        - **F**: []

      - **K Generated**
        - Physical protection for UNFSF is governed by 10 CFR Part 73
        - Material control and accounting is governed by 10 CFR Part 74
        - NRC Regulatory Guide 5.73 provides safety/security interface guidance

      - **K Unsupported**
        - Regulatory Guide 5.73 governs security and safeguards for UNFSF

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 1.0 (fully correct identification of governing regulations)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 1 / 3 = 0.33 (only UNFSF source explicitly supports the regulatory claim)
        - **CiH**: CiH = 1 (evidence hit via 1167010.pdf regulatory discussion)
        - **HR**: HR = 1 / 3 = 0.33 (RG 5.73 over-attributed as governing regulation)
        - **ViR**: ViR = null

      - **Scores**
        - **CoP_S**: 1.0
        - **CoP_N**: null
        - **CoP**: 1.0
        - **CiP**: 0.33
        - **CiH**: 1
        - **HR**: 0.33
        - **ViR**: null

### Q5
- **Query**: What is the objective of integrating safeguards and security early in design?

      - **GT Condensed**
        - **"10 CFR 73 objective**: early security design features; protect against theft/diversion and radiological sabotage"
        - **"10 CFR 74 objective**: early safeguards/MC&A features; deter, prevent, detect loss, theft, diversion, unauthorized production"

      - **GT Sets**
        - **E***
          - 1167010.pdf, Section 3.1.1
          - 1167010.pdf, Section 3.1.2
        - **F***: []

      - **Model Condensed**
        - Correctly states general objectives of 10 CFR Part 73 and Part 74
        - Frames objectives as operational protection and accounting goals
        - Does not explicitly mention early design-stage integration or reduced reliance on operational programs

      - **Extracted Sets**
        - **C**
          - 1167010.pdf, Page 13
          - 1834341.pdf, Page 6
        - **F**: []

      - **K Generated**
        - 10 CFR Part 73 aims to protect nuclear facilities against theft, sabotage, and malicious acts
        - 10 CFR Part 74 aims to ensure accurate control and accounting of special nuclear material

      - **K Unsupported**
        - Objectives are explicitly framed as early design integration goals
        - Objectives minimize reliance on operational programs

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.5 (partially correct: correct regulatory intent but misses early-design integration objective central to the question)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 1 / 2 = 0.5 (only 1167010.pdf supports the intended objective framing)
        - **CiH**: CiH = 1 (evidence hit via Section 3.1 discussion)
        - **HR**: HR = 2 / 2 = 1.0 (missing required design-stage qualifiers)
        - **ViR**: ViR = null

      - **Scores**
        - **CoP_S**: 0.5
        - **CoP_N**: null
        - **CoP**: 0.5
        - **CiP**: 0.5
        - **CiH**: 1
        - **HR**: 1.0
        - **ViR**: null

### Q6
- **Query**: Which system is selected to serve dual safeguards and security functions?

      - **GT Condensed**
        - Exit and Entry Control System for Protected Areas selected
        - It serves Protected Areas (PAs), Vital Areas (VAs), and Material Access Areas (MAAs)

      - **GT Sets**
        - **E***
          - **"1167010.pdf, Page**: 13, Section 3.2"
        - **F***: []

      - **Model Condensed**
        - Discusses general safety/security interface frameworks and regulatory context
        - Does not explicitly identify the Exit and Entry Control System
        - Introduces unrelated systems (IAEA C&S, neutrino detectors)

      - **Extracted Sets**
        - **C**
          - 1167010.pdf, Page 6
          - 1167010.pdf, Page 9
          - 1167010.pdf, Page 13
          - 1644065.pdf, Page 10
          - 1826602.pdf, Page 28
          - 1838164.pdf, Page 30
        - **F**: []

      - **K Generated**
        - Dual safeguards and security integration relies on NRC safety/security interface concepts
        - Regulatory frameworks guide early integration of safeguards and security
        - IAEA containment and surveillance systems can support safeguards and security
        - Neutrino detectors could provide additional monitoring capability

      - **K Unsupported**
        - IAEA C&S systems are selected as the UNFSF dual-function system
        - Neutrino detectors are part of the selected UNFSF safeguards–security system

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.25 (minimally correct: remains in-domain and cites correct section, but fails to identify the selected system)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 1 / 6 ≈ 0.17 (only 1167010.pdf p.13 supports the intended claim)
        - **CiH**: CiH = 1 (evidence hit: Section 3.2 cited)
        - **HR**: HR = 2 / 4 = 0.5 (introduction of unsupported systems)
        - **ViR**: ViR = null

      - **Scores**
        - **CoP_S**: 0.25
        - **CoP_N**: null
        - **CoP**: 0.25
        - **CiP**: 0.17
        - **CiH**: 1
        - **HR**: 0.5
        - **ViR**: null

### Q7
- **Query**: Regulatory considerations for selection of a system with dual safeguards and security functions

      - **GT Condensed**
        - Selection of a dual-function system is justified by overlapping safeguards and security requirements
        - Applicable regulatory guides are reviewed to derive functional design criteria and requirements
        - NRC Regulatory Guide 5.53 provides applicability guidance for safeguards and security at an Independent Spent Fuel Storage Installation

      - **GT Sets**
        - **E***
          - 1167010.pdf, PDF p.13–14, Section 3.2
          - 1167010.pdf, PDF p.18, Section 3.3 (RG 5.53 applicability discussion)
        - **F***: []

      - **Model Condensed**
        - Correctly identifies overlap of safeguards and security requirements as justification
        - Mentions NRC Regulatory Guide 5.53 in ISFSI context
        - Introduces additional regulatory frameworks not used for UNFSF system selection

      - **Extracted Sets**
        - **C**
          - 1167010.pdf, Page 6
          - 1167010.pdf, Page 9
          - 1167010.pdf, Page 13
          - 1167010.pdf, Page 14
        - **F**: []

      - **K Generated**
        - Overlapping safeguards and security requirements justify dual-function systems
        - Regulatory guidance is reviewed to derive design criteria
        - RG 5.53 provides guidance for safeguards and security at ISFSIs
        - 10 CFR 73.58 and RG 5.73 guide safety/security interface integration
        - 10 CFR 72 and NUREG-1619 govern ISFSI design and operation

      - **K Unsupported**
        - 10 CFR 73.58 is used to justify dual-function system selection in UNFSF
        - RG 5.73 governs safeguards/security selection for UNFSF
        - NUREG-1619 and DOE-NGSI-SBD-001 are used as selection criteria in the UNFSF framework
        - RG 3.24 is part of the UNFSF system-selection basis

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.5 (partially correct: captures overlap rationale and RG 5.53, but obscures selection logic with unrelated regulatory material)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 2 / 4 = 0.5 (only citations tied to Sections 3.2–3.3 support the intended justification)
        - **CiH**: CiH = 1 (evidence hit: Sections 3.2 and 3.3 cited)
        - **HR**: HR = 4 / 5 = 0.8 (substantial unsupported regulatory overreach)
        - **ViR**: ViR = null

      - **Scores**
        - **CoP_S**: 0.5
        - **CoP_N**: null
        - **CoP**: 0.5
        - **CiP**: 0.5
        - **CiH**: 1
        - **HR**: 0.8
        - **ViR**: null

### Q8
- **Query**: Application scope of the integration framework for safeguards and security

      - **GT Condensed**
        - Develop goals, criteria, and requirements
        - Identify methods and trade studies
        - Describe performance assessment process
        - Highlight benefits of early integration

      - **GT Sets**
        - **E***
          - 1167010.pdf, p. 13, Section 3
        - **F***: []

      - **Model Condensed**
        - Describes framework scope in terms of regulatory identification, system selection, and requirements development
        - Accurately cites Section 3 but omits trade studies, performance assessment, and explicit benefits

      - **Extracted Sets**
        - **C**
          - 1167010.pdf, Page 13
        - **F**: []

      - **K Generated**
        - Framework identifies applicable regulatory requirements
        - Framework selects a common dual-function safeguards and security system
        - Framework develops functional design criteria and requirements
        - Framework integrates safeguards and security design requirements early

      - **K Unsupported**
        - Explicit trade study identification
        - Explicit performance assessment process
        - Explicit articulation of benefits of early integration

      - **Metric Work**
        - **CoP**
          - **CoP_S**: 0.75 (mostly correct: captures core scope elements but omits trade studies, performance assessment, and benefits emphasis)
          - **CoP_N**: null → CoP = CoP_S
        - **CiP**: CiP = 1 / 1 = 1.0 (citation correctly supports framework description)
        - **CiH**: CiH = 1 (evidence hit: Section 3 cited)
        - **HR**: HR = 3 / 4 = 0.75 (missing GT-required scope elements)
        - **ViR**: ViR = null

      - **Scores**
        - **CoP_S**: 0.75
        - **CoP_N**: null
        - **CoP**: 0.75
        - **CiP**: 1.0
        - **CiH**: 1
        - **HR**: 0.75
        - **ViR**: null

    - **Case3 UNFSF Context Expansion**

      - **Q9**: SNM Doorway Monitor Detection Performance (Pu-239)

        - **GT Condensed**
          - Detect 0.5 g Pu-239 in 3 mm brass
          - 90% confidence
          - False alarm rate <0.1%

        - **GT Sets**
          - **E***
            - **"1167010.pdf, Pages**: 15–17, Section 3.3.2"
          - **F***: []

        - **Model Condensed**
          - Correctly states 0.5 g Pu-239 detection
          - Correctly specifies 3 mm brass shielding
          - Correctly specifies 90% confidence
          - Correctly specifies false alarm rate <0.1%

        - **Extracted Sets**
          - **C**
            - 1167010.pdf, Page 16
          - **F**: []

        - **K Generated**
          - Doorway monitor must detect 0.5 g Pu-239
          - Detection applies with 3 mm brass shielding
          - Detection confidence is 90%
          - False alarm rate must be less than 0.1%

        - **K Unsupported**: []

        - **Metric Work**
          - **CoP**
            - **CoP_S**: 1.0 (fully correct semantic description)
            - **CoP_N**: 1.0 (all numeric values correct)
            - **CoP**: 0.6·1.0 + 0.4·1.0 = 1.0
          - **CiP**: CiP = 1 / 1 = 1.0
          - **CiH**: CiH = 1 (evidence hit: Section 3.3.2)
          - **HR**: HR = 0 / 4 = 0.0
          - **ViR**: ViR = null

        - **Scores**
          - **CoP_S**: 1.0
          - **CoP_N**: 1.0
          - **CoP**: 1.0
          - **CiP**: 1.0
          - **CiH**: 1
          - **HR**: 0.0
          - **ViR**: null

      - **Q10**: Maximum specified false alarm rate is <0.1% for SNM doorway monitors

        - **GT Condensed**
          - False alarm rate less than 0.1% for all SNM (Pu-239, U-233, U-232, U-235)

        - **GT Sets**
          - **E***
            - **"1167010.pdf, Pages**: 15–17, Section 3.3.2"
          - **F***: []

        - **Model Condensed**
          - Correctly states maximum false alarm rate <0.1%

        - **Extracted Sets**
          - **C**
            - 1167010.pdf, Page 16
          - **F**: []

        - **K Generated**
          - Maximum false alarm rate for SNM doorway monitors is <0.1%

        - **K Unsupported**: []

        - **Metric Work**
          - **CoP**
            - **CoP_S**: 1.0 (correct and complete)
            - **CoP_N**: 1.0 (numeric requirement correct)
            - **CoP**: 0.6·1.0 + 0.4·1.0 = 1.0
          - **CiP**: CiP = 1 / 1 = 1.0
          - **CiH**: CiH = 1 (evidence hit)
          - **HR**: HR = 0 / 1 = 0.0
          - **ViR**: ViR = null

        - **Scores**
          - **CoP_S**: 1.0
          - **CoP_N**: 1.0
          - **CoP**: 1.0
          - **CiP**: 1.0
          - **CiH**: 1
          - **HR**: 0.0
          - **ViR**: null

      - **Q11**: Uranium Detection Requirements and Time Constraints

        - **GT Condensed**
          - Detect 1 g U-233
          - Within 4 hours of decay product removal
          - Encased in 3 mm brass

        - **GT Sets**
          - **E***
            - 1167010.pdf, Page 16, Section 3.3.2
          - **F***: []

        - **Model Condensed**
          - Correctly states 1 g U-233 detection
          - Correctly states 4-hour time window
          - Correctly states 3 mm brass shielding
          - Adds isotopic context consistent with text

        - **Extracted Sets**
          - **C**
            - 1167010.pdf, Page 16
          - **F**: []

        - **K Generated**
          - Doorway monitor must detect 1 g of U-233
          - Detection must occur within 4 hours of decay product removal
          - Material must be encased in 3 mm brass

        - **K Unsupported**: []

        - **Metric Work**
          - **CoP**
            - **CoP_S**: 1.0 (complete and correct)
            - **CoP_N**: 1.0 (all numeric values correct)
            - **CoP**: 0.6·1.0 + 0.4·1.0 = 1.0
          - **CiP**: CiP = 1 / 1 = 1.0
          - **CiH**: CiH = 1 (evidence hit)
          - **HR**: HR = 0 / 3 = 0.0
          - **ViR**: ViR = null

        - **Scores**
          - **CoP_S**: 1.0
          - **CoP_N**: 1.0
          - **CoP**: 1.0
          - **CiP**: 1.0
          - **CiH**: 1
          - **HR**: 0.0
          - **ViR**: null

      - **Q12**: Metal and Explosive Detector Performance Thresholds

        - **GT Condensed**
          - Metal detection ≥85%
          - Metal false alarm ≤10%
          - Explosive detection ≥200 g
          - Explosive detection ≥90%
          - Explosive false alarm ≤1%

        - **GT Sets**
          - **E***
            - **"1167010.pdf, Pages**: 17–18, Section 3.3.3"
          - **F***: []

        - **Model Condensed**
          - Correctly states metal detector thresholds
          - Correctly states explosive false alarm threshold
          - Omits explicit explosive mass and detection probability

        - **Extracted Sets**
          - **C**
            - 1167010.pdf, Pages 17–18
          - **F**: []

        - **K Generated**
          - Metal detectors require ≥85% detection effectiveness
          - Metal false alarm rate must be ≤10%
          - Explosive false alarm rate must be ≤1%

        - **K Unsupported**
          - Minimum detectable explosive mass (200 g)
          - Explosive detection probability ≥90%

        - **Metric Work**
          - **CoP**
            - **CoP_S**: 0.75 (mostly correct but missing two required explosive performance metrics)
            - **CoP_N**: 0.6 (numeric values present are correct but incomplete)
            - **CoP**: 0.6·0.75 + 0.4·0.6 = 0.69
          - **CiP**: CiP = 1 / 1 = 1.0
          - **CiH**: CiH = 1 (evidence hit)
          - **HR**: HR = 2 / 3 = 0.667
          - **ViR**: ViR = null

        - **Scores**
          - **CoP_S**: 0.75
          - **CoP_N**: 0.6
          - **CoP**: 0.69
          - **CiP**: 1.0
          - **CiH**: 1
          - **HR**: 0.667
          - **ViR**: null

  - **Aggregate Scores**: 100 sources
    - **Mean CoP**: 0.599   # Q1–Q12 (0.00 + 0.25 + 0.25 + 1.00 + 0.50 + 0.25 + 0.50 + 0.75 + 1.00 + 1.00 + 1.00 + 0.69) / 12 = 7.19 / 12 ≈ 0.599
    - **Mean CiP**: 0.708   # Q1–Q12 (0.00 + 1.00 + 1.00 + 0.33 + 0.50 + 0.17 + 0.50 + 1.00 + 1.00 + 1.00 + 1.00 + 1.00) / 12 = 8.50 / 12 ≈ 0.708
    - **Mean CiH**: 0.750   # Q1–Q12 (0 + 1 + 0 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1) / 12 = 9 / 12 = 0.750
    - **Mean HR**: 0.467   # Q1–Q12 (0.00 + 0.25 + 0.33 + 0.33 + 1.00 + 0.50 + 0.80 + 0.75 + 0.00 + 0.00 + 0.00 + 0.667) / 12 ≈ 5.60 / 12 ≈ 0.467
    - **Mean ViR**: 0.083   # Q1–Q3  (0.00 + 0.25 + 0.00) / 3 = 0.25 / 3 ≈ 0.083
