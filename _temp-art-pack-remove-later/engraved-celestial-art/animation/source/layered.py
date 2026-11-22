"""Layered rebuild: every element is its own clean paper piece, stacked back to front.
Nothing from the approved portrait is used as a backdrop. The approved portrait is only a
placement and colour reference (and the source of the outer frame, which is the top layer).

  python source/layered.py plan    -> build/layer-plan/ (each group alone + cumulative) and the PDF
"""
from math import hypot, pi
from random import Random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import label, binary_closing, binary_dilation, binary_fill_holes, gaussian_filter

import paper_scene as rig
from paper_scene import add, center, source, resized, alpha_mask, stock, grade, piece, render, W, H, RESAMPLE
import paper_approved as PA
from paper_approved import approved, window, polygon_mask, lean, edge, find_stars

layers = rig.layers
assets = rig.assets
work = PA.work
groups = []          # (title, start, end, made_from, motion, status)

# The reveal (behind the veil) runs down the left side to below the traveler's head.
reveal = [(25, 24), *[(x - 1, y) for x, y in edge], (70, 640), (40, 700), (26, 760)]
rig.reveal = reveal
rig.veil = [(0, 0), (W, 0), (W, H), (0, H)]


def group(title, made_from, motion, status):
    def deco(fn):
        start = len(layers)
        fn()
        groups.append((title, start, len(layers), made_from, motion, status))
    return deco


def sky_gradient():
    """Night navy at the top left, warming to cream around the sun and along the right horizon,
    with an engraved diagonal hatch and stipple in the transition."""
    yy, xx = np.indices((H, W), dtype=np.float32)
    d = np.hypot(xx - 525, (yy - 468) * .92)
    glow = np.clip(1 - (d - 95) / 270, 0, 1) ** 1.25
    horizon = np.clip((yy - 470) / 150, 0, 1) * np.clip((xx - 280) / 170, 0, 1) * np.clip((660 - yy) / 40, 0, 1)
    L = np.clip(np.maximum(glow, horizon * .95), 0, 1)
    navy, slate, cream = np.array([22, 39, 57.]), np.array([86, 104, 113.]), np.array([231, 212, 170.])
    a = np.clip(L / .45, 0, 1)[..., None]
    b = np.clip((L - .45) / .55, 0, 1)[..., None]
    rgb = navy * (1 - a) + slate * a
    rgb = rgb * (1 - b) + cream * b
    # engraved texture: the night-sky engraving's own hatching, used as light and shade
    tex = np.asarray(resized(piece('b01_night_sky'), W, H).convert('L'), dtype=np.float32)
    tex = (tex - gaussian_filter(tex, 6)) / 40
    lum = 1 + np.clip(tex, -1.2, 1.2)[..., None] * (.50 - .34 * b)
    rgb = rgb * lum
    # engraver's strokes: short pale dashes running up to the right, thicker where the sky is dark
    from scipy.ndimage import convolve
    rng0 = np.random.default_rng(11)
    k = np.zeros((9, 9), np.float32)
    for i in range(9):
        k[8 - i, i] = 1
    streak = convolve((rng0.random((H, W)) < .028).astype(np.float32), k)
    streak = np.clip(streak, 0, 1) * (1 - b[..., 0])
    rgb = rgb + streak[..., None] * np.array([30, 40, 46.])
    # stipple in the blue-to-cream transition, like the approved plate
    rng = np.random.default_rng(5)
    dots = (rng.random((H, W)) < (.16 * np.exp(-((L - .48) / .18) ** 2)))
    rgb[dots] = rgb[dots] * .55
    paper = Image.fromarray(np.clip(rgb, 0, 255).astype('uint8')).convert('RGBA')
    return paper


def veil_rim():
    """The rolled edge of the lifted veil, drawn along the approved edge, ending at the hand."""
    s = 3
    im = Image.new('RGBA', (W * s, H * s))
    d = ImageDraw.Draw(im)
    pts = [(x * s, y * s) for x, y in edge]
    d.line(pts, fill=(9, 16, 38, 255), width=7 * s, joint='curve')
    d.line([(x + 4.5 * s, y + 1 * s) for x, y in pts], fill=(92, 112, 158, 235), width=2 * s, joint='curve')
    d.line([(x + 8 * s, y + 1.5 * s) for x, y in pts], fill=(30, 45, 86, 200), width=1 * s, joint='curve')
    return im.resize((W, H), RESAMPLE)


