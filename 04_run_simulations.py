#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pypsa

import config as conf
import conversions as conv


def plot_bus_load_angles(
    bus_load_angles: list[list[float]],
    reactive_power_consumption_factory: list[int],
    plot_these_buses: list[int],
) -> None:
    """Plot load angles of selected buses.

    Args:
        bus_load_angles: Load angles on each bus.
        reactive_power_consumption_factory: A list of reactive power consumption of the Factory to iterate through.
        plot_these_buses: A list of buses for which we plot load angles.
    """
    fig, ax = plt.subplots()

    for bus in plot_these_buses:
        ax.plot(
            reactive_power_consumption_factory,
            bus_load_angles[bus],
            label=f"Bus {bus}",
        )

    ax.legend()
    ax.set_xlabel("Reactive power consumption 'Factory' [MVar]")
    ax.set_ylabel("Reactive load angle [°]")

    plt.title("Reactive Load Angles")
    plt.show()


def prepare_network(
    number_of_buses: int, cable_reactance: float, cable_resistance: float
) -> pypsa.components.Network:
    """Construct a network of a certain number of buses, connected with lines in a circle.

    Args:
        number_of_buses: How many buses shall our network consist of?
        cable_reactance: Reactance of each line, in [Ohm]
        cable_resistance: Resistance of each line, in [Ohm]
    Returns:
        A PyPSA network class instance.
    """
    network = pypsa.Network()

    for bus_number in range(conf.number_of_buses):
        network.add("Bus", f"My bus {bus_number}", v_nom=conf.nominal_voltage)

    # Add lines in a ring
    for i in range(number_of_buses):
        network.add(
            "Line",  # Element type
            f"My line {i}",  # Name
            bus0=f"My bus {i}",  # Origin
            bus1=f"My bus {(i + 1) % conf.number_of_buses}",  # Destination
            x=cable_reactance,  # Series reactance [Ohm]
            r=cable_resistance,  # Series resistance [Ohm]
        )

    return network


def calculate_bus_angles(
    network: pypsa.components.Network,
    number_of_buses: int,
    reactive_power_consumption_factory: list[int],
) -> list[list[float]]:
    """Set different reactive load angles for "Factory", calculate the
    Newton-Raphson power flow and extract its reactive load angles.

    Args:
        network: A PyPSA network class instance.
        number_of_buses: How many buses does the network consist of?
        reactive_power_consumption_factory: A list of reactive power consumption of the Factory to iterate through.

    Returns:
        Load angles on each bus.
    """
    bus_load_angles = [[] for _ in range(number_of_buses)]

    for reactive_load in reactive_power_consumption_factory:
        network.loads.loc[
            "Factory", "q_set"
        ] = reactive_load  # Reactive Power Consumption [MW]

        # Calculate a Newton-Raphson power flow
        network.pf()

        for index, bus in enumerate(range(number_of_buses)):
            angle_radians = network.buses_t.v_ang[f"My bus {index}"].iloc[0]
            angle_degrees = conv.radians_to_degrees(angle_radians)
            bus_load_angles[index].append(angle_degrees)

    return bus_load_angles


def main() -> None:
    """Main function of the simulation.

    Its code will show all logical steps involved.
    """
    network = prepare_network(
        number_of_buses=conf.number_of_buses,
        cable_reactance=conf.cable_reactance,
        cable_resistance=conf.cable_resistance,
    )

    network.add(
        "Generator",  # Element type
        "My generator",  # Name
        bus="My bus 0",  # Location
        p_set=conf.active_power_set_point,  # [MW]
        control="PQ",  # Control Strategy
    )
    network.add(
        "Load",  # Element type
        "Factory",  # Name
        bus="My bus 1",  # Location
        p_set=conf.active_power_consumption_factory,  # [MW]
        q_set=0,  # We will set those later!
    )
    network.add(
        "Load",  # Element type
        "Datacenter",  # Name
        bus="My bus 2",  # Location
        p_set=conf.active_power_consumption_datacenter,  # [MW]
        q_set=conf.reactive_power_consumption_datacenter,  # [MVar]
    )

    bus_load_angles = calculate_bus_angles(
        network=network,
        number_of_buses=conf.number_of_buses,
        reactive_power_consumption_factory=conf.reactive_power_consumption_factory,
    )

    plot_bus_load_angles(
        bus_load_angles=bus_load_angles,
        reactive_power_consumption_factory=conf.reactive_power_consumption_factory,
        plot_these_buses=conf.plot_these_buses,
    )


if __name__ == "__main__":
    main()
