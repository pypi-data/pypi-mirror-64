from pockethernet import LinkResult
from wiremapper.block.block import Block
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class LinkBlock(Block):
    def make(self, result):
        if not isinstance(result, LinkResult):
            return

        listbox = Gtk.ListBox()

        if result.up:
            duplexity = 'full duplex' if result.duplex else 'half duplex'
            status = Gtk.Label(label="Connected at {} {}".format(result.speed, duplexity), xalign=0)
            self._add_simple_row(listbox, status)
            self._add_seperator(listbox)

            grid = Gtk.Grid()
            grid.set_row_spacing(12)
            grid.set_column_spacing(12)

            grid.attach(Gtk.Label(label="Link partner", xalign=0), 0, 0, 1, 1)
            grid.attach(Gtk.Label(label="10 Mbps", xalign=1), 0, 1, 1, 1)
            grid.attach(Gtk.Label(label="100 Mbps", xalign=1), 0, 2, 1, 1)
            grid.attach(Gtk.Label(label="1000 Mbps", xalign=1), 0, 3, 1, 1)

            grid.attach(Gtk.Label(label="Half duplex", xalign=0), 1, 0, 1, 1)
            grid.attach(Gtk.Label(label="Full duplex", xalign=0), 2, 0, 1, 1)

            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_10HD), 1, 1, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_10FD), 2, 1, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_100HD), 1, 2, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_100FD), 2, 2, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_1000HD), 1, 3, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_1000FD), 2, 3, 1, 1)
            self._add_simple_row(listbox, grid)

        else:
            status = Gtk.Label(label="Could not establish link", xalign=0)
            self._add_simple_row(listbox, status)

        frame = Gtk.Frame()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        frame.add(listbox)
        return self._make_result("Link", frame)
