from js import document
from pyodide.ffi import create_proxy


def close_modal(evt):
    modal_bg = document.getElementById("modal-bg")
    if modal_bg:
        modal_bg.remove()


close_modal_proxy = create_proxy(close_modal)
document.getElementById("close-btn").addEventListener("click", close_modal_proxy)
