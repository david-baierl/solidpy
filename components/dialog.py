from dataclasses import dataclass
import tkinter as tk
from typing import Callable

from core.context import ctx
from core.event.helper import bind_direct, on
from core.event.types import DestroyEvent
from core.injectable import Injectable
from core.node.component import Component

WIDTH = 600
HEIGHT = 400

@dataclass
class DialogContext:
    root: tk.Tk
    close: Callable

DIALOG_CONTEXT = Injectable[DialogContext]()

def create_dialog(
    View: Component,
    on_close: Callable = lambda: None,
    width: int = WIDTH,
    height: int = HEIGHT,
) -> Callable:
    root = tk.Tk()

    def handle_close():
        root.destroy()
        on_close()

    # @HINT: zoom
    root.tk.call('tk', 'scaling', '-displayof', '.', 2)

    with ctx().scope() as s:

        s.insert(DIALOG_CONTEXT, DialogContext(
            root=root,
            close=handle_close,
        ))

        # catch destroy events
        s.subscribe(on(
            DestroyEvent,
            lambda event: event.stop(),
        ))

        # --- create canvas with scrollbar ---

        container = tk.Frame(root, width=width, height=height)
        container.pack(expand=True, fill="both")

        canvas = tk.Canvas(container, width=width, height=height)
        scrollbar_x = tk.Scrollbar(container, command=canvas.xview, orient='horizontal')
        scrollbar_y = tk.Scrollbar(container, command=canvas.yview, orient='vertical')

        scrollbar_x.pack(side=tk.BOTTOM, fill="x")
        scrollbar_y.pack(side=tk.RIGHT, fill="y")
        canvas.pack(side=tk.TOP, fill="both", expand=True)

        canvas.configure(
            yscrollcommand = scrollbar_y.set,
            xscrollcommand = scrollbar_x.set,
        )

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        def on_configure(event: tk.Event[tk.Canvas]):
            x1, y1, x2, y2 = canvas.bbox('all')
            canvas.configure(scrollregion=(
                x1, y1, max(x2, width), max(y2, height)
            ))

        canvas.bind('<Configure>', on_configure)

        # --- put frame in canvas ---

        frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')

        # --- add widgets in frame ---

        try:
            view = View()
            bind_direct(root, "<Destroy>", lambda _: view.destroy())
            view.render(frame).pack()
        except Exception as e:
            handle_close()
            raise e

    root.mainloop()

    return handle_close
