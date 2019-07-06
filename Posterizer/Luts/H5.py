'''
A little bit of code I wrote to make a 4*8*32 lut (2^5, 32^3) possible.

The Unlicense

 love, 
     -J

'''
from PIL import Image

hald_5 = Image.new('RGB', (256, 128))
hald_data = hald_5.load()
width, height = hald_5.size

for x in range(width):
    for y in range(height):
        hald_data[x, y] = ((x %32) * 8,(y %32) * 8, (x %32) + int(y / 32) * 64)

print(hald_data[-1, -1])
print(hald_data[0, 0])
hald_5.show()
