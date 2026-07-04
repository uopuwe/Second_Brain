# SerDes Batch 1 Top 10 Processing Summary - 2026-07-01

Processed on: 2026-07-02

Scope: only SerDes / PCIe / PLL / CDR / ADC / LDO-clocking technical content was extracted. Investing, compensation, HR-only, tax, banking, family, and daily-life content was excluded.

## Conversations Processed

1. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-06-06__PCIe7_Clocking_LDO学习计划.md`
2. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-06-02__Synopsys入职技术准备.md`
3. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-29__职位匹配与薪资分析.md`
4. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-13__SerDes_PLL_CDR_带宽.md`
5. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-10__ADC_RX建模与Python.md`
6. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-18__CTLE_FFE_面试准备.md`
7. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-02-15__SerDes_vs_RF_PLL_Jitter.md`
8. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-21__GF_22FDX_CPPLL设计.md`
9. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-04__总结A_224Gbs_Transceiver.md`
10. `../raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-24__高速TI-ADC时钟偏移.md`

## Notes Updated

- `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`
- `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md`
- `../../01_AnalogIC_SerDes/PLL_CDR_Clocking/phase_noise_jitter.md`
- `../../01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`
- `../../01_AnalogIC_SerDes/SerDes/pam4_receiver_basics.md`
- `../../01_AnalogIC_SerDes/SerDes/ctle_ffe_dfe_notes.md`
- `../../01_AnalogIC_SerDes/ADC/adc_based_receiver.md`
- `../../01_AnalogIC_SerDes/ADC/ti_sar_adc_calibration.md`
- `../../01_AnalogIC_SerDes/ADC/sampling_jitter_adc.md`
- `../../01_AnalogIC_SerDes/LDO_Bandgap/serdes_power_integrity.md`
- `../../01_AnalogIC_SerDes/Interview_QA/technical_story_bank.md`
- `../../01_AnalogIC_SerDes/Interview_QA/synopsys_relevant_qa.md`
- `../../01_AnalogIC_SerDes/Study_Plans/synopsys_4_week_prep_plan.md`

## Key Knowledge Extracted

- PCIe 7.0 clocking should be anchored around PAM4 timing scale, clock hierarchy, CDR behavior, and LDO/PDN-induced jitter rather than only standalone PLL phase noise.
- SerDes PLLs are best explained through timing jitter at launch/sampling edges; RF PLLs are often explained through phase-noise spectrum, close-in noise, EVM, ACLR, and spur purity.
- CDR bandwidth trades low-frequency tracking against high-frequency jitter/noise rejection; practical values are architecture-dependent and must be validated with jitter transfer, tolerance, generation, and BER.
- ADC-based SerDes receivers require joint modeling of channel loss, CTLE, AFE, sampler jitter, ADC quantization/TI mismatch, DSP equalization, timing recovery, and link metrics.
- CTLE/FFE/DFE should be framed as a combined equalization strategy: CTLE analog shaping, FFE FIR ISI cancellation, DFE post-cursor cancellation, and MLSD sequence estimation when residual memory remains.
- TI-ADC timing skew is deterministic and calibratable; random aperture jitter raises the noise floor and is not corrected the same way.
- LDO/PDN design for clocking must convert supply noise into phase/timing error through VCO, divider, PI, clock-buffer, and sampler supply sensitivities.
- Public 224G Synopsys transceiver takeaways were captured only as public technical architecture lessons; internal team/project relationship was marked 待确认.

## New Formulas or Worked Examples Added

- PCIe/PAM4 timing anchors:
  - `symbol rate = bit rate / 2` for PAM4.
  - `UI = 1 / symbol_rate`.
  - 224 Gb/s PAM4 example: `112 Gbaud`, `UI ~= 8.93 ps`, `Nyquist ~= 56 GHz`.
- Supply-to-jitter:
  - `Delta f = K_VDD * v_supply`
  - `Delta phi_pk = K_VDD * V_ripple_pk / f_ripple`
  - `Delta t_pk = Delta phi_pk / (2*pi*f_clk)`
- CPPLL loop estimate:
  - `G(s) = (Kpd * Kvco / N) * Z(s) / s`
  - `omega_n = sqrt(K/C)`
  - `zeta = (R/2)*sqrt(K*C)`
  - example using `Icp = 200 uA`, `Kvco = 200 MHz/V`, `N = 112`, `C = 20 pF`, giving loop bandwidth on the order of a few MHz.
- CDR normalized bandwidth example:
  - 112G PAM4: `56 Gbaud`, `UI = 17.86 ps`, `10 MHz / 56 GHz ~= 1.8e-4`.
- CTLE behavioral response:
  - `|H_ctle(f)| = A_dc * sqrt((1 + (f/fz)^2) / ((1 + (f/fp1)^2)*(1 + (f/fp2)^2)))`
- ADC aperture jitter:
  - `SNR_jitter ~= -20*log10(2*pi*f_in*sigma_t)`
- TI-ADC timing skew:
  - `t_m,n = n*T_s + m*T_s/M + Delta t_m`
  - `e_m ~= Delta t_m * dx/dt`
  - `f_spur = |k*f_s/M +/- f_in|`
- Deterministic skew estimation:
  - `sigma_mean = sigma_j / sqrt(N)`

## New Synopsys Onboarding Questions

- 待确认: Which PCIe 7.0 clocking mode is most relevant to the assigned work: common clock, SRIS, SRNS, retimer, or internal test mode?
- 待确认: Which internal jitter metrics are used for design review and signoff?
- 待确认: How are jitter budgets allocated across PLL, dividers, clock buffers, PI, sampler, CDR, and supplies?
- 待确认: How are LDO PSRR, PDN impedance, package resonance, and on-die decap translated into clock-jitter requirements?
- 待确认: Which simulations are considered signoff-critical: PSS/PNoise, transient noise, extracted transient, supply-ripple injection, behavioral BER, or lab correlation?
- 待确认: Is the assigned team directly connected to the public 224G transceiver work, a related Interface IP team, or a different project?
- 待确认: Which architectural blocks are relevant to the role: CMU/PLL, CCU/ILO/phase rotator, AFE, ADC, DSP, CDR, or power integrity?
- 待确认: What exact ADC-based RX partition, TI-ADC calibration loop, CDR/timing-recovery implementation, and equalization metrics are used internally?

## Items Marked 待确认

- Synopsys team/project relationship to public 224G transceiver work.
- Internal PCIe 7.0 compliance cases, clocking modes, and jitter metrics.
- Internal LDO/PDN-to-jitter signoff methodology.
- Internal clock-domain partitioning and supply-noise injection requirements.
- Exact ADC bit depth, TI interleaving ratio, calibration loops, DSP partition, and MLSD usage in assigned product.
- Exact GF22FDX or prior-project CPPLL schematic choices and targets, where not public.

## Recommended Next Batch

Process the PLL/CDR/clocking deep-dive conversations next, because Batch 1 added the high-level anchors but left several derivations and verification flows as follow-up work:

- `2026-02-18__112Gbps_SerDes_PLL建模.md`
- `2026-03-04__PLL_环路带宽解析.md`
- `2026-03-08__PLL传输函数推导.md`
- `2026-03-14__PLL非理想因素总结.md`
- `2026-03-29__VCO噪声与PLL整形.md`
- `2026-03-31__时钟恢复入门讲解.md`
- `2026-04-06__Jitter_Transfer_Tolerance_CDR.md`
- `2026-04-11__CDR架构与设计要点.md`
- `2026-04-16__PLL设计与仿真.md`
