from tests.trapezoidal_move import configure_trapezoidal, run_trapezoidal
from tests.square_wave import configure_square_wave, run_square_wave

TESTS = {
    "Trapezoidal Move": (configure_trapezoidal, run_trapezoidal),
    "Square Wave Response": (configure_square_wave, run_square_wave),
}