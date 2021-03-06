#!/usr/bin/env python
import threading

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit, FormattedTextControl, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Label

from pydoro.pydoro_core.tomato import Tomato
from pydoro.pydoro_core.util import every

tomato = Tomato()


def exit_clicked(_=None):
    get_app().exit()


# All the widgets for the UI.
btn_start = Button("Start", handler=tomato.start)
btn_pause = Button("Pause", handler=tomato.pause)
btn_reset = Button("Reset", handler=tomato.reset)
btn_reset_all = Button("Reset All", handler=tomato.reset_all)
btn_exit = Button("Exit", handler=exit_clicked)

# text_area = TextArea(read_only=True, height=11, focusable=False)
text_area = FormattedTextControl(focusable=False, show_cursor=False)
text_window = Window(
    content=text_area, dont_extend_height=True, height=11, style="bg:#ffffff #000000"
)

root_container = Box(
    HSplit(
        [
            Label(text="Press `Tab` to move the focus."),
            HSplit(
                [
                    VSplit(
                        [btn_start, btn_pause, btn_reset, btn_reset_all, btn_exit],
                        padding=1,
                        style="bg:#cccccc",
                    ),
                    text_window,
                ]
            ),
        ]
    )
)

layout = Layout(container=root_container, focused_element=btn_start)

# Key bindings.
kb = KeyBindings()
kb.add("tab")(focus_next)
kb.add("s-tab")(focus_previous)
kb.add("right")(focus_next)
kb.add("left")(focus_previous)
kb.add("q")(exit_clicked)

# Styling.
style = Style(
    [
        ("left-pane", "bg:#888800 #000000"),
        ("right-pane", "bg:#00aa00 #000000"),
        ("button", "#000000"),
        ("button-arrow", "#000000"),
        ("button focused", "bg:#ff0000"),
        ("red", "#ff0000"),
        ("green", "#00ff00"),
    ]
)

# Build a main application object.
application = Application(layout=layout, key_bindings=kb, style=style, full_screen=True)


def draw():
    tomato.update()
    text_area.text = tomato.as_formatted_text()
    application.invalidate()


def main():
    draw()
    threading.Thread(target=lambda: every(0.4, draw), daemon=True).start()
    application.run()


if __name__ == "__main__":
    main()
