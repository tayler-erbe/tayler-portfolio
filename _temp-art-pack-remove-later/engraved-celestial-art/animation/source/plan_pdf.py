"""Layer plan PDF: every layer alone and stacked, back to front, with what it is made from and how it moves."""
import json, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

here = Path(__file__).resolve().parent.parent
plan = here / 'build' / 'layer-plan'
groups = json.load(open(plan / 'groups.json'))
F = 'C:/Windows/Fonts/'
def font(name, size):
    return ImageFont.truetype(F + name, size)
H1, H2, BODY, SMALL, BOLD = font('georgiab.ttf', 44), font('georgiab.ttf', 30), font('georgia.ttf', 24), font('georgia.ttf', 20), font('georgiab.ttf', 22)
PW, PH, M = 1275, 1650, 70
INK, MUTE, BG = (34, 32, 40), (96, 92, 100), (250, 247, 240)


def page():
    im = Image.new('RGB', (PW, PH), BG)
    return im, ImageDraw.Draw(im)


def para(d, x, y, text, f=BODY, width=88, fill=INK, gap=8):
    for line in textwrap.wrap(text, width):
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + gap
    return y + 6


def fit(img, w, h):
    img = img.copy()
    img.thumbnail((w, h), Image.LANCZOS)
    return img


pages = []
# 1. Cover
im, d = page()
d.text((M, M), 'Opening scene: layer plan', font=H1, fill=INK)
y = para(d, M, M + 70, 'Why the last versions looked wrong: every version used your approved picture as the bottom layer and pasted moving pieces over it. The old sun rays, moon and stars were still printed underneath, so when the new pieces moved, the old ones showed behind them.', BODY)
y = para(d, M, y, 'This plan uses no picture underneath. Every element is its own clean paper piece, stacked from the back to the front, and nothing is painted twice. Your approved picture is only a guide for where each piece sits (and the source of the frame, which is the top layer).', BODY)
y = para(d, M, y, 'Left: your approved picture. Right: the same scene stacked from clean pieces only (still, no motion yet). Pages 3 onward show every layer alone and then added to the stack.', SMALL, fill=MUTE)
ap = fit(Image.open(here / 'current' / 'approved-portrait.webp').convert('RGB'), 540, 864)
full = fit(Image.open(plan / 'full.png'), 540, 864)
im.paste(ap, (M, y + 10)); im.paste(full, (PW - M - full.width, y + 10))
d.text((M, y + 20 + ap.height), 'Approved picture', font=SMALL, fill=MUTE)
d.text((PW - M - full.width, y + 20 + full.height), 'Built from clean layers', font=SMALL, fill=MUTE)
pages.append(im)

# 2. Table
im, d = page()
d.text((M, M), 'All layers, back to front', font=H1, fill=INK)
y = M + 75
d.text((M, y), '#', font=BOLD, fill=INK); d.text((M + 50, y), 'Layer', font=BOLD, fill=INK); d.text((M + 430, y), 'How it moves', font=BOLD, fill=INK)
y += 38
for i, (title, n, made, motion, status) in enumerate(groups, 1):
    d.line((M, y - 6, PW - M, y - 6), fill=(214, 208, 196))
    d.text((M, y), str(i), font=SMALL, fill=INK)
    y1 = para(d, M + 50, y, f'{title} ({n} piece{"s" if n != 1 else ""})', SMALL, width=30, gap=4)
    y2 = para(d, M + 430, y, motion, SMALL, width=62, gap=4)
    if status.startswith('Draft'):
        y2 = para(d, M + 430, y2 - 4, 'DRAFT PIECE: ' + status.split(':', 1)[1].strip(), SMALL, width=62, fill=(150, 60, 50), gap=4)
    y = max(y1, y2) + 6
pages.append(im)

# 3+. One page per layer
for i, (title, n, made, motion, status) in enumerate(groups, 1):
    im, d = page()
    d.text((M, M), f'Layer {i} of {len(groups)}: {title}', font=H2, fill=INK)
    y = M + 55
    y = para(d, M, y, 'Made from: ' + made, BODY, width=90)
    y = para(d, M, y, 'Moves: ' + motion, BODY, width=90)
    y = para(d, M, y, 'Status: ' + status, BODY, width=90, fill=(150, 60, 50) if status.startswith('Draft') else (40, 110, 60))
    w, h = 540, 864
    a = fit(Image.open(plan / f'{i:02d}-alone.png'), w, min(h, PH - y - 90))
    s = fit(Image.open(plan / f'{i:02d}-stack.png'), w, min(h, PH - y - 90))
    im.paste(a, (M, y + 10)); im.paste(s, (PW - M - s.width, y + 10))
    d.text((M, y + 18 + a.height), 'This layer alone (checks show where it is see-through)', font=SMALL, fill=MUTE)
    d.text((PW - M - s.width, y + 18 + s.height), f'Layers 1 to {i} stacked', font=SMALL, fill=MUTE)
    pages.append(im)

# Last: decisions
im, d = page()
d.text((M, M), 'Before I build the motion', font=H1, fill=INK)
y = M + 80
y = para(d, M, y, '1. Please check the order and the movement of each layer (page 2). Tell me anything you want moved, added, removed or animated differently.', BODY)
y = para(d, M, y, '2. The traveler, the hills and village, and the fields are now drawn from your approved picture, so they keep its pen-and-ink lines and coloured-pencil colour.', BODY)
y = para(d, M, y, '3. Four layers still read as digital next to them: the sky (made in code), the stars (her bright star pieces, glossier than your engraved ones), the clouds inside the sky, and the tree. I recommend drawing these four from your approved picture the same way: about $0.06 each, about $0.25 in total (art budget: $1.61 left of $10).', BODY)
y = para(d, M, y, '4. Every piece now casts a small soft shadow on the layer behind it and the whole picture has a paper grain, so it reads as cut paper.', BODY)
y = para(d, M, y, '5. Once you approve, I build the moving version from exactly these layers (nine poses a second, as before) and send the HTML and the GIF together.', BODY)
pages.append(im)

out = Path(sys.argv[1])
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=150)
print('pages', len(pages), out)
