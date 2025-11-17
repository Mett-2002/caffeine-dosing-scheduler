# Caffeine Dosing Scheduler

A tool to plan your caffeine intake so you stay alert without jitters or crashes. Enter your desired caffeine range and active hours, and the scheduler calculates a scientifically grounded dosing schedule.

---

## What This Tool Does

Imagine this: you sit down to work or study at 09:00, you want to stay alert until 18:00, and you want your caffeine level to remain in that magical zone where your brain feels sharp but not jittery. You pick a comfortable range—for example, 100 to 140 mg—and the scheduler handles everything else.

The script figures out:

* **When** your first intake should happen (often around 30–60 minutes before your start time).
* **How large** that dose should be so you arrive at your minimum target level right at your start time.
* **Middle doses** spaced across the day to keep you inside your target zone.
* **Final dose** calculated so by 18:00 you return exactly to your chosen minimum.

---

## Why It’s Useful

Caffeine’s effects are largely predictable once you model its absorption and elimination. Working with that predictability gives you a few big wins:

* Helps prevent overstimulation and anxiety by avoiding uncontrolled peaks.
* Protects your sleep by avoiding unwanted caffeine leftovers near bedtime.
* Stabilizes mental performance instead of pushing you into spike → crash cycles.

**In short: more focus, less chaos.**

---

## Key Features

The script walks you through everything in a simple command-line interface:

* Choose your peak (`Cmax_target`) and trough (`Cmin_target`).
* Pick your active window (`t_start` → `t_end`).
* Specify your bedtime for plotting.

Behind the scenes, it handles:

* First-dose sizing
* Dose-timing optimization
* Repeating-dose calculation
* Final-dose correction
* Full simulation of the caffeine curve using the PK model

You get **both a numerical regimen and a clean visual plot**.

---

## How to Interpret the Inputs

**`Cmax_target`**
Your ideal “high point” caffeine level.

**`Cmin_target`**
The lowest level you're comfortable being at during your focus window.

**`t_start`, `t_end`**
The time frame during which the model keeps you inside the band.

**`sleep_time`**
Used only for plotting, so you can visualize bedtime caffeine.

> **Note:** Times are decimal hours. Example: `8.5 = 8:30`.

---

## The Caffeine Model

The scheduler is built on a standard PK model with:

* **Absorption half-life:** 0.5 h
* **Elimination half-life:** 5 h

From those, it computes:

```text
k_a = ln(2)/0.5
k   = ln(2)/5.0
```

A single dose produces a concentration curve:

```text
C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

Peak occurs at:

```text
T_max = ln(k_a/k) / (k_a - k)
```

The peak multiplier is:

```text
pm = (k_a/(k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))
```

So the first dose is:

```text
D_first = Cmax_target / pm
```

Subsequent doses are solved numerically to keep the trough above `Cmin_target`.

---

## How the Algorithm Works

* Computes the required initial dose to hit your target peak.
* Rewinds that dose so you begin your window already inside the target range.
* Finds a repeating interval and dose that hold the trough steady.
* Adjusts the final dose so you end at your target trough exactly at `t_end`.
* Simulates the full curve, including bedtime residual caffeine.

---

## Example Run

**Input:**

* Peak: `80 mg`
* Trough: `30 mg`
* Focus window: `9 → 18`
* Bedtime: `23`

**Output:**
A complete dose regimen and a plot.
If bedtime caffeine looks too high, lower the trough or move `t_end` earlier.

---

## Example Plot

![Caffeine Dosing Schedule](Figure_1.png)

---
