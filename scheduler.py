import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# -----------------------------
# Friendly CLI header & instructions
# -----------------------------
print("=== Caffeine Dosing Scheduler ===")
print("This tool computes a dosing schedule that keeps caffeine levels between your")
print("desired MAX and MIN targets using a simple PK absorption/elimination model.")
print("Please enter numeric values when prompted (hours in decimal, mg for amounts).")
print("Example times: 8.5 = 08:30, 22.0 = 22:00")
print("---------------------------------------------------------------\n")

# -----------------------------
# Pharmacokinetics from half-lives
# -----------------------------
ka = np.log(2) / 0.5   # absorption rate constant (1/h)
k  = np.log(2) / 5.0   # elimination rate constant (1/h)

# -----------------------------
# User inputs (only prompts changed for friendliness)
# -----------------------------
Cmax_target = float(input("1) Desired PEAK caffeine (MAX) level to aim for (mg): "))
Cmin_target = float(input("2) Desired MINIMUM trough caffeine level to maintain (mg): "))
t_start     = float(input("3) Time (hours) at which you want to already be within range (e.g., 8.0 for 08:00): "))
t_end       = float(input("4) End time (hours) for the schedule (e.g., 20.0 to stop at 20:00): "))
sleep_time  = float(input("5) Sleeping start time (hours) — used for plotting bedtime marker (e.g., 23.0): "))

# -----------------------------
# Helper functions
# -----------------------------
def Tmax(ka, k):
    return np.log(ka / k) / (ka - k)

def single_dose_conc(D, t, ka=ka, k=k):
    t = np.asarray(t, dtype=float)
    resp = D * (ka / (ka - k)) * (np.exp(-k * t) - np.exp(-ka * t))
    return np.where(t >= 0, resp, 0.0)

def peak_multiplier(ka=ka, k=k):
    tmax = Tmax(ka, k)
    return (ka / (ka - k)) * (np.exp(-k * tmax) - np.exp(-ka * tmax))

def find_time_to_target_from_single_dose(D, C_target, ka=ka, k=k, t_hi=48.0):
    tmax = Tmax(ka, k)
    f = lambda t: single_dose_conc(D, t, ka, k) - C_target
    left = f(tmax)
    right = f(t_hi)
    tries = 0
    while left * right > 0 and t_hi < 7*24 and tries < 12:
        t_hi *= 1.5
        right = f(t_hi)
        tries += 1
    return brentq(f, tmax, t_hi)

# -----------------------------
# Step 1: First dose tuned to reach Cmax_target
# -----------------------------
pm = peak_multiplier(ka, k)
D_first = Cmax_target / pm

# -----------------------------
# Pre-stage: shift first dose backward
# -----------------------------
# Find upward crossing of Cmin_target after dose
f_up = lambda t: single_dose_conc(D_first, t, ka, k) - Cmin_target
first_crossing = brentq(f_up, 1e-6, Tmax(ka, k))
# If the user wants to be at target range at t_start,
# the actual first dose must have been taken earlier:
t_first_dose = t_start - first_crossing

# -----------------------------
# Step 2: Interval calculation
# -----------------------------
first_interval = find_time_to_target_from_single_dose(D_first, Cmin_target, ka, k)

f = lambda t: single_dose_conc(D_first, t, ka, k) - Cmin_target
t_up = brentq(f, 1e-6, Tmax(ka, k))
t_down = brentq(f, Tmax(ka, k), 7*24)
subsequent_interval = t_down - t_up

intervals = [first_interval, subsequent_interval]

# -----------------------------
# Step 3: Compute subsequent dose D_next
# -----------------------------
unit_at_interval = single_dose_conc(1.0, subsequent_interval, ka, k)
resid_first_at_2int = single_dose_conc(D_first, first_interval + subsequent_interval, ka, k)

if unit_at_interval <= 0:
    raise RuntimeError("Unit response at 'interval' is non-positive; check ka, k, and interval.")

