from js import document


def close_modal(id: str) -> None:
    """Close a modal dialog by its DOM element ID."""
    modal_bg = document.getElementById(id)
    if modal_bg:
        modal_bg.remove()


def continue_modal(id: str) -> None:
    """Close a modal dialog by its DOM element ID."""
    close_modal(id)
    # Focus the input field
    input_box = document.getElementById("text-input")
    input_box.focus()
