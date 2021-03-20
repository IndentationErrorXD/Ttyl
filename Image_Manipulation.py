from PIL import Image, ImageFont, ImageDraw 
import numpy as np

#188x920px
img = Image.open('Template.png')

width, height = img.size
print(height, width)

new_color = (255,0,0)



'''for y in range(84,106):
    for x in range(248,273):
        img.putpixel( (x,y), new_color)

for y in range(84,106):
    for x in range(276,301):
        img.putpixel( (x,y), new_color)   

for y in range(109,132):
    for x in range(248,273):
        img.putpixel( (x,y), new_color)      

for y in range(84,106):
    for x in range(333,358):
        img.putpixel( (x,y), new_color) '''              

img.show()