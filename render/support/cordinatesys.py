from .configsys import Config
from .custdataclasses import cord

def cordstoxy(starcords:cord,config:Config):
    bounds=config.bounds
    xrang=bounds[1].x-bounds[0].x
    yrang=bounds[1].y-bounds[0].y

    # xcoef=(starcords.x-bounds[0].x)/xrang
    # ycoef=(starcords.y-bounds[0].y)/yrang

    xcoef=(bounds[1].x-starcords.x)/xrang  #TODO CHECK
    ycoef=(bounds[1].y-starcords.y)/yrang

    x=xcoef*config.bg.width
    y=ycoef*config.bg.height
    return (x,y)