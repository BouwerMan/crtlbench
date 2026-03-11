from dataclasses import dataclass, field
from enum import Enum


@dataclass
class PidGains:
    kp: float = 0.0
    ki: float = 0.0
    kd: float = 0.0
    integral_limit_max: float = 1000.0
    integral_limit_min: float = 1000.0


@dataclass
class PlantConfig:
    response: float = 1.0  # How well the plant tracks commands (0.0–1.0)
    disturbance: float = 0.0  # Constant force applied each tick


@dataclass
class ProfileConfig:
    max_velocity: float = 0.0
    acceleration: float = 0.0
    deceleration: float = 0.0


@dataclass
class SimResult:
    time: list[float] = field(default_factory=list)
    setpoint: list[float] = field(default_factory=list)
    actual: list[float] = field(default_factory=list)
    error: list[float] = field(default_factory=list)
    output: list[float] = field(default_factory=list)
    integral: list[float] = field(default_factory=list)


class Simulator:
    """
    Runs a PID controller against a simulated plant and returns time-series data.
    """

    def __init__(self, gains: PidGains, plant: PlantConfig, profile: ProfileConfig):
        self.gains = gains
        self.plant = plant
        self.profile = profile

    def run(self, start: float, end: float) -> SimResult:
        """
        Simulate a move from start to end position.

        Args:
            start: Starting position.
            end: Target position.

        Returns:
            SimResult containing all recorded signals.
        """
        print(f"Hello from Simulator! Moving from {start} to {end}.")
        return SimResult()


class ProfileGeneratorState(Enum):
    IDLE = 0
    ACCELERATING = 1
    CRUISING = 2
    DECELERATING = 3


class ProfileGenerator:
    def __init__(self, profile: ProfileConfig):
        self.profile = profile
        self.state = ProfileGeneratorState.IDLE

    @property
    def profile(self) -> ProfileConfig:
        return self._profile

    @profile.setter
    def profile(self, profile: ProfileConfig):
        self._profile = profile

    def move(self, start: float, end: float):
        pass
