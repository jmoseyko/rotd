import os
from PIL import Image

def crop(images_path, images_out_path):
    """Crop BDD 1280 x 720 img to 1280 x 704 img (mult. of 32). TO-DO: add dimensions in as input."""
    
    for img in os.listdir(images_path):
        if img.endswith('.jpg'):
            image = Image.open(images_path + img)
            w, h = image.size
            cropped_image = image.crop((0, 8, w, h-8))
            cropped_image.save(images_out_path + img)
        else:
            continue

if __name__ == '__main__':
    images_path = 'IMAGES_DIR'
    images_out_path = 'OUT_DIR' # existing directory
    crop(images_path, images_out_path) 

