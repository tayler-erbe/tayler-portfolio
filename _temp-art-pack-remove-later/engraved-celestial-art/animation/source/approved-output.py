from paper_approved import *
from io import BytesIO
import json,base64,subprocess,sys
from math import cos

destination=work
destination.mkdir(exist_ok=True)
make()

def atlas_pack():
    # Pad each crop so bilinear interpolation cannot pick up its neighbor.
    placements={}
    tile_margin=4
    atlas_width=1248
    x=y=height=0
    for key,im in sorted(assets.items(),key=lambda item: -item[1].height):
        box=im.getbbox()
        assert box, key
        w,h=box[2]-box[0],box[3]-box[1]
        if x+w+tile_margin>atlas_width:
            x=0;y+=height;height=0
        placements[key]=[x+2,y+2,w,h,*box[:2]]
        x+=w+tile_margin
        height=max(height,h+tile_margin)
    atlas=Image.new('RGBA',(atlas_width,y+height))
    for key,(x,y,w,h,dx,dy) in placements.items():
        atlas.alpha_composite(assets[key].crop((dx,dy,dx+w,dy+h)),(x,y))
    return atlas,placements

def webp(im,quality):
    sink=BytesIO(); im.save(sink,format='WEBP',quality=quality,method=6)
    return base64.b64encode(sink.getvalue()).decode()

def html():
    atlas,placements=atlas_pack()
    still=render(0).convert('RGB')
    still.save(work/'approved-animation-still.webp',quality=90,method=6)
    template=Path(__file__).with_name('paper-opening.template.html').read_text()
    page=template.replace('{{STILL}}',webp(still,87)).replace('{{ATLAS}}',webp(atlas,84))
    data={'assets':placements,'layers':layers,'clipPaths':{'dome':solar,'reveal':reveal}}
    page=page.replace('{{DATA}}',json.dumps(data,separators=(',',':')))
    (destination/'celestial-opening.html').write_text(page)
    size=(destination/'celestial-opening.html').stat().st_size
    print('HTML',size,'bytes,',len(assets),'assets,',len(layers),'placements.')
    assert size<2_000_000

def gif():
    # Direct rendering avoids video-compression flicker between unchanged paper pieces.
    width,height=400,640
    raw=work/'frames.rgb'
    with raw.open('wb') as sink:
        for step in range(108):
            # Rock the paper plates back to their start without a cut in the GIF.
            # The live renderer advances independently while the app loads.
            t=3.45*(1-cos(2*pi*step/108))
            im=render(t).convert('RGB').resize((width,height),RESAMPLE)
            sink.write(im.tobytes())
    command=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
        '-video_size',f'{width}x{height}','-framerate','9','-i',str(raw),
        '-filter_complex_threads','1','-filter_complex',
        'split[a][b];[a]palettegen=max_colors=224[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
        '-loop','0',str(destination/'celestial-motion.gif')]
    subprocess.run(command,check=True)
    raw.unlink()
    print('GIF', (destination/'celestial-motion.gif').stat().st_size,'bytes.')

if 'gif' in sys.argv: gif()
if 'html' in sys.argv: html()
