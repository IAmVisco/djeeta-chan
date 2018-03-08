from os import listdir, getcwd
from os.path import isfile, join
import sys
from PIL import Image, ImageFont, ImageDraw

folder = input("Folder with emotes: ")

pics = [getcwd() + "\\" + folder + "\\" + f for f in listdir(getcwd() + "\\" + folder)]

images = map(Image.open, pics)

width = 1800
height = (len(pics)//12 - 1) * 160

new_im = Image.new('RGBA', (width, height), (0,0,0))
draw = ImageDraw.Draw(new_im)
font = ImageFont.truetype("arial.ttf", 16)

x_offset = 0
y_offset = 0
ctr = 0
for im in images:
	image_name = str(im.fp.name)
	new_im.paste(im.resize((120,120), Image.ANTIALIAS), (x_offset,y_offset))
	draw.text((x_offset, y_offset + 130), image_name.split("\\")[-1], (255,255,255), font = font)
	ctr += 1
	if ctr > 12:
		ctr = 0
		y_offset += 160
		x_offset = 0
	else:
		x_offset += 150

new_im.save(getcwd() + '\\' + folder + '.png')