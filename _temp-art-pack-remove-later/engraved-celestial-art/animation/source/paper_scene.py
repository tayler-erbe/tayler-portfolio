from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from math import sin, cos, pi, floor, hypot
from random import Random
import numpy as np
from compose import piece, grade

W,H=600,960
RESAMPLE=Image.Resampling.LANCZOS
work=Path(__file__).resolve().parent.parent/'build'
work.mkdir(exist_ok=True)
art=Image.open(work.parent/'studies/02-portrait/selected-portrait.jpeg').convert('RGBA').resize((W,H),RESAMPLE)
assets={}
layers=[]
rng=Random(1138)

def resized(im,w,h=None):
    return im.resize((w,h or round(w*im.height/im.width)),RESAMPLE)

def source(name,w,h=None,sat=.8,light=.96):
    return grade(resized(piece(name),w,h),sat,light)

def crop_grid(name,canvas,box):
    im=piece(name)
    return im.crop(tuple(round(p*d/s) for p,d,s in zip(box,(im.width,im.height)*2,canvas*2)))

def alpha_mask(im,coords,shape='polygon',blur=.45):
    mask=Image.new('L',im.size)
    getattr(ImageDraw.Draw(mask),shape)(coords,fill=255)
    if blur: mask=mask.filter(ImageFilter.GaussianBlur(blur))
    result=im.copy()
    result.putalpha(Image.fromarray((np.asarray(im.getchannel('A'),dtype=np.float32)*np.asarray(mask)/255).astype('uint8')))
    return result

def add(key,im,x,y,origin=(0,0),size=1,slide=None,sway=None,spin=0,clip=None,variant=None,cels=None,hold=None):
    assets[key]=im
    row={'key':key,'at':[x,y],'pivot':list(origin)}
    if size!=1: row['scale']=size
    if slide: row['slide']=slide
    if sway: row['sway']=sway
    if spin: row['spin']=spin
    if clip: row['clip']=clip
    if variant: row['variant']=variant
    if cels: row['cels']=cels; row['hold']=hold
    layers.append(row)

def center(key,im,x,y,**kwargs):
    add(key,im,x,y,(im.width/2,im.height/2),**kwargs)

def cubic(p0,p1,p2,p3):
    return [tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3)) for t in (i/32 for i in range(33))]

edge=cubic((371,21),(265,78),(105,272),(81,474))+cubic((81,474),(68,539),(90,559),(132,580))
bottom=cubic((132,580),(233,640),(379,406),(582,324))
veil=edge+bottom+[(629,313),(631,14)]
reveal=[(18,18),*edge,(148,684),(16,698)]

def stock(name,canvas,box,w,light=.95):
    return grade(resized(crop_grid(name,canvas,box),w),.84,light)

