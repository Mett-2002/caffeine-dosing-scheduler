# Caffeine Dosing Scheduler

Imagine sitting down to work or study at **09:00** and wanting to stay alert until **18:00**, keeping your caffeine level in the sweet spot where your brain feels sharp but not jittery. You choose a comfortable range—for example, **100–140 mg**—and the scheduler calculates the optimal caffeine doses and timings for you.

It determines:

- When your **first dose** should occur (typically 30–60 minutes before start)  
- How large that dose must be to reach your **minimum target** at the start of your work window  
- **Middle doses** spaced throughout the day to maintain the target range  
- A **final dose** to return caffeine levels to the minimum at **t_end**  

Widening the target band automatically adjusts intervals and dose sizes. Both a minimum and maximum are required because the model maintains a range rather than a single value.

The scheduler uses a standard pharmacokinetic model to simulate caffeine absorption and elimination, producing:

- Exact **dose amounts** and **timings**  
- A **full concentration curve**  
- Estimated caffeine remaining at **sleep time**  

This ensures a stable caffeine curve, avoiding spikes, crashes, lingering caffeine at bedtime, and guesswork.

---

## Installation & Running

Save the script as:

```bash
caffeine_scheduler.py
````

Install dependencies:

```bash
pip install numpy scipy matplotlib
```

Run:

```bash
python caffeine_scheduler.py
```

The program will prompt for:

* **Cmax_target** – peak caffeine level
* **Cmin_target** – minimum caffeine level
* **t_start** – start time
* **t_end** – end time
* **sleep_time** – for plotting

> Times are decimal hours (e.g., 8.5 = 08:30).

---

## How It Works

Caffeine enters and leaves the body following predictable pharmacokinetics:

* **Absorption half-life (t₁/₂,a):** 0.5 h
* **Elimination half-life (t₁/₂,e):** 5.0 h

Caffeine concentration after a single dose is:

```
C_D(t) = D * (k_a / (k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

Where:

* `k_a = ln(2)/t₁/₂,a` is the absorption rate constant
* `k   = ln(2)/t₁/₂,e` is the elimination rate constant
* `D` is the dose in mg
* `t` is time since ingestion in hours

Peak time for a single dose:

```
T_max = ln(k_a / k) / (k_a - k)
```

### Dose Scheduling Logic

1. **First dose:**
   Calculated to reach your target caffeine range at `t_start`. Both dose size and timing are determined to ensure caffeine rises smoothly from zero to the minimum target level at the start of your active period:

   ```
   D_first = Cmax_target / peak_multiplier
   ```

2. **Middle doses:**
   Using numerical simulation, the scheduler inserts doses whenever projected caffeine would fall below `Cmin_target` before `t_end`. Dose size and timing are adjusted to keep levels within the target band.

3. **Final dose:**
   Computed to return caffeine to `Cmin_target` exactly at `t_end`, avoiding residual caffeine that could affect sleep.

4. **Simulation:**
   After calculating all doses, the script simulates and plots the full concentration curve, showing caffeine throughout the day and estimated levels at sleep time.

This method maintains a smooth, predictable caffeine curve, balancing alertness and minimal sleep disruption.

---

## Example Scenario

**Input:**

```
Cmax_target = 140
Cmin_target = 100
t_start = 9.0
t_end = 18.0
sleep_time = 23.0
```

**Scheduler output:**

* First dose around **08:30**
* Several equal middle doses spaced through the day
* Final dose returning to 100 mg at **18:00**
* Graph visualizing caffeine levels and remaining caffeine at sleep time

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)

```
