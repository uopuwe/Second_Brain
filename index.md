# Tony Second Brain

## Purpose

This is my personal Second Brain for organizing long-term knowledge from ChatGPT conversations, work notes, investment analysis, health records, and life administration.

The goal is not to save every chat word-for-word, but to extract reusable knowledge, decisions, action items, and reference notes.

---

## Main Domains

### 1. Analog IC / SerDes

Folder: `01_AnalogIC_SerDes`

Use this for:

- Analog IC design
- SerDes architecture
- PCIe 7.0
- PLL / CDR / clocking
- ADC-based receiver
- LDO / bandgap
- Interview preparation
- Papers, books, study plans

Key files to create later:

- `analog_ic_serdes_master_index.md`
- `serdes_clocking_study_plan.md`
- `interview_qa_master.md`
- `pci_express_7_clocking.md`

Current key notes:

- `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`

Main technical areas:

- `01_AnalogIC_SerDes/SerDes/`
- `01_AnalogIC_SerDes/PLL_CDR_Clocking/`
- `01_AnalogIC_SerDes/ADC/`
- `01_AnalogIC_SerDes/LDO_Bandgap/`
- `01_AnalogIC_SerDes/Interview_QA/`
- `01_AnalogIC_SerDes/Papers_Books/`
- `01_AnalogIC_SerDes/Study_Plans/`

Active technical notes:

- `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`
- `01_AnalogIC_SerDes/Study_Plans/synopsys_4_week_prep_plan.md`
- `01_AnalogIC_SerDes/SerDes/pcie7_overview.md`
- `01_AnalogIC_SerDes/PLL_CDR_Clocking/phase_noise_jitter.md`
- `01_AnalogIC_SerDes/LDO_Bandgap/serdes_power_integrity.md`
- `01_AnalogIC_SerDes/LDO_Bandgap/ldo_psrr_notes.md`
- `01_AnalogIC_SerDes/LDO_Bandgap/ldo_stability_notes.md`
- `01_AnalogIC_SerDes/LDO_Bandgap/bandgap_reference_notes.md`

---

### 2. Synopsys Work

Folder: `02_Synopsys_Work`

Use this for:

- Synopsys offer and compensation
- Onboarding
- HR contacts
- Benefits and dental insurance
- Role preparation
- First-year technical focus
- Career strategy after joining

Key files to create later:

- `synopsys_master_note.md`
- `onboarding_plan.md`
- `benefits_dental.md`
- `first_90_days_plan.md`

Current key notes:

- `02_Synopsys_Work/synopsys_master_note.md`
- `02_Synopsys_Work/onboarding_plan.md`
- `02_Synopsys_Work/benefits_dental.md`
---

### 3. Investing

Folder: `03_Investing`

Use this for:

- Portfolio tracking
- QQU / QQC / QQQ strategy
- XCHP / CHPS / semiconductor ETFs
- Individual stocks
- Backtests
- RRSP / TFSA / non-registered accounts
- Tax-related investment notes

Key files to create later:

- `investing_master_note.md`
- `portfolio_current_state.md`
- `qqu_strategy.md`
- `rrsp_tfsa_strategy.md`

---

### 4. Canada Life

Folder: `04_Canada_Life`

Use this for:

- Banking
- RBC / Questrade / Qtrade
- CRA / tax filing
- Insurance
- Housing and real estate
- Family administration
- Travel and tickets
- Daily logistics in Canada

Key files to create later:

- `canada_life_master_note.md`
- `banking_rbc_master_note.md`
- `tax_canada_master_note.md`
- `family_admin.md`

---

### 5. Health / Medical

Folder: `05_Health_Medical`

Use this for:

- Dental care
- Sinus / respiratory issues
- Eye care
- Supplements
- Medical emails
- Insurance coverage questions
- Questions for doctors and dentists

Key files to create later:

- `health_master_note.md`
- `dental_master_note.md`
- `sinus_respiratory_note.md`
- `eye_health_note.md`

---

### 6. Other Affairs

Folder: `06_Other_Affairs`

Use this for:

- Miscellaneous tasks
- Restaurants
- Events
- Car issues
- Travel details
- Household matters
- One-off questions that do not deserve a major category

Key files to create later:

- `other_affairs_master_note.md`
- `restaurants_events.md`
- `household_tasks.md`

---

## Current Priorities

1. Build the Second Brain structure.
2. Organize Synopsys onboarding and role preparation.
3. Consolidate Analog IC / SerDes / PCIe 7.0 study notes.
4. Organize investment strategy and backtest records.
5. Keep health and dental records searchable.
6. Archive raw ChatGPT conversations without mixing them into clean notes.

---

## Workflow

### Weekly Workflow

1. Export or copy important ChatGPT conversations.
2. Save raw materials into `00_Inbox` after that folder is created.
3. Ask ChatGPT to summarize and extract reusable notes.
4. Save processed notes into the correct domain folder.
5. Use Codex to clean file names, update indexes, and create backlinks.
6. Review changes manually.
7. Commit changes with Git.

### Git Workflow

```powershell
git status
git add .
git commit -m "Update second brain notes"