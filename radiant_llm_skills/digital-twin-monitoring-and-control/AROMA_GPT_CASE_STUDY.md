# AROMA-GPT Case Study
## AI-Assisted Digital Twin Guidance for Reactor Monitoring, Residual Analysis, and Supervisory Advisory Control

**AROMA-GPT** stands for **Advanced Reactor Operation and Monitoring Assistant (GPT-based)**: a retrieval-augmented, human-supervised AI agent for real-time monitoring, anomaly detection, and advisory control of advanced reactors. The acronym is used throughout this file in its abbreviated form after this first definition.

## Purpose
This adjacent file provides an illustrative case-study-style extension to the generic digital-twin skill. It is intended to deepen guidance for users interested in AI-assisted digital twins for advanced reactor monitoring, anomaly-aware supervision, reduced-order dynamic modeling, and supervisory control recommendations.

This file is **supplemental** to `SKILL.md`. It does not replace the generic skill. It is an example of how a specific project or study can be represented as an adjacent case-study note while preserving traceability and appropriate caution.

## How To Use This File
Use this file when the user asks for:
- A practical digital-twin workflow rather than only a conceptual explanation
- Guidance on black-box or reduced-order modeling for reactor monitoring
- State-space framing for reactor digital twins
- Transfer-function interpretation around operating points
- Residual generation and anomaly-diagnosis structure
- Supervisory inference of hidden or difficult-to-measure quantities
- Human-supervised digital-twin advisory control
- Case-study-grounded examples inspired by AROMA-GPT

If multiple adjacent case-study files exist in this folder, treat them as examples of method families and implementation patterns. Do not assume one case study universally applies to all reactor concepts.

## Scope and Caution
This file reflects a **generalized and non-proprietary** interpretation of a reactor digital-twin case-study pattern inspired by AROMA-GPT-related work.

It is suitable for:
- advisory discussion
- digital-twin architecture design
- workflow planning
- reduced-order model formulation
- residual-based monitoring logic
- interpretation of inferred quantities

It is **not** a substitute for:
- licensed control-system design
- plant-specific safety analysis
- qualified instrumentation engineering
- validated estimator tuning
- final anomaly-classification authority
- autonomous safety-critical control logic

## Traceable High-Level Takeaways
The AROMA-GPT-related material supports the following generalized claims:

- An LLM-assisted digital twin can be used as a **human-supervised advisory layer** for advanced reactor monitoring and control support.
- The plant may be treated as a **modular black box** for the purpose of building an external monitoring and supervisory advisory framework.
- A reduced-order dynamic simulator or digital twin can be used to:
  - monitor state evolution over time
  - issue anomaly warnings
  - support mitigation recommendations
  - answer operator questions about plant state and behavior
- High-level operator goals can be translated into **quantitative, physically meaningful supervisory recommendations**, including actuator-related guidance, while preserving human authority.
- Retrieval-augmented knowledge support can complement real-time monitoring by enabling:
  - reactor-state queries
  - generic knowledge queries
  - post-transient interpretation
  - historical-event review

These are case-study-level architecture patterns, not universal guarantees.

## Generalized Architecture Pattern
A useful abstraction for an AI-assisted reactor digital twin is:

1. **Plant or trusted plant surrogate**
   - real plant, simulator, or high-fidelity benchmark model

2. **Data acquisition and synchronization layer**
   - time-stamped sensors
   - operator commands
   - actuator records
   - status flags
   - disturbances when available

3. **Reduced-order digital twin**
   - first-principles, reduced-order, identified, or hybrid model
   - suitable for estimation and near-real-time prediction

4. **Estimator or observer**
   - state estimator, observer, filter, or hybrid inference module
   - reconstructs hidden states or denoised trends

5. **Prediction layer**
   - simulates expected outputs under current or candidate inputs
   - may use state-space, transfer-function, surrogate, or hybrid methods

6. **Residual and consistency engine**
   - compares observed behavior with predicted behavior
   - computes residuals, innovations, or anomaly scores
   - checks multichannel physical consistency

7. **Diagnostic and advisory logic**
   - interprets deviations
   - distinguishes likely process upset, sensor issue, actuator issue, model drift, or cyber-physical inconsistency
   - recommends next checks or cautious operator actions

8. **LLM and knowledge layer**
   - explains plant behavior
   - answers questions
   - retrieves relevant references or prior cases
   - converts high-level intent into structured advisory guidance

9. **Human authority / approved plant systems**
   - final authority remains with qualified humans and approved control/safety systems

## Recommended Workflow for Users Building a Digital Twin
This workflow is intended to generalize across reactor concepts and case studies.

### Step 1: Define the Purpose
Decide whether the twin is primarily for:
- state estimation
- anomaly detection
- virtual sensing
- operator advisory support
- optimization support
- what-if simulation
- actuator recommendation under supervision

