import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from ctrlbench.sim import PidGains, PlantConfig, ProfileConfig, Simulator
from ctrlbench.plot import plot_interactive_dashboard
import pandas as pd
import math

STEP_ANGLE_DEG = 1.8
RADIANS_PER_STEP = math.radians(STEP_ANGLE_DEG)

def configure_square_wave(sidebar: DeltaGenerator, plant):
    """Draw test-specific sidebar widgets."""

    u = plant.display_units  # "steps", "rad", "mm", etc.
    sidebar.number_input("Step Amplitude (Steps)", key="step_amplitude", min_value=1, value=10)
    sidebar.number_input(f"Wave Period (s)", key="wave_period", min_value=0.1, value=2.0, step=0.1)
    sidebar.number_input(
        "Total Sim Duration (s)", key="sim_duration", min_value=1.0, value=5.0, step=1.0
    )

def run_square_wave(gains, plant, dt) -> pd.DataFrame:
    """Read params from session state, run sim, return df."""

    s = plant.display_scale
    amplitude = st.session_state["step_amplitude"] / s
    wave_period = st.session_state["wave_period"]
    sim_duration = st.session_state["sim_duration"]

    sim = Simulator(gains=gains, plant=plant, profile=None)

    
    def square_wave(t: float) -> float:
        return amplitude if (t % wave_period) < (wave_period / 2.0) else 0.0

    df = sim.run_signal(square_wave, duration=sim_duration, dt=dt)

    df["setpoint"] = df["setpoint"] * s
    df["actual"] = df["actual"] * s
    df["error"] = df["error"] * s

    return df