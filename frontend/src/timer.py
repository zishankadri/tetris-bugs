from constants import TIMER_MINUTES
from js import clearInterval, document, setInterval
from pyodide.ffi import create_proxy

time_left = TIMER_MINUTES * 60
interval_id = None


def run_timer() -> None:
    """Run the timer."""
    global time_left, interval_id  # noqa: PLW0603
    timer_element = document.getElementById("timer")
    if not timer_element:
        return

    minutes = time_left // 60
    seconds = time_left % 60
    timer_element.textContent = f"{minutes:02d}:{seconds:02d}"

    time_left -= 1
    if time_left < 0:
        clearInterval(interval_id)
        interval_id = None


def start_timer() -> None:
    """Start the timer."""
    global interval_id  # noqa: PLW0603
    if interval_id is None:
        run_timer()
        timer_proxy = create_proxy(run_timer)
        interval_id = setInterval(timer_proxy, 1000)
