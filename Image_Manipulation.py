from PIL import Image, ImageFont, ImageDraw 
import numpy as np
import img2pdf
import os

def make_images(range_in_focus):
	for row in range_in_focus:
		#190x920px
		img = Image.open('mid-template.png')

		#width, height = img.size
		#print(height, width)

		colors_dict={'red': (255,0,0), 'orange':(255,165,0), 'blue':(0,0,255), 'green':(0,255,0), 'yellow':(255,255,0), 'white':(255,255,255)}

		def index_to_gridindex(i):  #staring from 0
			hrs_index = i//4
			min_index = i%4
			return {'x':hrs_index, 'y':min_index}

		x0=248
		y0=1
		x_diff=25
		y_diff=23
		x_border = y_border = 3
		for i in range(96):
			xgi = index_to_gridindex(i)['x']  #x grid index
			ygi = index_to_gridindex(i)['y']  #y grid index
			x_start = x0 + xgi*(x_diff+x_border)
			y_start = y0 + ygi*(y_diff+y_border)

			color = row[i+1] #Since first element is date
			
			for y in range(y_start, y_start+y_diff):
				for x in range(x_start, x_start+x_diff):
					img.putpixel( (x,y), colors_dict[color])
		
		img.save(rel_path(row[0]+'.png'))			

def rel_path(x):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = f"pdf-pics-temp/{x}"
		abs_file_path = os.path.join(script_dir, rel_path)
		return abs_file_path

def concat_images(range_in_focus):
	im_pages=[]
	images = [Image.open(rel_path(x[0]+'.png')) for x in range_in_focus]
	for i in range(0, len(images), 7):
		head = Image.open("head.png")

		batch = [head] + images[i:i+7]
		widths, heights = zip(*(i.size for i in batch))

		max_width = max(widths)
		total_height = sum(heights)

		new_im = Image.new('RGB', (max_width, total_height))

		y_offset = 0
		for im in batch:
		  new_im.paste(im, (0, y_offset))
		  y_offset += im.size[1]

		im_pages.append(new_im)
	for x in im_pages:
		print(x)
	im_pages[0].save('result.pdf', "PDF", save_all=True)
	for im in im_pages[1:]:
		im.save('result.pdf', "PDF", save_all=True, append=True)

'''
for y in range(84,106):
    for x in range(248,273):
        img.putpixel( (x,y), new_color)

for y in range(84,106):
    for x in range(276,301):
        img.putpixel( (x,y), new_color)   

for y in range(109,132):
    for x in range(248,273):
        img.putpixel( (x,y), new_color)             
'''
