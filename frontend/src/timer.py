from constants import TIMER_MINUTES
from js import clearInterval, document, setInterval
from pyodide.ffi import create_proxy

time_left = TIMER_MINUTES * 60
interval_id = None
timer_proxy = None


def run_timer() -> None:
    """Update the timer once per second."""
    global time_left, interval_id  # noqa: PLW0603

    # Always update display
    timer_element = document.getElementById("timer")
    if timer_element:
        m, s = divmod(time_left, 60)
        timer_element.textContent = f"{m:02d}:{s:02d}"

    # If paused, stop ticking
    if not document.getElementById("pause-screen").hidden:
        return

    # Countdown
    time_left -= 1
    if time_left < 0:
        clearInterval(interval_id)
        interval_id = None


def start_timer() -> None:
    """Start or restart from full time."""
    global time_left, interval_id, timer_proxy  # noqa: PLW0603
    time_left = TIMER_MINUTES * 60
    if timer_proxy is None:
        timer_proxy = create_proxy(run_timer)
    if interval_id is None:
        run_timer()  # initial draw
        interval_id = setInterval(timer_proxy, 1000)


def resume_timer() -> None:
    """Resume after pause."""
    global interval_id, timer_proxy  # noqa: PLW0603
    if timer_proxy is None:
        timer_proxy = create_proxy(run_timer)
    if interval_id is None and document.getElementById("pause-screen").hidden:
        interval_id = setInterval(timer_proxy, 1000)


def pause_timer() -> None:
    """Pause manually."""
    global interval_id  # noqa: PLW0603
    if interval_id is not None:
        clearInterval(interval_id)
        interval_id = None