def make():
    # Use the approved portrait's engraved border, with the movable art behind it.
    frame_alpha=Image.new('L',(W,H),255)
    ImageDraw.Draw(frame_alpha).rectangle((28,26,573,934),fill=0)
    frame=art.copy()
    frame.putalpha(frame_alpha)
    day=source('sky_patch',599,655,.64,.95)
    paper=Image.new('RGBA',(W,H),'#403e34')
    paper.alpha_composite(day,(0,0))
    ground=piece('ground_fill').crop((0,601,1536,1024))
    paper.alpha_composite(grade(resized(ground,584,271),.76,.86),(12,656))
    add('paper',paper,0,0)

    night=source('b01_night_sky',411,410,.74,.91)
    gap=Image.new('RGBA',(W,H),'#647781')
    gap.alpha_composite(source('sky_patch',550,570,.65,.71),(0,163))
    na=np.asarray(night.getchannel('A'),dtype=np.float32).copy()
    na*=np.clip((340-np.arange(night.height))/165,0,1)[:,None]
    night.putalpha(Image.fromarray(na.astype('uint8')))
    gap.alpha_composite(night,(0,0))
    add('reveal paper',alpha_mask(gap,reveal),0,0)

    def beyond(name,x,y,w,dx,dy,period,phase,angle=0,light=.86):
        im=source(name,w,sat=.71,light=light)
        if angle: im=im.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        center(name,im,x,y,slide=[dx,dy,period,phase],clip='reveal')

    beyond('b03_sun_rays',258,10,130,2,-3,31,0,light=.76)
    beyond('b07_cloud_far',191,106,344,7,2,22,0)
    beyond('b06_light_band_2',195,137,397,-9,3,19,.4,light=.82)
    beyond('b04_rainbow',171,195,119,4,-4,23,0,light=.89)
    beyond('b08_cloud_2',145,229,295,12,-4,17,0,angle=10)
    beyond('b05_light_band_1',108,274,327,-13,4,19,0,light=.74)
    beyond('b09_cloud_3',110,312,290,13,-6,14,0,angle=9)
    beyond('b12_zigzag_glow',61,360,185,-14,4,18,0,angle=12,light=.70)
    beyond('b10_cloud_4',61,391,222,13,-7,12,.3,angle=13)
    beyond('b11_cloud_near',61,483,221,-15,7,11,.1,angle=13)

    # Clockwork shares one axle. Its separate pinions use the tooth ratio of the large gear.
    def gear(box,center_local,radius,width):
        im=crop_grid('w4_gears',(550,420),box)
        scale=im.width/(box[2]-box[0])
        x,y=center_local
        r=radius
        im=alpha_mask(im,tuple(v*scale for v in (x-r,y-r,x+r,y+r)),'ellipse')
        return grade(resized(im,width),.74,.83)
    gx,gy=57,139
    ring=gear((0,0,395,398),(198,199),197,128)
    pinion=gear((337,10,550,230),(106,111),108,70)
    redpin=gear((336,205,550,420),(105,108),105,57)
    center('clock rim',ring,gx,gy,spin=4.5,clip='reveal')
    disk=source('w1_wheel_only',102,sat=.65,light=.86)
    center('clock wheel',disk,gx,gy,spin=4.5,clip='reveal')
    crescent=source('w2_crescent_only',54,98,sat=.66,light=.96)
    add('clock crescent',crescent,gx,gy,(5,49),spin=-3.2,clip='reveal')
    center('clock hub',source('w3_hub',22,sat=.69,light=.91),gx,gy,spin=-5.4,clip='reveal')
    center('brass pinion',pinion,145,107,spin=-8.5,clip='reveal')
    center('red pinion',redpin,135,190,spin=-10,clip='reveal')

    # The paper sun is three parts: a full rotating corona, a stationary medallion,
    # and two prepared expression cels.
    sun=source('sun_face',284,sat=.70,light=.97)
    sc=(round(sun.width*.499),round(sun.height*.484))
    rs=round(sun.width*.175)
    bounds=(sc[0]-rs,sc[1]-rs,sc[0]+rs,sc[1]+rs)
    disk=alpha_mask(sun,bounds,'ellipse')
    rays=sun.copy()
    # Retain a two-pixel overlap beneath the face to hide the circular seam.
    hole=Image.new('L',sun.size,255)
    ImageDraw.Draw(hole).ellipse((bounds[0]+2,bounds[1]+2,bounds[2]-2,bounds[3]-2),fill=0)
    rays.putalpha(Image.fromarray(np.minimum(np.asarray(rays.getchannel('A')),np.asarray(hole))))
    sx,sy=526,440
    add('sun rays',rays,sx,sy,sc,spin=8.8)
    face=disk.crop(bounds)
    from scipy.ndimage import map_coordinates
    yy,xx=np.indices((face.height,face.width),dtype=np.float32)
    field=np.zeros_like(xx)
    for eye in [36,69]:
        field+=3.3*np.exp(-(((xx-eye)/6.5)**2+((yy-40)/4.2)**2))
    original=np.asarray(face)
    glance=Image.fromarray(np.stack(
        [map_coordinates(original[:,:,i],[yy,xx+field],order=1,mode='nearest') for i in range(4)],axis=-1))
    assets['sun side glance']=glance
    center('sun face',face,sx,sy,variant='sun side glance')

    # Beyond-sky planets are cut from their own sheet and turned on separate pivots.
    saturn=stock('x4_planets',(550,314),(0,4,222,148),42,.83)
    blue=stock('x4_planets',(550,314),(268,180,397,307),30,.88)
    red=stock('x4_planets',(550,314),(408,10,531,139),23,.74)
    center('ringed planet',saturn,221,78,spin=7,slide=[3,-2,23,0],clip='reveal')
    center('blue planet',blue,63,338,spin=-8,slide=[-3,3,17,.5],clip='reveal')
    center('red planet',red,113,280,spin=9,clip='reveal')

    navy=source('b01_night_sky',606,725,.84,.99)
    veil_fill=Image.new('RGBA',(W,H),'#142d45')
    veil_fill.alpha_composite(navy,(0,0))
    shape=alpha_mask(veil_fill,veil)
    draw=ImageDraw.Draw(shape)
    draw.line(edge,fill='#1a2021',width=4)
    draw.line([(x+2,y) for x,y in edge],fill='#a89969',width=1)
    add('sky dome',shape,0,0)
    for idx, (x,y,w) in enumerate([(513,359,201),(421,420,222),(328,482,179),(243,542,153)]):
        im=source(['b08_cloud_2','b09_cloud_3','b10_cloud_4','b11_cloud_near'][idx],w,sat=.54,light=.76)
        im=im.rotate(16+idx*3,Image.Resampling.BICUBIC,expand=True)
        center(f'dome cloud {idx}',im,x,y,slide=[-4+idx*2,2,20-idx*2,idx*.4],clip='dome')

    center('crescent moon',source('moon_crescent',105,sat=.61,light=.94),463,120,sway=[4,15,0])
    mask=Image.new('L',(W,H))
    ImageDraw.Draw(mask).polygon(veil,fill=255)
    placed=[]
    for i in range(8):
        im=source(f'star_{i+1:02d}',38,sat=.82,light=.99)
        assets[f'star cutout {i}']=im
    variants=[(1,0,81,85),(185,0,255,82),(357,7,447,86),
              (186,92,258,169),(477,85,544,171),(4,263,76,346)]
    for i,box in enumerate(variants,8):
        assets[f'star cutout {i}']=stock('x1_stars',(550,351),box,38,1.0)
    for _ in range(2400):
        x,y=rng.randint(102,555),rng.randint(41,599)
        if not mask.getpixel((x,y)) or min(mask.getpixel((max(0,x-16),y)),mask.getpixel((x,min(H-1,y+19))))==0:
            continue
        if hypot((x-465)*.9,y-124)<63 or any(hypot(x-a,y-b)<21 for a,b in placed): continue
        placed.append((x,y))
        i=rng.randrange(14)
        w=rng.choices([8,12,16,22,31],[4,5,5,3,2])[0]
        name=f'star cutout {i}'
        center(name,assets[name],x,y,size=w/38,spin=rng.choice([-1,1])*rng.uniform(5,22),sway=[rng.uniform(9,41),rng.uniform(7,18),rng.random()*3])
        if len(placed)>=66: break

    # Brown terrain, hill strips and the village are separate static paper plates.
    land=Image.new('RGBA',(W,H))
    land.alpha_composite(source('village_horizon',550,75,.69,.88),(27,625))
    land.alpha_composite(source('landscape_foreground',562,196,.78,.87),(19,750))
    add('engraved land',land,0,0)
    # Real detached boughs are pivoted at the fork in the trunk.
    tree=source('tree',215,sat=.81,light=.86)
    origin=(274,405)
    def tree_section(name,points,pivot,angle,period,phase):
        section=alpha_mask(tree,[(x*tree.width/269,y*tree.height/470) for x,y in points])
        box=section.getbbox()
        px,py=pivot[0]*tree.width/269,pivot[1]*tree.height/470
        add(name,section.crop(box),origin[0]+px,origin[1]+py,(px-box[0],py-box[1]),sway=[angle,period,phase] if angle else None)
    tree_section('tree trunk',[(5,146),(67,122),(105,155),(129,143),(164,173),(157,235),(228,217),(269,253),(268,469),(0,469)],(126,236),0,0,0)
    tree_section('tree crown',[(0,0),(269,0),(269,126),(191,137),(159,168),(124,197),(97,172),(82,151),(0,144)],(126,178),3.3,8.5,.2)
    tree_section('right bough',[(140,134),(175,105),(269,94),(269,166),(192,169),(149,203),(126,242),(107,231)],(126,225),-4.2,7.1,0)
    tree_section('low branch',[(119,242),(147,213),(220,185),(260,210),(269,257),(170,258),(128,291),(115,279)],(124,289),4.1,9.5,.3)

    add('traveler',source('figure_with_cloak',384,245,.81,.94),28,579)
    grass=source('plants',192,sat=.80,light=.89)
    main=alpha_mask(grass,[(0,0),(101,0),(111,31),(115,61),(123,82),(0,84)])
    flowers=alpha_mask(grass,[(102,0),(191,0),(191,79),(105,84),(113,62),(97,48)])
    add('grass leaf fan',main,427,910,(65,72),sway=[5,6.5,0])
    add('flower and tall grass',flowers,478,923,(132,78),sway=[-4.3,7.8,.35])
    blade=stock('plants',(550,239),(66,63,250,180),53,.89)
    add('near grass leaves',blade,99,880,(27,30),sway=[5.5,5.5,.4])
    add('engraved frame',frame,0,0)