def star_positions():
    """Centre and size of every star in the approved portrait (big ones included)."""
    rgb = np.asarray(approved.convert('RGB'), dtype=np.int16)
    r, g, b = rgb.transpose(2, 0, 1)
    yy, xx = np.indices((H, W))
    allowed = np.asarray(polygon_mask([*[(x + 13, y) for x, y in edge[:26]], (97, 565), (140, 567), (184, 533),
        (223, 484), (280, 439), (316, 383), (403, 326), (480, 296), (570, 271), (570, 27)])) > 0
    moon = ((xx - 447) / 82) ** 2 + ((yy - 130) / 82) ** 2 < 1
    bright = (r - b > 34) & (g - b > 18) & (r > 150) & allowed & ~moon
    comps, n = label(bright, np.ones((3, 3), dtype=int))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(comps == i)
        if not 6 <= len(xs) <= 1200:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if not (3 <= w <= 48 and 3 <= h <= 48):
            continue
        out.append(((xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2, max(w, h)))
    return out


def split_tree():
    """Her tree as a paper armature: the trunk and branches, plus separate leaf clumps.
    Each clump takes its own leaves and the twigs inside it, so nothing is left behind when it rocks."""
    tree = resized(piece('tree'), 250)
    a = np.asarray(tree, dtype=np.int16)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    leaf = (al > 100) & (g >= r - 4) & (g > b + 18)
    leaf = binary_closing(leaf, iterations=3)
    leaf = binary_fill_holes(leaf)
    comps, n = label(binary_dilation(leaf, iterations=2))
    pieces = []
    for i in range(1, n + 1):
        m = (comps == i) & (al > 20)
        if m.sum() < 220:
            continue
        pieces.append(m)
    taken = np.zeros_like(leaf)
    clumps = []
    for m in pieces:
        taken |= m
        ys, xs = np.where(m)
        l, t, rr, bb = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        cut = Image.fromarray(np.where(m[..., None], a, 0).astype('uint8'), 'RGBA').crop((l, t, rr, bb))
        clumps.append((cut, (l, t, rr, bb)))
    trunk = Image.fromarray(np.where(taken[..., None], 0, a).astype('uint8'), 'RGBA')
    return tree, trunk, clumps


def split_daisy(name, w):
    """A flower as two pieces: the stem and leaves (still), and the round head (turns)."""
    im = resized(piece(name), w)
    a = np.asarray(im, dtype=np.int16)
    pink = (a[..., 3] > 100) & (a[..., 0] - a[..., 1] > 40) & (a[..., 0] > 140)
    ys, xs = np.where(pink)
    cx, cy = xs.mean(), ys.mean()
    rad = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 * 1.08
    disc = Image.new('L', im.size)
    ImageDraw.Draw(disc).ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=255)
    head = window(im, disc).crop((round(cx - rad) - 1, round(cy - rad) - 1, round(cx + rad) + 2, round(cy + rad) + 2))
    stem = window(im, Image.eval(disc, lambda v: 255 - v))
    return stem, head, (cx, cy)


