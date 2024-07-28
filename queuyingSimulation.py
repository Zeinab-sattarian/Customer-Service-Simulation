import math
import random
import pandas as pd



def generate_exponential(rate):
    R = random.random()
    return -1 / rate * math.log(R)

def generate_standard_normal():
    R = random.random()
    return (R ** 0.135 - (1 - R) ** 0.135) / 0.1975

def generate_normal(mu, sigma):
    standard_normal = generate_standard_normal()
    return max(0.01, mu + sigma * standard_normal)  # Ensuring no zero service times

def simulate(total_customers, lambda_val, mu_service, sigma_service, mu_cashier, sigma_cashier):
    num_clerks = 3  # Number of clerks in server 2
    interarrival_times = [generate_exponential(lambda_val) for _ in range(total_customers)]
    arrival_times = [sum(interarrival_times[:i+1]) for i in range(total_customers)]

    servers_free_at = [0] * num_clerks
    customer_waiting_times = [0] * total_customers
    customer_service_times = [0] * total_customers
    customer_total_times = [0] * total_customers
    clerk_idle_times = [[0] * total_customers for _ in range(num_clerks)]
    cashier_idle_time = [0] * total_customers
    customer_data = []
    queues = []

    # Routing customers to either self-service or server 2 with 3 clerks
    for i in range(total_customers):
        if random.choice([True, False]):  # Randomly choosing between self-service and server 2
            service_time = 0  # Self-service has no service time
            service_end_time = arrival_times[i]
            wait_time = 0
        else:
            # Assign to the least busy clerk, favoring idle clerks
            idle_clerks = [j for j in range(num_clerks) if servers_free_at[j] <= arrival_times[i]]
            if idle_clerks:
                next_clerk = idle_clerks[0]  # Select the first idle clerk
            else:
                next_clerk = servers_free_at.index(min(servers_free_at))  # Select the least busy clerk

            wait_time = max(0, servers_free_at[next_clerk] - arrival_times[i])
            service_start_time = max(servers_free_at[next_clerk], arrival_times[i])
            service_time = generate_normal(mu_service[next_clerk], sigma_service[next_clerk])
            service_end_time = service_start_time + service_time
            clerk_idle_times[next_clerk][i] = max(0, arrival_times[i] - servers_free_at[next_clerk])
            servers_free_at[next_clerk] = service_end_time
            customer_waiting_times[i] = wait_time
        
        customer_service_times[i] = service_time
        queues.append((i, service_end_time))  # Add to server 3 queue

        customer_data.append((i + 1, round(arrival_times[i], 2), round(wait_time, 2), round(service_time, 2), round(service_end_time, 2), 'self-service' if service_time == 0 else f'clerk {next_clerk + 1}'))

    # Second part: service by cashier (server 3)
    # Sort the queue by service end time to ensure correct order
    queues.sort(key=lambda x: x[1])
    cashier_free_at = 0
    for customer_index, arrival_time in queues:
        wait_time = max(0, cashier_free_at - arrival_time)
        service_start_time = max(cashier_free_at, arrival_time)
        service_time = generate_normal(mu_cashier, sigma_cashier)
        service_end_time = service_start_time + service_time
        cashier_idle_time[customer_index] = max(0, arrival_time - cashier_free_at)
        cashier_free_at = service_end_time

        customer_waiting_times[customer_index] += wait_time
        customer_service_times[customer_index] += service_time
        customer_total_times[customer_index] = service_end_time  # Update the total time in system to cashier's end time

        customer_data.append((customer_index + 1, round(arrival_time, 2), round(wait_time, 2), round(service_time, 2), round(service_end_time, 2), 'cashier'))

    average_waiting_time = sum(customer_waiting_times) / total_customers
    probability_of_wait = sum(1 for wait in customer_waiting_times if wait > 0) / total_customers
    average_service_time = sum(customer_service_times) / total_customers
    average_time_between_arrivals = sum(interarrival_times) / total_customers
    average_time_in_system = sum(customer_total_times) / total_customers
   
    print_results(average_waiting_time, probability_of_wait, average_service_time, average_time_between_arrivals, average_time_in_system)
    print_customer_table(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks)
    save_to_excel(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks)

def print_results(average_waiting_time, probability_of_wait, average_service_time, average_time_between_arrivals, average_time_in_system):
    print(f"Average Waiting Time: {average_waiting_time:.2f}")
    print(f"Probability of Waiting: {probability_of_wait:.2f}")
    print(f"Average Service Time: {average_service_time:.2f}")
    print(f"Average Time Between Arrivals: {average_time_between_arrivals:.2f}")
    print(f"Average Time in System: {average_time_in_system:.2f}")

def print_customer_table(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks):
    print(f"{'Customer ID':<12}{'Arrival Time':<15}{'Waiting Time':<15}{'Service Time':<15}{'End Time':<12}{'Server ID':<15}{'Time in System':<15}{'Idle Clerk 1':<15}{'Idle Clerk 2':<15}{'Idle Clerk 3':<15}{'Idle Cashier':<15}")
    for data in customer_data:
        customer_id = data[0]
        print(f"{customer_id:<12}{data[1]:<15}{data[2]:<15}{data[3]:<15}{data[4]:<12}{data[5]:<15}{round(customer_total_times[customer_id - 1], 2):<15}{round(clerk_idle_times[0][customer_id - 1], 2):<15}{round(clerk_idle_times[1][customer_id - 1], 2):<15}{round(clerk_idle_times[2][customer_id - 1], 2):<15}{round(cashier_idle_time[customer_id - 1], 2):<15}")

def save_to_excel(customer_data, clerk_idle_times, cashier_idle_time, customer_total_times, total_customers, num_clerks):
    df = pd.DataFrame(customer_data, columns=['Customer ID', 'Arrival Time', 'Waiting Time', 'Service Time', 'End Time', 'Server ID'])
    df['Time in System'] = df['Customer ID'].apply(lambda x: round(customer_total_times[x-1], 2))
    for i in range(num_clerks):
        df[f'Idle Clerk {i + 1}'] = df['Customer ID'].apply(lambda x: round(clerk_idle_times[i][x - 1], 2))
    df['Idle Cashier'] = df['Customer ID'].apply(lambda x: round(cashier_idle_time[x - 1], 2))
    
    # Save to Excel file
    df.to_excel('simulation_results.xlsx', index=False)

# values given in the class
total_customers = 100
lambda_val = 4
mu_service = [1.0, 2.0, 1.0]
sigma_service = [1.0, 1.0, 0.5]
mu_cashier = 4.0
sigma_cashier = 2.0

simulate(total_customers, lambda_val, mu_service, sigma_service, mu_cashier, sigma_cashier)
