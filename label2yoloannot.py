# Adapted label2det.py from https://github.com/ucbdrive/bdd-data to prepare annotations for YOLO v3 training via Darknet

import argparse
import json
import os
from os import path as osp
import sys


def parse_args():
    # not used specifically in this implementation; label2det.py helper function 
    """Use argparse to get command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('label_dir', help='path to the label dir')
    parser.add_argument('det_path', help='path to output detection file')
    args = parser.parse_args()

    return args

def cat_int_id(cat):
    # new function
    """Map string category to integer id. Return id."""
    cats = {'bike': 0,'bus': 1,'car': 2,'motor': 3,'person': 4,'rider': 5, 
            'traffic light': 6, 'traffic sign': 7, 'train': 8, 'truck': 9}
    id = cats[cat]
    return id

def ftis(float):
    # new function
    """Converts number from float to int to string."""
    integer = int(round(float))
    return str(integer)

def y_mod(float):
    # new function 
    """Convert numbers to YOLO input format. Assumes y-coord as input. 
    1. Crops y-coords to be in (8, 711) inclusive range
    2. Converts float to strings."""
    y = float
    
    if (y < 8):
        y = 8
    elif (y > 711):
        y = 711
    
    #if (y != float):
        #print('Previous y: ' + str(float) + ', new y: ' + str(y))
    
    new_y = str(y)
    return new_y

def crop_coord(float):
    # new function 
    """Convert numbers to YOLO input format. Assumes y-coord as input. 
    Crops y-coords to be in (8, 711) inclusive range.
    """
    y = float
    
    if (y < 8):
        y = 8
    elif (y > 711):
        y = 711
    
    #if (y != float):
        #print('Previous y: ' + str(float) + ', new y: ' + str(y))
        
    return y
    

def label2annot(label):
    # adapted function from label2det.py
    """ Creates annotation
    1. adds class id and box coordinates 
    2. concatenates as string 
    """
    # hardcoded values for BDD images, TO-DO: make function input
    im_width = 1280
    im_height = 704
    
    box = ''
    for frame in label['frames']:
        for obj in frame['objects']:
            if 'box2d' not in obj:
                continue
            xy = obj['box2d']
            if xy['x1'] >= xy['x2'] and xy['y1'] >= xy['y2']:
                continue
            
            # adaption for YOLO annotation
            cat = obj['category']
            cat_id = cat_int_id(cat)
            box += str(cat_id)
            
            x1 = xy['x1']
            x2 = xy['x2']
            y1 = crop_coord(xy['y1'])
            y2 = crop_coord(xy['y2'])
            
            abs_width = round(x2 - x1 + 1, 6)
            abs_height = round(y2 - y1 + 1, 6)
            
            abs_x = x1 + (abs_width/2) # absolute center x
            abs_y = y1 + (abs_height/2) # absolute center y
            
            x = round(abs_x/im_width, 6)
            y = round(abs_y/im_height, 6)
            width = round(abs_width/im_width, 6)
            height = round(abs_height/im_height, 6)
            
            box += ' ' + str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n'
    return box


def make_annotations(label_dir, imgs_dir, path_to_darknet):
    # adapted change_dir function from label2d.py
    """Prepare text files for Darknet YOLO training. 
    1. Creates and writes to 'train.txt' with paths to images. Saved in darknet .../data/ dir. 
    2. Creates corresponding '.txt' file for each image with the annotations. Saved in same dir as images."""
    
    if not osp.exists(label_dir):
        print('Can not find', label_dir)
        return
    print('Processing', label_dir)
    input_names = [n for n in os.listdir(label_dir)
                   if osp.splitext(n)[1] == '.json']
    
    count = 0
    train_file = open(path_to_darknet + 'build/darknet/x64/data/train.txt', 'w+')
    for name in input_names:
        root_name = os.path.splitext(name)[0]
        
        # create new file to write to
        f_name = imgs_dir + root_name + '.txt'
        f = open(f_name, 'w+')
        
        # read label and convert to annotation, writing to file
        in_path = osp.join(label_dir, name)
        out = label2annot(json.load(open(in_path, 'r')))
        f.write(out) 
        
        # write image path to train.txt
        train_file.write(imgs_dir + root_name + '.jpg\n')
        
        count += 1
        if count % 1000 == 0:
            print('Finished', count)


def main():
    # args = parse_args()
    label_dir = 'PATH_TO_JSON_FILES'
    imgs_dir = 'PATH_TO_IMAGES'
    path_to_darknet = 'PATH_TO_DARKNET' # from https://github.com/AlexeyAB/darknet 
    make_annotations(label_dir, imgs_dir, path_to_darknet)


if __name__ == '__main__':
    main()
