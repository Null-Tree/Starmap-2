# import random
import time
# import json
# import matplotlib.pyplot as plt
# import numpy as np
# import csv
# import sqlite3
# import math
# import sys
# from tqdm import tqdm
# from tkinter import * 
# from PIL import Image,ImageDraw, ImageFont #Pillow library
# import scipy.ndimage as ndi

# import astropy.units as u
# import astropy.time
# import astropy.coordinates

# from dataclasses import dataclass

# from PIL import ImageOps
# import pickle

from support.custdataclasses import *

from support import configsys
from support import imaging
from support import starformatting
from support import constellations

import pickle

def main():
    # Gets configuration for render
    config=configsys.getconfig()
    

    # creates background image
    img=imaging.createimg(config)
    # img.show()

    if config.axis.drawAxis:
        imaging.render_axis(img,config)

    # load constellations
    print("Handeling Constellations")
    constellations.handleconsjson(config.cons.jsonfile,config.cons.txtfile,img,config)


    # open all stars and load binary
    targetfilepath=r"render\static\data\binaries\all_stars"
    with open(targetfilepath, 'rb') as allsbfile:
        star_raw_array=pickle.load(allsbfile)

    # get all cosmetic information of stars (how stars will be drawn)
    print("formatting stars")
    star_graphicinfo_array=starformatting.format_all_stars(star_raw_array,config)
    
    # sort stars by radius
    star_graphicinfo_array.sort(key=lambda x: x.radius)

    

    print("drawing stars")
    if config.multi_process:
        print(f"multithreading with {config.n_process}")
        imaging.thread_stars(img,star_graphicinfo_array,config)
    else:
        imaging.place_list_stars(img,star_graphicinfo_array,config)

    # img.show()

    imaging.saveimg(img)

if __name__=="__main__":
    st=time.time()
    main()
    et=time.time()
    print(time.strftime("%H hours %M minutes %S seconds", time.gmtime(et - st)),f" elapsed")