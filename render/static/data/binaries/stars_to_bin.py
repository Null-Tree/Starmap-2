
import time
import csv
import math
import sys
from tqdm import tqdm
from tkinter import * 
import os

import astropy.units as u
import astropy.time
import astropy.coordinates

from dataclasses import dataclass

from color_system.color_system import *


import pickle

####CONF


# color system
cs = cs_hdtv


###########


@dataclass         
class Star:
    appmag:float=None
    bprp:float=None

    ra: float=None
    dec:float=None

    gal_l:float=None
    gal_b:float=None

    K:float=None
    RGB:tuple[int]=None


ALL_STARS=[]
n=0

chucked=0

lam = np.arange(380., 781., 5)
def K_to_rgb(K):
    global lam
    spec = planck(lam, K)
    rgb = cs.spec_to_rgb(spec).tolist()
    for i in range(3):
        rgb[i] = int(round(rgb[i]*256))
    # print(rgb)
    return rgb

def input_until_valid(prompt,acceptable,errmsg=None):
    print(prompt,end="")
    vin=input()
    if vin in acceptable:
        return vin
    else:
        if errmsg:
            print(errmsg)
        return input_until_valid(prompt,acceptable,errmsg)
    

def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord





def getfilelen(filepath):
    with open(filepath, 'r') as fp:
        for count, line in enumerate(fp):
            pass
    return count+1

# handles gaia stars
def processcsv(filepath):
    global ALL_STARS
    flen=getfilelen(filepath)
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            
            for row in tqdm(reader,total=flen):
                if rowcount==0:
                    rowcount+=1
                    continue
                
                

                tochuck=False
                for titem in row:
                    item=titem.lstrip()
                    if item =='' or item == None:
                        global chucked
                        # print(f"     {rowcount} chuck: {row}")
                        chucked+=1
                        tochuck=True

                if tochuck:
                    continue 
                
                kelvin=BPRP_to_teff(float(row[3]))
                star=Star(
                        float(row[2]),
                        float(row[3]),
                        float(row[0]),
                        float(row[1]),
                        float(row[4]),
                        float(row[5]),
                        kelvin,
                        K_to_rgb(kelvin)
                        
                        )
                
                ALL_STARS.append(star)

 

                rowcount+=1
    


#handles bright stars
def processBS(filepath):
    global ALL_STARS
    flen=getfilelen(filepath)
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            # idents,ra,dec,V,B-V,parallax 

            for drow in tqdm(reader,total=flen):
                if rowcount==0:
                    # for i in range(len(drow)):
                    #     print(f"{i} {drow[i]}")
                    rowcount+=1
                    continue
            
                row=drow.copy()

                row[0]=int(row[0])
                
                for i in range(2,15):
                    if row[i] and row[i].lstrip()!="":
                        row[i]=float(row[i])


                #  id
                # 1  designation
                # 2  appmag
                # 3  absmag
                # 4  b-v; interpret as bprp
                # 5  ra
                # 6  dec
                # 7  ly
                # 8  parallax
                # 9  parsec
                # 10  from earth X
                # 11  from earth Y
                # 12  from earth Z
                # 13  galactic l
                # 14  galactic b

                    # float(row[2]),
                    # float(row[4]),
                    # float(row[5]),
                    # float(row[6])

                kelvin=BPRP_to_teff(float(row[4]))

                star=Star(
                        float(row[2]),
                        float(row[4]),
                        float(row[5]),
                        float(row[6]),
                        float(row[13]),
                        float(row[14]),
                        kelvin,
                        K_to_rgb(kelvin)
                        
                    )
                
                ALL_STARS.append(star)
                    
                    # placestar(imgstar,img)


def BPRP_to_teff(bprp):
    """returns in kelvins"""
    teff = 5040/(0.4929+0.5092*bprp-0.0353*bprp**2)
    return teff           

n_stars=0


    
def ra2deg(ra:list):
    """converts list of hours cords to degrees"""
    list=ra
    result=[0 for i in range(len(list))]
    for i in range(len(list)):
        result[i]=float(list[i])/24*360
    return result

#================================



def sort_by_appmag():
    # orig_list.sort(key=lambda x: x.count, reverse=True)
    global ALL_STARS
    ALL_STARS.sort(key=lambda x: x.appmag)

    
#===============================================================================================================

def main():

    
    print("\nprocessing csv")
    print("gaia catalouge")

    processcsv("csv/million_wgal.csv")
    print("amended bright stars")
    processBS("csv/brightstars.csv")
    print("csv processeds\n")


    print("sorting stars")
    sort_by_appmag()
    print("stars sorted\n")

    print(len(ALL_STARS))
    # for star in tqdm(ALL_STARS):
    #     print(star.appmag,star.bprp)

    targetfilepath=r"binaries/all_stars"
    if os.path.exists(targetfilepath):
        print(f"{targetfilepath} already exists, replace?")
        selected=input_until_valid("Y/N: ",["Y","N"])
        if selected=="N":
            return
        os.remove(targetfilepath)

    with open(targetfilepath, "x"):
        print("newfilecreated")

    with open(targetfilepath, 'ab') as outfile:
        pickle.dump(ALL_STARS,outfile)
    print("data dumped")





if __name__=="__main__":
    start = time.time()
    main()
    print(time.strftime("%H hours %M minutes %S seconds", time.gmtime(time.time() - start)),f" elapsed")

