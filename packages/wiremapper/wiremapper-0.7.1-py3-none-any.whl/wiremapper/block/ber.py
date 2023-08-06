from pockethernet import BerResult
from wiremapper.block.block import Block
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class BerBlock(Block):
    def make(self, result):
        if not isinstance(result, BerResult):
            return

        listbox = Gtk.ListBox()

        if result.status:
            sent = "{:n}".format(result.sent)
            received = "{:n}".format(result.received)
            errors = "{} ({:.2f}%)".format(result.errors, (result.errors / result.sent) * 100.0)

            grid = Gtk.Grid()
            grid.set_row_spacing(12)
            grid.set_column_spacing(12)

            grid.attach(self._dim_label("Packets sent", xalign=1), 0, 0, 1, 1)
            grid.attach(self._dim_label("Packets received", xalign=1), 0, 1, 1, 1)
            grid.attach(self._dim_label("Errors", xalign=1), 0, 2, 1, 1)

            grid.attach(Gtk.Label(label=sent, xalign=0), 1, 0, 1, 1)
            grid.attach(Gtk.Label(label=received, xalign=0), 1, 1, 1, 1)
            grid.attach(Gtk.Label(label=errors, xalign=0), 1, 2, 1, 1)
            self._add_simple_row(listbox, grid)
        else:
            self._add_simple_row(listbox, Gtk.Label(label="No packet sucessfully received", xalign=0))

        frame = Gtk.Frame()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        frame.add(listbox)
        return self._make_result("Bit error rate", frame)