def pose(row,time):
    x,y=row['at']
    ang=row.get('spin',0)*time
    if slide:=row.get('slide'):
        dx,dy,p,phase=slide
        x+=dx*sin(2*pi*time/p+phase)
        y+=dy*sin(2*pi*time/p+phase)
    if motion:=row.get('sway'):
        deg,p,phase=motion
        ang+=deg*sin(2*pi*time/p+phase)
    return x,y,ang

from functools import lru_cache
@lru_cache
def clip_masks():
    maps={}
    for name,points in [('reveal',reveal),('dome',veil)]:
        mask=Image.new('L',(W,H)); ImageDraw.Draw(mask).polygon(points,fill=255)
        maps[name]=mask
    return maps

def render(seconds):
    t=floor(seconds*9+1e-7)/9
    frame=Image.new('RGBA',(W,H))
    clipmaps=clip_masks()
    for row in layers:
        key=row['key']
        if row.get('variant') and 1.3<((t+.3)%6.2)<2.4: key=row['variant']
        if row.get('cels'): key=row['cels'][floor(t/row['hold']+1e-7)%len(row['cels'])]
        im=assets[key]
        x,y,ang=pose(row,t)
        px,py=row['pivot']
        scale=row.get('scale',1)
        if ang or scale!=1:
            pad=max(3,round(max(hypot(px,py),hypot(im.width-px,py),
                                hypot(px,im.height-py),hypot(im.width-px,im.height-py))*scale)+2)
            radius=ang*pi/180
            a,b=cos(radius)/scale,sin(radius)/scale
            im=im.transform((2*pad,2*pad),Image.Transform.AFFINE,
                (a,b,px-pad*(a+b),-b,a,py-pad*(a-b)),Image.Resampling.BICUBIC)
            px=py=pad
        if clip:=row.get('clip'):
            pos=(round(x-px),round(y-py))
            crop=(pos[0],pos[1],pos[0]+im.width,pos[1]+im.height)
            im=im.copy()
            im.putalpha(Image.fromarray((np.asarray(im.getchannel('A'),dtype=np.float32)*
                        np.asarray(clipmaps[clip].crop(crop))/255).astype('uint8')))
            frame.alpha_composite(im,pos)
        else: frame.alpha_composite(im,(round(x-px),round(y-py)))
    return frame

if __name__=='__main__':
    make()
    render(0).convert('RGB').save(work/'still.jpg',quality=94)
    render(3).convert('RGB').save(work/'later.jpg',quality=94)
