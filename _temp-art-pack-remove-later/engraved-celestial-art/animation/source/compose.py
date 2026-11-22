from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
from scipy.ndimage import gaussian_filter, binary_fill_holes, distance_transform_edt, label

work = Path(__file__).resolve().parent
pack = work.parents[1]
reference = Image.open(pack/'reference/original_engraving_reference.jpg').convert('RGB')
W,H = reference.size
inner = (109,94,914,708)
files = {p.stem:p for p in pack.glob('*/*.png')}

@lru_cache
def piece(name):
    im = Image.open(files[name]).convert('RGBA')
    arr = np.array(im,dtype=np.float32)
    rgb,alpha = arr[:,:,:3],arr[:,:,3]/255
    r,g,b = rgb.transpose(2,0,1)
    key = (name.startswith(('b0','b1','w1','w4','x')) and not name.startswith('b01')) or name=='sky_dome_wide'
    if key:
        # Account for the source files' near-magenta matte and its antialiasing.
        chroma = np.minimum(r,b)-g
        keyed = (chroma > 7) & (b >= .72*r)
        clean = np.clip((137-chroma)/123,0,1)
        alpha *= np.where(keyed,clean,1)
        solid = ~keyed
        _, iy = distance_transform_edt(~solid,return_indices=True)
        rgb[:] = np.where((keyed & (alpha>0))[:,:,None],rgb[iy[0],iy[1]],rgb)
        alpha = np.minimum(alpha*1.55,gaussian_filter(alpha,0.70))
    elif name in {'figure_no_cloak','cloak_held','w2_crescent_only','w3_hub'}:
        alpha = np.clip((alpha-.46)/.49,0,1)
    elif im.getextrema()[3][0] < 255:
        edge = (alpha > 0) & (alpha < .96)
        alpha = np.clip((alpha-.055)/.93,0,1)
        fringe = edge & (((r > 1.65*g) & (g > .85*b)) | ((r > 1.35*b) & (g > 1.35*b)))
        rgb[fringe] = .63*rgb[fringe]+.37*(rgb[fringe] @ np.array([.26,.56,.18]))[:,None]
    arr[:,:,3]=255*alpha
    out = Image.fromarray(np.clip(arr,0,255).astype('uint8'),'RGBA')
    return out.crop(out.getbbox())

def grade(im, saturation=1, light=1, tint=(1,1,1)):
    a = im.getchannel('A')
    out = ImageEnhance.Color(im.convert('RGB')).enhance(saturation)
    lut = [int(np.clip(x*light*t,0,255)) for t in tint for x in range(256)]
    out = out.point(lut).convert('RGBA')
    out.putalpha(a)
    return out

def sprite(name, x,y,w, h=None, sat=1, light=1, angle=0, tint=(1,1,1)):
    im = piece(name)
    if not h: h = round(w*im.height/im.width)
    im = grade(im.resize((w,h),Image.Resampling.LANCZOS),sat,light,tint)
    if angle: im = im.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    base = Image.new('RGBA',(W,H))
    base.alpha_composite(im,(x,y))
    return base

def draw(target,*args,**kwargs):
    target.alpha_composite(sprite(*args,**kwargs))

def masked(sprite, mask):
    sprite = sprite.copy()
    sprite.putalpha(Image.fromarray((np.asarray(sprite.getchannel('A'), dtype=np.float32)*np.asarray(mask)/255).astype('uint8')))
    return sprite

def main():
    dome = sprite('sky_dome',134,56,805,665,sat=.83,light=.90,tint=(.91,.99,1.065))
    domeAlpha = np.asarray(dome.getchannel('A'))
    boundary = []
    for y in range(H):
        hits = np.flatnonzero(domeAlpha[y]>95)
        boundary.append(hits[0] if len(hits) else 132)
    for y in range(65):
        boundary[y] = boundary[65]+(65-y)*1.8
    opening = Image.new('L',(W,H))
    ImageDraw.Draw(opening).polygon([(0,0), *[(int(x)+4,y) for y,x in enumerate(boundary)],(0,H-1)], fill=255)
    opening = opening.filter(ImageFilter.GaussianBlur(.56))
    print('dome coordinates',[(y,boundary[y]) for y in range(100,720,40)])
    daylight = sprite('sky_patch',100,65,840,515,sat=.67,light=.96,tint=(1.02,1.01,.98))
    draw(daylight,'ground_fill',105,341,817,370,sat=.78,light=.76)
    # Preserve the engraved daytime sky above the hill texture in the fill.
    sky = sprite('sky_patch',100,64,839,522,sat=.66,light=.95,tint=(1,1,1))
    sa = np.asarray(sky.getchannel('A')).copy()
    sa[515:] = sa[515:] * np.clip((548-np.arange(515,H))/33,0,1)[:,None]
    sky.putalpha(Image.fromarray(sa))
    daylight.alpha_composite(sky)
    draw(daylight,'sun_face',669,239,355,sat=.71,light=.92,tint=(1.02,1,.95))
    beyond = sprite('b01_night_sky',92,56,614,445,sat=.75,light=.96)
    haze = sprite('sky_patch',89,194,589,528,sat=.60,light=.64,tint=(.91,1,1.07))
    ha = np.asarray(haze.getchannel('A')).copy()
    ha[:] = ha * np.clip((np.arange(H)-209)/130,0,1)[:,None]
    haze.putalpha(Image.fromarray(ha))
    beyond.alpha_composite(haze)
    draw(beyond,'b06_light_band_2',84,100,552,sat=.62,light=.83)
    draw(beyond,'b03_sun_rays',307,-61,236,sat=.58,light=.80)
    draw(beyond,'b02_wheel',6,98,187,sat=.77,light=.88)
    draw(beyond,'b07_cloud_far',89,179,451,sat=.63,light=.93,angle=9)
    draw(beyond,'b04_rainbow',225,195,145,sat=.57,light=.86)
    draw(beyond,'b05_light_band_1',79,228,406,sat=.58,light=.82)
    draw(beyond,'b09_cloud_3',64,213,418,sat=.59,light=.77,angle=7)
    draw(beyond,'b08_cloud_2',51,282,381,sat=.63,light=.86,angle=12)
    draw(beyond,'b11_cloud_near',42,374,279,sat=.67,light=.83,angle=12)
    draw(beyond,'b10_cloud_4',43,496,229,sat=.54,light=.73,angle=20)
    daylight.alpha_composite(masked(beyond,opening))
    daylight.alpha_composite(dome)

    land = Image.new('RGBA',(W,H))
    draw(land,'landscape_foreground',103,520,819,195,sat=.79,light=.80,tint=(1,.993,1.01))
    draw(land,'village_horizon',253,508,680,88,sat=.68,light=.84)
    # Fade only the leftmost part of the hills into the oblique veil.
    land_alpha = np.asarray(land.getchannel('A')).copy()
    left = np.asarray(boundary)[:,None]
    land_alpha[:] = land_alpha * np.clip((np.arange(W)[None,:]-left+7)/10,0,1)
    land.putalpha(Image.fromarray(land_alpha))
    daylight.alpha_composite(land)
    draw(daylight,'tree',492,342,181,sat=.80,light=.85,tint=(1,1.02,.94))
    draw(daylight,'figure_with_cloak',135,478,394,sat=.78,light=.91,tint=(.99,.99,1))
    frame = reference.copy()
    frame.paste(daylight.crop(inner).convert('RGB'),inner[:2])
    frame.save('work/draft.webp',quality=93,method=6)
    return frame
if __name__=='__main__': main()