D_next = (Cmin_target - resid_first_at_2int) / unit_at_interval
D_next = float(max(D_next, 0.0))

def total_conc_after_second_at(t_after_second):
    return single_dose_conc(D_first, first_interval + t_after_second, ka, k) + single_dose_conc(D_next, t_after_second, ka, k)

trough_after_second = total_conc_after_second_at(subsequent_interval)

t_grid = np.linspace(0.0, subsequent_interval, 1000)
vals = [total_conc_after_second_at(x) for x in t_grid]
peak_after_second = max(vals)
t_peak_after_second = t_grid[int(np.argmax(vals))]

# -----------------------------
# Step 4: Build dose schedule
# -----------------------------
dose_times = []
dose_amounts = []

t = t_first_dose
first_flag = True
interval_index = 0
while t <= t_end + 1e-9:
    if first_flag:
        dose_times.append(t)
        dose_amounts.append(float(D_first))
        first_flag = False
    else:
        dose_times.append(t)
        dose_amounts.append(float(D_next))
    t += intervals[min(interval_index, 1)]
    interval_index += 1

# -----------------------------
# Step 4b: Adjust last dose
# -----------------------------
last_index = max(i for i, td in enumerate(dose_times) if td <= t_end)
last_td = dose_times[last_index]

conc_other = 0.0
for i, (D, td) in enumerate(zip(dose_amounts, dose_times)):
    if i != last_index:
        conc_other += float(single_dose_conc(D, t_end - td, ka, k))

unit_at_end = float(single_dose_conc(1.0, t_end - last_td, ka, k))
if unit_at_end > 0:
    D_last = (Cmin_target - conc_other) / unit_at_end
    D_last = float(max(D_last, 0.0))
    dose_amounts[last_index] = D_last

# -----------------------------
# Step 5: Simulate concentration
# -----------------------------
t_last = t_end + subsequent_interval + 6.0
times = np.linspace(0.0, t_last, 2400)
conc = np.zeros_like(times)

for D, td in zip(dose_amounts, dose_times):
    conc += single_dose_conc(D, times - td, ka, k)

# -----------------------------
# Output schedule
# -----------------------------
print("\n--- Computed Regimen ---")
print(f"First dose (to hit Cmax):            {D_first:.2f} mg")
print(f"Subsequent fixed dose (D_next):      {D_next:.2f} mg")
print(f"First upward crossing shift:         {first_crossing:.2f} h earlier")
print(f"Actual first dose time:              {t_first_dose:.2f} h")
print(f"First interval:                      {first_interval:.2f} h")
print(f"Subsequent repeating interval:       {subsequent_interval:.2f} h")
print("\nSecond-interval checks (after 2nd dose):")
print(f"  Peak within 2nd interval:          {peak_after_second:.2f} mg at t+{t_peak_after_second:.2f} h")
print(f"  Level at next dose time:           {trough_after_second:.2f} mg (target {Cmin_target:.2f} mg)")
print("\nDose times & amounts:")
for i, (td, D) in enumerate(zip(dose_times, dose_amounts), 1):
    flag = " (adjusted)" if i == last_index+1 else ""
    print(f"  {i:02d}: t = {td:.2f} h, D = {float(D):.2f} mg{flag}")


# -----------------------------
# Plot (timeline style)
# -----------------------------
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# Plot (timeline style)
# -----------------------------
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# Plot (timeline style)
# -----------------------------
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# Plot (timeline style)
# -----------------------------
plt.figure(figsize=(11,6))

# Plot caffeine concentration
plt.plot(times, conc, label="Caffeine level in body", color="steelblue", linewidth=2)

# Target lines
plt.axhline(Cmax_target, linestyle="--", color="red", alpha=0.6, label="Target MAX")
plt.axhline(Cmin_target, linestyle="--", color="green", alpha=0.6, label="Target MIN")

# Helper function for ordinals
def ordinal(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    else:
        return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n%10]}"

