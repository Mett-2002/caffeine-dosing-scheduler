# Caffeine Dosing Scheduler

Keep your caffeine levels in the sweet spot for alertness without jitters or crashes. Enter your desired range and active hours, and the scheduler calculates a scientifically grounded dosing plan.

---

## How It Works

The scheduler uses a standard **pharmacokinetic model** for caffeine:

- **Absorption half-life:** 0.5 h  
- **Elimination half-life:** 5.0 h  

Caffeine concentration after a single dose \(D\) at time \(t\) is:

```

C_D(t) = D * (k_a / (k_a - k)) * (exp(-k*t) - exp(-k_a*t))

```

Where:

- `k_a = ln(2)/0.5` (absorption rate constant)  
- `k = ln(2)/5.0` (elimination rate constant)

The **peak time** after a single dose is:

```

T_max = ln(k_a / k) / (k_a - k)

```

### First Dose

The **first dose** is computed to hit the desired **Cmax_target** at its peak:

```

D_first = Cmax_target / peak_multiplier

```

Here, **peak_multiplier** is:

```

peak_multiplier = (k_a / (k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))

```

It represents the maximum concentration reached from a **1 mg dose**. Dividing your target peak by this factor gives the actual dose needed.

Since you want to already be within range at `t_start`, the script shifts the first dose **earlier** so that the caffeine curve reaches **Cmin_target** at your start time.  

---

### Middle and Final Doses

- **Middle doses:** Calculated numerically to maintain caffeine above `Cmin_target` without exceeding `Cmax_target`. Intervals are based on the time when levels would drop to the minimum.  
- **Final dose:** Adjusted to ensure that caffeine at `t_end` returns to `Cmin_target`, preventing excess caffeine toward bedtime.

---

## Inputs

The program prompts for:

1. **Cmax_target** – desired peak caffeine (mg)  
2. **Cmin_target** – desired minimum trough caffeine (mg)  
3. **t_start** – start of active period (hours in decimal, e.g., 8.5 = 08:30)  
4. **t_end** – end of active period  
5. **sleep_time** – bedtime (for plotting)

---

## Outputs

- **Dose schedule:** Amounts and exact times for first, middle, and last doses  
- **Simulation curve:** Full caffeine concentration over time  
- **Bedtime caffeine estimate:** To evaluate sleep impact  
- **Plot:** Timeline showing doses, concentration curve, and target range  

---

## Example Scenario

**Inputs:**

```

Cmax_target = 140
Cmin_target = 100
t_start = 9.0
t_end = 18.0
sleep_time = 23.0

````

**Scheduler output:**

- First dose: ~08:30  
- Several middle doses spaced to maintain levels  
- Final dose returning to 100 mg at 18:00  
- Graph visualizing caffeine curve and bedtime concentration  

---

## Installation & Running

1. Save the script as `caffeine_scheduler.py`.  
2. Install dependencies:

```bash
pip install numpy scipy matplotlib
````

3. Run:

```bash
python caffeine_scheduler.py
```

Follow prompts to enter your target caffeine levels and times.

---


