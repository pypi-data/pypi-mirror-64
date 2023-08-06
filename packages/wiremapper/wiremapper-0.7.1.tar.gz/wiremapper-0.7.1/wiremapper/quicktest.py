import logging
import threading

import gi
import pockethernet
from pockethernet import DhcpResult, CdpResult

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf


class Quicktest(threading.Thread):
    def __init__(self, callback, mac):
        threading.Thread.__init__(self)
        self.callback = callback
        self.mac = mac
        self.cancelled = threading.Event()

    def all_none(self, data):
        return all(x is None for x in data)

    def cancel(self):
        self.cancelled.set()
        GLib.idle_add(self.callback, True, "Stopping tests...", [])

    def run(self):
        GLib.idle_add(self.callback, True, "Connecting to the Pockethernet\n{}".format(self.mac))
        client = pockethernet.Pockethernet()
        client.connect(self.mac)
        GLib.idle_add(self.callback, True, "Running wiremap")

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        wiremap = client.get_wiremap()

        GLib.idle_add(self.callback, True, "Running TDR")
        tdr = client.get_tdr(long_distance=True)
        if not tdr.valid:
            tdr = client.get_tdr(long_distance=False)

        spf = ""
        if sum(tdr.split) > 0:
            spf = "\nSplit pair detected"

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        logging.debug('Wiremap connections: {}'.format(wiremap.connections))
        logging.debug('Wiremap shorts     : {}'.format(wiremap.shorts))

        # Check the situations that guarantee a wiremap adapter is connected first because it's very fast and
        # guarantees the other tests will fail anyway
        if wiremap.connections == [None, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Straight cable, unshielded" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [0, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Straight cable, shielded" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [None, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "2-pair cable, unshielded" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [0, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "2-pair cable, shielded" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [None, 8, 7, 6, 5, 4, 3, 2, 1] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Rollover cable (for serial console)" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [None, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Crossover cable, unshielded" + spf, [wiremap, tdr])
            return

        if wiremap.connections == [0, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Crossover cable, shielded" + spf, [wiremap, tdr])
            return

        if wiremap.shorts == [None, 3, 6, None, 7, 8, None, None, None] and self.all_none(wiremap.connections):
            GLib.idle_add(self.callback, True, "Running BER test")
            ber = client.get_ber(speed=100, large_packet=True)
            if ber.errors == 0 and ber.status:
                ber = client.get_ber(speed=1000, large_packet=True)
            if ber.errors == 0 and ber.status:
                ber_status = "BER test successful"
            else:
                ber_status = "BER test FAILED"
            GLib.idle_add(self.callback, False, ber_status, [ber])
            return

        if self.all_none(wiremap.connections) and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Open" + spf, [wiremap, tdr])
            return

        # Test a link because weird wiremap reading might just be an ethernet port
        GLib.idle_add(self.callback, True, "Running link test")
        link = client.get_link()

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        if link.up:
            client.link_reset()
            client.set_vlan(-1)
            client.enable_dhcp()
            client.set_capture_mode(dhcp=True, lldp=True, traffic=False)
            GLib.idle_add(self.callback, True, "Running PoE test", [link])
            poe = client.get_poe()

            if self.cancelled.is_set():
                GLib.idle_add(self.callback, False, "Stopped", [])
                return

            poe_status = "no PoE"
            if poe.poe_a_volt + poe.poe_b_volt > 3:
                if poe.poe_a_volt > poe.poe_b_volt:
                    poe_status = "PoE 802.3af mode A ({}V)".format(poe.poe_a_volt)
                else:
                    poe_status = "PoE 802.3af mode B ({}V)".format(poe.poe_b_volt)
            elif sum(poe.pair_volts) > 3:
                poe_status = "passive PoE ({}v)".format(max(poe.pair_volts))

            GLib.idle_add(self.callback, True, "{} link established\n{}".format(link.speed, poe_status), [poe])

            client.get_link(speed=pockethernet.PHY_ADVERTIZE_100BASET)
            got_lease = False
            while not got_lease:
                result = client.wait_for_capture_results()
                if isinstance(result, DhcpResult):
                    got_lease = True
                    GLib.idle_add(self.callback, False, None, [result])
                if isinstance(result, CdpResult):
                    GLib.idle_add(self.callback, True, None, [result])
            return

        # Running PoE test after failed link because it might be a PoE injector without upstream
        GLib.idle_add(self.callback, True, "Running PoE test")
        poe = client.get_poe()

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        # Assume the cable is messed up and my software works for now :)
        GLib.idle_add(self.callback, False, "Miswire", [wiremap, tdr, link, poe])
        return
