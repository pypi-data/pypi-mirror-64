from pockethernet import TdrResult
from wiremapper.block.block import Block
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class TdrBlock(Block):
    def make(self, result):
        if not isinstance(result, TdrResult):
            return

        frame = Gtk.Frame()
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        splits_found = [i for i, x in enumerate(result.split) if x]
        if len(splits_found) > 0:
            error_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            error_row.set_margin_start(12)
            error_row.set_margin_end(12)
            error_row.set_margin_top(16)
            error_row.set_margin_bottom(14)
            if len(splits_found) == 1:
                text = "Split pair detected in pair {}".format(splits_found[0] + 1)
            elif len(splits_found) == 2:
                text = "Split pair detected between pair {} and {}".format(splits_found[0] + 1, splits_found[1] + 1)
            else:
                text = "Split pair detected"
            split_label = Gtk.Label(xalign=0)
            split_label.set_markup('<b>{}</b>'.format(text))
            split_label.get_style_context().add_class('error')

            split_label.set_line_wrap(True)
            error_row.pack_start(split_label, False, False, True)
            help_label = Gtk.Label(label="Significant crosstalk detected inside the cable, this is either a cable with "
                                         "split pairs or the cable has no twisting", xalign=0)
            help_label.set_line_wrap(True)
            help_label.get_style_context().add_class('error')
            error_row.pack_start(help_label, False, False, True)

            self._add_passive_row(listbox, error_row)
            self._add_seperator(listbox)

        info_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_row.set_margin_start(12)
        info_row.set_margin_end(12)
        info_row.set_margin_top(16)
        info_row.set_margin_bottom(14)
        self._add_passive_row(listbox, info_row)

        info_label = Gtk.Label(label="Pair lengths are {:.1f}m, {:.1f}m, {:.1f}m, {:.1f}m ".format(*result.distance),
                               xalign=0)
        info_label.set_line_wrap(True)
        info_row.pack_start(info_label, False, False, True)

        self._add_class(frame, 'view')
        frame.add(listbox)

        return self._make_result("Time domain reflectometry", frame)
