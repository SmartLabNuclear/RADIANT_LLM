# Page-Level Scoring Template
# Benchmark Family: Page-Level

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
- Model: GPT-4.1
- Total Queries: 30
- alpha: 0.6

### Notes
- Page-level benchmark scoring focuses on CoP, HR, and ViR; CiP/CiH are defined here for vocabulary consistency but are not averaged in the page-level summary tables.
- Citation strings are retained for provenance review, but exact page-string equality is not required when the evidence item is otherwise unambiguous.
- If a claim is both wrong and unsupported: it increases HR and decreases CoP.

## Calculus Parabolic Gate / Ellipse Geometry

#### Source: Calculus_p116_73.pdf

### Q1
- Query: From Fig. 51, what are the explicitly labeled geometric dimensions of the schematic (horizontal and vertical), and are these dimensions plotted axes or physical lengths?
- GT

```text
GT Condensed
- The horizontal dimension is labeled 10 ft and the vertical dimension is 6 ft.
- These are physical geometric lengths, not plotted x–y axes.
GT Sets
- E*:
  - Calculus_p116_73.pdf, p.1, Fig. 51
- F*:
  - Horizontal arrow label: 10', => 10 ft
  - Vertical arrow label: 6', => 6 ft
  - Parabola with a base labeled "0"
  - A chord intersecting at two points; "A" on the left, and "B" on the right
```

- Model Answer

```text
- "Claims horizontal dimension labeled as 4"
- "Interprets x and y as plotted axes"
- "Explicitly states dimensions are not physical lengths"
```

- Scores: CoP **0** | HR **0.6667** | ViR **0.25**

```text
Metric Work
- CoP note: Condensed answer is wrong on dimensions (4 vs 10 ft), misclassifies schematic as plotted axes, and contradicts GT that labels are physical lengths. CoP_S = 0 (incorrect).
- HR note: Treating the three bullets as generated factual claims, two are clearly unsupported vs Fig. 51 / GT (fabricated “4”; axes-as-plotted); the third is also false vs GT but counted with your split → |K_unsupported| = 2, |K_generated| = 3 → HR = 2/3.
- ViR note: |F*| = 4; at most one visual element plausibly aligns with recovered content in your scheme → ViR = 1/4 = 0.25 (matches your summary).
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 0.6667
- ViR: 0.25
```

### Q2
- Query: Does the figure depict plotted x–y axes with tick marks, or a geometric schematic with physical dimensions? Justify using only visible labels.
- GT

```text
GT Condensed
- The figure is a geometric schematic with physical dimensions, not a plotted graph with axes or tick marks.
GT Sets
- E*:
  - Calculus_p116_73.pdf, p.1, Fig. 51
- F*:
  - Horizontal arrow label: 10', => 10 ft
  - Vertical arrow label: 6', => 6 ft
  - Parabola with a base labeled "0"
  - A chord intersecting at two points; "A" on the left, and "B" on the right
  - Presence of dimension labels
  - Absence of axis ticks or numeric scales
```

- Model Answer

```text
- "Correctly classifies figure as schematic"
- "Incorrectly claims x–y axes are present"
- "Uses fabricated dimension label '4'"
```

- Scores: CoP **0** | HR **0.6667** | ViR **0.175**

```text
Metric Work
- CoP note: GT requires schematic with physical dimensions and no axis ticks; model correctly notes schematic but also asserts x–y axes and fabricated “4”, so the overall condensed answer is incorrect → CoP_S = 0.
- HR note: Same 3-claim accounting as Q1: two clear hallucinations/unsupported claims (axes present; “4”) → HR = 2/3 (aligned with your summary).
- ViR note: |F*| = 7; schematic/dimension facts largely not recovered correctly → ViR ≈ 0.175 per your calibration (≈1.2/7 if interpreted as partial overlap with dimension-label presence).
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 0.6667
- ViR: 0.175
```

### Q3
- Query: What ellipse equation is explicitly shown adjacent to the figure, and what semi-axis lengths does it imply?
- GT

```text
GT Condensed
- The equation is x^2/64 + y^2/36 = 1,
- The implied semi-axes are 8 (horizontal)and 6 (vertical).
GT Sets
- E*:
  - Calculus_p116_73.pdf, p.1, text near Fig. 51
- F*:
  - Equation: x^2/64 + y^2/36 = 1
```

- Model Answer

```text
- "Correctly reproduces ellipse equation"
- "Correctly derives a = 8 and b = 6"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT condensed equation and semi-axes (8 horizontal, 6 vertical). CoP_S = 1 (fully correct).
- HR note: Both summary claims are correct vs E*; no unsupported factual additions in this decomposition → HR = 0/2 = 0.
- ViR note: F* is the displayed equation; model recovers it explicitly → |F_i ∩ F*| / |F*| = 1/1 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q4
- Query: What are the implied full coordinate extents of the ellipse based on the displayed equation?
- GT

```text
GT Condensed
- The ellipse spans from x = −8 to +8 and y = −6 to +6.
GT Sets
- E*:
  - Calculus_p116_73.pdf, p.1, ellipse equation
- F*:
  - Denominators 64 and 36 in ellipse equation
