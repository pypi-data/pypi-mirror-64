import json
import os
import threading

import gi
import pockethernet
import logging

from pockethernet import WiremapResult, LinkResult, PoEResult, BerResult, TdrResult, DhcpResult, CdpResult

import wiremapper.discover
import wiremapper.wiremap
from wiremapper.block.ber import BerBlock
from wiremapper.block.dhcp import DhcpBlock
from wiremapper.block.link import LinkBlock
from wiremapper.block.poe import PoEBlock
from wiremapper.block.tdr import TdrBlock
from wiremapper.block.wiremap import WiremapBlock
from wiremapper.quicktest import Quicktest

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf

gi.require_version('Handy', '0.0')
from gi.repository import Handy

logging.basicConfig(level=logging.DEBUG)


class DeviceFinder(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
        devices = list(wiremapper.discover.get_paired_devices())
        GLib.idle_add(self.callback, devices)


class ResultSlot:
    def __init__(self):
        self.label = None

        self.wiremap = None
        self.link = None
        self.poe = None
        self.tdr = None
        self.ber = None

    def all_none(self, data):
        return all(x is None for x in data)

    def get_wiremap_label(self):
        wiremap = self.wiremap
        if wiremap.connections == [None, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            return "Straight cable, unshielded"

        if wiremap.connections == [0, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            return "Straight cable, shielded"

        if wiremap.connections == [None, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            return "2-pair cable, unshielded"

        if wiremap.connections == [0, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            return "2-pair cable, shielded"

        if wiremap.connections == [None, 8, 7, 6, 5, 4, 3, 2, 1] and self.all_none(wiremap.shorts):
            return "Rollover cable (for serial console)"

        if wiremap.connections == [None, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            return "Crossover cable, unshielded"

        if wiremap.connections == [0, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            return "Crossover cable, shielded"

        if wiremap.shorts == [None, 3, 6, None, 7, 8, None, None, None] and self.all_none(wiremap.connections):
            return "Loopback adapter"

        if self.all_none(wiremap.connections) and self.all_none(wiremap.shorts):
            return "Open cable"

    def get_link_label(self):
        link = self.link
        return link.speed + " link established"

    def get_poe_label(self):
        poe = self.poe
        poe_status = "no PoE"
        if poe.poe_a_volt + poe.poe_b_volt > 3:
            if poe.poe_a_volt > poe.poe_b_volt:
                poe_status = "PoE 802.3af mode A ({}V)".format(poe.poe_a_volt)
            else:
                poe_status = "PoE 802.3af mode B ({}V)".format(poe.poe_b_volt)
        elif sum(poe.pair_volts) > 3:
            poe_status = "passive PoE ({}v)".format(max(poe.pair_volts))
        return poe_status

    def get_label(self):
        if self.wiremap is None and self.link is None and self.poe is None:
            return 'No result yet'

        label = ''
        if self.wiremap is not None:
            label += 'wiremap: {}, '.format(self.get_wiremap_label())

        if self.link is not None and self.link.up:
            label = self.get_link_label()

        if self.poe is not None:
            label += ', ' + self.get_poe_label()

        return label.strip()

    def get_json(self):
        result = {}
        if self.wiremap is not None:
            result['wiremap'] = {
                'status': self.get_wiremap_label(),
                'connections': self.wiremap.connections,
                'shorts': self.wiremap.shorts
            }
        if self.link is not None and self.link.up:
            result['link'] = {
                'up': True,
                'speed': self.link.speed,
                'duplex': self.link.duplex,
                'mdix': self.link.mdix,
                'link_partner_advertized': {
                    '10HD': self.link.link_partner_10HD,
                    '10FD': self.link.link_partner_10FD,
                    '100HD': self.link.link_partner_100HD,
                    '100FD': self.link.link_partner_100FD,
                    '1000HD': self.link.link_partner_1000HD,
                    '1000FD': self.link.link_partner_1000FD
                },
                'skew': [self.link.skew_pair1, self.link.skew_pair2, self.link.skew_pair3, self.link.skew_pair4]
            }
        elif self.link is not None:
            result['link'] = {
                'up': False
            }

        if self.poe is not None:
            result['poe'] = {
                'a': self.poe.poe_a_volt,
                'b': self.poe.poe_b_volt,
                'passive': self.poe.pair_volts
            }

        return {
            "label": self.label,
            "result": result
        }


class CustomTest(threading.Thread):
    def __init__(self, callback, mac, tests):
        threading.Thread.__init__(self)
        self.callback = callback
        self.mac = mac
        self.tests = tests
        self.cancelled = threading.Event()

    def all_none(self, data):
        return all(x is None for x in data)

    def cancel(self):
        self.cancelled.set()

    def run(self) -> None:
        GLib.idle_add(self.callback, True)
        client = pockethernet.Pockethernet()
        client.connect(self.mac)

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False)
            return
        if "wiremap" in self.tests:
            wiremap = client.get_wiremap()
            GLib.idle_add(self.callback, True, wiremap)

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False)
            return
        if "tdr" in self.tests:
            tdr = client.get_tdr()
            GLib.idle_add(self.callback, True, tdr)

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False)
            return
        if "poe" in self.tests:
            poe = client.get_poe()
            GLib.idle_add(self.callback, True, poe)

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False)
            return
        if "link" in self.tests:
            link = client.get_link()
            GLib.idle_add(self.callback, True, link)

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False)
            return
        if "ber" in self.tests:
            ber = client.get_ber(speed=1000, large_packet=True)
            GLib.idle_add(self.callback, True, ber)

        GLib.idle_add(self.callback, False)


class WiremapperApplication(Gtk.Application):
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        AppWindow(self)


class AppWindow:
    def __init__(self, application):
        self.application = application
        builder = Gtk.Builder()
        builder.add_from_resource('/nl/brixit/wiremapper/ui/wiremapper.ui')
        builder.connect_signals(Handler(builder, self))

        css = Gio.resources_lookup_data("/nl/brixit/wiremapper/ui/style.css", 0)

        self.provider = Gtk.CssProvider()
        self.provider.load_from_data(css.get_data())

        window = builder.get_object("main_window")
        window.set_application(self.application)

        self.apply_css(window, self.provider)

        window.show_all()

        Gtk.main()

    def apply_css(self, widget, provider):
        Gtk.StyleContext.add_provider(widget.get_style_context(),
                                      provider,
                                      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        if isinstance(widget, Gtk.Container):
            widget.forall(self.apply_css, provider)


class Handler:
    def __init__(self, builder, application):
        self.builder = builder
        self.application = application
        self.window = builder.get_object('main_window')
        self.mobile_stackswitcher = builder.get_object('mobile_stackswitcher')
        self.quicktest_spinner = builder.get_object('quicktest_spinner')
        self.quicktest_start = builder.get_object('quicktest_start')
        self.quicktest_status = builder.get_object('quicktest_status')
        self.device_list = builder.get_object('device_list')
        self.quicktest_result = builder.get_object('quicktest_result')
        self.custom_start = builder.get_object('custom_start')
        self.custom_spinner = builder.get_object('custom_spinner')
        self.custom_result = builder.get_object('custom_result')
        self.custom_slot_list = builder.get_object('custom_slot_list')

        self.custom_wiremap = builder.get_object('custom_wiremap')
        self.custom_link = builder.get_object('custom_link')
        self.custom_poe = builder.get_object('custom_poe')
        self.custom_tdr = builder.get_object('custom_tdr')
        self.custom_ber = builder.get_object('custom_ber')

        self.mac = None

        self.quicktest_running = False
        self.quicktest_thread = None
        self.custom_running = False
        self.custom_thread = None

        self.slot_count = 0

        save_json_action = Gio.SimpleAction.new("save_json", None)
        save_json_action.connect('change-state', self.on_save_json)
        self.window.add_action(save_json_action)

    def on_quit(self, *args):
        Gtk.main_quit()

    def on_headerbar_squeezer_notify(self, squeezer, event):
        """
        This handler gets called when the squeezer in the headerbar changes the visible control.
        If the window is wide enough the visible control is a GtkStackSwitcher. if it is too small
        to show that control it will display an empty GtkBox.

        If the stackswitcher is hidden it shows the mobile stackswitcher at the bottom instead
        """
        child = str(squeezer.get_visible_child())
        self.mobile_stackswitcher.set_reveal(child.startswith('<Gtk.Box'))

    def on_start(self, *args):
        thread = DeviceFinder(self.devicefinder_update)
        thread.start()

        add_image = Gtk.Image.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON)
        self.custom_slot_list.add(add_image)
        self.custom_slot_list.show_all()

    def devicefinder_update(self, devices):
        logging.debug('Got devicefinder callback with {} devices'.format(len(devices)))

        # model.clear()
        amount = len(devices)
        i = 0

        if amount == 1:
            self.mac = devices[0][0]

        for address, label in devices:
            i += 1
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            label_mac = Gtk.Label(label=address, xalign=0)
            label_name = Gtk.Label(label=label, xalign=0)
            label_name.set_markup('<b>{}</b>'.format(label))
            box.pack_start(label_name, False, False, True)
            box.pack_start(label_mac, False, False, True)
            if i != amount:
                box.pack_start(Gtk.Separator(), False, False, True)

            checkmark = Gtk.Image()
            if i == 1:
                checkmark.set_from_icon_name('object-select-symbolic', Gtk.IconSize.BUTTON)

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            hbox.pack_start(box, False, False, True)
            hbox.pack_start(checkmark, False, False, True)

            self.device_list.pack_start(hbox, False, False, True)
        self.device_list.show_all()
        # if len(devices) == 1:
        #    self.device_selector.set_active(0)

    def on_device_change(self, combobox):
        tree_iter = combobox.get_active()
        if tree_iter is not None and tree_iter > -1:
            model = combobox.get_model()
            self.mac = model[tree_iter][1]
            logging.debug('Changing device to {}'.format(self.mac))

    def on_quicktest_start_clicked(self, button):
        if self.quicktest_running:
            self.quicktest_thread.cancel()
            button.set_sensitive(False)
        else:
            self.quicktest_running = True
            self.quicktest_thread = Quicktest(self.quicktest_update, self.mac)
            self.quicktest_thread.daemon = True
            self.quicktest_thread.start()
            button.set_label("Cancel")
            ctx = button.get_style_context()
            ctx.remove_class('suggested-action')
            ctx.add_class('destructive-action')

            old_results = self.quicktest_result.get_children()
            for w in old_results:
                self.quicktest_result.remove(w)

    def quicktest_update(self, running, status, result=None):
        if running:
            self.quicktest_spinner.start()
        else:
            self.quicktest_running = False
            self.quicktest_spinner.stop()
            self.quicktest_start.set_label("Start")

            if status == "Stopped":
                self.quicktest_start.set_sensitive(True)
            ctx = self.quicktest_start.get_style_context()
            ctx.remove_class('destructive-action')
            ctx.add_class('suggested-action')

        if status is not None:
            self.quicktest_status.set_label(status)

        if result:
            for block in result:
                box = self.make_result_block(block)
                self.quicktest_result.pack_start(box, False, False, True)

            self.application.apply_css(self.quicktest_result, self.application.provider)
            self.quicktest_result.show_all()

    def on_custom_start_clicked(self, button):
        if self.custom_running:
            self.custom_thread.cancel()
            button.set_sensitive(False)
        else:
            tests = []
            if self.custom_wiremap.get_active():
                tests.append('wiremap')
            if self.custom_link.get_active():
                tests.append('link')
            if self.custom_poe.get_active():
                tests.append('poe')
            if self.custom_tdr.get_active():
                tests.append('tdr')
            if self.custom_ber.get_active():
                tests.append('ber')

            if len(tests) == 0:
                return
            self.custom_thread = CustomTest(self.custom_update, self.mac, tests)
            self.custom_thread.daemon = True
            self.custom_thread.start()
            button.set_label("Cancel")
            ctx = button.get_style_context()
            ctx.remove_class('suggested-action')
            ctx.add_class('destructive-action')
            self.custom_running = True

            old_results = self.custom_result.get_children()
            for w in old_results:
                self.custom_result.remove(w)

    def custom_update(self, running, result=None):
        if running:
            self.custom_spinner.start()
        else:
            self.custom_spinner.stop()
            self.custom_running = False
            self.custom_start.set_label("Start")
            ctx = self.custom_start.get_style_context()
            ctx.remove_class('destructive-action')
            ctx.add_class('suggested-action')
            self.custom_start.set_sensitive(True)

        slot_selected_row = self.custom_slot_list.get_selected_row()
        slot_selected = False
        if slot_selected_row:
            slot_selected = True
            slot_result = slot_selected_row.get_children()[0]

        if result:
            box = self.make_result_block(result)
            self.custom_result.pack_start(box, False, False, True)
            if slot_selected:
                if isinstance(result, LinkResult):
                    slot_result.result.link = result
                elif isinstance(result, WiremapResult):
                    slot_result.result.wiremap = result
                elif isinstance(result, PoEResult):
                    slot_result.result.poe = result
                elif isinstance(result, TdrResult):
                    slot_result.result.tdr = result
                elif isinstance(result, BerResult):
                    slot_result.result.ber = result

            self.custom_result.show_all()

        if slot_selected:
            self.update_slot_result(slot_result)

    def make_result_block(self, result):
        if isinstance(result, WiremapResult):
            block = WiremapBlock()
        elif isinstance(result, TdrResult):
            block = TdrBlock()
        elif isinstance(result, LinkResult):
            block = LinkBlock()
        elif isinstance(result, PoEResult):
            block = PoEBlock()
        elif isinstance(result, BerResult):
            block = BerBlock()
        elif isinstance(result, DhcpResult):
            block = DhcpBlock()

        else:
            raise ValueError("Block not supported by this function")

        return block.make(result)

    def add_class(self, widget, new_class):
        ctx = widget.get_style_context()
        ctx.add_class(new_class)

    def on_custom_slot_list_row_activated(self, listbox, row):
        if isinstance(row.get_child(), Gtk.Image):
            self.add_slot()
            return

    def add_slot(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        label = Gtk.Entry()
        label.connect("activate", self.rename_slot)
        delete_image = Gtk.Image.new_from_icon_name('edit-delete-symbolic', Gtk.IconSize.BUTTON)
        deleter = Gtk.Button()
        deleter.connect("clicked", self.delete_slot)
        deleter.add(delete_image)
        vbox.pack_start(label, False, False, True)
        box.pack_start(vbox, True, True, True)
        box.pack_end(deleter, False, False, True)

        box.result = ResultSlot()

        self.custom_slot_list.insert(box, self.slot_count)
        self.custom_slot_list.unselect_all()
        self.custom_slot_list.show_all()
        self.slot_count += 1

    def delete_slot(self, button):
        result_box = button.get_parent()
        listboxrow = result_box.get_parent()
        listbox = listboxrow.get_parent()
        listbox.remove(listboxrow)
        listbox.show_all()
        self.slot_count -= 1

    def rename_slot(self, entry):
        vbox = entry.get_parent()
        result_box = vbox.get_parent()
        name = entry.get_text()
        result_box.result.label = name

        label = Gtk.Label(xalign=0)
        label.set_markup('<b>{}</b>'.format(name))

        vbox.remove(entry)
        vbox.add(label)
        vbox.add(Gtk.Label(xalign=0, label="No result yet"))
        vbox.show_all()

    def update_slot_result(self, box):
        result_label = box.get_children()[0].get_children()[1]
        result_label.set_markup(box.result.get_label())
        box.show_all()

    def on_save_json(self, *args):
        result = []
        for child in self.custom_slot_list.get_children()[:-1]:
            box = child.get_children()[0]
            data = box.result.get_json()
            result.append(data)

        dialog = Gtk.FileChooserDialog("Please choose a target file", self.window, Gtk.FileChooserAction.SAVE, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        ))
        dialog.set_current_name("Untitled.json")
        dialog.set_local_only(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename(), 'w') as handle:
                json.dump(result, handle)
        dialog.destroy()


def main():
    # This is to make the Handy module actually loaded to be used in the GtkBuilder
    Handy.Column()

    if os.path.isfile('wiremapper.gresource'):
        print("Using resources from cwd")
        resource = Gio.resource_load("wiremapper.gresource")
        Gio.Resource._register(resource)
    else:
        print("Using resources from pkg_resources")
        with pkg_resources.path('wiremapper', 'wiremapper.gresource') as resource_file:
            resource = Gio.resource_load(str(resource_file))
            Gio.Resource._register(resource)

    app = WiremapperApplication("nl.brixit.wiremapper", Gio.ApplicationFlags.FLAGS_NONE)
    app.run()


if __name__ == '__main__':
    main()
