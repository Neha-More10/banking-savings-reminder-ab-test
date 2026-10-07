# Banking Savings Reminder A/B Test

Does a savings reminder encourage more banking customers to put money
into savings?

This Python project explores that question through an A/B test using
10,000 fictional customers. All data is simulated; no real customer
information is used.

## The experiment

Customers are randomly assigned to two groups:

- Group A: no additional savings reminder.
- Group B: receives a savings reminder.

Each row represents one customer's activity over a 30-day period.

The main metric is the percentage of customers who make at least one
savings deposit. Average net savings is also reported, including
customers who make no deposits.

## How the simulation works

The generator assumes a 20% deposit probability for Group A and 23%
for Group B. It also generates starting balances, deposits and
withdrawals.

These probabilities are inputs chosen for learning. The analysis
demonstrates how to evaluate an experiment; it does not establish
whether reminders work in real banking.

A fixed random seed makes the dataset reproducible.

## What the analysis does

1. Checks for missing values and duplicate customer IDs.
2. Calculates deposit rates and average net savings for each group.
3. Measures the percentage point difference and relative change.
4. Runs a two-sided two-proportion z-test.
5. Calculates an approximate 95% confidence interval for the difference.

The test uses a 5% significance threshold.

## Results

| Metric                  | Group A | Group B |
| ----------------------- | ------: | ------: |
| Customers               |   5,061 |   4,939 |
| Customers who deposited |   1,042 |   1,173 |
| Deposit rate            |  20.59% |  23.75% |
| Average net savings (£) |    9.76 |   20.31 |

- Absolute increase: 3.16 percentage points.
- Relative increase: 15.35%.
- Two-sided p-value: 0.000141.
- Approximate 95% confidence interval: +1.53 to +4.79 percentage points.

## Understanding the results

The p-value describes how unusual a difference at least this extreme
would be if both groups had the same underlying deposit probability.
It is not the probability that the null hypothesis is true.

The confidence interval expresses uncertainty around the estimated
difference. Here, the whole interval is above zero.

At the chosen 5% threshold, Group B has a statistically significantly
higher deposit rate in this simulated experiment.

## Business interpretation and limitations

The simulated result favours the reminder for deposit participation.
It does not justify launching a real banking feature.

A real experiment would also need a sample-size plan, a fixed observation
period, checks that random assignment worked correctly, and measures
of customer harm such as overdraft use or complaints.

The difference in average net savings is descriptive only; this project
does not test its statistical significance. Making a deposit does not
necessarily mean savings increased overall.

## Project files

- `generate_data.py`: generates and saves the fictional customer data.
- `analyse_experiment.py`: checks the data and runs the analysis.
- `data/savings_experiment.csv`: generated dataset.

## Run the project

Generate the dataset:

    python generate_data.py

Run the analysis:

    python analyse_experiment.py

## Possible future improvements

- Estimate the sample size needed before running an experiment.
- Check whether group sizes match the intended random allocation.
- Add charts showing deposit rates and uncertainty.
- Analyse the difference in average net savings.
- Add FastAPI endpoints to create experiments and retrieve results.