### Step 2: Define the System Boundary
Specify:
- plant subsystem or whole-plant scope
- relevant operating modes
- expected disturbances
- actuator boundaries
- trusted versus uncertain measurements

### Step 3: Identify Inputs, Outputs, States, and Hidden Quantities
Typical categories:
- **inputs**: actuator commands, boundary conditions, operator setpoints
- **outputs**: measured temperatures, power, flow, flux, pressures, statuses
- **states**: reduced-order internal dynamic variables
- **hidden quantities**: inferred effectiveness, reactivity-related indicators, actuator contribution, latent degradation indicators

### Step 4: Formulate a Dynamic Model
A practical starting point is a dynamic model of the form:
$$\dot{x}(t) = f(x(t), u(t), d(t), \theta)$$

$$y(t) = g(x(t), u(t), \theta) + v(t)$$

where:
- $x$: internal state vector
- $u$: input or control vector
- $d$: disturbance vector
- $\theta$: model parameters
- $y$: measured output vector
- $v$: measurement uncertainty

This may come from:
- first-principles balances
- reduced-order approximations
- identified input-output dynamics
- hybrid physics/ML models

### Step 5: Convert to State-Space Form
For estimation and residual generation, represent the model in state-space form.

Continuous-time linearized form:
$$\dot{x}(t) = A x(t) + B u(t) + E d(t)$$

$$y(t) = C x(t) + D u(t)$$

Discrete-time form:
$$x_{k+1} = A_d x_k + B_d u_k + E_d d_k + w_k$$

$$y_k = C_d x_k + D_d u_k + v_k$$

This is useful for:
- observers
- Kalman-style estimation
- simulation
- residual generation
- hidden-state inference
- actuator-effect interpretation

### Step 6: Derive Transfer-Function Relations When Helpful
For local linear interpretation around an operating point:
$$G(s) = C (sI - A)^{-1} B + D$$

This is useful when users want to understand:
- how an input affects an output
- local dynamic sensitivity
- actuator-to-response mapping
- time-domain or frequency-domain intuition around a nominal state

This does **not** imply global validity across all regimes.

### Step 7: Generate Predictions
Use the model or estimator to compute:
- expected outputs
- expected state evolution
- expected response to known actuator inputs
- expected response under candidate control actions

Denote predicted outputs as:
$$\hat{y}_k$$

and predicted or estimated states as:
$$\hat{x}_k$$

### Step 8: Compute Residuals
Residuals compare observed and predicted behavior.

Basic residual:
$$r_k = y_k^{obs} - \hat{y}_k$$

Channel-wise residual:
$$r_{i,k} = y_{i,k}^{obs} - \hat{y}_{i,k}$$

Normalized residual:
$$\tilde{r}_{i,k} = \frac{y_{i,k}^{obs} - \hat{y}_{i,k}}{\sigma_i}$$

Innovation form:
$$\nu_k = y_k - C \hat{x}_{k|k-1} - D u_k$$

Weighted anomaly score:
$$J_k = r_k^\top W r_k$$

Simple norm-based score:
$$J_k = \|r_k\|_2$$

Optional moving-window aggregation:
$$\bar{J}_{k,N} = \sum_{j=k-N+1}^{k} r_j^\top W r_j$$

These are generic forms. Thresholds, window lengths, and weights must be plant-specific and validated.

## Interpreting Residuals
Residuals can support diagnostic reasoning, but interpretation must be cautious.

### Residual Patterns and Possible Meanings
- **small residuals within expected uncertainty**  
  nominal model-to-measurement agreement

- **persistent bias in one channel**  
  possible drift, calibration issue, unmodeled disturbance, or local model mismatch

- **persistent bias across multiple physically related channels**  
  possible state-estimation issue, model mismatch, disturbance shift, or evolving process anomaly

- **oscillatory or delayed mismatch**  
  possible actuator lag, control interaction, unmodeled dynamics, or mode transition

- **command-response inconsistency**  
  possible actuator fault, controller issue, or cyber/data integrity concern

- **individually plausible but jointly impossible measurements**  
  possible instrumentation inconsistency, synchronization issue, or cyber-physical anomaly

Residuals alone do not prove causality. They support structured triage.

## Supervisory Inference of Hidden Quantities
A key digital-twin use case is inference of quantities that are not directly measured or are only indirectly observable.

Generic hidden-quantity inference:
$$\hat{z}_k = f_z(\hat{x}_k, u_k, y_k, \theta)$$

Possible inferred quantities include:
- actuator contribution
- effective control authority
- reactivity-related indicators
- latent degradation markers
- unmeasured internal thermal states
- operational consistency indicators

