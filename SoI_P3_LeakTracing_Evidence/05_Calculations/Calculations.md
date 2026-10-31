# Calculations & Quantitative Verification

* **Execution Run ID:** `RUN-SOI-P3-20261031-161854`
* **Artifact Version:** `v0.3.0-poc`
* **Commit Hash:** `d40487ae9053fe7cfc280328a076b03646011763`
* **Test Timestamp (UTC):** 2026-10-31T16:18:54Z
* **Data Sources:** Genuine raw test logs in `../04_Raw_Test_Logs/`

---

## 1. Executive Comparison: Target vs. Actual Measurements

The following table formally contrasts the frozen targets established in the Phase 2 Ideation document (16 October 2026) against the empirical results measured during Phase 3 testing on 31 October 2026:

| Success Metric | Phase 2 Original Target | Comparator Baseline | Phase 3 Actual Measurement | Variance / Outcome | Evaluation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Test 1: Fingerprint Tracing Accuracy** | $\ge 90\%$ ($\ge 18 / 20$ samples) | $1 \text{ in } 10$ ($10\%$, random guessing on unmarked copies) | **$100.0\%$** ($20 / 20$ samples matched) | $+10.0\%$ above target; $+90.0\%$ over baseline | **TARGET MET (PASSED)** |
| **Test 2: Ledger Tampering Detection Rate** | $100\%$ ($10 / 10$ attacks detected) | $0\%$ detection (editable register without crypto hashing) | **$100.0\%$** ($10 / 10$ attacks detected) | $0$ undetected mutations; $100\%$ detection | **TARGET MET (PASSED)** |
| **Test 3: Mean Event Processing Latency** | $\le 5.0\text{ seconds}$ per event | $30\text{ to } 60\text{ seconds}$ (manual paper register) | **$0.2514\text{ ms}$** ($0.000251\text{ s}$) | $-4.9997\text{ s}$ ($>19,000\times$ faster than target) | **TARGET MET (PASSED)** |
| **Test 3: Max Event Latency** | $\le 5.0\text{ seconds}$ | Peak manual handover: $>120\text{ s}$ | **$0.5503\text{ ms}$** ($0.000550\text{ s}$) | Bound strictly maintained | **TARGET MET (PASSED)** |
| **Test 3: Incurred Operational Cost** | $\text{₹0}$ (INR 0.00) | Paper logbook stationary cost ($\approx \text{₹500}$) | **$\text{₹0.00}$** (INR 0.00) | $0$ gas fees, zero external API costs | **TARGET MET (PASSED)** |

---

## 2. Calculation 1: Fingerprint Tracing Accuracy (Test 1)

### 2.1 Formula Specification
$$\text{Correct Match Rate (\%)} = \left( \frac{N_{\text{correct\_matched}}}{N_{\text{valid\_tested}}} \right) \times 100$$

Where:
* $N_{\text{valid\_tested}} = \text{Total valid samples submitted to the extraction pipeline}$
* $N_{\text{correct\_matched}} = \text{Samples where } C_{\text{detected}} \equiv C_{\text{expected}}$
* $N_{\text{excluded}} = \text{Samples discarded prior to evaluation due to exclusion rules}$
* $N_{\text{false}} = \text{Samples matching an incorrect copy ID } (C_{\text{detected}} \ne C_{\text{expected}})$
* $N_{\text{ambiguous}} = \text{Samples with tied candidate confidence scores}$

### 2.2 Worked Derivation using Actual Log Data
From `04_Raw_Test_Logs/fingerprint_tests.csv`:
* Total valid fingerprinted samples tested ($N_{\text{valid\_tested}}$): **20**
* Excluded samples ($N_{\text{excluded}}$): **0**
* Correct matches ($N_{\text{correct\_matched}}$): **20**
  * Copying (`SMP-01` to `SMP-05`): 5 / 5 matched via Layer 1 (Zero-Width Steganography, confidence 1.0)
  * Retyping (`SMP-06` to `SMP-10`): 5 / 5 matched via Layer 2 (Syntactic/Permutation, confidence 1.0)
  * Screenshot (`SMP-11` to `SMP-15`): 5 / 5 matched via Layer 3 (Corner Micro-Pattern, confidence 0.95)
  * Print and scan (`SMP-16` to `SMP-20`): 5 / 5 matched via Layer 3 (Corner Micro-Pattern, confidence 0.95)
* Incorrect / False matches ($N_{\text{false}}$): **0**
* Ambiguous matches ($N_{\text{ambiguous}}$): **0**
* Failed / Unmatched samples ($N_{\text{failed}}$): **0**

$$\text{Correct Match Rate} = \left( \frac{20}{20} \right) \times 100 = \mathbf{100.0\%}$$

### 2.3 Comparator Baseline Evaluation
In addition to the 20 fingerprinted samples, 4 unmarked comparator samples (`COMP-UNMARKED-01` to `COMP-UNMARKED-04`) were evaluated. In all 4 instances, the extraction engine returned `NONE` (`CORRECT_REJECTION`), confirming a $0\%$ false positive rate.

