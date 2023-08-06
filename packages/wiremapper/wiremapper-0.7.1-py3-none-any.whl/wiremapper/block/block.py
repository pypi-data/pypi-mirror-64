import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class Block:

    def _make_result(self, name, frame):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        label = Gtk.Label(label=name, xalign=0)
        label.set_markup('<b>{}</b>'.format(name))
        box.pack_start(label, False, False, True)
        box.pack_start(frame, False, False, True)
        return box

    def _add_class(self, widget, new_class):
        ctx = widget.get_style_context()
        ctx.add_class(new_class)

    def _add_passive_row(self, listbox, widget):
        row = Gtk.ListBoxRow(selectable=False, activatable=False)
        row.add(widget)
        listbox.insert(row, -1)

    def _add_simple_row(self, listbox, widget):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(16)
        box.set_margin_bottom(14)
        self._add_passive_row(listbox, box)
        box.pack_start(widget, False, False, True)

    def _add_seperator(self, listbox):
        self._add_passive_row(listbox, Gtk.Separator())

    def _dim_label(self, text, xalign=0):
        label = Gtk.Label(label=text, xalign=xalign)
        label.get_style_context().add_class('dim-label')
        return label
