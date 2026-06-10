---
name: digital-twin-monitoring-and-control
description: Use for digital twins, monitoring, telemetry, sensor fusion, state estimation, anomaly detection, residual analysis, data assimilation, supervisory analytics, control-caveat questions, and adjacent case-study guidance when available.
---

# Digital Twin, Monitoring, and Control Skill

## Purpose
Support traceable discussion of digital twins, monitoring architectures, state estimation, anomaly detection, supervisory analytics, and control-related caveats for advanced reactors.

This skill is intentionally generic and self-contained. It may also be complemented by adjacent case-study or equation-note files when available. Those adjacent files can deepen topic-specific guidance, but this file remains the primary reusable guidance layer.

## When To Use
- Digital twin, monitoring, telemetry, sensor fusion, state estimation, observer design, Kalman filtering, anomaly detection, residual analysis, data assimilation, supervisory control, virtual sensing, smart reference-governor framing, or control-caveat questions
- Questions about how to structure a reduced-order or black-box reactor digital twin for monitoring, diagnostics, prediction, or operator advisory support
- Questions about mapping physics-based or reduced-order models into state-space or transfer-function forms for estimation and monitoring

## Core Questions This Skill Helps Answer
- What role is the digital twin playing: estimation, prediction, diagnostics, optimization, virtual sensing, or advisory control?
- Which measurements, model assumptions, update rules, and operating modes matter?
- How should measurements, predictions, estimated states, and inferred hidden variables be kept distinct?
- How can residuals be defined and interpreted without overstating anomaly significance?
- What limits should be stated before turning analytics into operational recommendations?

## Scope and Non-Goals
- This skill supports interpretation of monitoring, estimation, residual-generation, and supervisory-control concepts.
- This skill may guide users in setting up generic reduced-order, black-box, or state-space digital twin workflows.
- This skill may support conceptual interpretation of transfer functions, observers, innovations, residuals, and inferred hidden quantities.
- This skill does **not** authorize closed-loop control actions or safety-critical control logic.
- This skill does **not** replace validated plant models, qualified instrumentation, plant procedures, safety-system logic, or licensed control design.

## Adjacent File Convention
- This `SKILL.md` is the primary generic guidance file.
- If adjacent files exist in this skill folder, they may be used as progressive-disclosure resources for:
  - case studies
  - equation notes
  - implementation examples
  - workflow templates
  - validation notes
- Adjacent files are illustrative and supplemental. They may reflect plant- or study-specific assumptions.
- When using adjacent files:
  - preserve the distinction between generic method and case-specific implementation
  - do not present case-study coefficients, thresholds, mappings, or correlations as universal
  - carry forward any stated assumptions, operating limits, and validation caveats
- If multiple adjacent case-study files exist, treat them as examples of method families, not interchangeable truth sources.

## Required Evidence Posture
- Separate:
  1. measured data,
  2. model assumptions,
  3. predicted outputs,
  4. estimated states,
  5. inferred hidden parameters or quantities,
  6. operator intent or supervisory recommendations.
- State whether a claim is based on:
  - first-principles physics,
  - reduced-order modeling,
  - identified black-box dynamics,
  - simulation,
  - estimation,
  - diagnostics,
  - or control synthesis.
- State the relevant operating mode, time scale, and update cadence when they matter.
- Flag observability, identifiability, latency, noise, drift, and mode-coverage limitations before suggesting decisions.
- Keep supervisory analytics distinct from operator authority and safety-system actuation.

## Reasoning Checklist
- Define system boundaries, operating mode, and the twin’s intended role.
- Identify measured inputs, outputs, disturbances, candidate states, and hidden quantities of interest.
- State whether the model is:
  - first-principles,
  - reduced-order,
  - black-box,
  - linearized,
  - hybrid physics/ML,
  - or data-driven.
- Clarify whether predictions are obtained from:
  - direct simulation,
  - observer-based estimation,
  - transfer-function response,
  - surrogate models,
  - or data-driven forecasting.
- Define residuals or innovations before interpreting anomalies.
- State whether anomaly logic is:
  - qualitative,
  - threshold-based,
  - statistical,
  - model-based,
  - or hybrid.
- Check observability, sensor health, calibration, synchronization, and mode validity.
- Preserve human authority for consequential actions.

## Preferred Source Hierarchy
1. This skill’s reference anchors and equation/formula notes
2. Adjacent case-study or implementation-note files in this skill folder
3. User local RAG evidence
4. Stable estimation, controls, monitoring, and digital-twin literature

## References
- Standard state-estimation and control references: use for state-space notation, observers, innovations, residual concepts, observability, identifiability, and control-caveat language.
- Digital-twin and model-based monitoring literature: use for synchronization, virtual sensing, diagnostics, predictive analytics, and lifecycle alignment of models with plant data.
- Nuclear instrumentation and monitoring references: use for plant-specific measurement considerations, uncertainty, latency, calibration, and operational caveats.
- Reactor digital-twin case studies: use as examples of human-supervised monitoring and advisory architectures, not universal control laws.

## Equations and Formulae

### 1. Generic State-Space Framing
Use generic state and measurement equations when discussing estimation, observers, simulation, or residual generation. Define symbols before use.

Continuous time:
$$\dot{x}(t) = A x(t) + B u(t) + E d(t)$$

$$y(t) = C x(t) + D u(t) + v(t)$$

