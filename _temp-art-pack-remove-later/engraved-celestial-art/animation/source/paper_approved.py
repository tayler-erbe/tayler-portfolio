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
                      rng.choice([-1,1])*rng.uniform(4,16)))
    return clean,specs

def with_grounded_foliage():
    # Two small branch tips and foreground paper-grass pieces. The trunk and traveler
    # are carried by the exact approved backdrop and do not move.
    branch=stock('tree',(269,470),(146,203,229,287),59,.82)
    add('small right bough',branch,358,573,(7,48),sway=[2.85,11.2,0])
    tip=stock('tree',(269,470),(161,96,268,178),66,.80)
    add('outer bough tip',tip,353,444,(14,48),sway=[2.1,14,0])
    grass=stock('plants',(550,239),(72,64,261,214),40,.82)
    add('grass at the tree roots',grass,438,803,(19,29),sway=[4.0,13,0])
    blades=stock('plants',(550,239),(67,64,250,209),35,.75)
    add('near blades',blades,290,912,(17,25),sway=[-3.2,10,0])

def make():
    plate,stars=find_stars(approved)
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

    sheet('high silver pattern','b05_light_band_1',159,64,313,0,-2,1,36,.66,.77)
    sheet('far cloud sheet','b07_cloud_far',178,79,341,6,4,-1,32,.48,.98,1.22)
    sheet('gold patterned sheet','b06_light_band_2',165,115,395,3,-5,2,29,.69,.90)
    sheet('far solar disc','b03_sun_rays',247,-2,181,-3,2,2,40,.69,.83)
    ringed=stock('x4_planets',(550,314),(0,4,222,148),31,.86)
    center('far ringed planet',ringed,208,106,spin=-2.6,slide=[4,1,29,0],clip='reveal')
    sheet('clouds behind the wheel','b08_cloud_2',168,143,347,8,5,-2,22,.49,.97,1.21)

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

    sheet('clouds in front of wheel','b09_cloud_3',142,198,321,10,6,-2,18,.51,.96,1.26)
    sheet('rainbow disc','b04_rainbow',150,180,108,0,3,-1,27,.77,.93)
    # This arc is tucked back beneath its own cloud bank.
    sheet('bright bank over rainbow','b07_cloud_far',145,210,320,8,-5,2,23,.47,1.01,1.30)
    sheet('first engraved ribbon','b05_light_band_1',124,235,339,4,-7,2,24,.49,.84)
    sheet('deep scalloped cloud','b10_cloud_4',96,266,295,12,8,-3,19,.49,1.00,1.38)
    blue=stock('x4_planets',(550,314),(268,180,397,307),19,.89)
    center('middle blue planet',blue,84,300,spin=3.7,slide=[-4,2,22,0],clip='reveal')
    sheet('middle scalloped cloud','b08_cloud_2',83,319,265,11,-8,3,17,.50,.98,1.40)
    sheet('second engraved ribbon','b06_light_band_2',81,352,268,8,9,-4,21,.51,.84)
    sheet('cloud over patterned band','b09_cloud_3',78,379,270,13,-9,5,15,.49,.99,1.39)
    sheet('lower zigzag pattern','b12_zigzag_glow',53,410,211,12,9,-4,19,.55,.83)
    red=stock('x4_planets',(550,314),(408,10,531,139),19,.82)
    center('near rust planet',red,45,442,spin=-4.4,slide=[4,-3,19,0],clip='reveal')
    sheet('clouds around near planet','b10_cloud_4',51,457,250,12,-8,4,16,.47,1.00,1.34)
    sheet('nearest cloud sheet','b11_cloud_near',46,512,242,13,10,-5,13,.48,1.01,1.38)
    sheet('low cloud in front of all sheets','b08_cloud_2',10,573,218,18,-6,3,15,.49,.95,1.24)

    for name,cut,x,y,pivot,spin in stars:
        add(name,cut,x,y,pivot,spin=spin)

    # A clean solar paper backing and full rays cut from the separate engraving plate.
    paper=Image.new('RGBA',(W,H))
    neutral=source('sky_patch',254,385,.39,1.08)
    paper.alpha_composite(neutral,(371,256))
    add('paper behind the turning rays',window(paper,polygon_mask(solar,3.3)),0,0)
    rays=source('sun_face',345,sat=.66,light=.92)
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
    yy,xx=np.indices((face.height,face.width),dtype=np.float32)
    field=np.zeros_like(xx)
    for eye in [43,87]:
        field+=2.8*np.exp(-(((xx-eye)/7)**2+((yy-49)/4.8)**2))
    rgba=np.asarray(face)
    glance=Image.fromarray(np.stack([map_coordinates(rgba[:,:,i],[yy,xx+field],order=1,mode='nearest') for i in range(4)],axis=-1))
    assets['sun glances sideways']=glance
    center('sun medallion',face,sx,sy,variant='sun glances sideways')

    with_grounded_foliage()
    frame_mask=Image.new('L',(W,H),255)
    ImageDraw.Draw(frame_mask).rectangle((28,26,573,934),fill=0)
    add('original engraved frame',window(approved,frame_mask),0,0)
    print(f'{len(stars)} independent stars and {len(layers)} total placements')

if __name__=='__main__':
    make()
    for t in [0,3,6]:
        render(t).convert('RGB').save(work/f'cloud-revision-{t}.jpg',quality=93)
