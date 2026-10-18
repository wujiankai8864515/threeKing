"""Move the existing RGBA skill-panel group without changing the vertical frame rim.

Coordinates are native 1024x1536 frame coordinates. Text must use the same dy.
Example: python move_passive_panels.py gold-empty-generated-1024.png out.png --dy -258
The default rectangle is specific to the current four-frame master.
"""
from PIL import Image
from pathlib import Path
import argparse


def move_passive_panels(frame, dy, box=(660, 915, 939, 1170)):
    im = frame.convert('RGBA')
    x0, y0, x1, y1 = box
    if not (0 <= y0 + dy < y1 + dy <= im.height):
        raise ValueError('Moved panel group would leave the image')
    panel = im.crop(box)
    cleared = im.copy()
    cleared.paste((0, 0, 0, 0), box)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(panel, (x0, y0 + dy))
    return Image.alpha_composite(cleared, layer), cleared, layer


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source')
    p.add_argument('output')
    p.add_argument('--dy', type=int, required=True)
    a = p.parse_args()
    out, cleared, layer = move_passive_panels(Image.open(a.source), a.dy)
    out.save(a.output)
    q = Path(a.output)
    cleared.save(q.with_name(q.stem + '-without-panels.png'))
    layer.save(q.with_name(q.stem + '-panels-layer.png'))
