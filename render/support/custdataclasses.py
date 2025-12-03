from dataclasses import dataclass

@dataclass         
class Star:
    appmag:float=None
    bprp:float=None

    ra: float=None
    dec:float=None

    gal_l:float=None
    gal_b:float=None

    K:float=None
    RGB:tuple=None



@dataclass         
class stargraphic:
    rgb:list = None
    radius:int=1
    x:int=None
    y:int=None
    
    # temp
    appmag:float=None

#a3 export

@dataclass         
class cord:
    x:float = None
    y:float=None