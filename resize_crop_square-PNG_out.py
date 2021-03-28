# This script loops through all image files in a directory called "input",
# and converts, resizes and crops them and saves them as JPGs in a directory
# called "output"
#
# Script author: Blake Fall-Conroy, with some augmentation by Doug Rosman

from PIL import Image, ImageOps
import pathlib

width = 1024
height = 1024
good_filetypes = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".tif", ".TIF", ".tiff", ".TIFF", ".gif", ".GIF") 
dpi = 72
output_name = "img"
img_count = 0

#iterate through input path (relative)
for input_img_path in pathlib.Path("input").iterdir():
    #relative output path
    output_img_path = str(input_img_path).replace("input","output")
    
    #only process image files
    myPath = str(input_img_path)
    if myPath.endswith(good_filetypes):

        #open image
        with Image.open(input_img_path) as im:
            # check if "P", "RGBA" or "CMYK" so we can convert to RGB
            if im.mode in ["CMYK"]:
                im = im.convert('RGB')
            # if "P", convert to "RGBA" first
            if im.mode in ["P"]:
                im = im.convert('RGBA')
            if im.mode in ["RGBA"]:
                # the default im.convert('RGB') doesn't do a good job dealing
                # with transparency. It replaces the alpha channel with a black
                # background, and creates jagged edges around objects.
                # here, we "paste" the RGBA image onto a new all-white RGB
                # image, which results in much better JPG outputs
                background = Image.new("RGB", im.size, (255, 255, 255))
                background.paste(im, mask=im.split()[3])
                im = background
            #fit to size and center crop
            im = ImageOps.fit(im, (width, height), method = 0, 
                    bleed = 0.0, centering =(0.5, 0.5))
            # im = PIL.Image.fromarray(img, { 1: 'L', 3: 'RGB' }[channels])
            #save as uncompressed png
            img_count_str = f'{img_count:06d}'
            im.save("output/" + output_name + img_count_str + ".png", format='png', compress_level=0, optimize=False)
            print(f"processing file {input_img_path} done...")
            img_count += 1