```

- Model Answer

```text
- "Correctly derives x and y coordinate ranges"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: GT extents x ∈ [−8,8], y ∈ [−6,6] follow from the equation; summary states correct derivation → CoP_S = 1.
- HR note: Single claim, correct → HR = 0/1 = 0.
- ViR note: F* lists denominators 64 and 36; correct range statement encodes both visually implied parameters → treat as full recovery of the two-item F* → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q5
- Query: According to Fig. 51 and the accompanying text, which physical quantities are to be calculated for the vertical parabolic gate, and are any geometric dimensions stated in the text that differ from those shown in the figure?
- GT

```text
GT Condensed
- Problem 1 requires calculating the pressure on the parabolic gate if the edge AB lies on the water surface and 5 ft below the surface.
- Problem 2 requires calculating the pressure on the semicircular gate whose diameter is 10 ft long and lies on the surface of the water
- No; the figure provides a horizontal width of 10 ft and a vertical depth of 6 ft
- 5 ft in problem 1 is just a position, not a dimension.
GT Sets
- E*:
  - Calculus_p116_73.pdf, p.1, Fig. 51
  - Calculus_p116_73.pdf, p.1, problem statement text
- F*:
  - Horizontal dimension labeled 10 ft
  - Vertical dimension labeled 6 ft
  - If the edge lies 5 ft below the surface
```

- Model Answer

```text
- "Correctly identifies hydrostatic pressure to compute"
- "Incorrectly states base width is labeled as 4"
- "Claims no discrepancy between text and figure"
```

- Scores: CoP **0.25** | HR **0.6667** | ViR **0**

```text
Metric Work
- CoP note: GT requires two pressure problems (parabolic + semicircular), correct 10 ft / 6 ft vs text, and clarifies 5 ft as depth not a conflicting dimension. Model only loosely names hydrostatic pressure, fabricates “4”, and wrongly denies text–figure discrepancy → CoP_S = 0.25 (minimally correct fragment).
- HR note: |K_generated| = 3; unsupported/wrong vs GT: fabricated base width “4”; “no discrepancy” → |K_unsupported| = 2 → HR = 2/3.
- ViR note: F* has three visual/text facts (10 ft, 6 ft, 5 ft condition); none are recovered correctly → ViR = 0/3 = 0.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.6667
- ViR: 0
```

## Homogeneous Cylindrical Reactor - Flux and Heat Generation

#### Source: Todreas_and_Kazimi_p53.pdf

### Q6
- Query: What spatial directions and coordinate references are explicitly labeled in Figure 3-3 for the homogeneous cylindrical reactor, and how are the radial and axial dimensions indicated?
- GT

```text
GT Condensed
- Figure 3-3 explicitly indicates the axial direction (z) and the radial direction (r). Not expliitly labelled but implied - The reactor is shown as a right circular cylinder with axial height and radial extent indicated schematically, without numeric dimension values. - "Cylindrical geometry shown implied" - 11 variables labelled:
- Neutron fluxes and volumetric heat-generation rate profiles: ϕ(r), ϕ(z), q'''(r)
- Radial Markers:  r = 0, R, Re"
- Axial Markers: z = 0, +L/2, -L/2 +Le/2, -Le/2
GT Sets
- E*:
  - Todreas_and_Kazimi_p53.pdf, p. 53, Figure 3-3
- F*:
  - 11 variables labelled
  - Right circular cylinder with axial height and radial extent indicated schematically
  - Shape functions for flux and heat generation present: ϕ(r), ϕ(z), q'''(r)
```

- Model Answer

```text
- "Identifies radial coordinate r and radius R"
- "Introduces extrapolated boundary R₀ (instead of R_e)"
- "Claims axial direction has no explicit coordinate symbol"
- "Misses axial markers ±L/2 and ±L_e/2"
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.3333**

```text
Metric Work
- CoP note: GT requires z and r, many labeled markers (±L/2, ±L_e/2, r=0,R,Re), and flux/heat labels. Model partially names r/R but invents R₀ and falsely denies explicit axial symbols while missing ±L/2, ±L_e/2 → CoP_S = 0.25 (minimally correct).
- HR note: Four decomposition lines; two assert incorrect figure content (R₀; “no explicit axial coordinate symbol”) → |K_unsupported| = 2, |K_generated| = 4 → HR = 0.5.
- ViR note: F* has three grouped visual facts; roughly one cluster (radial r/R) partially aligns → ViR ≈ 1/3 = 0.3333.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.5
- ViR: 0.3333
```

### Q7
- Query: According to Figure 3-3, how do the neutron flux and heat-generation rate profiles vary radially and axially within the homogeneous cylindrical reactor?
- GT

```text
GT Condensed
- Both neutron fluxes and volumetric heat-generation rate vary spatially in the radial and axial directions;
- They peak near the core center (z= 0, r = 0) and decrease toward the boundaries in both directions.
- They both approximate to zero at the extrapolated boundaries (+Le/2, -Le/2, +re, -Re).
GT Sets
- E*:
  - Todreas_and_Kazimi_p53.pdf, p. 53, Figure 3-3
