from lib.components.button import Button
from lib.components.dialog import DIALOG_CONTEXT, create_dialog
from lib.components.frame import Frame
from lib.components.label import Label
from lib.core.context import Context, ctx
from lib.core.node.component import component
from lib.core.signal import Computed, Signal

@component
def App():
    dialog = ctx().get(DIALOG_CONTEXT)
    assert(dialog)
    dialog.root.title("Hello World!")

    counter = Signal(0)

    @Computed
    def text():
        return f"count: {counter()}"

    return Frame(children=lambda: [
        Label(text="Hello World!"),
        Label(textvariable=text),
        Button(text="increment", command=lambda: counter.set(counter() + 1)),
        Button(text="decrement", command=lambda: counter.set(counter() - 1)),
    ])

def main():
    # create initial context
    with Context().self():
        create_dialog(App)

if __name__ == '__main__':
    main()
