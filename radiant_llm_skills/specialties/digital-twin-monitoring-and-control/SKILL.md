---
name: digital-twin-monitoring-and-control
description: Use for digital twins, monitoring, telemetry, sensor fusion, state estimation, Kalman filtering, anomaly detection, residual analysis, data assimilation, supervisory analytics, and control-caveat questions.
---

# Digital Twin, Monitoring, and Control Skill

## Purpose
Support traceable discussion of digital twins, monitoring architectures, state estimation, anomaly detection, supervisory analytics, and control-related caveats for advanced reactors.

## When To Use
- Digital twin, monitoring, telemetry, sensor fusion, state estimation, Kalman filtering, anomaly detection, residual analysis, data assimilation, or supervisory control questions

## Core Questions This Skill Helps Answer
- What role is the digital twin playing: estimation, prediction, diagnostics, optimization, or advisory control?
- Which measurements, model assumptions, and update rules matter?
- What limits should be stated before turning analytics into operational recommendations?

## Scope and Non-Goals
- This skill supports interpretation of monitoring and estimation concepts.
- It does not authorize closed-loop control actions or safety-critical control logic.

## Required Evidence Posture
- Separate measurement data, model assumptions, and inferred states.
- State whether the claim is based on estimation, simulation, diagnostics, or control synthesis.
- Keep supervisory analytics distinct from operator authority and safety-system actuation.

## Reasoning Checklist
- Define measurements, estimated states, model assumptions, and update cadence.
- Note whether residuals or anomalies are qualitative, statistical, or model-based.
- Flag observability, latency, and data-quality limitations before suggesting decisions.

## Preferred Source Hierarchy
1. This skill's reference anchors and equation/formula notes
2. User local RAG evidence
3. Stable estimation, controls, and digital-twin literature

## References
- Standard state-estimation and control references: use for filter notation, residual concepts, observability, and control-caveat language.
- Digital-twin and model-based monitoring literature: use for synchronization, virtual sensors, diagnostics, and predictive analytics framing.
- Nuclear instrumentation and monitoring references: use for plant-specific measurement considerations and operational caveats.

## Equations and Formulae
- State-space framing: use generic state and measurement equations only when discussing estimation or observer structure conceptually. Define symbols before use.
- Residual or innovation interpretation: residuals are model-versus-measurement differences used for monitoring and diagnosis. Do not claim anomaly significance thresholds without a stated detection rule or statistical basis.
- Kalman-style updates: notation may be used conceptually for state estimation, uncertainty, and sensor fusion. Do not fabricate covariance matrices, tuning values, or stability claims.

## Examples
- Explain how a digital twin can support state estimation without becoming an automatic control authority.
- Summarize anomaly detection results while separating measured facts from model-based inference.
- Draft a monitoring architecture note that identifies telemetry, model state, residuals, and response boundaries.

## Limitations and Disclaimer
- Monitoring and control interpretations depend on plant instrumentation, model fidelity, and validation status.
- Verify with qualified controls, instrumentation, and safety personnel before operational use.
