from pathlib import Path
from math import sqrt, erfc
import pandas as pd
import matplotlib.pyplot as plt


# Load the data we generated.
file_path = (
    Path(__file__).resolve().parent
    / "data"
    / "savings_experiment.csv"
)

data = pd.read_csv(file_path)

# Check for missing values and repeated customers.
print("Missing values:", data.isna().sum().sum())
print("Duplicate customer IDs:", data["customer_id"].duplicated().sum())

# Calculate results for each group.
summary = data.groupby("group").agg(
    total_customers=("customer_id", "count"),
    customers_who_deposited=("added_to_savings", "sum"),
    deposit_rate=("added_to_savings", "mean"),
    average_net_savings=("net_savings_change", "mean"),
)

summary["deposit_rate_percent"] = summary["deposit_rate"] * 100

print("\nGroup results:")
print(
    summary[
        [
            "total_customers",
            "customers_who_deposited",
            "deposit_rate_percent",
            "average_net_savings",
        ]
    ].round(2).to_string()
)

# Compare the deposit rates.
rate_a = summary.loc["A", "deposit_rate"]
rate_b = summary.loc["B", "deposit_rate"]

difference = (rate_b - rate_a) * 100

print(f"\nDifference (B minus A): {difference:.2f} percentage points")

if rate_a > 0:
    relative_change = ((rate_b - rate_a) / rate_a) * 100
    print(f"Relative change: {relative_change:.2f}%")
else:
    print("Relative change cannot be calculated because A's rate is zero.")
    

# Use a 5% significance threshold.
alpha = 0.05

n_a = summary.loc["A", "total_customers"]
n_b = summary.loc["B", "total_customers"]

deposits_a = summary.loc["A", "customers_who_deposited"]
deposits_b = summary.loc["B", "customers_who_deposited"]

# Under the null hypothesis, assume one shared deposit probability.
pooled_rate = (deposits_a + deposits_b) / (n_a + n_b)

# Expected variation in the difference under the null hypothesis.
test_standard_error = sqrt(
    pooled_rate * (1 - pooled_rate) * (1 / n_a + 1 / n_b)
)

rate_difference = rate_b - rate_a

z_score = rate_difference / test_standard_error

# Two-sided p-value calculated using Python's standard math library.
p_value = erfc(abs(z_score) / sqrt(2))

# Approximate 95% confidence interval for B minus A.
# Here we use each group's observed rate, rather than the pooled rate.
interval_standard_error = sqrt(
    rate_a * (1 - rate_a) / n_a
    + rate_b * (1 - rate_b) / n_b
)

ci_lower = rate_difference - 1.96 * interval_standard_error
ci_upper = rate_difference + 1.96 * interval_standard_error

print("\nStatistical test:")
print(f"Z-score: {z_score:.2f}")
print(f"P-value: {p_value:.6f}")
print(
    "95% confidence interval for B minus A: "
    f"{ci_lower * 100:.2f} to {ci_upper * 100:.2f} percentage points"
)

if p_value < alpha:
    direction = "higher" if rate_difference > 0 else "lower"
    print(
        f"\nGroup B's deposit rate is statistically significantly "
        f"{direction} than Group A's at the 5% level."
    )
else:
    print(
        "\nThere is insufficient evidence of a difference "
        "at the 5% significance level."
    )

print(
    "\nThese results describe simulated data. "
    "They do not demonstrate an effect in real banking customers."
)    

# Create a folder to store the chart.
results_folder = Path(__file__).resolve().parent / "results"
results_folder.mkdir(exist_ok=True)

# Use the rates calculated from our dataset.
labels = ["A: No reminder", "B: Savings reminder"]
rates = [rate_a * 100, rate_b * 100]

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    labels,
    rates,
    color=["#64748B", "#0F766E"],
    width=0.55,
)

# Display the percentage above each bar.
ax.bar_label(bars, fmt="%.2f%%", padding=5)

ax.set_title(
    "Does a savings reminder increase deposits?",
    fontsize=14,
    pad=18,
)
ax.set_ylabel("Customers who made a deposit (%)")
ax.set_ylim(0, max(rates) + 8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.2)

# Show the estimated difference and its uncertainty.
fig.text(
    0.5,
    0.07,
    f"B minus A: {rate_difference * 100:+.2f} percentage points"
    f" | 95% CI: {ci_lower * 100:+.2f} to {ci_upper * 100:+.2f}",
    ha="center",
    fontsize=10,
)

fig.text(
    0.5,
    0.02,
    "Simulated customer data • 30-day observation period",
    ha="center",
    fontsize=9,
    color="#555555",
)

fig.tight_layout(rect=[0, 0.14, 1, 1])

chart_path = results_folder / "deposit_rate_comparison.png"
fig.savefig(chart_path, dpi=200, bbox_inches="tight")
plt.close(fig)

print(f"\nChart saved to: {chart_path}")


# Check whether group sizes are consistent with a 50/50 assignment.
total_customers = n_a + n_b
expected_per_group = total_customers / 2

allocation_z = (
    (n_a - expected_per_group)
    / sqrt(total_customers * 0.5 * 0.5)
)

allocation_p_value = erfc(abs(allocation_z) / sqrt(2))

print("\nRandom assignment check:")
print(f"Expected customers per group: {expected_per_group:,.0f}")
print(f"Actual: A = {n_a:,}, B = {n_b:,}")
print(f"Allocation p-value: {allocation_p_value:.4f}")

# A strict threshold helps flag unusually large allocation differences.
if allocation_p_value < 0.001:
    print("Warning: investigate the group allocation before trusting results.")
else:
    print("No evidence of a sample ratio mismatch at the 0.1% threshold.")