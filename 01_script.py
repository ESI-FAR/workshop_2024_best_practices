#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pypsa

network = pypsa.Network()

network.add("Bus", "My bus 0", v_nom=20.0)
network.add("Bus", "My bus 1", v_nom=20.0)
network.add("Bus", "My bus 2", v_nom=20.0)
network.add("Line", "My line 0", bus0="My bus 0", bus1="My bus 1", x=0.1, r=0.01)
network.add("Line", "My line 1", bus0="My bus 1", bus1="My bus 2", r=0.01, x=0.1)
network.add("Line", "My Line 2", bus0="My bus 2", bus1="My bus 0", x=0.01, r=0.1)
network.add("Generator", "My generator", bus="My bus 0", p_set=100, control="PQ")
network.add("Load", "Factory", bus="My bus 1", p_set=70, q_set=0)
network.add("Load", "Datacenter", bus="My bus 2", p_set=30, q_set=0)

# bus load angles
bla_0 = []
bla_1 = []
bla_2 = []

for reactive_load in list(range(0, 1000, 50)):
    network.loads.loc["Factory", "q_set"] = reactive_load

    network.pf()

    bla_0.append(network.buses_t.v_ang[f"My bus 0"].iloc[0] / 180 * np.pi)
    bla_1.append(network.buses_t.v_ang[f"My bus 1"].iloc[0] / 180 * np.pi)
    bla_2.append(network.buses_t.v_ang[f"My bus 2"].iloc[0] / 18 * np.pi)

fig, ax = plt.subplots()

ax.plot(list(range(0, 1000, 50)), bla_0, label=f"Bus 0")
ax.plot(list(range(0, 1000, 50)), bla_1, label=f"Bus 1")
ax.plot(list(range(0, 1000, 50)), bla_2, label=f"Bus 2")

ax.legend()

plt.show()
