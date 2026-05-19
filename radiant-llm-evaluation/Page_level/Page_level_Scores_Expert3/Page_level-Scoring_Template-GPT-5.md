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
- Model: GPT-5
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
- "Claims horizontal axis is x and vertical axis is y"
- "Claims these are plotted coordinate axes"
- "Claims figure includes a curve y^2 = 32x"
- "Claims no physical dimensions are annotated"
```

- Scores: CoP **0** | HR **1** | ViR **0**

```text
Metric Work
- CoP note: GT: 10 ft / 6 ft physical dimensions, not plotted axes; model asserts x–y coordinate axes, parabola y²=32x, and no physical dimensions → CoP_S = 0.
- HR note: Four decomposition bullets are all false vs Fig. 51 / GT → HR = 4/4 = 1.
- ViR note: |F*|=4; no correct visual facts recovered → ViR = 0/4 = 0.
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 1
- ViR: 0
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
- "Claims it is a coordinate sketch with labeled x–y axes"
- "Also states there are no tick marks and no units"
```

- Scores: CoP **0** | HR **1** | ViR **0**

```text
Metric Work
- CoP note: GT requires geometric schematic with physical dimensions; model claims a coordinate sketch with x–y axes → CoP_S = 0.
- HR note: Two bullets contradict GT (axes vs schematic) → HR = 2/2 = 1.
- ViR note: |F*|=7; no faithful recovery → ViR = 0/7 = 0.
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 1
- ViR: 0
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
- "Claims no ellipse equation is shown adjacent to the figure"
- "Claims the only adjacent equation is y^2 = 32x (parabola)"
```

- Scores: CoP **0** | HR **1** | ViR **0**

```text
Metric Work
- CoP note: GT ellipse x²/64+y²/36=1 adjacent to figure; model denies ellipse and cites wrong parabola equation → CoP_S = 0.
- HR note: Both claims false → HR = 2/2 = 1.
- ViR note: Equation in F* not recovered → ViR = 0/1 = 0.
- CoP_S: 0
- CoP_N:
- CoP: 0
- HR: 1
- ViR: 0
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
- "Correctly uses x^2/64 + y^2/36 = 1"
- "Correctly derives x = ±8 and y = ±6"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Extents ±8 and ±6 consistent with GT from the ellipse equation → CoP_S = 1.
- HR note: Two correct claims → HR = 0/2 = 0.
- ViR note: Denominators / extents implied correctly → ViR = 2/2 = 1.
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
- "Correctly identifies the quantity: pressure/force on gate for two cases"
- "Correctly mentions AB at surface and AB 5 ft below"
- "Incorrectly claims figure only labels x, y, y^2 = 32x and has no numeric dimensions"
```

- Scores: CoP **0.75** | HR **0.3333** | ViR **0.3333**

```text
Metric Work
- CoP note: Pressure cases (surface / 5 ft below) align with GT Problem 1; omits semicircular-gate Problem 2; third bullet falsely denies numeric figure dimensions → CoP_S = 0.75.
- HR note: Three bullets; one is a clear false claim about figure labeling → HR = 1/3 = 0.3333.
- ViR note: F* has three items; two text-condition facts partially recovered, figure dimensions denied → ViR ≈ 1/3 = 0.3333.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0.3333
- ViR: 0.3333
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
- "Identifies ϕ(r), q'''(r), r, R"
- "Says axial (z) dimension is not shown; no z-axis/axial coordinate labeled"
```

- Scores: CoP **0.5** | HR **0.5** | ViR **0.6667**

```text
Metric Work
- CoP note: Partial recovery of ϕ(r), q′′′(r), r, R; false denial that axial z is labeled vs GT axial markers → CoP_S = 0.5.
- HR note: Two bullets; one is incorrect about z labeling → HR = 1/2 = 0.5.
- ViR note: Two of three F* clusters partially hit (radial/flux notation) → ViR ≈ 2/3 = 0.6667.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.5
- ViR: 0.6667
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
- "Describes radial center-peaked ϕ(r) and q'''(r)"
- "Says axial variation is not depicted"
```

- Scores: CoP **0.5** | HR **0.5** | ViR **0.6667**

```text
Metric Work
- CoP note: Radial center-peaked behavior matches GT; denying axial depiction contradicts GT axial profiles and boundaries → CoP_S = 0.5.
- HR note: One of two bullets is materially wrong vs figure/GT → HR = 1/2 = 0.5.
- ViR note: ϕ(r), q′′′(r) partially reflected; axial ϕ(z) not → ViR ≈ 2/3 = 0.6667.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.5
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
- "Correctly reproduces Eq. (3-36)"
- "Correctly states integral over core volume of shape function with dV"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Eq. (3-36) structure and core volume integral match GT → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: F* empty → ViR = 1 by convention.
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
- "Correctly attributes flattening to preferential burnup in high-flux regions"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Burnup in high-flux regions matches GT flattening explanation → CoP_S = 1.
- HR note: HR = 0/1 = 0.
- ViR note: F* empty → ViR = 1 by convention.
- CoP_S: 1
- CoP_N:
- CoP: 1
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
- "Correctly identifies radial profiles ϕ(r) and q'''(r)"
- "Correctly describes center-peaked radial behavior"
- "Incorrectly claims axial dimension is not shown and no z-dependence exists"
- "Does not identify extrapolated boundaries or axial markers"
```

- Scores: CoP **0.5** | HR **0.25** | ViR **0.5**

```text
Metric Work
- CoP note: Radial ϕ(r), q′′′(r) and center-peaked behavior match GT; incorrect denial of axial z depiction and missing extrapolated boundaries → CoP_S = 0.5.
- HR note: Four bullets; one is a false axial claim → HR = 1/4 = 0.25.
- ViR note: Partial consistency with plotted profiles vs F* → ViR = 0.5.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.25
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
- "Gives R1 = 1.206 m (inner) and R2 = 1.333 m (outer)"
- "Adds derived thickness ≈ 0.127 m (= R2 − R1)"
```

- Scores: CoP **1** | HR **0.3333** | ViR **1**

```text
Metric Work
- CoP note: Inner/outer radii 1.206 m and 1.333 m match GT → CoP_S = 1.
- HR note: Derived thickness is an extra numeric claim not in GT F* → HR = 1/3 = 0.3333.
- ViR note: Both required radii in F* recovered → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0.3333
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
- "States R1 is inner surface and R2 is outer surface"
- "Does not restate numeric values"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Inner/outer mapping matches GT (values implied by prior context) → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: F* satisfied for placement + numeric radii → ViR = 3/3 = 1.
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
- "Correctly says no numerical radius is given for core barrel"
- "Mentions only the two thermal-shield radii are labeled"
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT: no core-barrel numeric radius; contrasts thermal-shield labels → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Core-barrel label fact recovered → ViR = 1/1 = 1.
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
- "States purpose is to protect pressure vessel"
- "Lists gamma-ray heating and neutron-induced radiation damage"
```

- Scores: CoP **1** | HR **0** | ViR **0**

```text
Metric Work
- CoP note: Purpose and γ / neutron mechanisms match GT → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Shield placement in Fig. 3-7 not articulated → ViR = 0/1 = 0.
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
- "States plane-source + slab simplification"
- "States justification is small thickness-to-radius ratio"
```

- Scores: CoP **1** | HR **0** | ViR **0.5**

```text
Metric Work
- CoP note: Plane-source + slab model and thin shield ratio match GT → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Thin annulus geometry only loosely tied to figure → ViR = 0.5.
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
- CoP note: Three flow paths and SG thermal link match GT → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Six F* visual elements; four reflected in answer → ViR ≈ 4/6 = 0.6667.
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
- Correct on state 5 and states 1-4, but it never recovers the 7/8 condenser-cooling labels.
```

- Scores: CoP **0.5** | HR **0** | ViR **0.6667**

```text
Metric Work
- CoP note: Recovers primary {5,6} and secondary {1–4} but omits condenser-cooling {7,8} per GT → CoP_S = 0.5.
- HR note: Self-critical summary; no fabricated state labels → HR = 0/1 = 0.
- ViR note: Two of three F* groupings correct → ViR = 2/3 = 0.6667.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0
- ViR: 0.6667
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
- Component order is right, but the state-point numbering is wrong.
- Unsupported detail: Secondary-loop states are shifted by one position (2/3/4/1 instead of 3/4/1/2).
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.4**

