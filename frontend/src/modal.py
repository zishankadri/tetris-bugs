from js import document


def close_modal(id: str) -> None:
    """Close a modal dialog by its DOM element ID."""
    modal_bg = document.getElementById(id)
    if modal_bg:
        modal_bg.remove()
