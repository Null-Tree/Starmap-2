





import PIL
from PIL import Image,ImageDraw, ImageFont,ImageOps #Pillow library

import numpy as np
from dataclasses import dataclass

@dataclass
class cord2:
    x:float
    y:float


def createimg(height:int,width:int,colour:tuple):
    img = Image.new(mode="RGB",size=(width,height), color=colour)
    return img


# def cast(img:Image):
#     img_width,img_height=img.size
    
#     for x in range(img_width):
#         for y in range(img_height):
#             colour=img[x][y]

def clip(v,min,max):
    """clip also np.clip, such that -9 into [0,10] will +10 into 1"""
    # if not in bounds
    p=max-min
    d=max-v
    r=d%p
    v=max-r
    return v



def proj_cords(x,y,width,height):
    norm_x = x / (width - 1)
    norm_y = y / (height - 1)

    # Convert to spherical coordinates (longitude phi, latitude theta)
    # Phi ranges from -pi to pi, theta from -pi/2 to pi/2
    phi = (norm_x * 2 * np.pi) - np.pi
    theta = (norm_y * np.pi) - (np.pi / 2)

    # Example: Simple direct mapping (will show distortion)
    # Adjust these calculations based on your desired projection
    texture_x = int(((phi + np.pi) / (2 * np.pi)) * (width - 1))
    texture_y = int(((theta + (np.pi / 2)) / np.pi) * (height - 1))

    # Clamp coordinates to ensure they are within the texture bounds
    texture_x = np.clip(texture_x, 0, width - 1)
    texture_y = np.clip(texture_y, 0, height - 1)

    return texture_x,texture_y


from tqdm import tqdm

def cast(bg:Image,img:Image):
    bgW,bgH = bg.size

    imgW,imgH=img.size

    bgarray=bg.load()
    imgarray=img.load()

    for x in tqdm(range(imgW)):
        for y in range(imgH):
            color=imgarray[x,y]

            nx,ny=proj_cords(x,y,bgW,bgH)
            # print(nx,ny)
            print(color)
            bgarray[nx,ny]=color