
from .configsys import Config
from .custdataclasses import *
from PIL import Image,ImageDraw, ImageFont, ImageOps #Pillow library
from .cordinatesys import cordstoxy


def createimg(config:Config):    
    img = Image.new(mode="RGB",size=(config.bg.width,config.bg.height), color=config.bg.fillcolor)
    return img


#for drawing axis
def drawline_single(img,cord1:cord,cord2:cord,width,rgb):
    draw = ImageDraw.Draw(img)
    cordslist=[(cord1.x,cord1.y),(cord2.x,cord2.y)]
    draw.line(cordslist, fill =rgb, width = width)

def drawsingletext_XY(x , y, string,fontsize, img:Image,txtfill,antialius):
    draw=ImageDraw.Draw(img)
    fill=txtfill    
    ImageDraw.ImageDraw.fontmode=antialius
    font = ImageFont.truetype(r'render\static\visuals\fonts\times.ttf', fontsize) 
    draw.text((x,y),string,fill=fill,font=font)





# draw axis
def render_axis(img,config:Config):
    bounds=config.bounds
    
    sx1,sy1,sx2,sy2=[bounds[0].x,bounds[0].y,bounds[1].x,bounds[1].y]

    gridsize=0.5

    # IN X DIR
    for i in range(int((sx2-sx1)//gridsize)):
        sx=i*gridsize+sx1
        
        px1,py1=cordstoxy(cord(sx,sy1),config)
        px2,py2=cordstoxy(cord(sx,sy2),config)
        c1=cord(px1,py1)
        c2=cord(px2,py2)

        width=4 if sx%1==0 else 2
        
        drawline_single(img,c1,c2,width,config.axis.linefill)

        text=str(round(sx,1))
        fontsize=20

        if sx%10==0:
            drawsingletext_XY(px1,py1,text,fontsize,img,config.axis.textfill,config.antialius)
            drawsingletext_XY(px2,py2,text,fontsize,img,config.axis.textfill,config.antialius)
        
    # in Y dir
    for i in range(int((sy2-sy1)//gridsize)):
        sy=i*gridsize+sy1
        
        px1,py1=cordstoxy(cord(sx1,sy),config)
        px2,py2=cordstoxy(cord(sx2,sy),config)
        c1=cord(px1,py1)
        c2=cord(px2,py2)

        width=4 if sy%1==0 else 2
        
        drawline_single(img,c1,c2,width,config.axis.linefill)

        text=str(round(sy,1))
        fontsize=20

        if sy%5==0:
            drawsingletext_XY(px1,py1,text,fontsize,img,config.axis.textfill,config.antialius)
            drawsingletext_XY(px2,py2,text,fontsize,img,config.axis.textfill,config.antialius)



from tqdm import tqdm
# stars



def rgb_to_greyscale(rgb):

    # for avg

    # sum=0
    # for i in rgb:
    #     sum+=i
    # mean=sum//3
    
    # for peak
    mean=max(rgb)

    return (mean,mean,mean)

def tint_img(src:Image, color):
    """tints input image, src png, color rgb"""
    src.load()
    # extract alpha transparency
    r, g, b, alpha = src.split()
    # extract greyscale
    gray = ImageOps.grayscale(src)
    # color by input
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    # apply transparency
    result.putalpha(alpha)
    return result


def placestar(starg:stargraphic,img:Image, center:bool,config:Config):
    basicrender_currstar=config.basicrender
    
    r=starg.radius

    centercord=cord(starg.x,starg.y)
       
    final_rgb=list(starg.rgb)
    grey_rgb=rgb_to_greyscale(final_rgb)
    
    if r<1 and center:
        # do not draw white cores for smallstars
        return

    if r<1:
        # smoothing
        for i in range(3):    
            final_rgb[i] = int(round((r**0.5)*(final_rgb[i])))
        

    # change rgb back to tuple
    final_rgb=tuple(final_rgb)


    # percentage of star radius for white center
    p_s_size = config.stars.whitecore_coef

    # raw adjustment to radius
    
    r =  int(r) + config.stars.raw_r_adj

    # if rendering normal
    if not basicrender_currstar:
        
        star_img_original = config.stars.stargraphic


        if not center:
            star_img=star_img_original.copy()

            star_img = star_img.resize((2*r,2*r))
            star_img=tint_img(star_img,final_rgb)

            # img.paste(star_graphic, top_left_cords ,star_graphic)
            caststar(img,star_img,centercord)

        else:
            # white center
            r_w = round(r* p_s_size)
            wc_img=star_img_original.copy()
            wc_img = wc_img.resize((2*r_w,2*r_w))
            wc_img=tint_img(wc_img,grey_rgb)
            # img.paste(white_center, top_left_cords ,white_center)
            caststar(img,wc_img,centercord)

    # basic render
    else:
        if not center:
            # draw.circle((starg.x,starg.y), radius=starg.radius, fill=final_rgb)
            drawcircle(img,cord(starg.x,starg.y),r,final_rgb)
        else:
            # inner circle
            # draw.circle((starg.x,starg.y), radius=starg.radius*p_s_size, fill=rgb_to_greyscale(final_rgb))
            drawcircle(img,cord(starg.x,starg.y),r*p_s_size,rgb_to_greyscale(final_rgb))

    # debug
    # draw = ImageDraw.Draw(img)
    # draw.circle((starg.x,starg.y), radius=round(max(starg.radius*1.6,7)), width=round(starg.radius*0.4),outline=final_rgb)

import numpy as np

def caststar(bg:Image,img:Image,centercords:cord):
    bgW,bgH = bg.size
    imgW,imgH=img.size

    topleft=cord(centercords.x - (imgW/2),centercords.y - (imgH/2))


    bgarray=bg.load()
    imgarray=img.load()

    for x in (range(imgW)):
        for y in range(imgH):
            color=imgarray[x,y]

            nx=np.clip(x+topleft.x,0,bgW-1)
            ny=np.clip(y+topleft.y,0,bgH-1)

            rgb=((color)[0:3])
            # tuple(list
            a=color[3]/255


            bg_rgb=bgarray[nx,ny]
            
            out = tuple([int(bg_rgb[i]*(1-a) + rgb[i]*a) for i in range(3)])
            
                
            bgarray[nx,ny]=out

def drawcircle(img:Image,center:cord,r,color:tuple):
    W,H = img.size
    img_array=img.load()
    
    cx,cy,r=[round(n) for n in [center.x,center.y,r]]
    r-=1
    for x in range(cx-r,cx+r+1):
        for y in range(cy-r,cy+r+1):
            # mask
            if (x-cx)**2 + (y-cy)**2 <= r**2:
                nx=np.clip(x,0,W-1)
                ny=np.clip(y,0,H-1)
                img_array[nx,ny]=color



def place_list_stars(img:Image,star_graphicinfo_array,config:Config):

    # # place glows
    # print("glows")
    # for starg in tqdm(star_g_items):
    #     placestar(starg,img,False)

    # # place white centers
    # print("centers")
    # for starg in tqdm(star_g_items):
    #     placestar(starg,img,True)

    # new
    
    for starg in tqdm(star_graphicinfo_array):
        placestar(starg,img,False,config)
        placestar(starg,img,True,config)


def saveimg(img):
    # img.save(sys.stdout, "PNG")
    string=f"render/exports/Export{tempfile()}.png"
    # string="v1WesternLOW.png"
    print(f"saved as {string}")
    img.save(string)
    tempfile(1)

def tempfile(n = None):
    filePath = r"render\exports\ref.txt"
    if not n:                      # If not provided return file content
        with open(filePath, "r") as f:
            n = int(f.read())
            return n
    else:
        with open(filePath, "r") as f:
            n = int(f.read())
        with  open(filePath, "a") as f:# Create a blank file
            f.seek(0)  # sets  point at the beginning of the file
            f.truncate()  # Clear previous content
            f.write(f"{n+1}") # Write file
            return n+1



# for constelllations:

def drawtext(ralist : list, declist : list, strlist : list, img:Image,config:Config):
    draw=ImageDraw.Draw(img)
    rl=ralist
    dl=declist
    namelist=strlist

    bounds=config.bounds

    for i in range(len(rl)):
        x=rl[i]
        y=dl[i]

        if x < bounds[0].x or x > bounds[1].x or y<bounds[0].y or y > bounds[1].y:
            continue 

        # x= config.bg.width-int((float(x-bounds[0].x) / (bounds[1].x-bounds[0].x)) * config.bg.width)  # inverted
        # y= int(((float( (y)-bounds[0].y ))/(bounds[1].y-bounds[0].y)) * config.bg.height) 

        x,y=cordstoxy(cord(x,y),config)

        
        name=namelist[i]

        
        ImageDraw.ImageDraw.fontmode=config.antialius
        font = ImageFont.truetype(r'fonts/times.ttf', config.cons.label.labelsize) 
        draw.text((x,y),name,fill = config.cons.label.labelcolor,font=font)


def drawline(xlist,ylist,img,config:Config):

    if config.cons.draw_cons == False:
        return

    draw = ImageDraw.Draw(img)
    consborderRGB=config.cons.consborderRGB
    xl=xlist
    yl=ylist
    cordslist=[]

    bounds=config.bounds

    for i in range(len(xlist)):
        x=xl[i]
        y=yl[i]
        
        # x= config.bg.width-int((float(x-bounds[0].x) / (bounds[1].x-bounds[0].x)) * config.bg.width)  # inverted
        # y= int(((float( (y)-bounds[0].y ))/(bounds[1].y-bounds[0].y)) * config.bg.height) 

        x,y=cordstoxy(cord(x,y),config)
        cordslist.append((x,y))

        # print(cordslist)

    
    
    draw.line(cordslist, fill =consborderRGB, width = config.cons.conslinewidth)