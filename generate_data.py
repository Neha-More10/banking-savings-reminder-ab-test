from pathlib import Path

import numpy as np
import pandas as pd


def generate_data(number_of_customers=10000, seed=42):
    # A fixed seed makes the results reproducible.
    rng = np.random.default_rng(seed)

    customer_ids = np.arange(1, number_of_customers + 1)

    # Randomly assign each customer to one group.
    groups = rng.choice(["A", "B"], size=number_of_customers)

    # Simulate each customer's savings before the experiment.
    starting_balances = np.round(
        rng.uniform(100, 5000, size=number_of_customers), 2
    )

    # Assumed deposit probabilities for this fictional experiment:
    # A = no reminder, B = savings reminder.
    deposit_probabilities = np.where(groups == "A", 0.20, 0.23)

    # 1 means the customer deposited money; 0 means they did not.
    added_to_savings = rng.binomial(1, deposit_probabilities)

    # Total deposits during the 30-day experiment.
    deposits = np.where(
        added_to_savings == 1,
        np.round(rng.uniform(10, 500, size=number_of_customers), 2),
        0.0,
    )

    # Customers can also withdraw money, whether or not they deposit.
    made_withdrawal = rng.binomial(
        1, 0.15, size=number_of_customers
    )

    withdrawals = np.where(
        made_withdrawal == 1,
        np.round(
            starting_balances
            * rng.uniform(0.01, 0.20, size=number_of_customers),
            2,
        ),
        0.0,
    )

    net_savings_change = np.round(deposits - withdrawals, 2)

    data = pd.DataFrame({
        "customer_id": customer_ids,
        "group": groups,
        "starting_balance": starting_balances,
        "added_to_savings": added_to_savings,
        "total_deposits": deposits,
        "total_withdrawals": withdrawals,
        "net_savings_change": net_savings_change,
        "ending_balance": np.round(
            starting_balances + net_savings_change, 2
        ),
    })

    return data


# Run this section only when this file is executed directly.
if __name__ == "__main__":
    data = generate_data()

    output_folder = Path(__file__).resolve().parent / "data"
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "savings_experiment.csv"
    data.to_csv(output_file, index=False)

    print(f"Saved {len(data):,} fictional customers to {output_file}")
    print("\nFirst five rows:")
    print(data.head().to_string(index=False))

    summary = data.groupby("group").agg(
        customers=("customer_id", "count"),
        customers_who_deposited=("added_to_savings", "sum"),
        deposit_rate=("added_to_savings", "mean"),
        average_net_savings=("net_savings_change", "mean"),
    )

    summary["deposit_rate_percent"] = (
        summary.pop("deposit_rate") * 100
    )

    print("\nExperiment summary:")
    print(summary.round(2).to_string())