import simpy
import random
import matplotlib.pyplot as plt
from fpdf import FPDF

# fixed random seed for reproducibility
random.seed(1)

# Constants
SIM_TIME = 1440  # Simulation time in minutes (24 hours)
PUMP_COUNT = 4
TILL_COUNT = 1
ARRIVAL_RATE = 500 / 1440  # cars per minute
TRAVEL_TIME = 1  # Travel time between car and shop

# Data collection
pump_utilization = [0] * PUMP_COUNT
pump_occupied_time = [0] * PUMP_COUNT
cashier_occupied_time = 0
waiting_times = []
total_customers = 0

# Car arrival process
def car(env, name, pumps, till):
    global total_customers, cashier_occupied_time
    arrival_time = env.now
    yield env.timeout(TRAVEL_TIME)

    # Request a pump
    with pumps.request() as req:
        yield req
        pump_start = env.now
        wait_time = pump_start - arrival_time
        waiting_times.append(wait_time)
        pump_index = pumps.count - 1
        pump_utilization[pump_index] += 1
        fueling_time = random.triangular(0.5, 1, 3)
        pump_occupied_time[pump_index] += fueling_time
        yield env.timeout(fueling_time)

    # Travel to payment
    yield env.timeout(TRAVEL_TIME)

    # Payment process
    with till.request() as req:
        yield req
        payment_start = env.now
        payment_time = random.triangular(0.1667, 0.5, 2)
        cashier_occupied_time += payment_time
        yield env.timeout(payment_time)

    # Travel to exit
    yield env.timeout(TRAVEL_TIME)

    # Car exits
    total_customers += 1

# Car generator
def car_generator(env, pumps, till):
    i = 0
    while True:
        i += 1
        yield env.timeout(random.expovariate(ARRIVAL_RATE))
        env.process(car(env, f"Car {i}", pumps, till))

# Visualization of results
def visualize_results(pump_usage, waiting_times):
    plt.figure(figsize=(8, 5))
    plt.bar([f"Pump {i+1}" for i in range(PUMP_COUNT)], pump_usage)
    plt.title("Pump Utilization")
    plt.xlabel("Pump Number")
    plt.ylabel("Utilization (%)")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.hist(waiting_times, bins=20, edgecolor='black')
    plt.title("Distribution of Waiting Times")
    plt.xlabel("Waiting Time (minutes)")
    plt.ylabel("Number of Cars")
    plt.show()

# Generate PDF report
def generate_report(total_customers, pump_usage, cashier_util, avg_wait_time):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Petrol Station Simulation Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Total cars served: {total_customers}", ln=True)
    pdf.cell(200, 10, txt=f"Cashier Utilization: {cashier_util:.2%}", ln=True)
    for i, usage in enumerate(pump_usage):
        pdf.cell(200, 10, txt=f"Pump {i+1} Utilization: {usage:.2%}", ln=True)
    pdf.cell(200, 10, txt=f"Average Waiting Time: {avg_wait_time:.2f} minutes", ln=True)
    pdf.output("Petrol_Station_Simulation_Report.pdf")

# Simulation setup
def run_simulation():
    env = simpy.Environment()
    pumps = simpy.Resource(env, capacity=PUMP_COUNT)
    till = simpy.Resource(env, capacity=TILL_COUNT)
    env.process(car_generator(env, pumps, till))
    env.run(until=SIM_TIME)

    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    pump_usage = [util / SIM_TIME for util in pump_occupied_time]
    cashier_util = cashier_occupied_time / SIM_TIME

    print("\n--- Simulation Results ---")
    print(f"Total cars served: {total_customers}")
    print(f"Average waiting time: {avg_waiting_time:.2f} minutes")
    print(f"Cashier utilization: {cashier_util:.2%}")
    for i, usage in enumerate(pump_usage, 1):
        print(f"Pump {i} utilization: {usage:.2%}")

    generate_report(total_customers, pump_usage, cashier_util, avg_waiting_time)
    visualize_results(pump_usage, waiting_times)

run_simulation()
