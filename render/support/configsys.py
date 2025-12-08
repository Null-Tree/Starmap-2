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

    config.multi_process=True
    config.n_process=4
    
    sizepower=14
    config.bg.width=2**sizepower
    config.bg.height=2**(sizepower-1)
    config.bg.fillcolor=(0,0,0)

    config.stars.minradius=0
    config.stars.colormin=0
    config.stars.appmagreq=10
    config.stars.maxradius=80
    config.stars.raw_r_adj=2

    config.cons.draw_cons=True
    config.cons.consborderRGB=(80,80,80) 
    config.cons.conslinewidth=12//2

    config.cons.label.labelcolor=(109, 191, 184)
    config.cons.label.labelsize=32
    config.cons.label.label=False
    config.antialius=True

    config.stars.stargraphic=Image.open(r"render\static\visuals\graphics\stargraphic.png")
    config.basicrender=False
    config.cord_mode="celestial" # /"celestial" or "galactic"

    # config.bounds=[cord(150.5,-20.50),cord(190.75,20.000)]

    config.bounds=[cord(0,-90),cord(360,90)]


    config.axis.drawAxis=False
    config.axis.linefill=(10, 32, 90)
    config.axis.textfill=(109, 191, 184)

    config.stars.whitecore_coef=0.6

    config.cons.skylore='iau'  #'iau or boorong

    if config.cons.skylore=='iau':
        config.cons.jsonfile=r"render\static\data\csv\iau.json"
        config.cons.txtfile=r'render\static\data\csv\iau.coords.txt'
    elif config.cons.skylore=="boorong":
        config.cons.jsonfile=r"render\static\data\csv\boorong\boorong.json"
        config.cons.txtfile=r'render\static\data\csv\boorong\boorong_cords.txt'       

    return config