### Generic Reactivity-Related or Actuator-Effect Mapping
A generalized mapping may be represented as:
$$\hat{\rho}_{act,k} = f_\rho(\hat{x}_k, u_k, y_k)$$

where $\hat{\rho}_{act,k}$ is a generic inferred actuator-effect or reactivity-related contribution.

### Generic Actuator State or Position Inference
A generalized mapping may be represented as:
$$\hat{p}_{act,k} = f_p(\hat{x}_k, u_k, y_k)$$

where $\hat{p}_{act,k}$ is a generic inferred actuator state or position-related quantity.

These equations are intentionally generic. They allow the skill to guide users conceptually without exposing plant-specific proprietary formulas.

## Applying This Pattern to Control-Rod-Related Inference
For reactor concepts where control rods or equivalent actuators are relevant, a digital twin may support:

- interpretation of actuator effectiveness
- inferred rod-position consistency checks
- translation of operator power-intent into quantitative supervisory guidance
- comparison of commanded versus inferred actuator impact
- consistency checking between measured plant response and expected actuator-effect mapping

The safe generalized framing is:
- treat rod worth or rod-effect relationships as **plant-specific nonlinear mappings**
- treat rod-position inference as **measured, estimated, or reconstructed depending on instrumentation and model structure**
- require calibration and validation before using such relations for consequential advisory logic

Do **not** present any one rod-worth curve or mapping as universal.

## Worked Case-Study Derivation: Reactivity From the Transfer Function (AROMA-GPT)
This section shows, at a generalizable and non-proprietary level, how AROMA-GPT derives a required reactivity change from a transfer-function (DC-gain) view of the plant. Plant-specific matrices and coefficients are intentionally omitted; only the method and its assumptions are given, so the workflow can be reused for any plant with an identifiable linear model.

### Step 1: Linearized state-space model
Around a chosen operating point, the plant is represented as a linear time-invariant state-space system:
$$\dot{X}(t) = A X(t) + B U(t), \qquad Y(t) = C X(t) + D U(t)$$

where $X$ is the state, $U$ the input (e.g., reactivity and boundary perturbations), and $Y$ the measured output (e.g., power and temperatures). In AROMA-GPT, $A, B, C, D$ are obtained by linearizing a nonlinear physics-based simulator that couples point-reactor kinetics, energy and momentum balances, and reactivity/temperature feedbacks. In general the same matrices can instead be identified from operating data (e.g., extended or unscented Kalman filtering, subspace identification), which is what makes the method portable to other simulators or a real facility.

### Step 2: Transfer function and DC gain
The input-output transfer function of the LTI model is
$$G(s) = C (sI - A)^{-1} B + D.$$

For a steady-state (constant-input) maneuver, evaluate the transfer function at $s \to 0$ to obtain the DC-gain matrix:
$$G_{DC} = G(0) = D - C A^{-1} B, \qquad Y_{ss} = G_{DC}\, U_{ss}.$$

$G_{DC}$ relates steady input perturbations to steady-state output changes.

### Step 3: Invert the DC gain for the required reactivity
To achieve a desired steady power change $\Delta P_{desired}$ while holding the secondary inlet temperature perturbation at zero ($\Delta T_{sec,in} = 0$), invert the relevant single-input/single-output element of the DC-gain relation:
$$\Delta \rho_{needed} = \frac{\Delta P_{desired}}{[G_{DC}]_{1,1}}.$$

This is the core of the reactivity-prediction logic: the reactivity insertion needed for a power maneuver is read directly from the inverse DC gain, rather than by trial-and-error simulation.

### Step 4: Map reactivity to rod motion
The required $\Delta\rho_{needed}$ is then mapped to physical control-rod positions through the nonlinear, S-shaped rod-worth curve. In AROMA-GPT this curve is built by normalizing TRIGA experimental rod-worth data into characteristic shape functions and scaling them to the target core by assigning a maximum worth to each rod (e.g., SHIM, REGULATING, TRANSIENT), with the worth coefficients tuned so the combined worth exceeds the shutdown (SCRAM) margin.

### Assumptions and Their Implications
- **Linearization about an operating point.** $A, B, C, D$ describe small-perturbation behavior only. Because the real plant/simulator is fully nonlinear, the linear prediction carries a small steady-state error; in the AROMA-GPT demonstration this was about 2.6% (a predicted 86.18% rod insertion versus the realized steady power). Accuracy degrades as the maneuver moves further from the operating point.
- **Steady-state (DC) inversion.** Using $G_{DC} = G(0)$ assumes the maneuver targets a new equilibrium and that $A$ is invertible (no pure integrators or marginal modes). Transient overshoot and settling are not captured by the DC gain alone.
- **Channel decoupling.** Holding $\Delta T_{sec,in} = 0$ reduces the problem to the single $[G_{DC}]_{1,1}$ element. If secondary-side conditions change, the off-diagonal couplings of $G_{DC}$ must be retained.
- **Invertibility and observability.** The inversion is only meaningful when $[G_{DC}]_{1,1} \neq 0$ and the model is sufficiently observable/identifiable.
- **Rod-worth transferability.** The S-shaped worth curve is treated as a universal qualitative characteristic, but absolute worths are plant-specific. A curve scaled from a different reactor (e.g., TRIGA to an LFR) is an engineering approximation, not a validated worth for the target core, and must be calibrated.

