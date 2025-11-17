# Caffeine Dosing Scheduler

A tool to plan your caffeine intake throughout the day to stay alert without jitters or crashes. It calculates exact doses and timings to maintain your caffeine levels in a comfortable target range.

---

## Overview

The scheduler helps you stay focused between a start and end time, e.g., 09:00–18:00, by maintaining your caffeine concentration between a minimum (`Cmin`) and maximum (`Cmax`) target.  

It automatically calculates:

- **First dose** timing and size to reach your minimum target by start time.
- **Middle doses** to stay within the target range.
- **Final dose** to return to the minimum level by the end of your work/study period.

Widening your target range adapts the schedule automatically with more flexible intervals and doses.

---

## How It Works

The program uses a standard pharmacokinetic model:

- **Absorption half-life:** 0.5 hours  
- **Elimination half-life:** 5.0 hours  

From this, it calculates:

- First dose amount and timing
- All middle dose amounts and intervals
- Final dose to hit the minimum target at the end time

### Core Formula

Caffeine concentration after one dose:

```

C_D(t) = D * (k_a / (k_a - k)) * (exp(-k * t) - exp(-k_a * t))

```

Where:

```

k_a = ln(2)/0.5
k   = ln(2)/5.0

```

Peak time:

```

T_max = ln(k_a/k) / (k_a - k)

````

---

## Features

- Calculates exact dose amounts and times
- Provides a full simulation curve of caffeine concentration
- Estimates caffeine remaining at sleep time
- Avoids spikes, crashes, and lingering caffeine at bedtime

---

## Installation

1. Save the script as `caffeine_scheduler.py`
2. Install dependencies:

```bash
pip install numpy scipy matplotlib
````

3. Run:

```bash
python caffeine_scheduler.py
```

---

## Input Parameters

The program will ask for:

* **Cmax_target:** Maximum desired caffeine level (mg)
* **Cmin_target:** Minimum desired caffeine level (mg)
* **t_start:** Start time in decimal hours (e.g., 8.5 = 08:30)
* **t_end:** End time in decimal hours
* **sleep_time:** Sleep time for plotting purposes

---

## Example Scenario

Input:

* `Cmax_target = 140`
* `Cmin_target = 100`
* `t_start = 9.0`
* `t_end = 18.0`
* `sleep_time = 23.0`

Output:

* First dose around 08:30
* Several equal middle doses across the day
* Final dose to return to 100 mg at 18:00
* Simulation curve showing caffeine levels throughout the day

---

## Why Use It

Maintaining a stable caffeine curve helps avoid:

* Anxiety from spikes
* Late-afternoon crashes
* Hidden caffeine at bedtime
* Random guesswork about when to drink next

This scheduler provides a precise, science-based way to manage focus and alertness.

---

## Visualization

The program plots the caffeine concentration curve over the day, including projected levels at sleep time, so you can see the full impact of your dosing schedule.

```