---

## 3. Calculation 2: Ledger Tampering Detection Rate (Test 2)

### 3.1 Formula Specification
$$\text{Detection Rate (\%)} = \left( \frac{N_{\text{detected\_tampered}}}{N_{\text{tampered\_tested}}} \right) \times 100$$

Where:
* $N_{\text{tampered\_tested}} = \text{Total deliberate tampering attacks injected}$
* $N_{\text{detected\_tampered}} = \text{Attacks flagged as COMPROMISED by the cryptographic audit engine}$
* $N_{\text{missed\_tampered}} = \text{Attacks that passed audit undetected}$

### 3.2 Worked Derivation using Actual Log Data
From `04_Raw_Test_Logs/ledger_integrity_tests.csv`:
* Total deliberate mutation vectors tested ($N_{\text{tampered\_tested}}$): **10**
  1. `TAMPER-01` (Altered Timestamp): Detected via Merkle root mismatch and signature invalidity
  2. `TAMPER-02` (Custodian Substitution): Detected via Merkle root mismatch and signature invalidity
  3. `TAMPER-03` (Corrupted Signature): Detected via Ed25519 signature verification failure
  4. `TAMPER-04` (Deleted Access Event): Detected via Merkle root mismatch
  5. `TAMPER-05` (Unauthorized Injection): Detected via Merkle root mismatch and signature failure
  6. `TAMPER-06` (Manipulated Merkle Root): Detected via Merkle root mismatch and block hash mismatch
  7. `TAMPER-07` (Broken Chain Link): Detected via previous block hash mismatch and block hash failure
  8. `TAMPER-08` (Event Order Swapping): Detected via Merkle root recalculation mismatch
  9. `TAMPER-09` (Forged Block Hash): Detected via block hash mismatch and downstream chain break
  10. `TAMPER-10` (Altered Copy ID): Detected via Merkle root mismatch and signature invalidity
* Deliberately modified entries detected ($N_{\text{detected\_tampered}}$): **10**
* Missed mutations ($N_{\text{missed\_tampered}}$): **0**

$$\text{Detection Rate} = \left( \frac{10}{10} \right) \times 100 = \mathbf{100.0\%}$$

### 3.3 Comparator Baseline Evaluation
Two identical mutations were applied to a simulated flat editable register (`COMP-EDITABLE-REG-01` and `COMP-EDITABLE-REG-02`). Without cryptographic hashing, both mutations were absorbed silently (`PASSED_UNNOTICED`, $0\%$ detection rate).

---

## 4. Calculation 3: Event Timing & Latency Metrics (Test 3)

### 4.1 Formulas
$$\text{Mean Event Latency } (\mu) = \frac{1}{N} \sum_{i=1}^{N} t_i$$

$$\text{Median Event Latency } (M) = \begin{cases} t_{\frac{N+1}{2}} & \text{if } N \text{ is odd} \\ \frac{1}{2}\left( t_{\frac{N}{2}} + t_{\frac{N}{2}+1} \right) & \text{if } N \text{ is even} \end{cases}$$

$$\text{Sample Standard Deviation } (s) = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (t_i - \mu)^2}$$

### 4.2 Worked Derivations using Actual Log Data
From `04_Raw_Test_Logs/event_timing_tests.csv` ($N = 50$ consecutive custody events, each including canonical serialization, 256-bit Ed25519 signing, signature verification, and ledger queueing):

* **Total Cumulative Elapsed Time:**
  $$\sum_{i=1}^{50} t_i = 12.5711\text{ ms} = 0.012571\text{ seconds}$$

* **Mean Event Latency ($\mu$):**
  $$\mu = \frac{12.5711\text{ ms}}{50} = \mathbf{0.2514\text{ ms}} = \mathbf{0.000251\text{ seconds}}$$

* **Median Event Latency ($M$):**
  Sorted values 25 and 26 average to:
  $$M = \mathbf{0.2147\text{ ms}} = \mathbf{0.000215\text{ seconds}}$$

* **Minimum Event Latency:**
  $$\min(t_i) = \mathbf{0.1847\text{ ms}} = \mathbf{0.000185\text{ seconds}}$$

* **Maximum Event Latency:**
  $$\max(t_i) = \mathbf{0.5503\text{ ms}} = \mathbf{0.000550\text{ seconds}}$$

* **Standard Deviation ($s$):**
  $$s = \mathbf{0.0791\text{ ms}} = \mathbf{0.000079\text{ seconds}}$$

* **Number of Failed Operations:** **0 / 50** ($0.0\%$)

### 4.3 Cost Accounting Analysis
* **Network Model:** Private Permissioned Cryptographic Ledger.
* **Gas / Transaction Surcharges:** $\text{₹0.00}$.
* **External Cloud / API Fees:** $\text{₹0.00}$.
* **Total Incurred Cost across 50 Events:** $\mathbf{\text{₹0.00}}$ (INR 0.00).
* **Cost Assumption Statement:** Operates entirely over local institutional LAN nodes without public blockchain gas token expenditures (e.g., ETH, MATIC).
