# Processed Batch 2: SerDes / PCIe / PLL / CDR / ADC

Date processed: 2026-07-01

## Source Packet Used

* `../manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

Note: This packet is a manual first-pass reconstruction before official ChatGPT data export is available. It should not be treated as complete conversation history.

---

## Notes Updated

Primary target notes:

* `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../../01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`
* `../../01_AnalogIC_SerDes/SerDes/pam4_receiver_basics.md`
* `../../01_AnalogIC_SerDes/SerDes/ctle_ffe_dfe_notes.md`
* `../../01_AnalogIC_SerDes/ADC/adc_based_receiver.md`
* `../../01_AnalogIC_SerDes/ADC/ti_sar_adc_calibration.md`
* `../../01_AnalogIC_SerDes/ADC/sampling_jitter_adc.md`
* `../../01_AnalogIC_SerDes/Interview_QA/technical_story_bank.md`
* `../../01_AnalogIC_SerDes/Interview_QA/synopsys_relevant_qa.md`
* `../../01_AnalogIC_SerDes/Study_Plans/synopsys_4_week_prep_plan.md`

Secondary target notes:

* `../../01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`
* `../../01_AnalogIC_SerDes/SerDes/pcie7_overview.md`
* `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/phase_noise_jitter.md`
* `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
* `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md`
* `../../01_AnalogIC_SerDes/LDO_Bandgap/serdes_power_integrity.md`
* `../../index.md`

---

## Key Themes Extracted

* PCIe 7.0 should be studied as a high-speed SerDes PHY problem centered on 128 GT/s PAM4, clocking, jitter, equalization, CDR, power integrity, and calibration.
* PLL phase noise becomes timing jitter, and the useful number depends on integration bandwidth, measurement point, PVT, supply condition, and clock path.
* CDR must be understood through jitter transfer, jitter tolerance, jitter generation, acquisition, equalization interaction, and PAM4 timing recovery challenges.
* CTLE, FFE, and DFE are coupled to CDR because equalization shapes the waveform used for phase detection and timing recovery.
* ADC-based PAM4 RX is a long-term SerDes target area; it connects sampling jitter, TI-ADC mismatch calibration, DSP equalization, and PAM4 decision margin.
* TI-SAR / TI-ADC calibration should focus on offset, gain, timing skew, bandwidth mismatch, background calibration, and interaction with RX adaptation loops.
* LDO work should be framed as SerDes power integrity: finite PSRR, output noise, transient response, and stability can become jitter, amplitude error, or calibration drift.
* Synopsys preparation should connect prior LDO, ADC, PLL / DCO, and automation experience to PCIe 7.0 clocking and SerDes system margin.

---

## New Open Questions

* 待确认: What exact PCIe 7.0 clocking block or supply domain will be assigned at Synopsys?
* 待确认: What clock domains, clock frequencies, divider ratios, and clock distribution topology are used?
* 待确认: What PLL architecture is used in the relevant IP?
* 待确认: What integrated jitter target and phase-noise integration bandwidth are used internally?
* 待确认: What CDR architecture is used: baud-rate, oversampling, bang-bang, linear, PI-based, DSP-based, or another implementation?
* 待确认: How are CDR jitter transfer, jitter tolerance, and jitter generation verified?
* 待确认: How are CTLE / FFE / DFE adaptation and CDR lock sequenced during link training?
* 待确认: Is the relevant PCIe 7.0 RX slicer-based or ADC-based?
* 待确认: If ADC-based, what ADC architecture, sample rate, resolution, interleaving factor, and calibration approach are used?
* 待确认: Which LDOs power PLL, CDR, clock buffers, RX front-end, ADC, or references?
* 待确认: Which supply-induced jitter and power-integrity simulations are signoff-critical?
* 待确认: What internal scripts, testbenches, and result formats are expected for signoff review?

---

## Items Marked As 待确认

The updated notes mark these categories as `待确认`:

* Synopsys internal PCIe 7.0 architecture
* Synopsys internal clocking implementation
* Synopsys internal PLL architecture and jitter targets
* Synopsys internal CDR architecture and loop behavior
* Synopsys internal equalization partitioning and adaptation sequence
* Synopsys internal RX architecture, including slicer-based vs ADC-based choices
* Synopsys internal ADC specifications and calibration flow
* Synopsys internal LDO supply domains, PSRR targets, and output-noise budgets
* Synopsys internal supply-induced jitter and power-integrity signoff flow
* Synopsys internal simulation, regression, and review workflow

---

## Recommended Next Study Actions

1. Review `pcie7_clocking_notes.md`, `phase_noise_jitter.md`, `pll_fundamentals.md`, and `cdr_fundamentals.md` together as the Week 2 clocking bundle.
2. Build one clean PCIe 7.0 clocking block diagram after internal architecture is available.
3. Add numeric worked examples for phase-noise integration and ADC jitter-limited SNR.
4. Create concise 2-minute story versions for LDO, ADC, PLL / DCO, and automation.
5. Add one comparison table for CTLE vs FFE vs DFE and one table for slicer-based vs ADC-based PAM4 RX.
6. During onboarding, collect approved internal terminology, jitter metrics, signoff benches, and ownership boundaries before adding Synopsys-specific facts.
