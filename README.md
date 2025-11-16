# Caffeine Dosing Scheduler

**Purpose**
This tool calculates a caffeine dosing schedule that keeps your blood/tissue caffeine levels within a target range (MIN .. MAX) during a specified activity window.

*Example:* Stay at a steady “focused / hype” level from **09:00** (study start) to **18:00** (study end), avoiding big peaks and crashes.

---

## Quick Overview

* Uses a simple **one-compartment pharmacokinetic (PK) model** with first-order absorption and elimination.
* Calculates the first dose to reach your desired peak (C_max_target), then shifts it earlier so you are already within range at `t_start`.
* Computes a repeating interval and fixed subsequent dose to maintain troughs near your desired minimum (C_min_target).
* Reduces oscillations in caffeine levels and keeps them inside your chosen band across the target window.

---

## Why It Matters — Q&A

**Q: Why does caffeine make people anxious?**
A: Extra doses on top of residual caffeine can spike levels above an anxiety threshold. Accumulation is the main cause.

**Q: Why can caffeine affect sleep?**
A: Caffeine blocks adenosine receptors, preventing sleepiness. With a multi-hour half-life, it can linger into bedtime if evening dosing or residual troughs are high.

**Q: Why do caffeine effects feel like “hype” then crash?**
A: Single doses peak and fall naturally. Poorly spaced doses create noticeable oscillations. This scheduler minimizes those fluctuations.

---

## Features

* Interactive CLI prompts for:

  * Target peak (`Cmax_target`) and trough (`Cmin_target`) in mg
  * Schedule start/end times in hours
  * Bedtime marker for plotting
* Uses realistic PK parameters (default absorption half-life = 0.5 h, elimination half-life = 5.0 h) to calculate:

  * First dose (C_max_target)
  * First dose timing shift to start in-range at `t_start`
  * Repeating interval and fixed subsequent dose (`D_next`)
  * Last dose adjustment to hit trough at `t_end`
  * Simulation timeline plot with concentration curve, dose markers, and bedtime concentration
* Provides a numeric regimen summary and plot.

---

## Installation & Usage

1. Save the script as `caffeine_scheduler.py`.
2. Install dependencies (recommend using a virtual environment):

```bash
pip install numpy scipy matplotlib
```

3. Run:

```bash
python caffeine_scheduler.py
```

4. Enter values when prompted:

* Desired **peak caffeine** (mg)
* Desired **trough caffeine** (mg)
* **Start time** in hours (e.g., 9.0)
* **End time** in hours (e.g., 18.0)
* **Bedtime** in hours for plotting (e.g., 23.0)

---

## Input Explained

* `Cmax_target` (mg): Target peak concentration in the window.
* `Cmin_target` (mg): Minimum concentration to maintain steady effect.
* `t_start` (hours): Time you want to be within the target band.
* `t_end` (hours): Time to stop the scheduled maintenance.
* `sleep_time` (hours): Bedtime for plot annotation.

*Note:* Times are decimal hours (e.g., 8.5 = 08:30).

---

## Model & Formulas

**Default PK parameters:**

* Absorption half-life: 0.5 h → `k_a = ln(2)/0.5`
* Elimination half-life: 5.0 h → `k = ln(2)/5.0`

**Single-dose concentration:**
`C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))`

**Time to peak after a single dose:**
`T_max = ln(k_a/k) / (k_a - k)`

**Peak multiplier:**
`pm = (k_a/(k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))`

**First dose:**
`D_first = Cmax_target / pm`

**Subsequent doses:** Calculated numerically to keep troughs near `Cmin_target` using root-finding (Brent).

---

## Algorithm Steps

1. Compute `k_a` and `k` from half-lives, calculate `pm`, and set `D_first`.
2. Shift the first dose earlier so you’re in-range at `t_start`.
3. Compute the first interval and repeating interval using single-dose response.
4. Compute fixed subsequent dose (`D_next`) considering residual caffeine.
5. Generate dose times up to `t_end` and adjust the last dose to meet the trough.
6. Simulate total concentration over time and plot:

   * Concentration curve
   * MIN / MAX target lines
   * Dose markers
   * Bedtime marker and concentration
   * Highlight concentrations above the trough

---

## Output Interpretation

* **First dose (Cmax)** — calculated initial dose.
* **Subsequent fixed dose (`D_next`)** — dose for repeated use.
* **First upward crossing shift** — how much earlier to take first dose.
* **Intervals** — time between doses.
* **Peak/trough diagnostics** — check target maintenance.
* **Dose times & amounts** — full schedule in hours.

Plot shows concentration curve, dose times, and bedtime concentration.

---

## Example Run

Input values:

* `Cmax_target = 80`
* `Cmin_target = 30`
* `t_start = 9.0`
* `t_end = 18.0`
* `sleep_time = 23.0`

Output: numeric regimen + timeline plot. Adjust `Cmin_target`, `t_end`, or `Cmax_target` as needed to reduce sleep disruption.

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)
