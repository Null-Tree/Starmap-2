from dataclasses import dataclass

from PIL import Image

from .custdataclasses import cord

@dataclass
class backgroundConfig:
    width:float = None
    height:float= None
    fillcolor:tuple= None

@dataclass
class starsConfig:
    maxradius:float= None
    minradius:float= None
    colormin:int= None
    appmagreq:float= None
    stargraphic:Image= None
    whitecore_coef:float=None
    raw_r_adj:int=None

@dataclass
class labelConfig:
    label:bool= None
    labelcolor:tuple= None
    labelsize:int= None
    

@dataclass
class constellationConfig:
    draw_cons:bool= None
    skylore:str = None
    jsonfile:str=None
    txtfile:str=None
    consborderRGB:tuple= None
    conslinewidth:int= None
    label:labelConfig= None

@dataclass
class positioningConfig:
    warp:bool= None
    cord_mode:str= None

@dataclass
class axisConfig:
    drawAxis:bool = None
    linefill:tuple=None
    textfill:tuple=None

@dataclass
class Config:
    bg:backgroundConfig= None
    stars:starsConfig= None
    cons:constellationConfig= None
    axis:axisConfig=None
    warp:bool= None
    cord_mode:str= None
    bounds:list= None
    basicrender:bool= None
    antialius:bool= None
    multi_process:bool=None
    n_process:int=None

##################################

def getconfig():

    config=Config(backgroundConfig(),starsConfig(),constellationConfig(label=labelConfig()),axisConfig())

    # Choose whever to use multi processing, speeds up rendering drastically
    config.multi_process=True
    config.n_process=6
    
    # configure output image size 
    # sizepow 15->  32k by 16k
    # sizepow 14->  16k by 8k
    # sizepow 13->  8k by 4k
    # sizepow 12->  4k by 2k
    sizepower=15
    config.bg.width=2**sizepower
    config.bg.height=2**(sizepower-1)
    
    # RGB of background
    config.bg.fillcolor=(0,0,0)

    # set min radius of a star on display
    config.stars.minradius=0
    # min color intensity rgb, 0-255
    config.stars.colormin=0

    # dimmest app mag star rendered
    config.stars.appmagreq=10

    # radius to render a star of app mag -2
    # reccom: 160 for sp 15, 80 for sp 14, and so on
    config.stars.maxradius=80 *2

    # adjust radius of all stars
    config.stars.raw_r_adj=2

    # choose whever to render constellation lines
    config.cons.draw_cons=True
    # constellation line colour
    config.cons.consborderRGB=(80,80,80) 
    # thickness of constellation line
    # recomm: 12 for sp15, 6 for sp14 and so on, with min of 2
    config.cons.conslinewidth=12

    # label constellation names
    config.cons.label.label=False
    config.cons.label.labelcolor=(109, 191, 184)
    config.cons.label.labelsize=32
    config.antialius=True

    # star template
    config.stars.stargraphic=Image.open(r"render/static/visuals/graphics/stargraphic.png")
    
    # whever to render simple stars
    # true: draws solid fill circles, faster but doesnt look as good 
    # false: uses star template, slower
    config.basicrender=False

    # use radec or lb
    config.cord_mode="galactic" # /"celestial" or "galactic"

    # set top left and bottom right of sky selection
    config.bounds=[cord(0,-90),cord(360,90)]
    # config.bounds=[cord(150.5,-20.50),cord(190.75,20.000)]
    

    # whever to draw axis to label cordinate lines
    config.axis.drawAxis=False
    config.axis.linefill=(10, 32, 90)
    config.axis.textfill=(109, 191, 184)

    # prop of star be white center
    config.stars.whitecore_coef=0.6

    # skly lore system
    config.cons.skylore='iau'  #'iau or boorong

    if config.cons.skylore=='iau':
        config.cons.jsonfile=r"render/static/data/csv/iau.json"
        config.cons.txtfile=r'render/static/data/csv/iau_coords.txt'
    elif config.cons.skylore=="boorong":
        config.cons.jsonfile=r"render/static/data/csv/boorong/boorong.json"
        config.cons.txtfile=r'render/static/data/csv/boorong/boorong_cords.txt'       

    return config