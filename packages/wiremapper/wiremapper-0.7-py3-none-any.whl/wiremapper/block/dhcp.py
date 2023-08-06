from pockethernet import DhcpResult
from wiremapper.block.block import Block
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class DhcpBlock(Block):
    def make(self, result):
        if not isinstance(result, DhcpResult):
            return

        listbox = Gtk.ListBox()

        grid = Gtk.Grid()
        grid.set_row_spacing(12)
        grid.set_column_spacing(12)

        grid.attach(self._dim_label("Address", xalign=1), 0, 0, 1, 1)
        grid.attach(self._dim_label("Netmask", xalign=1), 0, 1, 1, 1)
        grid.attach(self._dim_label("Gateway", xalign=1), 0, 2, 1, 1)
        grid.attach(self._dim_label("DNS", xalign=1), 0, 3, 1, 1)
        grid.attach(self._dim_label("Filename", xalign=1), 0, 4, 1, 1)
        grid.attach(self._dim_label("Server", xalign=1), 0, 5, 1, 1)

        grid.attach(Gtk.Label(label=result.your_ip, xalign=0), 1, 0, 1, 1)
        grid.attach(Gtk.Label(label=result.subnet_mask, xalign=0), 1, 1, 1, 1)
        grid.attach(Gtk.Label(label=result.gateway, xalign=0), 1, 2, 1, 1)
        grid.attach(Gtk.Label(label=", ".join(result.nameservers), xalign=0), 1, 3, 1, 1)
        grid.attach(Gtk.Label(label=result.filename, xalign=0), 1, 4, 1, 1)
        grid.attach(Gtk.Label(label=result.next_server, xalign=0), 1, 5, 1, 1)
        self._add_simple_row(listbox, grid)

        frame = Gtk.Frame()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        frame.add(listbox)
        return self._make_result("DHCP", frame)
