"""Simulation parameters"""

number_of_buses = 100

nominal_voltage = 20.0  # [V]

cable_reactance = 0.1  # [Ohm]
cable_resistance = 0.01  # [Ohm]

active_power_set_point = 100  # [MW]

active_power_consumption_datacenter = 30  # [MW]
reactive_power_consumption_datacenter = 0  # [MVar]
active_power_consumption_factory = 70  # [MW]

# We will iterate through a range of values we want to test.
# [0, 50, 100, ... 950]
reactive_power_consumption_factory = list(range(0, 1000, 50))  # [MVar]

plot_these_buses = [0, 1, 2, 10, 50]
