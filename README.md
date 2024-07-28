# Customer Service Simulation

## Introduction

This repository contains a Python script to simulate customer service processes involving multiple clerks and a cashier. The simulation models the flow of customers through self-service stations, clerks, and a final cashier, capturing various performance metrics like waiting times, service times, and idle times.

## Prerequisites

- Python 3.x
- `pandas` library

## Installation

1. **Clone the Repository**:

   ```bash
https://github.com/Zeinab-sattarian/Customer-Service-Simulation.git
   ```

   ```

2. **Install Dependencies**:

   ```bash
   pip install pandas
   ```

## Usage

### Running the Simulation

To run the simulation with the default parameters, execute:

```bash
python simulate.py
```

### Parameters

- `total_customers`: The number of customers to simulate.
- `lambda_val`: The rate parameter for the exponential distribution of interarrival times.
- `mu_service`: The mean service times for each of the clerks.
- `sigma_service`: The standard deviation of the service times for each of the clerks.
- `mu_cashier`: The mean service time for the cashier.
- `sigma_cashier`: The standard deviation of the service time for the cashier.

These parameters can be modified in the `simulate.py` file:

```python
total_customers = 100
lambda_val = 4
mu_service = [1.0, 2.0, 1.0]
sigma_service = [1.0, 1.0, 0.5]
mu_cashier = 4.0
sigma_cashier = 2.0

simulate(total_customers, lambda_val, mu_service, sigma_service, mu_cashier, sigma_cashier)
```

### Output

The script prints key performance metrics and a detailed table of each customer's journey through the system. Additionally, it saves the results to an Excel file named `simulation_results.xlsx`.

#### Performance Metrics

- **Average Waiting Time**
- **Probability of Waiting**
- **Average Service Time**
- **Average Time Between Arrivals**
- **Average Time in System**

#### Customer Data Table

- **Customer ID**
- **Arrival Time**
- **Waiting Time**
- **Service Time**
- **End Time**
- **Server ID**
- **Time in System**
- **Idle Time for Each Clerk**
- **Idle Time for Cashier**

## Functions

### `generate_exponential(rate)`

Generates an exponentially distributed random variable.

### `generate_standard_normal()`

Generates a standard normal random variable using a custom approximation.

### `generate_normal(mu, sigma)`

Generates a normal random variable with mean `mu` and standard deviation `sigma`, ensuring no zero service times.

### `simulate(total_customers, lambda_val, mu_service, sigma_service, mu_cashier, sigma_cashier)`

Runs the simulation with the specified parameters.

### `print_results(average_waiting_time, probability_of_wait, average_service_time, average_time_between_arrivals, average_time_in_system)`

Prints the performance metrics of the simulation.

### `print_customer_table(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks)`

Prints a detailed table of customer data including times and idle times.

### `save_to_excel(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks)`

Saves the simulation results to an Excel file.

## Acknowledgments
Developed by Zeinab Sattarian

- Developed by [Your Name]

---

For any issues, contributions, or feature requests, please open an issue or submit a pull request.
