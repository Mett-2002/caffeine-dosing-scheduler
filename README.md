# Caffeine Dosing Scheduler

This tool calculates a caffeine dosing schedule that keeps your blood/tissue caffeine levels within a target range (MIN .. MAX) during a specified activity window. For example, it helps maintain a steady “focused / hype” level from **09:00** (study start) to **18:00** (study end), avoiding large peaks and crashes.

---

## Overview

* Uses a **one-compartment pharmacokinetic (PK) model** with first-order absorption and elimination.
* Calculates the first dose to reach your desired peak (`Cmax_target`) and shifts it earlier to start in-range at `t_start`.
* Computes a repeating interval and fixed subsequent doses to maintain troughs near `Cmin_target`.
* Minimizes oscillations and keeps caffeine levels within your chosen band during the target window.

---

## Why It Matters

* **Avoid anxiety:** Prevent spikes above safe levels due to accumulated caffeine.
* **Protect sleep:** Avoid residual caffeine interfering with bedtime.
* **Reduce crashes:** Proper dose spacing minimizes peak–crash cycles.

---

## Features

* Interactive CLI for:

  * Target peak (`Cmax_target`) and trough (`Cmin_target`) in mg
  * Schedule start (`t_start`) and end (`t_end`) times in hours
  * Bedtime marker for plotting
* PK-based calculations:

  * First dose (`Cmax_target`)
  * Timing shift for first dose
  * Repeating interval and fixed subsequent dose (`D_next`)
  * Last dose adjustment to reach target trough at `t_end`
  * Simulation plot with concentration curve, dose markers, and bedtime concentration
* Outputs numeric regimen and visual timeline.

---

## Input Explanation

* `Cmax_target` (mg): Desired peak concentration.
* `Cmin_target` (mg): Desired minimum concentration.
* `t_start` (hours): Start of the maintenance window.
* `t_end` (hours): End of the maintenance window.
* `sleep_time` (hours): Bedtime marker for plotting.

*Note:* Times are decimal hours (e.g., 8.5 = 08:30).

---

## Model & Formulas

**Default PK Parameters:**

* Absorption half-life: 0.5 h → `k_a = ln(2)/0.5`
* Elimination half-life: 5.0 h → `k = ln(2)/5.0`

**Single-dose concentration:**

```
C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

**Time to peak:**

```
T_max = ln(k_a/k) / (k_a - k)
```

**Peak multiplier:**

```
pm = (k_a/(k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))
```

**First dose:**

```
D_first = Cmax_target / pm
```

**Subsequent doses:**
Calculated numerically to maintain troughs near `Cmin_target` using root-finding.

---

## Algorithm Steps

1. Compute `k_a` and `k`, calculate `pm`, and determine `D_first`.
2. Shift the first dose earlier to start in-range at `t_start`.
3. Compute the first interval and repeating intervals.
4. Determine fixed subsequent dose (`D_next`) considering residual caffeine.
5. Generate dose times up to `t_end` and adjust the last dose to hit trough.
6. Simulate concentration over time and create a plot showing:

   * Concentration curve
   * MIN/MAX target lines
   * Dose markers
   * Bedtime marker and concentration
   * Highlighted levels above the trough

---

## Output Interpretation

* **First dose (Cmax):** Initial dose to reach target peak.
* **Subsequent dose (`D_next`):** Fixed repeated dose.
* **First dose timing shift:** How much earlier to take the first dose.
* **Intervals:** Time between doses.
* **Peak/trough diagnostics:** Verify maintenance within target band.
* **Dose times & amounts:** Full schedule in hours.

Plot visualizes concentration, dose times, and bedtime level.

---

## Example Run

**Input:**

* `Cmax_target = 80`
* `Cmin_target = 30`
* `t_start = 9.0`
* `t_end = 18.0`
* `sleep_time = 23.0`

**Output:** Numeric regimen + timeline plot. Adjust `Cmin_target`, `t_end`, or `Cmax_target` to reduce sleep disruption.

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)
