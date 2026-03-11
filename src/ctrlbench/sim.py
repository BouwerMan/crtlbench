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


class PidController:
    """
    Owns error/integral/derivative math
    """

    pass


class PlantModel:
    """
    owns plant dynamics
    """

    pass


class ProfileGeneratorState(Enum):
    IDLE = 0
    ACCELERATING = 1
    CRUISING = 2
    DECELERATING = 3


class ProfileGenerator:
    def __init__(self, profile: ProfileConfig):
        self.profile = profile
        self.state = ProfileGeneratorState.IDLE
        self.direction = 1  # 1 for forward, -1 for reverse
        self.position = 0.0
        self.velocity = 0.0
        self.target_position = 0.0

    def is_finished(self) -> bool:
        return self.state == ProfileGeneratorState.IDLE

    def move(self, start: float, end: float):
        if end > start:
            new_direction = 1
        elif end < start:
            new_direction = -1
        else:
            self.state = ProfileGeneratorState.IDLE
            return

        if self.state != ProfileGeneratorState.IDLE:
            self.target_position = end

            if new_direction != self.direction:
                self.state = ProfileGeneratorState.DECELERATING
            elif self.state == ProfileGeneratorState.DECELERATING:
                dist_left = abs(self.target_position - start)
                if dist_left > self.calculate_braking_distance():
                    self.state = ProfileGeneratorState.ACCELERATING
        else:
            # Accelerating from standstill
            self.position = start
            self.target_position = end
            self.direction = new_direction
            self.velocity = 0.0
            self.state = ProfileGeneratorState.ACCELERATING

        self.calculate_next_step(0.0)

    def calculate_next_step(self, dt: float):
        if self.state == ProfileGeneratorState.IDLE:
            return

        match self.state:
            case ProfileGeneratorState.ACCELERATING:
                active_accel = self.profile.acceleration
            case ProfileGeneratorState.CRUISING:
                active_accel = 0.0
            case ProfileGeneratorState.DECELERATING:
                active_accel = -self.profile.deceleration

        distance_step = (self.velocity * dt) + (0.5 * active_accel * dt**2)
        self.position += self.direction * distance_step
        self.velocity += active_accel * dt

        if (
            self.state == ProfileGeneratorState.ACCELERATING
            and self.velocity >= self.profile.max_velocity
        ):
            self.velocity = self.profile.max_velocity
            self.state = ProfileGeneratorState.CRUISING
        elif self.state == ProfileGeneratorState.DECELERATING and self.velocity <= 0.0:
            self.velocity = 0.0
            dist_error = self.target_position - self.position
            if abs(dist_error) < 0.5:
                self.position = self.target_position
                self.state = ProfileGeneratorState.IDLE
            else:
                self.direction = 1 if dist_error > 0 else -1
                self.state = ProfileGeneratorState.ACCELERATING

        # Brake check
        if self.state in [
            ProfileGeneratorState.ACCELERATING,
            ProfileGeneratorState.CRUISING,
        ]:
            dist_left = abs(self.target_position - self.position)
            if dist_left <= self.calculate_braking_distance():
                self.state = ProfileGeneratorState.DECELERATING

    def calculate_braking_distance(self) -> float:
        assert self.profile.deceleration > 0, (
            "Deceleration must be greater than zero to calculate braking distance."
        )
        v_sq = self.velocity**2
        d_brake = 0.5 * (v_sq / self.profile.deceleration)
        return d_brake
