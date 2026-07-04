# Knowledge Tree

## Purpose

This document defines the vault architecture.
It is a structure standard, not a workflow.
For task routing, see [core/workflow_router.md](core/workflow_router.md).
For the complete scalable architecture, use [knowledge_architecture.md](knowledge_architecture.md).

## Canonical Top-Level Tree

```text
Second_Brain/
  00_Inbox/
  01_AnalogIC_SerDes/
  02_Synopsys_Work/
  03_Investing/
  04_Canada_Life/
  05_Health_Medical/
  06_Other_Affairs/
  70_Indexes/
  80_MOCs/
  90_Archive/
  99_Templates/
  .codex/
  export_data/
  tools/
```

## Routing Standard

- `00_Inbox/`: raw and semi-processed source material.
- `01_AnalogIC_SerDes/`: canonical reusable technical knowledge.
- `02_Synopsys_Work/`: work context, onboarding, and role-specific planning.
- `70_Indexes/`: curated inventory pages that answer what exists.
- `80_MOCs/`: Maps of Content that explain how topics connect.
- `90_Archive/`: processed, rejected, superseded, or sensitive source packets that have completed the ingestion pipeline.
- `99_Templates/`: user-facing Obsidian templates.
- `.codex/`: AI operating system.
- `tools/`: reusable scripts and analysis utilities.
- `export_data/`: generated or exported material unless proven otherwise.

## Analog IC / SerDes Branch

Canonical technical folders:

```text
01_AnalogIC_SerDes/
  SerDes/
  SerDes_RX/
  PLL_CDR_Clocking/
  ADC/
  ADC_TI_SAR/
  LDO_Bandgap/
  Interview_QA/
  Papers_Books/
  Study_Plans/
```

## Domain Ownership

- `SerDes/`: system architecture, PCIe, PAM4, equalization, signal integrity.
- `SerDes_RX/`: receiver-specific architecture and ADC/DSP receiver chains.
- `PLL_CDR_Clocking/`: PLL, CDR, phase noise, jitter, clock distribution.
- `ADC/`: converter fundamentals, sampling jitter, ADC-based receiver concepts.
- `ADC_TI_SAR/`: time-interleaved SAR implementation and calibration.
- `LDO_Bandgap/`: regulators, references, PSRR, stability, SerDes power integrity.
- `Interview_QA/`: interview answers and technical story bank.
- `Papers_Books/`: source-specific paper and book notes.
- `Study_Plans/`: learning plans and current focus.

## Good Routing Examples

```text
PCIe 7.0 clocking note -> PLL_CDR_Clocking/
ADC-based PAM4 RX paper -> Papers_Books/ plus links to ADC/ and SerDes_RX/
LDO noise affecting PLL jitter -> LDO_Bandgap/ plus links to PLL_CDR_Clocking/
PLL interview answer -> Interview_QA/ plus links to PLL_CDR_Clocking/
```

## Bad Routing Examples

```text
Raw chat transcript -> PLL_CDR_Clocking/
Paper summary mixed directly into a generic ADC note without citation.
Interview answer duplicated as a second technical reference note.
```

## Edge Cases

- If a note has two domains, choose the folder where a future reader would search first and add cross-links.
- If material is source-specific, keep it in `Papers_Books/` or `00_Inbox/` and promote only reusable synthesis.
- If a duplicate folder exists, treat the non-copy folder as canonical unless instructed otherwise.
- If work-specific information contains reusable learning, generalize the technical part before moving it into `01_AnalogIC_SerDes/`.
- If a source packet has completed processing, archive it under `90_Archive/` according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).

## Architecture Quality Gate

Before creating or moving a note:

- Is this raw source or durable knowledge?
- Is the destination canonical?
- Is the note purpose aligned with the folder?
- Are cross-domain relationships handled by links instead of duplication?
- Does an existing note already cover this topic?
