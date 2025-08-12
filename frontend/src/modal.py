from js import document
from pyodide.ffi import JsProxy


def close_modal(_evt: JsProxy) -> None:
    """Close the modal by removing its background element from the DOM."""
    modal_bg = document.getElementById("modal-bg")
    if modal_bg:
        modal_bg.remove()
