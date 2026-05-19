# Benchmark Queries Page-Level-GPT-4.1 Scoring

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

## Scoring Set

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
Model Condensed
- "Claims horizontal dimension labeled as 4"
- "Interprets x and y as plotted axes"
- "Explicitly states dimensions are not physical lengths"
Citations
- Calculus_p116_73.pdf
- Fig.51
K Unsupported
- "Horizontal dimension labeled as 4"
- "x and y are plotted coordinate axes"
- "Dimensions are not physical lengths"
```

- Scores

```text
Metric Work
- CoP_S: 0
- CoP_N: 0.4
- CoP: 0.16
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
Model Condensed
- "Correctly classifies figure as schematic"
- "Incorrectly claims x–y axes are present"
- "Uses fabricated dimension label '4'"
Citations
- Calculus_p116_73.pdf
- Fig.51
K Unsupported
- "Axes labeled x and y are present"
- "Dimension labeled 4 indicates physical width"
```

- Scores

```text
Metric Work
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.6667
- ViR: 0.25
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
Model Condensed
- "Correctly reproduces ellipse equation"
- "Correctly derives a = 8 and b = 6"
Citations
- Calculus_p116_73.pdf
- Fig.51
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: 1
- CoP: 1
- HR: 0
- ViR: null
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
Model Condensed
- "Correctly derives x and y coordinate ranges"
Citations
- Calculus_p116_73.pdf
- Fig.51
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: 1
- CoP: 1
- HR: 0
- ViR: null
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
Model Condensed
- "Correctly identifies hydrostatic pressure to compute"
- "Incorrectly states base width is labeled as 4"
- "Claims no discrepancy between text and figure"
Citations
- Calculus_p116_73.pdf
- Fig.51
K Unsupported
- "Base width of parabola is labeled as 4"
- "No discrepancy between figure and text"
```

- Scores

```text
Metric Work
- CoP_S: 0.5
- CoP_N: 0
- CoP: 0.3
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
Model Condensed
- "Identifies radial coordinate r and radius R"
- "Introduces extrapolated boundary R₀ (instead of R_e)"
- "Claims axial direction has no explicit coordinate symbol"
- "Misses axial markers ±L/2 and ±L_e/2"
Citations
- Todreas_and_Kazimi_p53.pdf
- p.53
K Unsupported
- "No explicit axial coordinate symbol shown"   # z, ±L/2 *are* shown in GT
```

- Scores

```text
Metric Work
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.2
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
Model Condensed
- "Correctly describes center-peaked radial profiles"
- "Correctly relates heat generation to flux"
- "Introduces axial behavior not explicitly shown in figure"
- "Claims parabolic shape"
Citations
- Todreas_and_Kazimi_p53.pdf
- p.53
K Unsupported
- "Axial profiles peak at midplane"
- "Profiles are parabolic"
```

- Scores

```text
Metric Work
- CoP_S: 0.5
- CoP_N: null
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
Model Condensed
- "Correctly reproduces structure of Eq. 3-36"
- "Correctly identifies integrated quantity"
Citations
- Todreas_and_Kazimi_p53.pdf
- p.53
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: 1
- CoP: 1
- HR: 0
- ViR: null
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
Model Condensed
- "Correctly attributes flattening to burnup and reactivity reduction"
Citations
- Todreas_and_Kazimi_p53.pdf
- p.53
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: null
- CoP: 1
- HR: 0
- ViR: null
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
Model Condensed
- "Correctly describes radial profiles and extrapolated boundary"
- "Does not identify axial markers"
- "Over-asserts axial behavior"
Citations
- Todreas_and_Kazimi_p53.pdf
- p.53
K Unsupported
- "Axial variation implied"
```

- Scores

```text
Metric Work
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.25
- ViR: 0.3333
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
Model Condensed
- "Correctly identifies r = 1.206 m as inner radius"
- "Correctly identifies r = 1.333 m as outer radius"
- "Does not introduce extraneous numeric values"
Citations
- Todreas_and_Kazimi_p62.pdf
- p.62
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: 1
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
Model Condensed
- "Correctly maps 1.206 m to inner surface"
- "Correctly maps 1.333 m to outer surface"
Citations
- Todreas_and_Kazimi_p62.pdf
- p.62
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- "Correctly states no numerical radius for core barrel"
- "Distinguishes from thermal-shield radii"
Citations
- Todreas_and_Kazimi_p62.pdf
- p.62
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- "Correctly identifies pressure-vessel protection"
- "Correctly lists gamma heating and neutron damage"
Citations
- Todreas_and_Kazimi_p62.pdf
- p.62
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: null
- CoP: 1
- HR: 0
- ViR: 1
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
Model Condensed
- "Correctly states plane-source + slab approximation"
- "Correctly states justification"
Citations
- Todreas_and_Kazimi_p62.pdf
- p.62
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP_S: 1
- CoP_N: null
- CoP: 1
- HR: 0
- ViR: 1
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
Model Condensed
- The figure shows: (1) the primary reactor coolant loop, (2) the secondary steam/power cycle loop, and (3) the external condenser cooling stream.
- The Steam Generator thermally links the primary and secondary reactor-related loops.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Three loops and the steam-generator link are correct.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
- CoP: 1
- HR: 0
- ViR: 1
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
Model Condensed
- Only part of the secondary-loop mapping is recovered; the rest is incorrect.
- Unsupported detail: Primary-loop state labels are reassigned to 1 and 4.
- Unsupported detail: States that the condenser-cooling stream is not explicitly labeled.
Citations
- []
K Unsupported
- Primary-loop state labels are reassigned to 1 and 4.
- States that the condenser-cooling stream is not explicitly labeled.
```

- Scores

```text
Metric Work
- CoP note: Only part of the secondary-loop mapping is recovered; the rest is incorrect.
- HR note: unsupported / generated = 0.5
- ViR note: recovered visual facts score = 0.33
- CoP_S: 0.25
- CoP_N: null
- CoP: 0.25
- HR: 0.5
- ViR: 0.33
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
Model Condensed
- Component order is right, but the state-point sequence is wrong.
- Unsupported detail: Secondary-loop state numbering is shifted (2/3/4/1/2 instead of 3/4/1/2).
Citations
- []
K Unsupported
- Secondary-loop state numbering is shifted (2/3/4/1/2 instead of 3/4/1/2).
```

- Scores

```text
Metric Work
- CoP note: Component order is right, but the state-point sequence is wrong.
- HR note: unsupported / generated = 0.4
- ViR note: recovered visual facts score = 0.4
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.4
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
Model Condensed
- The turbine-generator relationship is only partially captured.
- Unsupported detail: Treats the turbine itself as the electric-power-producing component.
Citations
- []
K Unsupported
- Treats the turbine itself as the electric-power-producing component.
```

- Scores

```text
Metric Work
- CoP note: The turbine-generator relationship is only partially captured.
- HR note: unsupported / generated = 0.25
- ViR note: recovered visual facts score = 0.5
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.25
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
Model Condensed
- The separate-secondary-loop point is right, but most of the explanation is extra.
- Unsupported detail: Radioactivity containment rationale is added.
- Unsupported detail: Operational-safety/equipment-longevity rationale is added.
- Unsupported detail: Design-optimization rationale is added.
Citations
- []
K Unsupported
- Radioactivity containment rationale is added.
- Operational-safety/equipment-longevity rationale is added.
- Design-optimization rationale is added.
```

- Scores

```text
Metric Work
- CoP note: The separate-secondary-loop point is right, but most of the explanation is extra.
- HR note: unsupported / generated = 0.5
- ViR note: recovered visual facts score = 1
- CoP_S: 0.5
- CoP_N: null
- CoP: 0.5
- HR: 0.5
- ViR: 1
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
Model Condensed
- The left branch is "Physical Security" with citation 10CFR73.
- The right branch is "Safeguards (MC&A)" with citation 10CFR74.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Both branch names and CFR citations are correct.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- Sequence is right except for 'Performance Design Criteria' instead of 'Functional Design Criteria'.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Sequence is right except for 'Performance Design Criteria' instead of 'Functional Design Criteria'.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 0.75
- CoP_N: null
- CoP: 0.75
- HR: 0
- ViR: 1
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
Model Condensed
- The central integration box is labeled "Integration of Design Requirements (Dual Function)".
- It represents the merging of security and safeguards design requirements into a combined or dual-function design basis.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Exact label and workflow meaning are correct.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- On the YES path, the workflow proceeds to "Final Design Optimized and Harmonized."
- On the NO paths, the process loops back to Final Design for further iteration.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: YES and NO path behavior is correctly described.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- Security Assessment Methods and Safeguards Assessment Methods appear alongside the Conceptual Design stage.
- Trade Studies appear alongside the Preliminary Design stage on both the left and right sides.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Supporting analysis activities and stages are correct.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
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
Model Condensed
- The control-volume structure is substantially wrong.
- Unsupported detail: Part A is reduced to reactor only.
- Unsupported detail: Part B is reduced to reactor plus steam generator.
- Unsupported detail: Part C is described as a cumulative expansion including turbine and fuel.
Citations
- []
K Unsupported
- Part A is reduced to reactor only.
- Part B is reduced to reactor plus steam generator.
- Part C is described as a cumulative expansion including turbine and fuel.
```

- Scores

```text
Metric Work
- CoP note: The control-volume structure is substantially wrong.
- HR note: unsupported / generated = 0.67
- ViR note: recovered visual facts score = 0.25
- CoP_S: 0
- CoP_N: null
- CoP: 0
- HR: 0.67
- ViR: 0.25
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
Model Condensed
- Both the panel identity and the label are wrong.
- Unsupported detail: Fuel is assigned to Part C instead of Part B.
- Unsupported detail: Uses q_fission instead of Q-dot at T_fuel.
Citations
- []
K Unsupported
- Fuel is assigned to Part C instead of Part B.
- Uses q_fission instead of Q-dot at T_fuel.
```

- Scores

```text
Metric Work
- CoP note: Both the panel identity and the label are wrong.
- HR note: unsupported / generated = 0.5
- ViR note: recovered visual facts score = 0
- CoP_S: 0.25
- CoP_N: null
- CoP: 0.25
- HR: 0.5
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
Model Condensed
- The split and heat-transfer label are only partially captured.
- Unsupported detail: Places Fuel in the left control volume.
- Unsupported detail: Omits C and P from the right volume.
- Unsupported detail: Uses Q_in instead of Q-dot at T_coolant.
Citations
- []
K Unsupported
- Places Fuel in the left control volume.
- Omits C and P from the right volume.
- Uses Q_in instead of Q-dot at T_coolant.
```

- Scores

```text
Metric Work
- CoP note: The split and heat-transfer label are only partially captured.
- HR note: unsupported / generated = 0.5
- ViR note: recovered visual facts score = 0.33
- CoP_S: 0.25
- CoP_N: null
- CoP: 0.25
- HR: 0.5
- ViR: 0.33
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
Model Condensed
- Electric output is recognized, but the atmospheric-flow labels are replaced by unsupported quantities.
- Unsupported detail: Adds Q_out as a right-side plant output.
- Unsupported detail: Adds temperature and heat-loss labels not present in the figure.
Citations
- []
K Unsupported
- Adds Q_out as a right-side plant output.
- Adds temperature and heat-loss labels not present in the figure.
```

- Scores

```text
Metric Work
- CoP note: Electric output is recognized, but the atmospheric-flow labels are replaced by unsupported quantities.
- HR note: unsupported / generated = 0.67
- ViR note: recovered visual facts score = 0.33
- CoP_S: 0.25
- CoP_N: null
- CoP: 0.25
- HR: 0.67
- ViR: 0.33
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
Model Condensed
- Figure 6-9 includes the component labels R, SG, T, G, C, and P.
- R represents the reactor, SG the steam generator, T the turbine, G the generator, C the condenser or cooler, and P the pump.
Citations
- []
K Unsupported
- []
```

- Scores

```text
Metric Work
- CoP note: Component-label meanings are correct.
- HR note: unsupported / generated = 0
- ViR note: recovered visual facts score = 1
- CoP_S: 1
- CoP_N: null
- CoP: 1
- HR: 0
- ViR: 1
```

## Average Scores

### GPT-4.1, Q1-Q15

| Metric | Score | Note/Remark |
| --- | --- | --- |
| Mean CoP | 0.764 | 15 questions |
| Mean HR | 0.2189 | 15 questions |
| Mean ViR | 0.5985 | 11 questions with defined ViR |

### GPT-4.1, Q16-Q30

| Metric | Score | Note/Remark |
| --- | --- | --- |
| Mean CoP | 0.6167 | 15 questions |
| Mean HR | 0.266 | 15 questions |
| Mean ViR | 0.676 | 15 questions with defined ViR |

### GPT-4.1, Q1-Q30

| Metric | Score | Note/Remark |
| --- | --- | --- |
| Mean CoP | 0.6903 | 30 questions |
| Mean HR | 0.2424 | 30 questions |
| Mean ViR | 0.6432 | 26 questions with defined ViR |
