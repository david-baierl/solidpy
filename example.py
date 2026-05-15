from components.button import Button
from components.dialog import DIALOG_CONTEXT, create_dialog
from components.frame import Frame
from components.label import Label
from core.context import Context, ctx
from core.helper import computed
from core.node.component import component
from core.signal import Signal

@component
def App():
    dialog = ctx().get(DIALOG_CONTEXT)
    assert(dialog)
    dialog.root.title("Hello World!")

    counter = Signal(0)

    @computed
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