def build():
    @group('Sky', 'Made in code: a painted gradient from night navy to warm cream around the sun, with an engraved hatch and stipple.',
           'Still.', 'Ready')
    def _():
        add('sky', sky_gradient(), 0, 0)

    @group('Behind the veil: backdrop', 'Made in code from the clean night-sky and pale-sky engravings. Shown only where the veil is lifted.',
           'Still.', 'Ready')
    def _():
        gap = Image.new('RGBA', (W, H), '#51656e')
        night = source('b01_night_sky', 565, 440, .72, .95)
        aa = np.asarray(night.getchannel('A'), dtype=np.float32).copy()
        aa *= np.clip((387 - np.arange(night.height)) / 213, 0, 1)[:, None]
        night.putalpha(Image.fromarray(aa.astype('uint8')))
        gap.alpha_composite(source('sky_patch', 459, 620, .63, .73), (0, 164))
        gap.alpha_composite(night, (0, 0))
        add('behind the veil backdrop', window(gap, polygon_mask(reveal, .4)), 0, 0)

    def sheet(key, name, x, y, w, angle, dx, dy, period, sat=.72, light=.86):
        center(key, lean(source(name, w, sat=sat, light=light), angle), x, y, slide=[dx, dy, period, 0], clip='reveal')

    def bank(key, name, x, y, w, angle, dx, dy, period, sat=.74, light=.98):
        im = grade(resized(piece(name), w), sat, light, (1, .985, .95))
        center(key, lean(im, angle), x, y, slide=[dx, dy, period, 0], clip='reveal')

    @group('Behind the veil: far layers', 'Existing clean pieces: a far sun disc, two patterned ribbons, a far cloud bank and a small ringed planet.',
           'Each sheet slides a few pixels on its own slow cycle, alternating directions. The disc and the planet turn slowly.', 'Ready')
    def _():
        sheet('high silver pattern', 'b05_light_band_1', 159, 64, 313, 0, -4, 2, 22, .66, .77)
        bank('far bank behind the gears', 'bank_1', 226, 98, 420, 8, 8, -2, 19, .66, .95)
        sheet('gold patterned sheet', 'b06_light_band_2', 165, 120, 395, 4, -10, 4, 17, .69, .90)
        disc = lean(source('b03_sun_rays', 181, sat=.69, light=.83), -3)
        center('far solar disc', disc, 247, -2, spin=3.0, clip='reveal')
        ringed = stock('x4_planets', (550, 314), (0, 4, 222, 148), 25, .86)
        center('far ringed planet', ringed, 236, 128, spin=-2.6, slide=[4, 1, 29, 0], clip='reveal')

    @group('Behind the veil: the clockwork', 'Existing clean pieces: the large brass gear, the blue spoked wheel, its cream crescent, the hub and the upper gear.',
           'Each turns on its own pivot at its own speed: the wheel one way, the crescent and hub the other, the upper gear meshing against the big gear.', 'Ready')
    def _():
        def clock_gear(box, w):
            g = stock('w4_gears', (550, 420), box, w, .84)
            return alpha_mask(g, (1, 1, g.width - 2, g.height - 2), 'ellipse', .6)
        center('upper meshing gear', lean(clock_gear((336, 11, 550, 230), 103), -9), 155, 73, spin=-5.4, clip='reveal')
        center('main brass gear', lean(clock_gear((0, 0, 395, 398), 230), 186), 20.6, 141, spin=2.82, clip='reveal')
        center('blue wheel spokes', source('w1_wheel_only', 200, sat=.73, light=.88), 20.6, 141, spin=2.82, clip='reveal')
        add('wheel crescent', source('w2_crescent_only', 72, 190, sat=.73, light=.91), 20.6, 141, (3, 95), spin=-1.9, clip='reveal')
        center('wheel hub', source('w3_hub', 34, sat=.75, light=.84), 20.6, 141, spin=-3.9, clip='reveal')

    @group('Behind the veil: banks, ribbons and planets', 'Existing clean pieces: the rainbow, five broad cloud banks, three engraved ribbons, the zigzag band and two small planets tucked between them.',
           'Every sheet slides on its own cycle; nearer sheets travel farther and faster, neighbours in opposite directions. Planets turn.', 'Ready')
    def _():
        sheet('rainbow disc', 'b04_rainbow', 152, 186, 112, 0, 6, -2, 16, .77, .93)
        bank('broad bank over the rainbow', 'bank_3', 104, 236, 600, 9, -10, 4, 14)
        sheet('first engraved ribbon', 'b05_light_band_1', 112, 300, 330, 8, -15, 4, 14, .55, .84)
        blue = stock('x4_planets', (550, 314), (268, 180, 397, 307), 15, .89)
        center('middle blue planet', blue, 152, 276, spin=3.7, slide=[-4, 2, 22, 0], clip='reveal')
        bank('second broad bank', 'bank_2', 60, 350, 560, 10, 15, -6, 11)
        sheet('second engraved ribbon', 'b06_light_band_2', 70, 402, 285, 10, 19, -8, 13, .55, .86)
        sheet('lower zigzag pattern', 'b12_zigzag_glow', 72, 424, 230, 11, 19, -8, 11, .66, .92)
        red = stock('x4_planets', (550, 314), (408, 10, 531, 139), 14, .82)
        center('near rust planet', red, 60, 436, spin=-4.4, slide=[4, -3, 19, 0], clip='reveal')
        bank('third bank over the pattern', 'bank_4', 30, 500, 540, 12, -17, 8, 10)
        sheet('third engraved ribbon', 'b05_light_band_1', 40, 530, 250, 12, 13, -6, 12, .55, .84)
        bank('near bank', 'bank_5', 10, 566, 500, 13, 17, -8, 8)
        bank('lowest bank by the hand', 'bank_3', 0, 640, 440, 16, -10, 6, 9)

    @group('Edge of the veil', 'Made in code: the rolled edge of the lifted sky, drawn along the approved curve down to the hand.',
           'Still.', 'Ready')
    def _():
        add('veil rim', veil_rim(), 0, 0)

    @group('Stars', 'Existing clean star pieces (her eight engraved stars), one per star, placed at the positions and sizes of the stars in the approved portrait.',
           'A third spin (each at its own speed and direction), a third swell and shrink by about a fifth, a third rock back and forth.', 'Ready')
    def _():
        rng = Random(31)
        art = [grade(piece(f'star_{i:02d}'), .82, .95) for i in range(1, 9)]
        for i, (cx, cy, size) in enumerate(star_positions()):
            im = resized(rng.choice(art), max(12, round(size * 1.55 + 5)))
            key = f'clean star {i + 1:02d}'
            spin = rng.choice([-1, 1]) * rng.uniform(40, 170)
            if i % 3 == 0:
                center(key, im, cx, cy, pulse=[.20, 1.6 + (i % 5) * .45, i * 1.3])
            elif i % 3 == 1:
                center(key, im, cx, cy, spin=spin)
            else:
                center(key, im, cx, cy, sway=[22 if spin > 0 else -22, 1.2 + (i % 7) * .35, i * .9])

    @group('Moon', 'Her clean crescent piece, turned and sized to sit where the approved moon sits.',
           'Rocks gently back and forth and drifts a few pixels (as you liked it).', 'Ready')
    def _():
        moon = grade(piece('moon_crescent'), .78, .97)
        moon = lean(resized(moon, 135), 4)
        center('moon', moon, 447.4, 131.7, sway=[5.5, 6.2, 0], slide=[5, -2, 8.5, 0])

    @group('Sun', 'Her clean sun piece for the rays (with the centre cut away), and the six drawn faces for the eyes.',
           'The rays turn slowly around the face. The face steps through its cels: eyes to the left, back, to the right, back, then the lids close for about two seconds. (Unchanged, as you liked it.)', 'Ready')
    def _():
        rays = grade(resized(piece('sun_face'), 345), .72, .97, (1.0, .955, .84))
        pivot = (round(rays.width * .499), round(rays.height * .484))
        hole = Image.new('L', rays.size, 255)
        ImageDraw.Draw(hole).ellipse((pivot[0] - 58, pivot[1] - 58, pivot[0] + 58, pivot[1] + 58), fill=0)
        rays.putalpha(Image.fromarray(np.minimum(np.asarray(rays.getchannel('A')), np.asarray(hole))))
        sx, sy = 518, 449
        add('sun rays', rays, sx, sy, pivot, spin=4.4)
        ref = alpha_mask(approved.crop((sx - 62, sy - 62, sx + 62, sy + 62)), (0, 0, 123, 123), 'ellipse', .8)
        want = np.asarray(ref.convert('RGB'), dtype=np.float32)[np.asarray(ref.getchannel('A')) > 200].mean(0)

        def cel(name):
            im = resized(piece(name), 124, 124)
            got = np.asarray(im.convert('RGB'), dtype=np.float32)[np.asarray(im.getchannel('A')) > 200].mean(0)
            return alpha_mask(grade(im, .86, 1, tuple(want / got)), (0, 0, 123, 123), 'ellipse', .8)
        names = {'face ahead': 'eyes_ahead', 'face left': 'eyes_left', 'face far left': 'eyes_far_left',
                 'face far right': 'eyes_far_right', 'face lids lowering': 'eyes_half', 'face eyes closed': 'eyes_closed'}
        for k, n in names.items():
            assets[k] = cel(n)
        C, L1, L2, R2, HALF, SHUT = 'face ahead', 'face left', 'face far left', 'face far right', 'face lids lowering', 'face eyes closed'
        order = [C, C, C, L1, L1, L2, L2, L2, L2, L1, L1, C, C, C, R2, R2, R2, R2, C, C, C, HALF, SHUT, SHUT, SHUT, SHUT, SHUT, HALF]
        center('face ahead', assets['face ahead'], sx, sy, cels=order, hold=4 / 9)

    @group('Clouds inside the sky', 'Clean cloud pieces with full outlines (no cut edges): one above the sun, one long bank to the left of the tree, one small one to the right.',
           'Each rocks a degree or two on a pin and shifts a few pixels, on different cycles.', 'Ready')
    def _():
        c1 = grade(resized(piece('cloud_layer_1'), 215), .62, .93)
        center('cloud above the sun', c1, 486, 298, sway=[1.7, 5.0, 0], slide=[4, 1, 5.0, 0])
        c2 = grade(resized(piece('b10_cloud_4'), 270), .62, .97)
        center('cloud left of the tree', c2, 318, 592, sway=[-1.5, 6.2, .8], slide=[-4, 1, 6.2, .8])
        c3 = grade(resized(piece('b07_cloud_far'), 150), .62, .97)
        center('cloud right of the tree', c3, 470, 612, sway=[1.6, 4.4, 2.0], slide=[3, -1, 4.4, 2.0])

    @group('Distant hills and village', 'Drawn from your approved picture as one cut-out strip: the grey-violet hills, the village with its spire, the hedgerows.',
           'Still.', 'Ready (redrawn from your approved picture).')
    def _():
        land = resized(piece('ap_hills_village'), 560)
        add('hills and village', land, 22, 606)

    @group('Ground and fields', 'Drawn from your approved picture: the striped fields and hedgerows coming forward to dark earth and grass.',
           'Still.', 'Ready (redrawn from your approved picture).')
    def _():
        f = piece('ap_fields')
        f = f.crop((0, round(f.height * .30), f.width, f.height))
        add('fields', resized(f, 572, 262), 14, 712)

    tree, trunk, clumps = split_tree()
    tx, ty = 348 - tree.width / 2, 778 - tree.height

    @group('Tree: trunk and branches', 'Her clean tree piece with the leaf clumps lifted off it, so the trunk and branches are a separate paper armature.',
           'Still.', 'Ready (her tree is close to the approved one but a little narrower).')
    def _():
        add('tree trunk', trunk, tx, ty)

    @group('Tree: leaf clumps', f'{len(clumps)} leaf clumps cut from the same tree, each with the twigs inside it.',
           'Each clump rocks a few degrees about the point where it joins its branch, on its own cycle.', 'Ready')
    def _():
        mid = tree.width / 2
        for i, (cut, (l, t, r, b)) in enumerate(clumps):
            px = (l + r) / 2 * .55 + mid * .45
            py = t + (b - t) * .78
            add(f'leaf clump {i + 1}', cut, tx + px, ty + py, (px - l, py - t), sway=[(3.4 + i % 3) * (-1) ** i, 4.6 + (i % 4) * .9, i * .7])

    @group('Grass and ferns', 'Clean paper pieces drawn earlier from your picture: six grass tufts and four ferns.',
           'Each blade group rocks from its root, quick and small, like a paper flap.', 'Ready')
    def _():
        spots = [('pc_bit_1', 300, 930, 70), ('pc_bit_3', 395, 925, 72), ('pc_bit_2', 470, 918, 60), ('pc_bit_5', 560, 905, 50),
                 ('pc_bit_7', 520, 880, 95), ('pc_bit_9', 385, 880, 100), ('pc_bit_8', 455, 870, 90), ('pc_bit_10', 560, 790, 80),
                 ('pc_bit_4', 270, 905, 66), ('pc_bit_6', 440, 800, 60)]
        for i, (n, x, y, w) in enumerate(spots):
            im = grade(resized(piece(n), round(w * 1.35)), .80, .86)
            add(f'grass {i + 1}', im, x, y, (im.width / 2, im.height * .96), sway=[(5 + i % 3) * (-1) ** i, 2.4 + (i % 4) * .6, i * .8])

    flowers = [('pc_bit_11', 515, 840, 122), ('pc_bit_13', 560, 860, 96), ('pc_bit_12', 425, 925, 124), ('pc_bit_14', 330, 930, 84)]

    @group('Flowers', 'Four clean daisy pieces, each split into a still stem and a separate round flower head.',
           'The stems stay still; each flower head turns slowly on its centre (different speeds and directions).', 'Ready')
    def _():
        for i, (n, x, y, w) in enumerate(flowers):
            stem, head, (cx, cy) = split_daisy(n, w)
            sim = grade(stem, .86, .9)
            add(f'flower stem {i + 1}', sim, x, y, (stem.width / 2, stem.height * .96))
            hx = x - stem.width / 2 + cx
            hy = y - stem.height * .96 + cy
            center(f'flower head {i + 1}', grade(head, .86, .92), hx, hy, spin=(7 + 3 * i) * (-1) ** i)

    @group('Rocks', 'Her clean rocks piece along the bottom left.', 'Still.', 'Ready')
    def _():
        add('rocks', grade(resized(piece('rocks'), 420), .70, .82), 20, 858)

    @group('The traveler', 'Drawn from your approved picture: the kneeling traveler, his hand gripping the small gathered fold of the starry veil, which hangs behind him to the ground.',
           'Still (he does not move).', 'Ready (redrawn from your approved picture).')
    def _():
        man = resized(piece('ap_traveler'), 350)
        a = np.asarray(man.getchannel('A')) > 128
        ys, xs = np.where(a)
        top = ys.min()
        hx = xs[ys < top + 6].mean()
        add('traveler', man, 82 - hx, 568 - top)

    @group('Paper grain', 'Made in code: a faint paper and pencil grain over the whole picture, so every piece reads as the same sheet of paper.',
           'Still.', 'Ready')
    def _():
        add('paper grain', paper_grain(), 0, 0)

    @group('Frame', 'The engraved frame from the approved portrait, with its inside fully cut away. It is the top layer and nothing shows outside it.',
           'Still.', 'Ready')
    def _():
        m = Image.new('L', (W, H), 255)
        ImageDraw.Draw(m).rectangle((28, 26, 573, 934), fill=0)
        add('frame', window(approved, m), 0, 0)


