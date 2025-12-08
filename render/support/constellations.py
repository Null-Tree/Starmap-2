import numpy as np
import json
from tqdm import tqdm
from .math_sp import *


import astropy.units as u
import astropy.time
import astropy.coordinates

from .imaging import *

horizontalshift=0

def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))
    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord




# 24 hour
def wrapped_line(ra,de): #numpy arrays
    # [23.63561223  0.30546109] [43.26807662 36.78522667] * pi. And * del And
    # takes an ra,dec pair and creates two new lines crossing 00:00-24:00 to join them
    # assumes Cartesian 2-D plot
    ra_new = np.zeros(4)
    de_new = np.zeros(4)
    ra_new[0] = ra[0]
    de_new[0] = de[0]
    ra_new[3] = ra[1]
    de_new[3] = de[1]
    if ra[0] > 12.0:
        ra_new[1] = 24.0
        de_new[1] = de[0] + (24.0-ra[0])/((ra[1]+24)-ra[0]) * (de[1]-de[0])
        ra_new[2] = 0.0
        de_new[2] = de[0] + (24.0-ra[0])/((ra[1]+24)-ra[0]) * (de[1]-de[0])
    else:
        ra_new[1] = 0.0
        de_new[1] = de[0] - (0.0-ra[0])/(ra[1]-ra[0]) * (de[1]-de[0])
        ra_new[2] = 24.0
        de_new[2] = de[0] - (0.0-ra[0])/(ra[1]-ra[0]) * (de[1]-de[0])
    
    

    return ra_new, de_new

def get_ra_dec(starname,identity,ra,de):
    #print(list(identity))
    index = list(identity).index(starname.strip())
    return ra[index], de[index]

def handleconsjson(jsonfile,txtfile,img,config:Config):
    namelist=[]
    ralist=[]
    declist=[]
    cord_mode=config.cord_mode


    # open list of stars with coordinates
    identity, ra_dec = np.loadtxt(txtfile,usecols=(1,5),delimiter='|',unpack=True,dtype=str)
    # print(ra_dec)
    for i in range(len(identity)):
        identity[i] = identity[i].strip()
    Nstars = len(ra_dec)
    ra = np.zeros(Nstars)
    de = np.zeros(Nstars)
    for i in range(len(ra_dec)):
        ra[i] = float(ra_dec[i].split()[0])
        de[i] = float(ra_dec[i].split()[1])
        
    # Opening JSON file
    f = open(jsonfile)        #       'csv/iau.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Iterating through the json list need
   
    for constellation in tqdm(data['constellations']): 
        cross=False
        
        

        n,rasum_l,decsum_l=0,[],[]
        
        constellationName = constellation['names'][0]['english']
        namelist.append(constellationName)

        this_lines = constellation['lines']
        # print(this_lines)
        # 
        for line in range(len(this_lines)):
            stars = this_lines[line]
            this_line_ra = np.zeros(len(stars)) 
            this_line_de = np.zeros(len(stars))
            
            for star in range(len(stars)):
                this_line_ra[star], this_line_de[star] = get_ra_dec(stars[star],identity,ra,de)

                # print(this_line_ra[star], this_line_de[star])
                this_line_ra[star] /= 15.0  #rn tlra inhours, tlde in degrees

                if cord_mode =="galactic":
                    #needs tobe deg in deg out
                    cord=equatorialtogalactic(this_line_ra[star] * 15,this_line_de[star])
                    this_line_ra[star]=cord.l.deg /15 # needs to be in hours for later comparison
                    vvx=this_line_ra[star]
                    this_line_ra[star]=wrap(vvx+0,0,24)
                    this_line_de[star]=cord.b.deg


            for i in range(len(this_line_ra)-1):
                if abs(this_line_ra[i+1]-this_line_ra[i])<12:
                    
                    #pass
                    finalra = ra2deg(this_line_ra)
                    # finalra=this_line_ra
                    # print(finalra)
                    for j in range(len(finalra)):
                        n+=1
                        rasum_l.append(finalra[j])
                        decsum_l.append(this_line_de[j])

                    
                    drawline(finalra[i:i+2],this_line_de[i:i+2],img,config)
                else:
                    # print(this_line_ra[i:i+2], this_line_de[i:i+2], stars[star-1], stars[star])
                    cross=True
                    ra_new, de_new = wrapped_line(this_line_ra[i:i+2], this_line_de[i:i+2])
                    
                    finalra=ra2deg(ra_new)
                    # finalra=ra_new
                    #condition for edge


                    drawline(finalra[0:2], de_new[0:2],img,config)
                    drawline(finalra[2:4], de_new[2:4],img,config)
                #TODO: get a position
        
        # check if cross boundaries


        # if len(rasum_l)==0
        


        if not cross:

            ramean=((sum(rasum_l)/n))

            decmean= ((sum(decsum_l)/n))

            # print(f"ra {ramean} de {decmean}")
            ralist.append(ramean)
            declist.append(decmean)
        else:
            # print(f"{constellationName} crosses broder")
            

            rasum_l.sort()

            # print(rasum_l)

            ral1,ral2=[],[]
            decl1,decl2=[],[]

            for i in range(len(rasum_l)):
                j=rasum_l[i]

                if j<180:
                    ral1.append(j)
                    decl1.append(decsum_l[i])
                else:
                    ral2.append(j)
                    decl2.append(decsum_l[i])

            # print(cross, ral1,ral2)
            ralist.append(  sum(ral1) / len(ral1) )
            declist.append( sum(decl1) / len(decl1) )


            namelist.append(constellationName)
            ralist.append(sum(ral2) / len(ral2))
            declist.append(sum(decl1) / len(decl1))

            
    
    
    if config.cons.label.label:
        drawtext(ralist,declist,namelist,img,config)
  

    # Close file
    f.close()

def ra2deg(ra:list):
    """converts list of hours cords to degrees"""
    list=ra
    result=[0 for i in range(len(list))]
    for i in range(len(list)):
        result[i]=float(list[i])/24*360
    return result

#================================