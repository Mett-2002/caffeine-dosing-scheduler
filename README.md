# Caffeine Dosing Scheduler

Imagine this: you sit down to work or study at **09:00**, you want to stay alert until **18:00**, and you want your caffeine level to remain in that magical zone where your brain feels sharp but not jittery. You pick a comfortable range—for example, **100 to 140 mg**—and the scheduler handles everything else.

The script figures out:

• When your **first intake** should happen (often around 30–60 minutes before your start time).
• How large that dose should be so you arrive at your **minimum target level** right at your start time.
• The **middle doses** spaced across the day to keep you inside your target zone.
• And the **final dose**, calculated so by **18:00** you return exactly to your chosen minimum.

If you widen your target band, the program automatically adapts—more room means different intervals and more middle doses to keep the curve accurate.
This is why the tool asks for both a minimum and maximum target level: the model needs a band to maintain, not a single point.

---

## What the Scheduler Does

It uses a standard pharmacokinetic model (the same math used in drug dosing) to simulate how caffeine is absorbed and eliminated. From this, it computes the full dosing schedule that keeps your curve between your chosen **Cmin** and **Cmax** during the entire active window.

The output includes:

• Dose amounts
• Exact dose times
• A full simulation curve
• Caffeine remaining at your sleep time

You get a scientifically grounded pacing strategy for your caffeine intake, not guesswork.

---

## Why Use It?

A stable caffeine curve avoids:

• Big spikes that trigger anxiety
• The late-afternoon crash
• Hidden caffeine hanging around at bedtime
• The guesswork of “should I drink more now?”

This is a small tool for people who want consistent, predictable focus throughout the day—without destroying their sleep.

---

## Installation & Running

Save the script as:

```
caffeine_scheduler.py
```

Install dependencies:

```bash
pip install numpy scipy matplotlib
```

Run:

```bash
python caffeine_scheduler.py
```

The program will ask for:

• Peak caffeine level (`Cmax_target`)
• Minimum level (`Cmin_target`)
• Start time (`t_start`)
• End time (`t_end`)
• Sleep time (for plotting)

Times are decimal hours (e.g., **8.5** means **08:30**).

---

## How It Works (Short Version)

Caffeine enters and leaves the body following predictable curves.
The model uses:

• **Absorption half-life:** 0.5 h
• **Elimination half-life:** 5.0 h

From these, it calculates:

• How big the first dose must be to hit your target peak
• How early you must take it to reach your trough at `t_start`
• The interval and amount of all middle doses
• A corrected last dose that returns you to your trough at `t_end`

It then simulates and plots your exact concentration across the day.

---

## Core Formula (Reference)

The concentration after one dose:

```
C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

Where:

```
k_a = ln(2)/0.5
k   = ln(2)/5.0
```

Peak time:

```
T_max = ln(k_a/k) / (k_a - k)
```

First dose:

```
D_first = Cmax_target / peak_multiplier
```

Subsequent doses are computed numerically to match `Cmin_target`.

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

The scheduler might tell you:

• Take your **first dose around 08:30**
• Several equal middle doses spaced across the day
• A final dose bringing you back to 100 mg at **18:00**
• Caffeine at sleep time (for evaluating sleep impact)

And it produces a graph that visualizes the entire curve.

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)

---


