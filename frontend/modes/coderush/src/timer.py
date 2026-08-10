from engine.constants import TIMER_MINUTES
from js import clearInterval, document, setInterval
from pyodide.ffi import create_proxy

# Timer state
time_left = TIMER_MINUTES * 60
interval_id = None
timer_proxy = None

# Optional callback when timer hits zero
on_time_up = None


def update_display() -> None:
    """Update the timer display on the page."""
    timer_element = document.getElementById("timer")
    if not timer_element:
        return

    minutes, seconds = divmod(time_left, 60)
    timer_element.textContent = f"{minutes:02d}:{seconds:02d}"


def run_timer() -> None:
    """Update timer every tick."""
    global time_left, interval_id  # noqa: PLW0603

    # Update the display first
    update_display()

    # If the pause screen is visible, skip countdown
    pause_screen = document.getElementById("pause-screen")
    if pause_screen and not pause_screen.hidden:
        return

    # Countdown logic
    time_left -= 1
    if time_left < 0:
        clearInterval(interval_id)
        interval_id = None

        # Fire callback if defined
        if on_time_up is not None:
            on_time_up()


def start_timer() -> None:
    """Start the timer or restart from full duration."""
    global time_left, interval_id, timer_proxy  # noqa: PLW0603

    # Reset time to full duration
    time_left = TIMER_MINUTES * 60

    # Create a proxy if not already set
    if timer_proxy is None:
        timer_proxy = create_proxy(run_timer)

    # Only start if not already running
    if interval_id is None:
        run_timer()  # Draw immediately
        interval_id = setInterval(timer_proxy, 1000)


def pause_timer() -> None:
    """Pause the timer."""
    global interval_id  # noqa: PLW0603
    if interval_id is not None:
        clearInterval(interval_id)
        interval_id = None


def resume_timer() -> None:
    """Resume timer if currently paused."""
    global interval_id, timer_proxy  # noqa: PLW0603
    if timer_proxy is None:
        timer_proxy = create_proxy(run_timer)
    pause_screen = document.getElementById("pause-screen")
    if interval_id is None and (pause_screen is None or pause_screen.hidden):
        interval_id = setInterval(timer_proxy, 1000)


def reset_timer() -> None:
    """Reset timer without starting."""
    global time_left, interval_id  # noqa: PLW0603
    time_left = TIMER_MINUTES * 60
    update_display()
    if interval_id is not None:
        clearInterval(interval_id)
        interval_id = None
