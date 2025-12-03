
from tqdm import tqdm
from .custdataclasses import *
from .configsys import Config

def format_all_stars(star_raw_array,config:Config):
    
    star_grapicinfo_array=[]

    for star in tqdm(star_raw_array):
        formattedstar=starformatter(star,config)
        if formattedstar != None:
            star_grapicinfo_array.append(formattedstar)

    return star_grapicinfo_array


from .cordinatesys import cordstoxy


import math
def appmag_to_size(appmag,config:Config):

    coef=  15.417/20 * (math.e ** (-0.425 * appmag))
    # coef 0 to 1
    size=coef*config.stars.maxradius
    size=max(size,config.stars.minradius)
    return size


def starformatter(star:Star,config:Config):    
    # /"celestial" or "galactic"
    if config.cord_mode=="celestial":
        starcords=cord(star.ra,star.dec)
    elif config.cord_mode=="galactic":
        starcords=cord(star.gal_l,star.gal_b)
    else:
        raise Exception("invalid cordinate mode")

    bounds=config.bounds

    # check in bounds
    if bounds[0].x <= starcords.x <= bounds[1].x and bounds[0].y <= starcords.y <= bounds[1].y:
        dot=stargraphic()
        dot.x,dot.y=cordstoxy(starcords,config)
        
            
        dot.radius=appmag_to_size(star.appmag,config)

        dot.rgb=star.RGB
        dot.appmag=star.appmag

        return dot
    else:
        # handle no out
        return None
