import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf

gi.require_version('Handy', '0.0')
from gi.repository import Handy


class PreferencesWindow:
    def __init__(self, parent):
        builder = Gtk.Builder()
        builder.add_from_resource('/nl/brixit/wiremapper/ui/preferences.ui')
        builder.connect_signals(Handler(builder, self))

        css = Gio.resources_lookup_data("/nl/brixit/wiremapper/ui/style.css", 0)

        self.provider = Gtk.CssProvider()
        self.provider.load_from_data(css.get_data())

        window = builder.get_object("preferences_window")

        window.set_transient_for(parent)
        window.set_modal(True)

        window.show_all()


class Item(GObject.GObject):
    text = GObject.property(type=str)

    def __init__(self, text):
        GObject.GObject.__init__(self)
        self.text = text


class Handler:
    def __init__(self, builder, application):
        self.builder = builder
        self.application = application
        self.window = builder.get_object('preferences_window')

        self.wire_colors = builder.get_object('wire_colors')
        wire_color_model = Gio.ListStore()
        wire_color_model.append(Item("T568 A"))
        wire_color_model.append(Item("T568 B"))
        self.wire_colors.bind_name_model(wire_color_model, self.combo_text)

        self.units = builder.get_object('units')
        units_model = Gio.ListStore()
        units_model.append(Item("Meters"))
        units_model.append(Item("Feet"))
        self.units.bind_name_model(units_model, self.combo_text)

        self.settings = Gio.Settings.new('nl.brixit.wiremapper')
        self.settings.connect('changed::wire-colors', self.on_combo_changed, self.wire_colors)
        self.settings.connect('changed::units', self.on_combo_changed, self.units)

        self.on_combo_changed(self.settings, 'wire-colors', self.wire_colors)
        self.on_combo_changed(self.settings, 'units', self.units)

        self.wire_colors.connect('notify::selected-index', self.on_wire_color_changed)
        self.units.connect('notify::selected-index', self.on_units_changed)

    def combo_text(self, item):
        return item.text

    def on_combo_changed(self, settings, key, widget):
        mapping = {
            'wire-colors': {
                'T568 A': 0,
                'T568 B': 1
            },
            'units': {
                'Meters': 0,
                'Feet': 1
            }
        }
        new_value = settings.get_string(key)
        index = mapping[key][new_value]
        widget.set_selected_index(index)

    def on_wire_color_changed(self, widget, *args):
        mapping = {
            0: 'T568 A',
            1: 'T568 B'
        }
        new_value = mapping[widget.get_selected_index()]
        self.settings.set_string("wire-colors", new_value)

    def on_units_changed(self, widget, *args):
        mapping = {
            0: 'Meters',
            1: 'Feet'
        }
        new_value = mapping[widget.get_selected_index()]
        self.settings.set_string("units", new_value)
