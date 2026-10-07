from pathlib import Path
from math import sqrt, erfc
import pandas as pd


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