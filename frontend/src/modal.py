from js import document
from pyodide.ffi import JsProxy, create_proxy


def close_modal(_evt: JsProxy) -> None:
    """Close the modal by removing its background element from the DOM."""
    modal_bg = document.getElementById("modal-bg")
    if modal_bg:
        modal_bg.remove()


close_modal_proxy = create_proxy(close_modal)
document.getElementById("close-btn").addEventListener("click", close_modal_proxy)