- F*:
  - Radial and axial profiles of neutron flux: ϕ(r), ϕ(z)
  - Radial profile of evidence (E_star): heat-generation rate: q'''(r)
```

- Model Answer

```text
- "Correctly describes center-peaked radial profiles"
- "Correctly relates heat generation to flux"
- "Introduces axial behavior not explicitly shown in figure"
- "Claims parabolic shape"
```

- Scores: CoP **0.5** | HR **0.25** | ViR **0.6667**

```text
Metric Work
- CoP note: Center-peaked radial behavior and flux–heat link match GT; “parabolic” overspecifies the plotted shape vs GT; axial “not explicitly shown” is a caveat, not GT content → CoP_S = 0.5 (partially correct).
- HR note: Four lines; one asserts an unsupported functional form (“parabolic”) → HR = 1/4 = 0.25.
- ViR note: F* lists ϕ(r), ϕ(z), q′′′(r); model’s summary aligns with radial profile and q′′′ coupling, weaker on explicit ϕ(z) → ViR ≈ 2/3 = 0.6667.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.25
- ViR: 0.6667
```

### Q8
- Query: What equation is given on this page for the overall core heat-generation rate, and what physical quantity is being integrated?
- GT

```text
GT Condensed
- The page presents an equation for the overall core heat-generation rate defined as a volume integral of the local volumetric heat-generation rate over the reactor core: $$\dot{Q} = q_{\rm max}^{\prime\prime\prime} \int\!\!\!\!\int\limits_{V_{\rm core}} F(\widehat{r})\, dV$$
GT Sets
- E*:
  - Todreas_and_Kazimi_p53.pdf, p. 53, Eq. (3-36)
- F*:
```

- Model Answer

```text
- "Correctly reproduces structure of Eq. 3-36"
- "Correctly identifies integrated quantity"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT Eq. (3-36) structure and identifies integration of volumetric heat generation over V_core → CoP_S = 1.
- HR note: Both summary claims correct; F* empty in rubric → no extra visual hallucinations counted here → HR = 0/2 = 0.
- ViR note: |F*| = 0 in template GT sets → define ViR = 1 by convention (no visual facts required); alternatively leave as full credit for equation-only item.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q9
- Query: What explanation does the text provide for the flattening of radial and axial power profiles in real reactors compared to the idealized profiles shown in Figure 3-3?
- GT

```text
GT Condensed
- The text explains that "In real reactors, the higher burnup of fuel at locations of high neutron fluxes leads to flattening of radial and axial power profiles".
GT Sets
- E*:
  - Todreas_and_Kazimi_p53.pdf, p. 53, explanatory text below Eq. (3-36)
- F*:
```

- Model Answer

```text
- "Correctly attributes flattening to burnup and reactivity reduction"
```

- Scores: CoP **0.75** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: GT cites higher burnup at high-flux locations; model adds “reactivity reduction,” which is not verbatim GT though related → CoP_S = 0.75 (mostly correct).
- HR note: Single bundled claim; burnup portion is GT-aligned so not counted as unsupported hallucination for HR → HR = 0/1 = 0.
- ViR note: F* empty → ViR = 1 by convention.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0
- ViR: 1
```

### Q10
- Query: How does Figure 3-3 visually support the text’s discussion of neutron flux and heat-generation behavior in a homogeneous cylindrical reactor?
- GT

```text
GT Condensed
- Figure 3-3 visually illustrates the spatial variation of neutron flux and heat-generation rate that the text describes analytically.
- These fluxes peaking near the core center (z= 0, r = 0) and decreasing toward the boundaries in both directions.
- They approximate to zero at the extrapolated boundaries (+Le/2, -Le/2, +re, -Re), reinforcing the relationship between reactor geometry and volumetric power distribution.
GT Sets
- E*:
  - Todreas_and_Kazimi_p53.pdf, p. 53, Figure 3-3
  - Todreas_and_Kazimi_p53.pdf, p. 53, surrounding explanatory text
- F*:
  - Consistency between plotted profiles (axial, radial curves and textual description
```

- Model Answer

```text
- "Correctly describes radial profiles and extrapolated boundary"
- "Does not identify axial markers"
- "Over-asserts axial behavior"
```

- Scores: CoP **0.5** | HR **0.3333** | ViR **0.5**

```text
Metric Work
- CoP note: Captures radial peaking and extrapolated boundary (matches GT in part) but omits axial marker detail and over-asserts axial behavior per summary → CoP_S = 0.5 (partially correct).
- HR note: Three lines; one flags incorrect over-assertion on axial behavior (counted as unsupported vs figure/GT emphasis) → HR ≈ 1/3 = 0.3333.
- ViR note: F* is a single “consistency” visual relation; partial capture of radial+boundary vs missing explicit axial consistency → ViR = 0.5.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.3333
- ViR: 0.5
```

## Cylindrical Reactor Shield Geometry

#### Source: Todreas_and_Kazimir_p62.pdf

### Q11
- Query: What radii are explicitly labeled for the thermal shield in Fig. 3-7 and what do they represent?
- GT

```text
GT Condensed
- The thermal shield radii are labeled as R = 1.206 (internal radius) m and R = 1.333 m (external radius).
- # factual_claims_K_factual: 2
GT Sets
- E*:
  - Todreas_and_Kazimir_p62.pdf, p.1, Fig. 3-7
- F*:
  - R = 1.206 m
  - R = 1.333 m
```

- Model Answer

```text
- "Correctly identifies r = 1.206 m as inner radius"
- "Correctly identifies r = 1.333 m as outer radius"
- "Does not introduce extraneous numeric values"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Values and inner/outer interpretation match GT (notation r vs R is benign) → CoP_S = 1.
- HR note: All three summary statements correct vs Fig. 3-7 → HR = 0/3 = 0.
- ViR note: F* lists R = 1.206 m and R = 1.333 m; both recovered → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q12
- Query: Which labeled radius corresponds to the inner surface of the thermal shield, and which corresponds to the outer surface?
- GT

```text
GT Condensed
- R = 1.206 m is the inner radius and R = 1.333 m is the outer radius.
GT Sets
- E*:
  - Todreas_and_Kazimir_p62.pdf, p.1, Fig. 3-7
- F*:
  - Relative placement of radius arrows
  - R = 1.206 m -> internal radius
  - R = 1.333 m -> external radius
```

- Model Answer

```text
- "Correctly maps 1.206 m to inner surface"
- "Correctly maps 1.333 m to outer surface"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT mapping 1.206 m inner, 1.333 m outer → CoP_S = 1.
- HR note: Two correct mapping claims → HR = 0/2 = 0.
- ViR note: F* includes relative placement and both radii; both numeric facts and mapping recovered → ViR = 3/3 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q13
- Query: Is a numerical radius explicitly given for the core barrel in Fig. 3-7?
- GT

```text
GT Condensed
- No numerical radius is specified for the core barrel.
GT Sets
- E*:
  - Todreas_and_Kazimir_p62.pdf, p.1, Fig. 3-7
- F*:
  - Text label 'Core Barrel' without numeric value
```

- Model Answer

```text
- "Correctly states no numerical radius for core barrel"
- "Distinguishes from thermal-shield radii"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT “no numerical radius for core barrel” and contrasts thermal shield numbers → CoP_S = 1.
- HR note: Both claims correct → HR = 0/2 = 0.
- ViR note: F* is “Core Barrel label without numeric value”; answer recovers that fact → ViR = 1/1 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q14
- Query: According to the text accompanying Fig. 3-7, what is the stated purpose of the thermal shield, and which physical damage mechanisms is it intended to mitigate?
- GT

```text
GT Condensed
- The thermal shield is used to protect the pressure vessel from γ-ray heating and neutron-induced radiation damage.
- The thermal shiled surrounds the core as shown in the figure and sated in the text.
GT Sets
- E*:
  - Todreas_and_Kazimir_p62.pdf, p.1, Example 3-4 text
- F*:
  - Thermal shield location surrounding the core in Fig. 3-7
```

- Model Answer

```text
- "Correctly identifies pressure-vessel protection"
- "Correctly lists gamma heating and neutron damage"
```

- Scores: CoP **1** | HR **0** | ViR **0**

```text
Metric Work
- CoP note: Matches GT purpose (protect pressure vessel) and mechanisms (γ heating, neutron damage) → CoP_S = 1.
- HR note: Two claims, both supported by Example 3-4 text → HR = 0/2 = 0.
- ViR note: F* is only the thermal-shield placement around the core in Fig. 3-7; the answer does not recover that visual fact → ViR = 0/1 = 0.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 0
```

### Q15
- Query: How does the text use the geometry shown in Fig. 3-7 to simplify the power-deposition calculation, and what geometric assumption is explicitly stated?
- GT

```text
GT Condensed
- The core is treated as an infinite plane source and the thermal shield as a slab.
- The assumption is justified by the small thickness-to-radius ratio of the shield.
GT Sets
- E*:
  - Todreas_and_Kazimir_p62.pdf, p.1, Example 3-4 text
- F*:
  - Thin annular thermal shield geometry in Fig. 3-7
```

- Model Answer

```text
- "Correctly states plane-source + slab approximation"
- "Correctly states justification"
```

- Scores: CoP **1** | HR **0** | ViR **0.5**

```text
Metric Work
- CoP note: Matches GT infinite plane source + slab model and small thickness-to-radius justification → CoP_S = 1.
- HR note: Two claims, both text-faithful → HR = 0/2 = 0.
- ViR note: F* references thin annular shield geometry; answer states approximation, not explicit annulus depiction → ViR = 0.5 (partial visual grounding).
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 0.5
```

## Simplified PWR Plant and Flow Paths

#### Source: Todreas_and_Kazimir_p186.pdf

### Q16
- Query: According to Figure 6-6, what are the three main flow paths shown in the simplified PWR plant, and which component thermally links the two reactor-related loops?
- GT

```text
GT Condensed
- The figure shows: (1) the primary reactor coolant loop, (2) the secondary steam/power cycle loop, and (3) the external condenser cooling stream.
- The Steam Generator thermally links the primary and secondary reactor-related loops.
GT Sets
- E*:
  - Todreas_and_Kazimir_p186.pdf, p.1, Fig. 6-6
  - Todreas_and_Kazimir_p186.pdf, p.1, surrounding explanatory text
- F*:
  - Labeled components: REACTOR, Steam Generator, Turbine, Condenser
  - Atmospheric Flow Stream connected to condenser
  - Primary loop from reactor to steam generator and back
  - Secondary loop from steam generator to turbine/condenser/pump and back
```

- Model Answer

```text
- The figure shows: (1) the primary reactor coolant loop, (2) the secondary steam/power cycle loop, and (3) the external condenser cooling stream.
- The Steam Generator thermally links the primary and secondary reactor-related loops.
```

- Scores: CoP **1** | HR **0** | ViR **0.6667**

```text
Metric Work
- CoP note: Matches GT on the three flow paths and SG as thermal link → CoP_S = 1.
- HR note: No extra unsupported factual claims in the pasted answer → HR = 0/2 = 0 (two sentences, both GT-aligned).
- ViR note: F* lists six visual elements; answer covers loops, SG, and major components textually but not every labeled block → ViR ≈ 4/6 = 0.6667.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 0.6667
```

### Q17
- Query: Which labeled state points belong to the primary loop, which belong to the secondary steam-power loop, and which are associated with the condenser cooling stream in Figure 6-6?
- GT

```text
GT Condensed
- Primary loop: 5 and 6
- Secondary steam-power loop: 1, 2, 3, and 4
- Condenser cooling stream: 7 and 8
GT Sets
- E*:
  - Todreas_and_Kazimir_p186.pdf, p.1, Fig. 6-6
- F*:
  - State labels 5 and 6 on the reactor-steam-generator loop
  - State labels 1, 2, 3, 4 on the steam-generator/turbine/condenser/pump loop
  - State labels 7 and 8 on the Atmospheric Flow Stream near the condenser
```

- Model Answer

```text
- Only part of the secondary-loop mapping is recovered; the rest is incorrect.
- Unsupported detail: Primary-loop state labels are reassigned to 1 and 4.
- Unsupported detail: States that the condenser-cooling stream is not explicitly labeled.
```

- Scores: CoP **0.25** | HR **0.6667** | ViR **0.3333**

```text
Metric Work
- CoP note: GT state-point partition (primary {5,6}, secondary {1–4}, cooling {7,8}) not recovered; only acknowledges partial secondary correctness → CoP_S = 0.25 (minimally correct).
- HR note: Three lines; two document false unsupported assignments (primary → 1/4; “cooling not labeled”) → HR = 2/3 = 0.6667.
- ViR note: F* has three state-point groupings on the figure; model does not recover any grouping correctly → ViR ≈ 1/3 = 0.3333 (weak partial if any incidental overlap).
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.6667
- ViR: 0.3333
```

### Q18
- Query: Using only Figure 6-6, trace the flow path of the secondary working fluid from the steam generator outlet back to the steam generator inlet, naming the major components and state points in order.
- GT

```text
GT Condensed
- The secondary working fluid leaves the Steam Generator at state 3,
- enters the Turbine,
- exits to the Condenser at state 4,
- leaves the condenser at state 1,
- passes through the Main Condensate Pump,
- and returns to the Steam Generator at state 2.
GT Sets
- E*:
  - Todreas_and_Kazimir_p186.pdf, p.1, Fig. 6-6
- F*:
  - State 3 on line from Steam Generator to Turbine
  - State 4 on line from Turbine to Condenser
  - State 1 at Condenser outlet
  - Main Condensate Pump on the return line
  - State 2 at line entering Steam Generator
```

- Model Answer

```text
- Component order is right, but the state-point sequence is wrong.
- Unsupported detail: Secondary-loop state numbering is shifted (2/3/4/1/2 instead of 3/4/1/2).
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.4**

```text
Metric Work
- CoP note: Component order acceptable but state-point sequence wrong vs GT (3→4→1→pump→2) → CoP_S = 0.25 (minimally correct).
- HR note: Two bullets; one asserts an incorrect shifted numbering pattern as model output → treat 1 unsupported factual claim out of 2 → HR = 0.5.
- ViR note: Five F* state/component anchors; correct component path partially overlaps figure, state labels largely wrong → ViR ≈ 2/5 = 0.4.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.5
- ViR: 0.4
```

### Q19
- Query: What component in Figure 6-6 is directly coupled to electric-power production, and how is that relationship depicted visually?
- GT

```text
GT Condensed
- The Turbine is mechanically coupled to the Generator, and the Generator is shown producing Electric Power.
- Visually, the Turbine is connected directly to the Generator, with an output labeled "Electric Power" extending from the Generator.
GT Sets
- E*:
  - Todreas_and_Kazimir_p186.pdf, p.1, Fig. 6-6
- F*:
  - Turbine connected to Generator
  - Label 'Electric Power' on output from Generator
```

- Model Answer

```text
- The turbine-generator relationship is only partially captured.
- Unsupported detail: Treats the turbine itself as the electric-power-producing component.
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.5**

```text
Metric Work
- CoP note: GT centers on Generator producing “Electric Power” with Turbine mechanically coupled; model misattributes power production to Turbine alone → CoP_S = 0.25 (incorrect core role).
- HR note: Two lines; one encodes an unsupported/wrong identification (turbine as producer) → HR = 1/2 = 0.5.
- ViR note: F* has Turbine–Generator link and Electric Power label; partial recovery of coupling, misses correct power-producing component → ViR ≈ 1/2 = 0.5.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.5
- ViR: 0.5
```

### Q20
- Query: According to the text and Figure 6-6, why does the PWR require a separate secondary system for turbine-driving vapor rather than sending primary coolant directly to the turbine?
- GT

```text
GT Condensed
- The text states that in a PWR the reactor coolant is limited to a nominal saturated mixed mean core outlet condition.
- Therefore, the turbine-driving vapor must be produced in a Steam Generator in a separate secondary system.
GT Sets
- E*:
  - Todreas_and_Kazimir_p186.pdf, p.1, surrounding explanatory text
  - Todreas_and_Kazimir_p186.pdf, p.1, Fig. 6-6
- F*:
  - Steam Generator shown between primary reactor loop and secondary turbine loop
  - Separate primary and secondary loops visibly distinct
```

- Model Answer

```text
- The separate-secondary-loop point is right, but most of the explanation is extra.
- Unsupported detail: Radioactivity containment rationale is added.
- Unsupported detail: Operational-safety/equipment-longevity rationale is added.
- Unsupported detail: Design-optimization rationale is added.
```

- Scores: CoP **0.5** | HR **0.75** | ViR **0.5**

```text
Metric Work
- CoP note: Core idea—separate secondary for turbine steam—is right, but GT explanation is saturated mixed mean outlet + SG; model adds three unsupported rationales → CoP_S = 0.5 (partially correct).
- HR note: Four bullets after the lead; three are explicit unsupported extras → HR = 3/4 = 0.75.
- ViR note: F* lists SG bridging loops and visually distinct loops; answer implies separation but not full diagram fidelity → ViR = 1/2 = 0.5.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.75
- ViR: 0.5
```

## Safeguards Integration Flowchart

#### Source: UNFSF_p21.pdf

### Q21
- Query: What are the two top-level regulatory branches shown in Figure 4, and which CFR citations are explicitly attached to them?
- GT

```text
GT Condensed
- The left branch is "Physical Security" with citation 10CFR73.
- The right branch is "Safeguards (MC&A)" with citation 10CFR74.
GT Sets
- E*:
  - UNFSF_p21.pdf, p.1, Figure 4
- F*:
  - Green box labeled 'Physical Security 10CFR73'
  - Green box labeled 'Safeguards (MC&A) 10CFR74'
```

- Model Answer

```text
- The left branch is "Physical Security" with citation 10CFR73.
- The right branch is "Safeguards (MC&A)" with citation 10CFR74.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT branches and CFR attachments verbatim → CoP_S = 1.
- HR note: Two sentences, both correct vs Figure 4 → HR = 0/2 = 0.
- ViR note: F* lists two green branch boxes; both labels and citations recovered → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q22
- Query: In Figure 4, what common sequence of design-development boxes appears under both the Physical Security and Safeguards (MC&A) branches before integration?
- GT

```text
GT Condensed
- Under both branches, the sequence is:
- Performance Goal
- Functional Design Criteria
- Design Requirements
GT Sets
- E*:
  - UNFSF_p21.pdf, p.1, Figure 4
- F*:
  - Parallel red boxes labeled 'Performance Goal'
  - Parallel cyan boxes labeled 'Functional Design Criteria'
  - Parallel cyan boxes labeled 'Design Requirements'
```

- Model Answer

```text
- Sequence is right except for 'Performance Design Criteria' instead of 'Functional Design Criteria'.
```

- Scores: CoP **0.75** | HR **0** | ViR **0.6667**

```text
Metric Work
- CoP note: Performance Goal + Design Requirements correct; middle box misnamed (“Performance Design Criteria” vs GT “Functional Design Criteria”) → CoP_S = 0.75 (mostly correct).
- HR note: Single self-diagnosing sentence—treat as one generated claim with embedded error but no separate unsupported hallucination line → HR = 0/1 = 0.
- ViR note: F* lists three parallel box types; two of three labels recovered exactly → ViR = 2/3 = 0.6667.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0
- ViR: 0.6667
```

### Q23
- Query: What is the exact label of the central integration box in Figure 4, and what dual-role concept does it represent in the workflow?
- GT

```text
GT Condensed
- The central integration box is labeled "Integration of Design Requirements (Dual Function)".
- It represents the merging of security and safeguards design requirements into a combined or dual-function design basis.
GT Sets
- E*:
  - UNFSF_p21.pdf, p.1, Figure 4
- F*:
  - Red box labeled 'Integration of Design Requirements (Dual Function)'
  - Placement below the two parallel Design Requirements boxes
```

- Model Answer

```text
- The central integration box is labeled "Integration of Design Requirements (Dual Function)".
- It represents the merging of security and safeguards design requirements into a combined or dual-function design basis.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Exact central label and dual-role interpretation match GT → CoP_S = 1.
- HR note: Two claims, both correct → HR = 0/2 = 0.
- ViR note: F* lists integration box text and placement requirement; both satisfied → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q24
- Query: After the Performance Assessment decision node in Figure 4, what happens on the YES path and what happens on the NO paths?
- GT

```text
GT Condensed
- On the YES path, the workflow proceeds to "Final Design Optimized and Harmonized."
- On the NO paths, the process loops back to Final Design for further iteration.
GT Sets
- E*:
  - UNFSF_p21.pdf, p.1, Figure 4
- F*:
  - Black diamond labeled 'Performance Assessment'
  - Red YES box below the diamond
  - Blue NO boxes on both sides
  - Blue final box labeled 'Final Design Optimized and Harmonized'
  - Arrows from NO paths returning to Final Design
```

- Model Answer

```text
- On the YES path, the workflow proceeds to "Final Design Optimized and Harmonized."
- On the NO paths, the process loops back to Final Design for further iteration.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: YES path to “Final Design Optimized and Harmonized” and NO paths looping to Final Design match GT → CoP_S = 1.
- HR note: Two claims, both correct → HR = 0/2 = 0.
- ViR note: F* enumerates diamond, YES/NO boxes, final box, and loop arrows; answer captures the decision outcomes implied by those elements → ViR = 5/5 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

### Q25
- Query: Which supporting analysis activities are shown alongside the design stages in Figure 4, and at what stages do they appear?
- GT

```text
GT Condensed
- Security Assessment Methods and Safeguards Assessment Methods appear alongside the Conceptual Design stage.
- Trade Studies appear alongside the Preliminary Design stage on both the left and right sides.
GT Sets
- E*:
  - UNFSF_p21.pdf, p.1, Figure 4
- F*:
  - Orange boxes labeled 'Security Assessment Methods' and 'Safeguards Assessment Methods'
  - These appear adjacent to Conceptual Design
  - Pink boxes labeled 'Trade Studies' on both sides
  - These appear adjacent to Preliminary Design
```

- Model Answer

```text
- Security Assessment Methods and Safeguards Assessment Methods appear alongside the Conceptual Design stage.
- Trade Studies appear alongside the Preliminary Design stage on both the left and right sides.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT on Security/Safeguards assessment methods at Conceptual Design and Trade Studies at Preliminary Design (both sides) → CoP_S = 1.
- HR note: Two sentences, both correct → HR = 0/2 = 0.
- ViR note: F* lists four visual groupings (two orange blocks + adjacency + pink trade studies); all reflected in answer → ViR = 4/4 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```

## Alternative Control Volume Representations of a Batch-Fueled Reactor Plant

#### Source: Todreas_and_Kazimir_p190.pdf

### Q26
- Query: In Figure 6-9, how do the control-volume boundaries differ across parts A, B, and C?
- GT

```text
GT Condensed
- In part A, a single dashed boundary labeled Control Volume 1 encloses the entire plant.
- In part B, the figure is split into two dashed control volumes: Control Volume 2 contains the Fuel block, while Control Volume 1 contains the reactor plant.
- In part C, the plant is again split into two dashed control volumes, but this time the left control volume contains the reactor-side components and the right control volume contains the power-conversion side.
GT Sets
- E*:
  - Todreas_and_Kazimir_p190.pdf, p.1, Figure 6-9
- F*:
  - Part A shows one dashed boundary labeled Control Volume 1
  - Part B shows two dashed boundaries labeled Control Volume 2 and Control Volume 1
  - Part C shows two dashed boundaries labeled Control Volume 2 and Control Volume 1
  - The enclosed components differ across A, B, and C
```

- Model Answer

```text
- The control-volume structure is substantially wrong.
- Unsupported detail: Part A is reduced to reactor only.
- Unsupported detail: Part B is reduced to reactor plus steam generator.
- Unsupported detail: Part C is described as a cumulative expansion including turbine and fuel.
```

- Scores: CoP **0** | HR **0.75** | ViR **0**

```text
Metric Work
- CoP note: GT control-volume story for A/B/C is not conveyed; answer documents major structural errors vs figure → CoP_S = 0 (incorrect).
- HR note: Four lines; first is evaluative (“substantially wrong”); three enumerate fabricated/wrong part descriptions → |K_unsupported| = 3, |K_generated| = 4 → HR = 0.75.
- ViR note: F* lists four distinct visual facts about dashed boundaries and enclosed regions; none are recovered correctly → ViR = 0/4 = 0.
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 0.75
- ViR: 0
```

### Q27
- Query: In Figure 6-9, which part explicitly separates the Fuel from the rest of the plant, and how is the energy transfer from Fuel into the plant labeled?
- GT

```text
GT Condensed
- Figure 6-9B explicitly separates the Fuel into its own control volume.
- The energy transfer from Fuel into the plant is labeled Q^dot at T_fuel.
GT Sets
- E*:
  - Todreas_and_Kazimir_p190.pdf, p.1, Figure 6-9
- F*:
  - Figure 6-9B contains a box labeled Fuel inside Control Volume 2
  - An arrow from Fuel toward the plant is labeled Q^dot at T_fuel
```

- Model Answer

```text
- Both the panel identity and the label are wrong.
- Unsupported detail: Fuel is assigned to Part C instead of Part B.
- Unsupported detail: Uses q_fission instead of Q-dot at T_fuel.
```

- Scores: CoP **0** | HR **0.6667** | ViR **0**

```text
Metric Work
- CoP note: GT requires Part B with Fuel in CV2 and Q̇ at T_fuel label; answer assigns wrong panel and wrong heat label → CoP_S = 0.
- HR note: Three bullets; two describe concrete wrong facts (panel C; q_fission) → HR = 2/3 = 0.6667 (first line is meta-summary, not counted as separate unsupported claim).
- ViR note: F* has two visual facts; neither recovered → ViR = 0/2 = 0.
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 0.6667
- ViR: 0
```

### Q28
- Query: In Figure 6-9C, which major components lie in the left control volume, which lie in the right control volume, and what heat-transfer label appears between them?
- GT

```text
GT Condensed
- In Figure 6-9C, the left control volume contains the reactor-side components R, SG, and P.
- The right control volume contains the power-conversion-side components SG, T, G, C, and P.
- The heat transfer between the two sides is labeled Q^dot at T_coolant.
GT Sets
- E*:
  - Todreas_and_Kazimir_p190.pdf, p.1, Figure 6-9
- F*:
  - Figure 6-9C left side contains R, SG, and P
  - Figure 6-9C right side contains SG, T, G, C, and P
  - Arrow between the two sides is labeled Q^dot at T_coolant
```

- Model Answer

```text
- The split and heat-transfer label are only partially captured.
- Unsupported detail: Places Fuel in the left control volume.
- Unsupported detail: Omits C and P from the right volume.
- Unsupported detail: Uses Q_in instead of Q-dot at T_coolant.
```

- Scores: CoP **0.25** | HR **0.75** | ViR **0.3333**

```text
Metric Work
- CoP note: GT split (left R,SG,P; right SG,T,G,C,P) and Q̇ at T_coolant not achieved; summary admits only partial capture → CoP_S = 0.25 (minimally correct).
- HR note: Four lines; three document specific wrong/missing figure facts → HR = 3/4 = 0.75.
- ViR note: F* has three grouped facts; at best one weakly aligned (SG presence) → ViR ≈ 1/3 = 0.3333.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.75
- ViR: 0.3333
```

### Q29
- Query: In Figure 6-9, which plant outputs or exchanges are shown on the right side of the schematic across the control-volume representations, and how are they labeled?
- GT

```text
GT Condensed
- The generator output is labeled Electric Power.
- The condenser-side atmospheric exchange is labeled with (s_i)AF and (s_o)AF.
- The external stream is labeled Atmospheric Flow Stream m_AF at p_o, T_o.
GT Sets
- E*:
  - Todreas_and_Kazimir_p190.pdf, p.1, Figure 6-9
- F*:
  - Electric Power label connected to G
  - (s_i)AF and (s_o)AF labels near the condenser side
  - Atmospheric Flow Stream m_AF at p_o, T_o label on the far right
```

- Model Answer

```text
- Electric output is recognized, but the atmospheric-flow labels are replaced by unsupported quantities.
- Unsupported detail: Adds Q_out as a right-side plant output.
- Unsupported detail: Adds temperature and heat-loss labels not present in the figure.
```

- Scores: CoP **0.25** | HR **0.6667** | ViR **0.3333**

```text
Metric Work
- CoP note: GT requires Electric Power plus (s_i)AF/(s_o)AF and Atmospheric Flow Stream labels on the right; model only partially recognizes electric output → CoP_S = 0.25 (minimally correct).
- HR note: Three lines; two enumerate fabricated right-side outputs/labels → HR = 2/3 = 0.6667.
- ViR note: F* lists three label families; one (Electric Power / G) partially recovered → ViR ≈ 1/3 = 0.3333.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.6667
- ViR: 0.3333
```

### Q30
- Query: In Figure 6-9, which component labels appear in the plant schematic, and what do they represent in the reactor plant layout?
- GT

```text
GT Condensed
- Figure 6-9 includes the component labels R, SG, T, G, C, and P.
- R represents the reactor, SG the steam generator, T the turbine, G the generator, C the condenser or cooler, and P the pump.
GT Sets
- E*:
  - Todreas_and_Kazimir_p190.pdf, p.1, Figure 6-9
  - Todreas_and_Kazimir_p190.pdf, p.1, surrounding text if needed
- F*:
  - R appears in the reactor section
  - SG appears at the reactor-to-power interface
  - T and G appear in the power-conversion section
  - C appears in the cooling/condensing section
  - P appears in the circulation loops
```

- Model Answer

```text
- Figure 6-9 includes the component labels R, SG, T, G, C, and P.
- R represents the reactor, SG the steam generator, T the turbine, G the generator, C the condenser or cooler, and P the pump.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Component list and role mapping match GT condensed answer exactly → CoP_S = 1.
- HR note: Two sentences, both correct → HR = 0/2 = 0.
- ViR note: F* lists six component placement facts; answer covers all labels and roles at schematic level → ViR = 6/6 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
```