FLAT = {'sky', 'behind the veil backdrop', 'veil rim', 'frame', 'paper grain'}


def paper_shadows(pad=4, dx=1.6, dy=2.4, blur=1.3, strength=.42):
    """Bake a small offset shadow under every cut piece, like card lifted a millimetre off the one behind."""
    done = {}
    for row in layers:
        if row['key'] in FLAT:
            continue
        keys = [row['key']] + ([row['variant']] if row.get('variant') else []) + list(row.get('cels') or [])
        for k in dict.fromkeys(keys):
            if k in done:
                continue
            im = assets[k]
            canvas = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad))
            sh = Image.new('RGBA', canvas.size)
            a = Image.new('L', canvas.size)
            a.paste(im.getchannel('A'), (pad + round(dx), pad + round(dy)))
            a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * strength))
            sh.paste((12, 10, 16, 255), (0, 0), a)
            canvas.alpha_composite(sh)
            canvas.alpha_composite(im, (pad, pad))
            assets[k] = canvas
            done[k] = True
        px, py = row['pivot']
        row['pivot'] = [px + pad, py + pad]


def paper_grain():
    rng = np.random.default_rng(8)
    n = gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), .7)
    fib = gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), (0.6, 5))
    v = np.clip(.55 * n + .45 * fib, -3, 3)
    a = np.clip(np.abs(v) * 14, 0, 40).astype('uint8')
    rgb = np.where(v[..., None] > 0, np.array([255, 248, 230]), np.array([40, 30, 20])).astype('uint8')
    im = Image.fromarray(np.dstack([rgb, a]), 'RGBA')
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle((28, 26, 573, 934), fill=255)
    return window(im, m)


