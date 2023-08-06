import cairo
from pockethernet import WiremapResult

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf

import wiremapper.wiremap as wiremap_draw
from wiremapper.block.block import Block


class WiremapBlock(Block):
    def make(self, result):
        if not isinstance(result, WiremapResult):
            return

        image = Gtk.DrawingArea()
        image.set_size_request(200, 150)
        image.connections = result.connections
        image.shorts = result.shorts
        image.connect("draw", self.expose_wiremap)

        frame = Gtk.Frame()
        self._add_class(frame, 'view')
        aligner = Gtk.Alignment()
        aligner.set_padding(12, 12, 12, 12)
        aligner.add(image)
        frame.add(aligner)

        return self._make_result("Wiremap", frame)

    def expose_wiremap(self, widget, ctx):
        style = widget.get_style_context()
        state = Gtk.StateFlags(1)
        font = style.get_font(state)
        font_color = style.get_color(state)

        ctx.set_font_size(font.get_size() / 1024)
        ctx.select_font_face(font.get_family(), cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        size = widget.get_allocation()
        wiremap_draw.draw_wiremap_cairo(ctx, width=size.width, height=size.height, connections=widget.connections,
                                        shorts=widget.shorts, color=font_color)
