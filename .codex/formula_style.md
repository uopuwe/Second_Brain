# Formula Style Standards

## Purpose

This document defines formula quality standards.
It is not a workflow.
Use it whenever adding or reviewing equations.
Continuous formula improvement is coordinated by [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md), which routes equation cleanup here instead of redefining formula rules.

## Mandatory Formula Elements

Every important formula must include:

- What it estimates.
- Assumptions.
- Symbol definitions.
- Units.
- Validity limits.
- Design implication when relevant.

## Standard Pattern

```markdown
For [stated model and assumptions]:

$$
equation
$$

where:

- $x$ is ... in ...

This approximation is useful for ... but does not include ...
```

## Good Example

```markdown
For small RMS phase error, time jitter is:

$$
\sigma_t = \frac{\sigma_\phi}{2\pi f_0}
$$

where:

- $\sigma_t$ is RMS time jitter in seconds.
- $\sigma_\phi$ is RMS phase error in radians.
- $f_0$ is carrier frequency in hertz.

The phase error must come from a specified phase-noise integration band.
```

## Bad Example

```markdown
jitter = phase noise / frequency
```

## High-Risk Formula Areas

- Phase noise to jitter conversion.
- ADC sampling jitter SNR.
- ENOB from SNDR.
- LDO pole/zero estimates.
- Bandgap temperature coefficients.
- Equalizer and channel response models.

## Formula Quality Gate

Before leaving an equation in a durable note:

- Are all symbols defined?
- Are units present?
- Is the model condition stated?
- Is it dimensionally reasonable?
- Is it being used outside its valid range?
- Does it imply a standards number without source support?
