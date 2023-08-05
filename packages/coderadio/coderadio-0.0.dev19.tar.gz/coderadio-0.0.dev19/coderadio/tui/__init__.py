from prompt_toolkit.application import Application
from prompt_toolkit.document import Document

from coderadio.tui.buffers.listview import LISTVIEW_BUFFER
from coderadio.tui.keybindings import kbindings
from coderadio.tui.layout import layout

from coderadio.utils import stations
from coderadio.radio import rb


class TUI:
    def __init__(self):
        self.app = Application(
            layout=layout,
            key_bindings=kbindings(),
            full_screen=True,
            mouse_support=True,
            enable_page_navigation_bindings=True
        )

    def initialize(self, *args, **kwargs):
        list_buffer = self.app.layout.get_buffer_by_name(
            LISTVIEW_BUFFER
        )
        stations.new(*rb.stations_by_tag("bbc"))
        list_buffer.update(str(stations))

    def run(self):
        self.app.run()


app = TUI()
app.initialize()
