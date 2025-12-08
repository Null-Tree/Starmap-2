
from imagehandeling import *

import PIL
from PIL import Image,ImageDraw, ImageFont,ImageOps #Pillow library

resolution=1080

img=createimg(resolution,resolution*2,(0,0,0))



bird=Image.open(r"panaramic_rending\assets\testbird.png")
birdsize=30
# img.paste(bird,(100,100))


cast(bird,img)
img.show()


