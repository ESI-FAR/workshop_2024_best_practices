"""Unit conversions"""

import numpy as np


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees

    Args:
        radians: Angle to be converted

    Returns:
        Radians angle converted to degrees
    """
    return radians * 360 / (2 * np.pi)  # in degrees


def degrees_to_radians(degrees: float) -> float:
    """Convert radians to degrees

    Args:
        degrees: Angle to be converted

    Returns:
        Degree angle converted to radians
    """

    radians = degrees / 360 * (2 * np.pi)
    return radians


if __name__ == "__main__":
    assert abs(radians_to_degrees(0) - 0) < 0.01
    assert abs(radians_to_degrees(1) - 57.30) < 0.01
    assert abs(radians_to_degrees(2) - 114.59) < 0.01
    print("'radians_to_degrees' passed!")

    assert abs(degrees_to_radians(0) - 0) < 0.0001
    assert abs(degrees_to_radians(10) - 0.1745) < 0.0001
    assert abs(degrees_to_radians(90) - 1.5708) < 0.0001
    print("'degrees_to_radians' passed!")
