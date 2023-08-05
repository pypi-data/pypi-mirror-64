import math


def draw_wiremap(connections, shorts, family, size, color):
    width = 300
    result = '<svg width="{}" height="{}">'.format(width, 9 * 16 + 5)

    colors = [
        '#000',
        '#F94',
        '#F90',
        '#4D4',
        '#08F',
        '#48F',
        '#0D0',
        '#975',
        '#850'
    ]

    font = 'font-family="{}" font-size="{}" fill="{}"'.format(family, size, color)

    for connection_from, connection_to in enumerate(connections):
        top = connection_from * 16 + 10.5
        pin_name = "S" if connection_from == 0 else connection_from
        result += '<text x="10.5" y="{}" {}>{}</text>'.format(top + 4, font, pin_name)
        result += '<text x="{}" y="{}" {}>{}</text>'.format(width - 16, top + 4, font, pin_name)

        d = 'M 20 {} h 32'.format(top)

        if connection_to is not None:
            target = connection_to * 16 + 10.5
            d = make_path(top, target, width)

        result += '<path d="{}" fill="transparent" stroke="{}" stroke-width="3" />'.format(d, colors[connection_from])

    for short_from, short_to in enumerate(shorts):
        top = short_from * 16 + 10.5
        if short_to is not None:
            target = short_to * 16 + 10.5

            d = 'M 52 {top} A {arc} {arc} 0 1 1 52 {target}'.format(top=top, arc=((target - top) / 2), target=target)
            result += '<path d="{}" fill="transparent" stroke="red" stroke-width="3" />'.format(d)

    return result + '</svg>'


def make_path(source_top, target_top, width):
    # Short circuit for straight wires
    if source_top == target_top:
        return 'M 20 {} L {} {}'.format(source_top, width - 20, target_top)

    # Simple bezier curve non-straight wires
    d = 'M 20 {}'.format(source_top)
    d += ' h 32'
    d += ' C {x1} {y1}, {x2} {y2}, {x} {y}'.format(x=(width - 20 - 32), y=target_top, x1=100, y1=source_top,
                                                   x2=(width - 100), y2=target_top)
    d += ' h 32'
    return d


def draw_wire(ctx, width, source_top, target_top):
    ctx.set_line_width(3)
    ctx.move_to(20, source_top)

    if target_top is None:
        ctx.line_to(32, source_top)
        ctx.stroke()
        return

    if source_top == target_top:
        ctx.line_to(width - 20, source_top)
        ctx.stroke()
        return

    bc1x = width / 3
    bc1y = source_top
    bc2x = width / 3 * 2
    bc2y = target_top
    ctx.curve_to(bc1x, bc1y, bc2x, bc2y, width - 20, target_top)
    ctx.stroke()


def draw_wiremap_cairo(ctx, width, height, connections, shorts, color):
    colors = [
        (0, 0, 0),
        (1, 0.6, 0.26),
        (1, 0.6, 0.26),
        (0.26, 0.86, 0.26),
        (0, 0.5, 1),
        (0, 0.5, 1),
        (0.26, 0.86, 0.26),
        (0.5, 0.33, 0),
        (0.5, 0.33, 0),
    ]

    for connection_from, connection_to in enumerate(connections):
        top = connection_from * 16 + 10.5
        pin_name = "S" if connection_from == 0 else connection_from
        ctx.set_source_rgba(color.red, color.green, color.blue)
        ctx.move_to(10, top + 4)
        ctx.show_text(str(pin_name))
        ctx.move_to(width - 16, top + 4)
        ctx.show_text(str(pin_name))

        target = None
        if connection_to is not None:
            target = connection_to * 16 + 10.5

        ctx.set_source_rgba(*colors[connection_from])
        ctx.set_dash([], 0)

        draw_wire(ctx, width, top, target)
        if connection_from % 2 == 1:
            ctx.set_source_rgba(1, 1, 1, 0.5)
            ctx.set_dash([4, 8], 0)
            draw_wire(ctx, width, top, target)

    for short_from, short_to in enumerate(shorts):
        top = short_from * 16 + 10.5
        if short_to is not None:
            target = short_to * 16 + 10.5

            ctx.set_source_rgba(1, 0, 0)
            ctx.set_dash([], 0)
            ctx.arc(32, (top + target) / 2, (target - top) / 2, -1 * math.pi / 2, math.pi / 2)
            ctx.stroke()


if __name__ == '__main__':
    connections = [None, 3, 6, 1, 4, 5, 2, 7, 8]
    shorts = [None, None, None, None, None, None, None, None, None]
    test = draw_wiremap(connections, shorts, "verdana", "11pt", "black")
    print(test)
