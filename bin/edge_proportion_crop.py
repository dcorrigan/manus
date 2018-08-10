import os
import sys
import cv2
import numpy as np
from skimage import feature
from skimage.color import rgb2gray
from skimage.filters import threshold_mean

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/..")
from manos.utils import auto_adjust_color
from manos.quantifiers import edge_proportion
from manos.crop import crop

from cli import base_parser, ImageIO, crop_args


def preprocess_image(image):
    image = auto_adjust_color(image)
    image = rgb2gray(image)
    thresh = threshold_mean(image)
    binary = image > thresh
    return feature.canny(binary, sigma=0.29)


def process_image(args):
    io = ImageIO(args)
    binary_img = preprocess_image(io.content)
    crops = crop(binary_img, edge_proportion, threshold_mult=2.5, dilate=1, **crop_args(args))
    io.write_output(io.content[crops[0]:crops[1], crops[2]:crops[3]])


if __name__ == "__main__":
    parser = base_parser()
    args = parser.parse_args()
    process_image(args)
