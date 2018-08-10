import os
import sys
import cv2
import argparse

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/..")
from manus.utils import auto_adjust_color, gimp2opencv, write_hsv
from manus.crop import crop
from manus.quantifiers import contrast_entropy
from cli import base_parser, ImageIO, crop_args


def preprocess_image(image):
    image = auto_adjust_color(image)
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def process_image(args):
    io = ImageIO(args)
    hsv = preprocess_image(io.content)
    crops = crop(hsv, contrast_entropy, **crop_args(args))
    io.write_output(io.content[crops[0]:crops[1], crops[2]:crops[3]])


if __name__ == "__main__":
    parser = base_parser()
    args = parser.parse_args()
    process_image(args)
