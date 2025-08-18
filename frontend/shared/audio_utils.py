from js import Audio


def play_place_sound() -> None:
    """Play the block place sound effect."""
    audio = Audio.new("/shared/audio/place.wav")
    audio.play()


def win_sound() -> None:
    """Play win sound."""
    audio = Audio.new("/shared/audio/win.wav")
    audio.play()
