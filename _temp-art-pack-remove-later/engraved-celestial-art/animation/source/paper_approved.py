from pathlib import Path
from math import hypot, sin, pi
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from scipy.ndimage import label, gaussian_filter, binary_dilation, map_coordinates
import numpy as np
from random import Random
import paper_scene as rig
from paper_scene import add, center, source, resized, alpha_mask, stock, crop_grid, grade, piece, render, W, H, RESAMPLE

work=Path(__file__).resolve().parent.parent/'build'
approved=Image.open(work.parent/'current/approved-portrait.webp').convert('RGBA').resize((W,H),RESAMPLE)
assets=rig.assets
layers=rig.layers
edge=[(355,25),(333,47),(312,68),(288,90),(265,114),(246,136),(230,156),
      (211,179),(195,202),(177,225),(161,250),(147,275),(134,300),(121,325),
      (110,346),(101,368),(92,393),(84,420),(78,444),(72,466),(67,489),
      (65,514),(65,532),(67,548),(72,569),(79,576)]
reveal=[(25,24),*[(x-1,y) for x,y in edge],(69,594),(55,609),(44,622),(26,630)]
# Clip at the actual overlapping cloud, tree and ridgeline edges in the approved portrait.
solar=[(577,285),(565,290),(535,306),(512,317),(480,329),(450,343),(432,355),
       (423,359),(415,372),(414,384),(423,399),(433,403),(438,414),(431,425),
       (437,439),(423,449),(425,462),(432,475),(439,486),(445,501),(426,505),
       (413,519),(395,528),(385,548),(386,561),(397,574),(419,573),(435,585),
       (443,598),(441,615),(466,625),(486,626),(501,622),(520,619),(541,619),(577,632)]
rig.reveal=reveal
rig.veil=solar

