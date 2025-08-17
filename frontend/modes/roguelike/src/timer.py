from js import clearInterval, document, setInterval
from pyodide.ffi import create_proxy
from shared.constants import TIMER_MINUTES

time_left = TIMER_MINUTES * 60
interval_id = None

# Callback to be called when timer runs out
on_time_up = None


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
        if on_time_up is not None:
            on_time_up()


def start_timer() -> None:
    """Start the timer."""
    global interval_id  # noqa: PLW0603
    if interval_id is None:
        run_timer()
        timer_proxy = create_proxy(run_timer)
        interval_id = setInterval(timer_proxy, 1000)


def reset_timer() -> None:
    """Reset the timer to full duration."""
    global time_left, interval_id  # noqa: PLW0603
    time_left = TIMER_MINUTES * 60
    if interval_id is not None:
        clearInterval(interval_id)
        interval_id = None