# Helper function to format time
def format_time(hour_float):
    hrs = int(hour_float)
    mins = int((hour_float - hrs)*60)
    return f"{hrs:02d}:{mins:02d}"

# List to collect text for detail box
detail_lines = []

# Dosing markers (short dotted purple lines with bordered labels)
for i, (td, D) in enumerate(zip(dose_times, dose_amounts), start=1):
    dose_height = np.interp(td, times, conc)
    # Draw vertical dotted line
    plt.vlines(td, 0, dose_height, color="purple", linestyle=":", alpha=0.4, linewidth=1.5)
    # Label with ordinal intake and dosage
    plt.text(td, dose_height + max(conc)*0.03,
             f"{ordinal(i)} intake: {int(D)} mg",
             fontsize=9, fontweight="bold", color="purple",
             ha='center',
             bbox=dict(facecolor='white', edgecolor='purple', boxstyle='round,pad=0.2', alpha=0.8))
    # # Additional label for exact intake time
    # plt.text(td, dose_height + max(conc)*0.08,
    #          f"{format_time(td)}",
    #          fontsize=8, color="purple", ha='center')
    # Add to detail lines (time + dose)
    detail_lines.append(f"{ordinal(i)} intake: {int(D)} mg at {format_time(td)}")

# Sleep marker (short dotted purple line only to curve + label)
sleep_height = np.interp(sleep_time, times, conc)
plt.vlines(sleep_time, 0, sleep_height, color="purple", linestyle=":", alpha=0.3, linewidth=1.5)
plt.scatter(sleep_time, sleep_height, color="darkblue", zorder=5)
plt.text(sleep_time, sleep_height + max(conc)*0.03,
         f"Bedtime caffeine: {sleep_height:.1f} mg",
         fontsize=9, fontweight="bold", color="purple", ha='center',
         bbox=dict(facecolor='white', edgecolor='purple', boxstyle='round,pad=0.2', alpha=0.8))
# Add sleep info to detail box
# detail_lines.append(f"Bedtime caffeine level at {format_time(sleep_time)}: {sleep_height:.1f} mg")


# End-of-schedule marker
end_height = np.interp(t_end, times, conc)
plt.vlines(t_end, 0, end_height, color="purple", linestyle=":", alpha=0.3, linewidth=1.5)
plt.text(t_end, end_height + max(conc)*0.03,
         "End",
         fontsize=9, fontweight="bold", color="purple", ha='center',
         bbox=dict(facecolor='white', edgecolor='purple', boxstyle='round,pad=0.2', alpha=0.8))

# Shaded therapeutic range
plt.fill_between(times, Cmin_target, conc, where=(conc >= Cmin_target),
                 alpha=0.1, interpolate=True, color='green')

# Axes limits: start 2 hours before first intake, end 2 hours after sleep
plt.xlim(max(0, min(dose_times)-2), sleep_time+2)
plt.ylim(0, max(conc)*1.2)

# Titles and labels
plt.title("Caffeine Dosing Schedule", fontsize=14, weight="bold")
plt.xlabel("Time (hours)")
plt.ylabel("Caffeine (mg)")

# X-axis ticks every 1 hour within the new range
x_start, x_end = plt.xlim()
xticks = range(int(x_start), int(x_end)+1, 1)  # Force 1-hour spacing
xtick_labels = [f"{int(x)%24:02d}:00" for x in xticks]
plt.xticks(xticks, xtick_labels)

# Y-axis ticks every 10 mg
y_start, y_end = plt.ylim()
yticks = range(0, int(y_end)+10, 10)
plt.yticks(yticks, [f"{y} mg" for y in yticks])

detail_text = "\n".join(detail_lines)

plt.gcf().text(
    0.66, 0.87, detail_text,
    fontsize=13,                        # Larger font
    ha='left', va='top',                # Align nicely to top-left of box
    bbox=dict(
        facecolor='white',
        alpha=0.95,
        edgecolor='purple',
        boxstyle='round,pad=1.0'        # More padding around text
    )
)

plt.legend(frameon=False)
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
