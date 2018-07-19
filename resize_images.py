import os
from os import path as osp
from PIL import Image

def crop(images_path, images_out_path, width, height):
    """Resize BDD 1280 x 720 img to width x height given as arguments."""
    
    for img in os.listdir(images_path):
        if img.endswith('.jpg'):
            image = Image.open(osp.join(images_path, img))
            w, h = image.size
            new_image = image.resize((width, height), Image.ANTIALIAS)
            new_image.save(osp.join(images_out_path, img))
        else:
            continue

if __name__ == '__main__':
    images_path = '/Users/julia/bddsamplejson/images'
    images_out_path = '/Users/julia/bddsamplejson/images/resized-images' # existing directory
    width = 416
    height = 416
    crop(images_path, images_out_path, width, height) 

