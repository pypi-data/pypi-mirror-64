from pockethernet import PoEResult
from wiremapper.block.block import Block
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class PoEBlock(Block):
    def make(self, result):
        if not isinstance(result, PoEResult):
            return

        listbox = Gtk.ListBox()

        if result.poe_a_volt == 0 and result.poe_b_volt == 0:
            self._add_simple_row(listbox, Gtk.Label(label="No 802.3af PoE detected", xalign=0))
            self._add_seperator(listbox)
        else:
            if result.poe_a_volt > 0:
                self._add_simple_row(listbox,
                                     Gtk.Label(label="{} V on 802.3af Mode A".format(result.poe_a_volt), xalign=0))
                self._add_seperator(listbox)

            if result.poe_b_volt > 0:
                self._add_simple_row(listbox,
                                     Gtk.Label(label="{} V on 802.3af Mode B".format(result.poe_b_volt), xalign=0))
                self._add_seperator(listbox)

        passive = [i for i, x in enumerate(result.pair_volts) if x]
        if len(passive) == 0:
            self._add_simple_row(listbox, Gtk.Label(label="No passive PoE detected", xalign=0))
        else:
            for pair in passive:
                text = "{} V on pair {}".format(result.pair_volts[pair], pair + 1)
                self._add_simple_row(listbox, Gtk.Label(label=text, xalign=0))

        frame = Gtk.Frame()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        frame.add(listbox)
        return self._make_result("Power over ethernet", frame)
