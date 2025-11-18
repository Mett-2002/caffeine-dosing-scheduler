# Caffeine Dosing Scheduler

A tool to **plan your caffeine intake** so you stay alert without jitters or crashes. Enter your desired caffeine range and active hours, and the scheduler calculates a scientifically grounded dosing schedule.

---

## 🌟 What This Tool Does

Imagine this: you start work or study at **09:00**, want to stay alert until **18:00**, and wish your caffeine level to remain in that “sweet spot” where your brain feels sharp but not jittery.

You pick a comfortable range—for example, **100 to 140 mg**—and the scheduler handles the rest.

The script calculates:

* **First dose timing** (often 30–60 minutes before your start time)
* **First dose size** to reach your minimum target level exactly at your start time
* **Middle doses** spaced to maintain caffeine within the chosen range
* **Final dose** to return precisely to your target minimum at the end of your active window

---

## 💡 Why It’s Useful

Caffeine’s effects are largely predictable once you model **absorption and elimination**. Using this predictability gives you a few big wins:

* Avoid overstimulation and anxiety by controlling peaks
* Protect your sleep by avoiding caffeine leftovers near bedtime
* Stabilize mental performance rather than cycling through spike → crash

**In short: more focus, less chaos.**

---

## ⚡ Features & Example Run

The scheduler guides you through caffeine management in a **single command-line workflow**. You provide:

* **Target peak** (`Cmax_target`)
* **Target trough** (`Cmin_target`)
* **Active window** (`t_start` → `t_end`)
* **Sleep time** for bedtime caffeine evaluation

The script then calculates a **complete dosing schedule** and simulates your caffeine curve.

It automatically handles:

* **First dose** sizing to reach your target range at `t_start`
* **Repeating doses** spaced to maintain caffeine within the chosen band
* **Final dose** adjustment to return to the trough at `t_end`
* **Full simulation** of the caffeine curve using the PK model

**Example Input:**

```text
Cmax_target = 140 mg
Cmin_target = 100 mg
t_start = 8.0 h (08:00)
t_end = 19.0 h (19:00)
sleep_time = 23.0 h (23:00)
```

**Example Output:**

* Exact dose amounts and timing for first, middle, and final doses
* Full daily caffeine concentration plot
* Estimated caffeine at bedtime for sleep evaluation

![Caffeine Dosing Schedule](output_example.png)

---

## 🔬 The Caffeine Model

The scheduler uses a standard **pharmacokinetic (PK) model**:

* **Absorption half-life:** 0.5 h
* **Elimination half-life:** 5 h

From these, the rates are computed:

```text
k_a = ln(2)/0.5
k   = ln(2)/5.0
```

A single dose produces a concentration curve:

```text
C_D(t) = D * (k_a/(k_a - k)) * (exp(-k*t) - exp(-k_a*t))
```

The peak occurs at:

```text
T_max = ln(k_a/k) / (k_a - k)
```

The **peak multiplier** is:

```text
pm = (k_a/(k_a - k)) * (exp(-k*T_max) - exp(-k_a*T_max))
```

So the **first dose** is:

```text
D_first = Cmax_target / pm
```

Subsequent doses are solved numerically to maintain **above the`Cmin_target`**.

---

## 🧮 How the Algorithm Works

1. Computes the **initial dose** to hit your target peak.
2. Rewinds the dose so your caffeine level starts inside the target range at `t_start`.
3. Finds a **repeating interval and dose** to maintain steady caffeine levels.
4. Adjusts the **final dose** to end at your target trough at `t_end`.
5. Simulates the **full caffeine curve**, including residual caffeine at bedtime.

---