Discrete time:
$$x_{k+1} = A_d x_k + B_d u_k + E_d d_k + w_k$$

$$y_k = C_d x_k + D_d u_k + v_k$$

Where:
- $x$: state vector
- $u$: control or input vector
- $d$: disturbance vector
- $y$: measured output vector
- $w$: process uncertainty or process noise term
- $v$: measurement uncertainty or noise term
- $A,B,C,D,E$: model matrices

Use this framing for:
- reduced-order reactor dynamics
- black-box input-output abstractions with internal states
- observer design
- state estimation
- residual generation
- virtual sensing or hidden-state inference

### 2. Transfer-Function Relation
For linear time-invariant realizations around a stated operating point, transfer-function notation may be used for input-output interpretation:

$$G(s) = C (sI - A)^{-1} B + D$$

Use transfer-function language for:
- input-output sensitivity
- actuator-to-output interpretation
- local linear response analysis
- control-oriented reasoning around an operating point

Do **not** imply global validity of a transfer function outside its stated assumptions, operating region, or linearization basis.

### 3. Residuals, Innovations, and Monitoring
Residuals are model-versus-measurement differences used for monitoring and diagnosis.

Basic residual:
$$r_k = y_k^{obs} - \hat{y}_k$$

Channel-wise residual:
$$r_{i,k} = y_{i,k}^{obs} - \hat{y}_{i,k}$$

Normalized residual:
$$\tilde{r}_{i,k} = \frac{y_{i,k}^{obs} - \hat{y}_{i,k}}{\sigma_i}$$

where $\sigma_i$ is a plant- or study-specific uncertainty scale for channel $i$.

Innovation form for observer-based estimation:
$$\nu_k = y_k - C \hat{x}_{k|k-1} - D u_k$$

Weighted residual score:
$$J_k = r_k^\top W r_k$$

or, in simpler form:
$$J_k = \|r_k\|_2$$

These equations support:
- consistency checking
- anomaly scoring
- channel comparison
- observer correction
- trend and drift interpretation

Do **not** claim anomaly significance thresholds without a stated detection rule, statistical basis, uncertainty model, or validation basis.

### 4. Hidden-State or Parameter Inference
Some quantities of interest may be measured directly, estimated as states, or inferred as hidden parameters depending on the model and instrumentation architecture.

Generic hidden-quantity mapping:
$$\hat{z}_k = f_z(\hat{x}_k, u_k, y_k, \theta)$$

For example, inferred control effectiveness, actuator contribution, or reactivity-related indicators may be represented generically as:
$$\hat{\rho}_{k} = f_\rho(\hat{x}_k, u_k, y_k)$$

$$\hat{p}_{k} = f_p(\hat{x}_k, u_k, y_k)$$

where:
- $\hat{\rho}_k$: inferred reactivity-related quantity or actuator-effect estimate
- $\hat{p}_k$: inferred actuator state or position-related quantity
- $f_\rho, f_p$: plant-specific mappings identified from physics, reduced-order structure, estimation logic, or calibrated data relationships

Do **not** present any such mapping as universal. Identification, calibration, observability, and validation are plant-specific.

### 5. Physics-to-Model Workflow Note
When appropriate, the skill may guide users from physics-based or reduced-order dynamics toward estimation-ready models:

1. define system boundary and operating mode  
2. identify key balances and dominant dynamics  
3. define candidate states, inputs, outputs, and disturbances  
4. derive or identify a reduced-order dynamic model  
5. linearize around an operating point if needed  
6. express the model in state-space form  
7. derive transfer-function relations if useful for interpretation  
8. validate predictions against measured or trusted simulated data  
9. deploy residual monitoring only within validated operating regions

## Interpretation Guidance
- Small, zero-mean, uncertainty-consistent residuals may indicate nominal agreement.
- Persistent bias may indicate sensor drift, calibration shift, disturbance bias, or model mismatch.
- Structured transients may indicate mode changes, actuator lag, disturbances, or evolving faults.
- Cross-channel inconsistencies may indicate instrumentation faults or coordinated data issues.
- Command-response mismatch may indicate actuator, controller, or cyber-physical integrity issues.
- Physically implausible multivariate behavior should be treated cautiously and may warrant defensive security review, instrumentation review, or model-validity review.

## Examples
- Explain how a digital twin can support state estimation without becoming automatic control authority.
- Show how to structure a reduced-order reactor model for monitoring and residual generation.
- Summarize anomaly detection logic while separating measured facts from model-based inference.
- Explain how transfer-function and state-space views complement each other in digital-twin design.
- Draft a monitoring architecture note that identifies telemetry, model state, residuals, inferred hidden quantities, and response boundaries.
- Interpret a control recommendation as supervisory guidance rather than autonomous actuation.

## Limitations and Disclaimer
- Monitoring and control interpretations depend on plant instrumentation, model fidelity, operating-mode coverage, and validation status.
- Transfer-function, state-space, and residual logic are only as reliable as the assumptions, calibration, and uncertainty treatment behind them.
- Digital-twin-based anomaly indicators do not by themselves prove fault causality.
- Thresholds, gains, covariance structures, and alarm logic should not be invented.
- Verify with qualified controls, instrumentation, safety, security, and operations personnel before operational use.
- Keep final authority for consequential actions with approved plant systems and qualified humans.