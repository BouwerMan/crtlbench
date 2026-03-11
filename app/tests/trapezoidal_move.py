import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from ctrlbench.sim import PidGains, PlantConfig, ProfileConfig, Simulator
from ctrlbench.plot import plot_interactive_dashboard
import pandas as pd
import math

STEP_ANGLE_DEG = 1.8
RADIANS_PER_STEP = math.radians(STEP_ANGLE_DEG)

def configure_trapezoidal(sidebar: DeltaGenerator, plant):
    """Draw test-specific sidebar widgets."""

    u = plant.display_units  # "steps", "rad", "mm", etc.
    sidebar.slider(f"Target ({u})", key="target", min_value=100, max_value=50000, value=10000, step=100)
    sidebar.number_input(f"Cruise Velocity ({u}/s)", key="cruise_vel", value=2000)
    sidebar.number_input(f"Acceleration ({u}/s²)", key="accel", value=5000)
    sidebar.number_input("Max Sim Time (s)", key="max_time", value=10.0, step=1.0)
 
def run_trapezoidal(gains, plant, dt) -> pd.DataFrame:
    """Read params from session state, run sim, return df."""

    s = plant.display_scale
    target_internal = st.session_state["target"] / s
    vel_internal = st.session_state["cruise_vel"] / s
    accel_internal = st.session_state["accel"] / s
    max_time = st.session_state["max_time"]

    profile = ProfileConfig(
        max_velocity=vel_internal, acceleration=accel_internal, deceleration=accel_internal)

    sim = Simulator(gains=gains, plant=plant, profile=profile)

    df = sim.run(start=0, end=target_internal, dt=dt, max_time=max_time)

    df["setpoint"] = df["setpoint"] * s
    df["actual"] = df["actual"] * s
    df["error"] = df["error"] * s

    return df