def render_rows(rows, t=0.0):
    keep = list(layers)
    layers[:] = rows
    try:
        return render(t)
    finally:
        layers[:] = keep


def checker(size, n=12):
    im = Image.new('RGB', size, (205, 205, 205))
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], n):
        for x in range(0, size[0], n):
            if (x // n + y // n) % 2:
                d.rectangle((x, y, x + n - 1, y + n - 1), fill=(235, 235, 235))
    return im


if __name__ == '__main__':
    import sys
    build()
    paper_shadows()
    out = work / 'layer-plan'
    out.mkdir(parents=True, exist_ok=True)
    for i, (title, s, e, *_r) in enumerate(groups, 1):
        alone = render_rows(layers[s:e])
        bg = checker(alone.size)
        bg.paste(alone, (0, 0), alone)
        bg.save(out / f'{i:02d}-alone.png')
        render_rows(layers[:e]).convert('RGB').save(out / f'{i:02d}-stack.png')
    render(0).convert('RGB').save(out / 'full.png')
    for t in (1.5, 3.0):
        render(t).convert('RGB').save(out / f'full-{t}.png')
    import json
    json.dump([(t, e - s, mf, mo, st) for t, s, e, mf, mo, st in groups], open(out / 'groups.json', 'w'), indent=1)
    print(len(groups), 'groups,', len(layers), 'pieces')
