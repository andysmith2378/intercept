import svgwrite


def sumOfSquares(x, y):
    return x * x + y * y


def squareDistance(px, py, ex, ey):
    tang = (ex * px + ey * py) / sumOfSquares(ex, ey)
    if tang > 1:
        tang = 1
    if tang < 0:
        tang = 0
    return sumOfSquares(ex * tang - px, ey * tang - py)


def get_pixel(offset, coord, size):
    return offset + coord * size


def get_text(number, pixelCoords):
    return svgwrite.text.Text(str(number + 1), pixelCoords,
        text_anchor="middle", dominant_baseline="middle")


if __name__ == "__main__":
    WIDTH_OF_RANGE_RULER_IN_SQUARES = 55 / 34
    PX_PER_SQUARE = 16
    BORDER = 1
    SPACING = 1.5
    MAX_RANGE = 13
    BLACK = "rgb(0, 0, 0)"

    margin = 2 * BORDER + 1
    halfWidth = WIDTH_OF_RANGE_RULER_IN_SQUARES / 2
    squareOfWidth = halfWidth * halfWidth
    maxRangePlusTwo = MAX_RANGE + 2
    height = PX_PER_SQUARE * maxRangePlusTwo * maxRangePlusTwo
    chart = svgwrite.Drawing("chart.svg", size=(height, height))
    throwRange = range(1, MAX_RANGE + 1)
    xOff = 0
    for ex in throwRange:
        columns = range(-BORDER, ex + BORDER + 1)
        yOff = 0
        for ey in throwRange:
            rows = range(-BORDER, ey + BORDER + 1)
            for px in columns:
                left, right = px + 0.5, px - 0.5
                pixelX = get_pixel(xOff, px, PX_PER_SQUARE)
                for py in rows:
                    up, down = py + 0.5, py - 0.5
                    pixelY = height - get_pixel(yOff, py, PX_PER_SQUARE)
                    if ((px == 0) and (py == 0)) or ((px == ex) and (py == ey)):
                        fillColour = BLACK
                    else:
                        if ((px < 0) or (py < 0) or (px > ex) or (py > ey) or
                                ((squareDistance(left, up, ex, ey) >= squareOfWidth) and
                                 (squareDistance(left, down, ex, ey) >= squareOfWidth) and
                                 (squareDistance(right, up, ex, ey) >= squareOfWidth) and
                                 (squareDistance(right, down, ex, ey) >= squareOfWidth))):
                            fillColour = "rgb(252, 247, 231)"
                        else:
                            fillColour = "rgb(173, 25, 2)"
                    square = svgwrite.shapes.Rect((pixelX, pixelY),
                                                  (PX_PER_SQUARE, PX_PER_SQUARE),
                                                  fill=fillColour,
                                                  stroke=BLACK,
                                                  stroke_width=1)
                    chart.add(square)
            [chart.add(get_text(rownum,
                                (get_pixel(xOff, -0.5, PX_PER_SQUARE),
                                 height - get_pixel(yOff, rownum + 0.5, PX_PER_SQUARE))))
                                 for rownum in range(-1, ey)]
            [chart.add(get_text(columnnum,
                                (get_pixel(xOff, columnnum + 1.5, PX_PER_SQUARE),
                                 height - get_pixel(yOff, -1.5, PX_PER_SQUARE))))
                                 for columnnum in range(-1, ex)]
            yOff += PX_PER_SQUARE * (ey + margin) * SPACING
        xOff += PX_PER_SQUARE * (ex + margin) * SPACING
    chart.save()

