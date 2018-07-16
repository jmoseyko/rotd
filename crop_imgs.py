"""help from https://dzone.com/articles/how-to-crop-a-photo-with-python and
https://stackoverflow.com/questions/9983263/crop-the-image-using-pil-in-python"""

import os
from PIL import Image

def crop(images_path, images_out_path):
    """crop BDD 1280 x 720 img to 1280 x 704 img (mult. of 32)"""
    
    for img in os.listdir(images_path):
        if img.endswith('.jpg'):
            image = Image.open(images_path + img)
            w, h = image.size
            cropped_image = image.crop((0, 8, w, h-8))
            cropped_image.save(images_out_path + img)
        else:
            continue

if __name__ == '__main__':
    images_path = '/Users/julia/bddsamplejson/images/'
    images_out_path = '/Users/julia/bddsamplejson/images/cropped-images/'
    crop(images_path, images_out_path) 