```text
Metric Work
- CoP note: Component order acceptable; state numbering wrong vs GT 3→4→1→pump→2 → CoP_S = 0.25.
- HR note: Two bullets; one documents incorrect shifted state sequence → HR = 1/2 = 0.5.
- ViR note: Partial path overlap; state anchors largely wrong → ViR ≈ 2/5 = 0.4.
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
- The Turbine is mechanically coupled to the Generator, and the Generator is shown producing Electric Power.
- Visually, the Turbine is connected directly to the Generator, with an output labeled "Electric Power" extending from the Generator.
```

- Scores: CoP **1** | HR **0** | ViR **1**

```text
Metric Work
- CoP note: Matches GT: Turbine–Generator coupling and Electric Power label → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Both F* visual facts recovered → ViR = 2/2 = 1.
- CoP_S: 1
- CoP_N:
- CoP: 1
- HR: 0
- ViR: 1
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
- Core explanation is right, with one extra unsupported rationale.
- Unsupported detail: Material-corrosion limits are added beyond the canonical explanation.
```

- Scores: CoP **0.75** | HR **0.5** | ViR **0.5**

```text
Metric Work
- CoP note: Core saturated outlet + SG secondary steam matches GT; adds corrosion rationale beyond canonical text → CoP_S = 0.75.
- HR note: Two bullets; second is unsupported extra → HR = 1/2 = 0.5.
- ViR note: Loop separation partially reflected → ViR = 1/2 = 0.5.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0.5
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
- Branch names are correct, but the CFR labels are missed.
- Unsupported detail: States that no explicit CFR citations are shown.
```

