
⛽ Petrol Station Simulation with SimPy

This project simulates the daily operations of a petrol station using discrete event simulation in Python with the SimPy library. The model includes 4 fuel pumps and 1 cashier serving 500 cars over a simulated 24-hour period.

---

Overview

- Language: Python
- Library: SimPy (Discrete Event Simulation)
- Duration: 24 simulated hours (1440 minutes)
- Entities:
  - 4 fuel pumps
  - 1 cashier
  - 500 car arrivals (modeled via exponential inter-arrival time)

---

Features

- Tracks car flow from arrival to exit
- Queuing at pumps and cashier
- Pump and cashier utilization metrics
- Waiting time statistics and histograms
- Auto-generated PDF performance report using FPDF
- Visualizations with Matplotlib

---

Tech Stack

- Python
- SimPy
- Matplotlib
- FPDF

---

How to Run

1. Install required libraries:
   pip install simpy matplotlib fpdf

2. Run the simulation:
   python Simulation.py

3. Outputs:
   - Console report of simulation results
   - PDF report: Petrol_Station_Simulation_Report.pdf
   - Graphs showing pump usage and waiting time distribution

---

License

This project is licensed under the MIT License.

---

Acknowledgments

- Developed as a school simulation assignment
- Based on real-world petrol station dynamics
