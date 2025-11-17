# Caffeine Dosing Scheduler

A Python tool to plan caffeine intake throughout the day for steady alertness without jitters or sleep disruption.

---

## Overview

The **Caffeine Dosing Scheduler** calculates optimal caffeine doses and timing to keep your blood caffeine level within a target range.

Example use case:

* You start work at **09:00** and want to stay alert until **18:00**.
* Your target caffeine level is **100–140 mg**.
* The scheduler figures out:

  * When to take your first dose
  * How much caffeine to take for the first and middle doses
  * Timing and amount of the last dose
  * Your expected caffeine level at bedtime

The program adapts automatically if you change your target range, providing a precise schedule to maintain consistent focus.

---

## How It Works

1. **Pharmacokinetic Model**
   Uses standard drug dosing math:

   * **Absorption half-life:** 0.5 hours
   * **Elimination half-life:** 5 hours

2. **Calculations**

   * Determines first dose size and timing to reach your minimum target at `t_start`.
   * Computes middle doses to maintain levels within your target range.
   * Adjusts the final dose so caffeine returns to your minimum at `t_end`.
   * Produces a simulation curve and caffeine remaining at sleep time.

3. **Core Formula**

   Caffeine concentration after one dose:

   [
   C_D(t) = D \times \frac{k_a}{k_a - k} \times \big(e^{-k t} - e^{-k_a t}\big)
   ]

   Where:

   ```
   k_a = ln(2) / 0.5  # absorption rate
   k   = ln(2) / 5.0  # elimination rate
   ```

   Peak time:

   ```
   T_max = ln(k_a / k) / (k_a - k)
   ```

   First dose:

   ```
   D_first = Cmax_target / peak_multiplier
   ```

   Subsequent doses are computed numerically to maintain the minimum target.

---

## Why Use It

Maintains a steady caffeine curve to avoid:

* Anxiety spikes
* Late-afternoon crashes
* Hidden caffeine interfering with sleep
* Guesswork about timing your next cup

Provides a **scientifically grounded, predictable focus schedule**.

---

## Installation

1. Save the script:

```
caffeine_scheduler.py
```

2. Install dependencies:

```bash
pip install numpy scipy matplotlib
```

3. Run the script:

```bash
python caffeine_scheduler.py
```

---

## Inputs

* **Cmax_target** – Maximum target caffeine (mg)
* **Cmin_target** – Minimum target caffeine (mg)
* **t_start** – Start of active period (decimal hours, e.g., 8.5 = 08:30)
* **t_end** – End of active period (decimal hours)
* **sleep_time** – Expected bedtime (for plotting)

---

## Example Scenario

Input:

```
Cmax_target = 140
Cmin_target = 100
t_start = 9.0
t_end = 18.0
sleep_time = 23.0
```

Output might be:

* First dose: 08:30
* Several equal middle doses throughout the day
* Final dose to return to 100 mg at 18:00
* Graph of caffeine curve including sleep-time levels

---

## Output

* **Dose amounts and times**
* **Simulation plot** of caffeine levels
* **Caffeine remaining at sleep time**

The result is a practical, visual guide for managing caffeine intake.

---