### Why this generalizes
The reactivity prediction does not require the proprietary internals of any specific reactor. Any plant with an identifiable linear realization $\{A, B, C, D\}$ admits the same DC-gain inversion. A user can therefore (1) identify or linearize their own model, (2) form $G_{DC}$, (3) invert the relevant element for the required input, and (4) map that input to actuator motion through a calibrated, plant-specific worth relationship, all under human supervision. This is why the case study can be exposed as method-level guidance while the plant-specific coefficients remain a black box.

## Physics-Based Models That Can Be Converted Into State-Space Form
For many reactor digital twins, a practical route is:

1. begin with dominant physics or reduced-order balances  
2. write coupled ordinary differential equations for the main dynamics  
3. define inputs, outputs, disturbances, and parameters  
4. choose an operating point or operating regime  
5. linearize if needed  
6. form a state-space realization  
7. validate against trusted data  
8. use the resulting model for monitoring, estimation, and advisory support

Examples of model families that may admit this workflow include:
- reduced neutronic-thermal coupling models
- thermal-hydraulic lumped-parameter models
- actuator-to-response reduced-order models
- empirical or semi-empirical black-box state-space models
- hybrid physics-guided ML surrogates with explicit state-update structure

## Smart Reference-Governor Framing
A useful way to explain AI-assisted supervisory control is:

- a conventional controller or reference governor preserves core control and constraint enforcement
- the digital twin predicts trajectory trends and evaluates consistency
- the AI layer explains plant behavior, flags early concern, and recommends cautious setpoint or actuator adjustments
- qualified humans and approved plant systems retain final authority

This framing is often safer and more defensible than portraying the LLM as the direct control authority.

## How RADIANT-LLM Should Generalize From This Case Study
When users ask for help in building a digital twin, RADIANT-LLM should be able to:

- guide them to define plant boundaries and objectives
- help structure a reduced-order or black-box model
- explain how to obtain a state-space form
- explain when a transfer function is useful
- help define predicted outputs and residuals
- explain how to normalize or aggregate residuals
- help distinguish process anomalies from sensor or actuator issues
- explain how hidden quantities may be inferred from model-data relationships
- preserve caveats about observability, validation, uncertainty, and human authority

## Suggested Template for Future Adjacent Case-Study Files
Users may add other adjacent case-study notes. A good pattern is:

1. **Purpose and scope**
2. **Plant or subsystem boundary**
3. **Operating modes covered**
4. **Inputs, outputs, states, disturbances**
5. **Model family used**
6. **Prediction method**
7. **Residual definitions**
8. **Anomaly interpretation logic**
9. **Hidden-state or parameter inference logic**
10. **Validation basis**
11. **Limits of applicability**
12. **References**

This makes the skill extensible without overloading the main `SKILL.md`.

## References and Traceability Notes
Use the following as case-study anchors rather than universal authority:

- Ndum et al., **“Large language model-assisted digital twin for remote monitoring and control of advanced reactors”**  
  User-provided journal link:  
  https://www.sciencedirect.com/science/article/pii/S0149197025005700

- Z. N. Ndum, **“A Generative AI-Driven Framework for Robust Automation of Nuclear Modeling and Simulation Workflows with Multi-Modal Domain Knowledge Integration,”** Ph.D. Dissertation, Texas A&M University.  
  See Chapter 6, *Case Study 3: Advanced Reactor Operation and Monitoring Assistant (AROMA-GPT)*, Section 6.3.1 (Reactivity and control-rod management tool library), Eqs. (6.1)–(6.3), for the state-space, DC-gain, and reactivity-inversion derivation summarized above.  
  Note: confirm the final degree year and any page/equation numbering before formal citation.

## Final Caution
This file is designed to help RADIANT-LLM reason more usefully about AI-assisted reactor digital twins. It should improve guidance quality, but it should not cause the model to:
- overclaim anomaly certainty
- invent thresholds or tuning constants
- present case-study mappings as universal laws
- recommend autonomous safety-critical action
- ignore instrumentation, validation, uncertainty, or operating-mode limits

Use this file as a structured advisory case study layered on top of the generic digital-twin skill.