def polygon_mask(points,blur=0):
    m=Image.new('L',(W,H))
    ImageDraw.Draw(m).polygon(points,fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m

def window(im, mask):
    result=im.copy()
    result.putalpha(Image.fromarray((np.asarray(result.getchannel('A'),dtype=np.float32)*np.asarray(mask)/255).astype('uint8')))
    return result

def lean(im,angle=0):
    return im.rotate(angle,Image.Resampling.BICUBIC,expand=True) if angle else im

def find_stars(plate):
    rgb=np.asarray(plate.convert('RGB'),dtype=np.int16)
    r,g,b=rgb.transpose(2,0,1)
    allowed=polygon_mask([*[(x+13,y) for x,y in edge[:26]],(97,565),(140,567),(184,533),
        (223,484),(280,439),(316,383),(403,326),(480,296),(570,271),(570,27)])
    yy,xx=np.indices((H,W))
    exclude=((xx-472)/66)**2+((yy-95)/66)**2<1
    bright=(r-b>34)&(g-b>18)&(r>150)&(np.asarray(allowed)>0)&~exclude
    components,n=label(bright,np.ones((3,3),dtype=int))
    specs=[]
    clean=plate.copy()
    rng=Random(102)
    for i in range(1,n+1):
        ys,xs=np.where(components==i)
        if not 6<=len(xs)<=220: continue
        x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
        if not (3<=x1-x0<=25 and 3<=y1-y0<=25): continue
        cx,cy=(x0+x1)/2,(y0+y1)/2
        bounds=(x0-2,y0-2,x1+2,y1+2)
        l,t,r,b=bounds
        mask=binary_dilation(components[t:b,l:r]==i,iterations=1)
        mask=Image.fromarray(np.uint8(gaussian_filter(mask.astype(np.float32),.45)*255))
        cut=window(plate.crop(bounds),mask)
        donor=None
        for dx,dy in [(16,0),(-16,0),(0,-16),(13,-13),(-13,-13),(0,17),(25,8),(-20,20),(19,-16),(-21,-10)]:
            if not (18<l+dx<r+dx<575 and 25<t+dy<b+dy<608): continue
            colors=rgb[t+dy:b+dy,l+dx:r+dx]
            if colors.shape[:2] != (b-t,r-l): continue
            if (colors[:,:,0]-colors[:,:,2]>25).mean()>.07: continue
            if (colors.mean(axis=2)>127).mean()>.12: continue
            donor=plate.crop((l+dx,t+dy,r+dx,b+dy))
            break
        if donor is None: continue
        clean.paste(donor,(l,t),mask)
        specs.append((f'star {len(specs)+1:02d}',cut,cx,cy,(cx-l,cy-t),
                      rng.choice([-1,1])*rng.uniform(14,58)))
    return clean,specs

def lift_moon(plate):
    # Cut the crescent off the plate as its own paper piece and patch the sky beneath it.
    rgb=np.asarray(plate.convert('RGB'),dtype=np.int16)
    r,g,b=rgb.transpose(2,0,1)
    yy,xx=np.indices((H,W))
    near=((xx-472)/78)**2+((yy-95)/78)**2<1
    comps,n=label((r>112)&(r-b>-6)&near,np.ones((3,3),dtype=int))
    sizes=[(comps==i).sum() for i in range(1,n+1)]
    body=binary_dilation(comps==1+int(np.argmax(sizes)),iterations=2)
    ys,xs=np.where(body)
    l,t,rr,bb=xs.min()-3,ys.min()-3,xs.max()+4,ys.max()+4
    soft=Image.fromarray(np.uint8(gaussian_filter(body.astype(np.float32),.6)*255))
    cut=window(plate,soft).crop((l,t,rr,bb))
    ring=binary_dilation(body,iterations=14)&~binary_dilation(body,iterations=4)&(r<95)
    tone=rgb[ring].mean(0); spread=rgb[ring].std(0)
    night=np.asarray(resized(piece('b01_night_sky'),W,H).convert('RGB'),dtype=np.float32)
    patch=(night-night[ring].mean(0))/(night[ring].std(0)+1e-3)*spread*.8+tone
    clean=plate.copy()
    cover=Image.fromarray(np.uint8(gaussian_filter(binary_dilation(body,iterations=3).astype(np.float32),1.1)*255))
    clean.paste(Image.fromarray(np.clip(patch,0,255).astype('uint8')).convert('RGBA'),(0,0),cover)
    return clean,cut,((l+rr)/2,(t+bb)/2)

def bough(key,box,pivot,sway):
    # A leafy clump lifted from the approved portrait; it rocks about the point where it joins the tree.
    l,t,r,b=box
    cut=alpha_mask(approved.crop(box),(2,2,r-l-3,b-t-3),'ellipse',3.0)
    add(key,cut,pivot[0],pivot[1],(pivot[0]-l,pivot[1]-t),sway=sway)

def with_grounded_foliage():
    # Two small branch tips and foreground paper-grass pieces. The trunk and traveler
    # are carried by the exact approved backdrop and do not move.
    branch=stock('tree',(269,470),(146,203,229,287),59,1.02)
    add('small right bough',branch,358,573,(7,48),sway=[5.2,6.4,0])
    tip=stock('tree',(269,470),(161,96,268,178),66,1.02)
    add('outer bough tip',tip,353,444,(14,48),sway=[4.4,7.6,0])
    bough('crown clump',(300,378,412,452),(372,450),[3.4,5.2,.6])
    bough('left clump',(226,470,326,548),(322,520),[-4.2,6.8,1.9])
    bough('upper right clump',(382,452,452,512),(386,500),[4.6,4.6,2.7])
    bough('lower right clump',(352,566,470,640),(360,618),[-3.8,7.4,.9])
    grass=stock('plants',(550,239),(72,64,261,214),40,.82)
    add('grass at the tree roots',grass,438,803,(19,29),sway=[6.5,5.8,0])
    blades=stock('plants',(550,239),(67,64,250,209),35,.75)
    add('near blades',blades,290,912,(17,25),sway=[-6.0,4.9,0])

def make():
    plate,stars=find_stars(approved)
    plate,moon,moon_at=lift_moon(plate)
    add('approved foreground and frame',plate,0,0)

    # Keep layer edges visible: parallel slanted ribbons and alternating
    # bands of textured paper, clouds and partially occluded discs.
    gap=Image.new('RGBA',(W,H),'#51656e')
    night=source('b01_night_sky',565,440,.72,.95)
    a=np.asarray(night.getchannel('A'),dtype=np.float32).copy()
    a*=np.clip((387-np.arange(night.height))/213,0,1)[:,None]
    night.putalpha(Image.fromarray((a).astype('uint8')))
    fill=source('sky_patch',459,482,.63,.73)
    gap.alpha_composite(fill,(0,164))
    gap.alpha_composite(night,(0,0))
    # The lowest plate is the original cloud beside the hand and the raised hem.
    aa=np.asarray(gap.getchannel('A'),dtype=np.float32).copy()
    aa*=np.clip((624-np.arange(H))/52,0,1)[:,None]
    gap.putalpha(Image.fromarray(aa.astype('uint8')))
    add('deep sky clean plate',window(gap,polygon_mask(reveal,.4)),0,0)
    def sheet(key,name,x,y,w,angle,dx,dy,period,sat=.72,light=.86,depth=None):
        im=source(name,w,sat=sat,light=light)
        if depth is not None:
            # Scale the cloud bodies without widening their stroke texture further.
            im=resized(im,w,round(im.height*depth))
            rgb=np.asarray(im,dtype=np.float32).copy()
            luma=rgb[:,:,:3] @ np.array([.24,.65,.11])
            highlight=np.clip((luma-50)/151,0,1)**.78
            rgb[:,:,:3]+=highlight[:,:,None]*np.array([21,23,25])
            im=Image.fromarray(np.clip(rgb,0,255).astype('uint8'))
        center(key,lean(im,angle),x,y,slide=[dx,dy,period,0],clip='reveal')

    def bank(key,name,x,y,w,angle,dx,dy,period,sat=.74,light=.98):
        # Broad cloud banks drawn for this reveal: near-ivory crowns, slate engraved
        # shadows and a hanging skirt of streaks, like the approved portrait's own banks.
        im=grade(resized(piece(name),w),sat,light,(1,.985,.95))
        center(key,lean(im,angle),x,y,slide=[dx,dy,period,0],clip='reveal')

    sheet('high silver pattern','b05_light_band_1',159,64,313,0,-4,2,22,.66,.77)
    bank('far bank behind the gears','bank_1',226,98,420,8,8,-2,19,.66,.95)
    sheet('gold patterned sheet','b06_light_band_2',165,120,395,4,-10,4,17,.69,.90)
    sheet('far solar disc','b03_sun_rays',247,-2,181,-3,4,4,24,.69,.83)
    ringed=stock('x4_planets',(550,314),(0,4,222,148),25,.86)
    center('far ringed planet',ringed,236,128,spin=-2.6,slide=[4,1,29,0],clip='reveal')

    # Wheel centres and apparent scale follow the approved portrait.
    def clock_gear(box,w):
        g=stock('w4_gears',(550,420),box,w,.84)
        x,y=g.width/2,g.height/2
        return alpha_mask(g,(1,1,g.width-2,g.height-2),'ellipse',.6)
    pinion=clock_gear((336,11,550,230),92)
    center('upper meshing gear',lean(pinion,-9),141,80,spin=-5.4,clip='reveal')
    center('main brass gear',lean(clock_gear((0,0,395,398),205),186),20.6,141,spin=2.82,clip='reveal')
    disk=source('w1_wheel_only',179,sat=.73,light=.88)
    center('blue wheel spokes',disk,20.6,141,spin=2.82,clip='reveal')
    crescent=source('w2_crescent_only',64,170,sat=.73,light=.91)
    add('wheel counter-rotating crescent',crescent,20.6,141,(3,85),spin=-1.9,clip='reveal')
    center('wheel hub',source('w3_hub',30,sat=.75,light=.84),20.6,141,spin=-3.9,clip='reveal')

    # Below the clockwork: bank, ribbon, bank, pattern, bank. Each later sheet overlaps
    # the one before it, and the small planets sit between sheets so only part of each shows.
    sheet('rainbow disc','b04_rainbow',152,186,112,0,6,-2,16,.77,.93)
    bank('broad bank over the rainbow','bank_3',104,236,600,9,-10,4,14)
    sheet('first engraved ribbon','b05_light_band_1',112,300,330,8,-15,4,14,.55,.84)
    blue=stock('x4_planets',(550,314),(268,180,397,307),15,.89)
    center('middle blue planet',blue,152,276,spin=3.7,slide=[-4,2,22,0],clip='reveal')
    bank('second broad bank','bank_2',60,350,560,10,15,-6,11)
    sheet('second engraved ribbon','b06_light_band_2',70,402,285,10,19,-8,13,.55,.86)
    sheet('lower zigzag pattern','b12_zigzag_glow',72,424,230,11,19,-8,11,.66,.92)
    red=stock('x4_planets',(550,314),(408,10,531,139),14,.82)
    center('near rust planet',red,60,436,spin=-4.4,slide=[4,-3,19,0],clip='reveal')
    bank('third bank over the pattern','bank_4',30,500,540,12,-17,8,10)
    sheet('third engraved ribbon','b05_light_band_1',40,530,250,12,13,-6,12,.55,.84)
    bank('near bank','bank_5',10,566,500,13,17,-8,8)
    bank('lowest bank by the hand','bank_3',0,622,420,16,-10,6,9)

    for i,(name,cut,x,y,pivot,spin) in enumerate(stars):
        if i%3==0: add(name,cut,x,y,pivot,sway=[22 if spin>0 else -22,1.2+(i%7)*.35,i*.9])
        else: add(name,cut,x,y,pivot,spin=spin)
    center('crescent moon',moon,moon_at[0],moon_at[1],sway=[5.5,6.2,0],slide=[5,-2,8.5,0])

    # A clean solar paper backing and full rays cut from the separate engraving plate.
    # The backing is the approved portrait blurred until the old rays disappear, so the
    # turning rays sit on the same warm paper tone as the rest of the plate.
    paper=approved.filter(ImageFilter.GaussianBlur(11))
    yy,xx=np.indices((H,W),dtype=np.float32)
    # Fade the backing with distance from the sun so no corner of it shows beside the tree.
    falloff=np.clip((196-np.hypot(xx-518,yy-449))/38,0,1)
    backing=Image.fromarray((np.asarray(polygon_mask(solar,2.2),dtype=np.float32)*falloff).astype('uint8'))
    add('paper behind the turning rays',window(paper,backing),0,0)
    rays=grade(resized(piece('sun_face'),345),.72,.97,(1.0,.955,.84))
    pivot=(round(rays.width*.499),round(rays.height*.484))
    radius=58
    hole=Image.new('L',rays.size,255)
    x,y=pivot
    ImageDraw.Draw(hole).ellipse((x-radius,y-radius,x+radius,y+radius),fill=0)
    rays.putalpha(Image.fromarray(np.minimum(np.asarray(rays.getchannel('A')),np.asarray(hole))))
    sx,sy=518,449
    add('independent solar rays',rays,sx,sy,pivot,spin=4.4,clip='dome')
    face=approved.crop((sx-62,sy-62,sx+62,sy+62))
    face=alpha_mask(face,(0,0,123,123),'ellipse',.8)
    # Eye cels drawn from the approved face: the eyes travel slowly from side to side,
    # then the lids lower and close. Each cel is matched to the approved medallion's size and tone.
    want=np.asarray(face.convert('RGB'),dtype=np.float32)[np.asarray(face.getchannel('A'))>200].mean(0)
    def cel(name):
        im=resized(piece(name),face.width,face.height)
        got=np.asarray(im.convert('RGB'),dtype=np.float32)[np.asarray(im.getchannel('A'))>200].mean(0)
        im=grade(im,.86,1,tuple(want/got))
        return alpha_mask(im,(0,0,face.width-1,face.height-1),'ellipse',.8)
    names={'sun medallion':'eyes_ahead','sun looks left':'eyes_left','sun looks far left':'eyes_far_left',
           'sun looks far right':'eyes_far_right','sun lids lowering':'eyes_half','sun eyes closed':'eyes_closed'}
    for key,name in names.items():
        if key!='sun medallion': assets[key]=cel(name)
    C,L1,L2,R2,HALF,SHUT='sun medallion','sun looks left','sun looks far left','sun looks far right','sun lids lowering','sun eyes closed'
    order=[C,C,C,L1,L1,L2,L2,L2,L2,L1,L1,C,C,C,R2,R2,R2,R2,C,C,C,HALF,SHUT,SHUT,SHUT,SHUT,SHUT,HALF]
    center('sun medallion',cel('eyes_ahead'),sx,sy,cels=order,hold=4/9)

    with_grounded_foliage()
    frame_mask=Image.new('L',(W,H),255)
    ImageDraw.Draw(frame_mask).rectangle((28,26,573,934),fill=0)
    add('original engraved frame',window(approved,frame_mask),0,0)
    print(f'{len(stars)} independent stars and {len(layers)} total placements')

if __name__=='__main__':
    make()
    ks=['sun looks far left','sun looks left','sun medallion','sun looks far right','sun lids lowering','sun eyes closed']
    strip=Image.new('RGBA',(496*7,496),'#777')
    strip.alpha_composite(approved.crop((518-62,449-62,518+62,449+62)).resize((496,496),RESAMPLE),(0,0))
    for i,k in enumerate(ks,1):
        strip.alpha_composite(assets[k].resize((496,496),RESAMPLE),(i*496,0))
    strip.convert('RGB').save(work/'eye-cels.jpg',quality=92)
    for t in [0,3,6]:
        render(t).convert('RGB').save(work/f'cloud-revision-{t}.jpg',quality=93)
