# Caffeine Dosing Scheduler

Imagine being able to dial in your ideal “focus zone” and stay there—no anxious spikes, no sluggish crashes. This tool builds a caffeine schedule tailored to you, using a pharmacokinetic model to keep your caffeine levels inside a target range during the hours you need to be sharp. If your productive window is **09:00 → 18:00**, the script designs a dosing pattern that stays within your chosen band the whole time.

---

## What This Tool Does

The scheduler uses a **one-compartment pharmacokinetic model**—a standard way to describe how caffeine moves through and leaves the body. You give it:

• A target peak caffeine level (the “high point” you want to reach).
• A target trough (the lowest level you’re willing to dip to).
• The hours during which you want your caffeine to stay in that zone.
• Your sleep time so the plot can show how much caffeine is still in your system.

From that, the tool calculates:

• The exact **first dose** needed to hit your peak.
• How much earlier than your start time you need to take it.
• A **fixed repeating dose** and interval that maintain a smooth curve between peak and trough.
• An adjusted final dose so you stay in-range right up to the end—without overshooting into your evening.

No guesswork, no shaky overdose, no mid-afternoon crash.

---

## Why It’s Useful

Caffeine’s effects are largely predictable once you model its absorption and elimination. Working with that predictability gives you a few big wins:

• It helps prevent overstimulation and anxiety by avoiding uncontrolled peaks.
• It protects your sleep by avoiding unwanted caffeine leftovers near bedtime.
• It stabilizes your mental performance instead of pushing you into spike→crash cycles.

In short: more focus, less chaos.

---

## Key Features

The script walks you through everything in a simple command-line interface:

• Choose your peak (`Cmax_target`) and trough (`Cmin_target`).
• Pick your active window (`t_start` → `t_end`).
• Specify your bedtime for plotting.

Behind the scenes, it handles:

• First dose sizing
• Dose timing shifts
• Repeating-dose optimization
• Final dose correction
• Full simulation of the caffeine curve using the PK model

You get both a numerical regimen and a clean visual plot.

---


## How to Interpret the Inputs

`Cmax_target`
Your ideal “high point” caffeine level.

`Cmin_target`
The lowest level you're comfortable being at during your focus window.

`t_start`, `t_end`
The time frame during which the model keeps you inside the band.

`sleep_time`
Used only for plotting, so you can visualize bedtime caffeine.

Note: Times are decimal hours. For example, 8.5 = 8:30.

---

## The Caffeine Model

The scheduler is built on a standard PK model with:

• Absorption half-life: 0.5 h
• Elimination half-life: 5 h

From those, it computes:

```
k_a = ln(2)/0.5
k   = ln(2)/5.0
```

A single dose produces a concentration curve:

```
C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

Peak occurs at:

```
T_max = ln(k_a/k) / (k_a - k)
```

The peak multiplier is:

```
pm = (k_a/(k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))
```

So the first dose is simply:

```
D_first = Cmax_target / pm
```

Subsequent doses are solved numerically to keep the trough near `Cmin_target`.

---

## How the Algorithm Works

Here’s the story behind the calculations:

• It first computes how big your initial dose must be to hit your target peak.
• Then it rewinds that dose backward in time so you start your window already inside the desired range.
• A repeating interval and a fixed dose are found that hold the trough steady.
• The final dose is tweaked so you hit your target trough exactly at `t_end`.
• The full curve is simulated, and the plot shows concentration, target band, dose times, and how much caffeine is left at bedtime.

---

## Understanding the Output

The script prints:

• Your first dose
• The repeating dose
• Dose times
• Intervals
• Peak/trough diagnostics

The plot shows everything visually:
your caffeine curve, your target range, your dose events, and bedtime’s residual level.

---

## Example Run

Input:

• Peak: `80 mg`
• Trough: `30 mg`
• Focus window: `9 → 18`
• Bedtime: `23`

Output: a complete dose regimen and a plot.
If bedtime caffeine looks too high, lower the trough or move `t_end` earlier.

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)

---