- Scores: CoP **0.5** | HR **0.6667** | ViR **0.5**

```text
Metric Work
- CoP note: Branch names correct; CFR 10CFR73/74 missing and falsely claims no CFR shown → CoP_S = 0.5.
- HR note: Three claims; two wrong (CFR absence + missed labels) → HR ≈ 2/3 = 0.6667.
- ViR note: Branch titles without CFR boxes in text → ViR = 1/2 = 0.5.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.6667
- ViR: 0.5
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
- The shared sequence is partially correct but includes one extra stage.
- Unsupported detail: Adds a Regulatory Guides/NUREGS/Codes-and-Standards box that is not part of the common sequence.
```

- Scores: CoP **0.75** | HR **0.5** | ViR **0.6667**

```text
Metric Work
- CoP note: Sequence mostly matches GT but adds an extra Regulatory Guides box not in the common three-box path → CoP_S = 0.75.
- HR note: Two bullets; one documents an unsupported extra stage → HR = 1/2 = 0.5.
- ViR note: Two of three F* box types recovered → ViR = 2/3 = 0.6667.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0.5
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
- The dual-function idea is right, but the exact label is wrong.
- Unsupported detail: Uses the wrong integration-box label: 'Integration of Design with Safeguard Requirements (Dual Function)'.
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.5**

```text
Metric Work
- CoP note: Dual-role concept partially right; exact integration-box label wrong vs GT → CoP_S = 0.25.
- HR note: Wrong label counted as unsupported vs figure text → HR = 1/2 = 0.5.
- ViR note: Placement concept partial → ViR = 1/2 = 0.5.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.5
- ViR: 0.5
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
- YES path is right; NO is described as a general redesign loop rather than the specific loop back to Final Design.
```

- Scores: CoP **0.75** | HR **0.5** | ViR **0.8**

```text
Metric Work
- CoP note: YES path matches GT; NO path described generically instead of explicit loop to Final Design → CoP_S = 0.75.
- HR note: Two bullets; second imprecise vs GT NO routing → HR = 1/2 = 0.5.
- ViR note: Most F* routing elements captured for YES; NO arrows weaker → ViR ≈ 4/5 = 0.8.
- CoP_S: 0.75
- CoP_N:
- CoP: 0.75
- HR: 0.5
- ViR: 0.8
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
- CoP note: Matches GT on assessment methods at Conceptual Design and Trade Studies at Preliminary Design → CoP_S = 1.
- HR note: HR = 0/2 = 0.
- ViR note: Four F* visual groupings recovered → ViR = 4/4 = 1.
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
- The control-volume decomposition is largely wrong.
- Unsupported detail: Invents two control volumes in Part A.
- Unsupported detail: Misstates the boundaries in Part B.
- Unsupported detail: Misstates the left/right split in Part C.
```

- Scores: CoP **0** | HR **0.75** | ViR **0**

```text
Metric Work
- CoP note: GT A/B/C control-volume story largely absent; summary flags major errors → CoP_S = 0.
- HR note: Four lines; three enumerate concrete wrong panel claims → HR = 3/4 = 0.75.
- ViR note: No correct F* boundary facts → ViR = 0/4 = 0.
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
- Correct panel, wrong transfer label.
- Unsupported detail: Uses 'fission rate' instead of Q-dot at T_fuel.
```

- Scores: CoP **0.25** | HR **0.5** | ViR **0.5**

```text
Metric Work
- CoP note: Correct panel (B) per decomposition but wrong energy label (fission vs Q̇ at T_fuel) → CoP_S = 0.25.
- HR note: Two bullets; one wrong label detail → HR = 1/2 = 0.5.
- ViR note: One of two F* items (panel) partially hit → ViR = 0.5.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.5
- ViR: 0.5
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
- The split is only partially captured.
- Unsupported detail: Places only R in the left volume.
- Unsupported detail: Says the heat-transfer label is not visible.
```

- Scores: CoP **0.25** | HR **0.6667** | ViR **0.2**

```text
Metric Work
- CoP note: High-level split only; wrong component sets and missing Q̇ at T_coolant per decomposition → CoP_S = 0.25.
- HR note: Three unsupported-detail bullets vs three summary lines → HR ≈ 2/3 = 0.6667.
- ViR note: Weak overlap with two-sided split → ViR ≈ 1/5 = 0.2.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.6667
- ViR: 0.2
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
- Only Electric Power is recoverable; the rest are unsupported substitutions.
- Unsupported detail: Steam listed as a right-side output.
- Unsupported detail: Condensate listed as a right-side output.
- Unsupported detail: Make-up water listed as a right-side output.
```

- Scores: CoP **0.25** | HR **0.75** | ViR **0.3333**

```text
Metric Work
- CoP note: Electric Power partially recovered; multiple fabricated right-side outputs per decomposition → CoP_S = 0.25.
- HR note: Four bullets; three document unsupported substitutions → HR = 3/4 = 0.75.
- ViR note: One of three F* label families (Electric Power) → ViR = 1/3 = 0.3333.
- CoP_S: 0.25
- CoP_N:
- CoP: 0.25
- HR: 0.75
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
- Some component mappings are correct, but the answer broadens the requested label set.
- Unsupported detail: Fuel is treated as a schematic component label.
- Unsupported detail: Control-volume labels are treated as component labels.
- Unsupported detail: Right-side stream labels are mixed into the answer.
```

- Scores: CoP **0.5** | HR **0.75** | ViR **0.6667**

```text
Metric Work
- CoP note: Core R/SG/T/G/C/P mapping partially right but answer broadens to Fuel and CV/stream labels per decomposition → CoP_S = 0.5.
- HR note: Four lines; three flag unsupported expansions → HR = 3/4 = 0.75.
- ViR note: Four of six component placement facts roughly recovered → ViR ≈ 4/6 = 0.6667.
- CoP_S: 0.5
- CoP_N:
- CoP: 0.5
- HR: 0.75
- ViR: 0.6667
```
