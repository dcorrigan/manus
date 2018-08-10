import os
import sys
import cv2
import argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/..")
from manus.utils import auto_adjust_color, gimp2opencv, write_hsv
from manus.crop import crop


def boundary(arg_string):
    margs = [int(i) for i in arg_string.split(":")]
    return gimp2opencv(np.array(margs))

def white_proportion(img, upper, lower):
    mask = cv2.inRange(img, upper, lower)
    result = cv2.bitwise_and(img, img, mask=mask)
    pixel_count = result.shape[0] * result.shape[1]
    binary = (result == 0).all(2)
    count = np.count_nonzero(binary == True)
    return 1.0 - (count / pixel_count)


def make_mask_proportion(tl, tu, pl, pu):

    def mask_proportion(img):
        text_prop = white_proportion(img, tl, tu)
        page_prop = white_proportion(img, pl, pu)
        print("*************")
        print("text: {}".format(text_prop))
        print("page: {}".format(page_prop))

        total = text_prop + page_prop
        avg = (text_prop + page_prop) / 2
        result = total * avg

        print("result: {}".format(result))

        return result

    return mask_proportion


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="the file to crop")
parser.add_argument(
    "-tl",
    "--text_lower",
    help="HSV lower bound for text",
    type=boundary,
    default=np.array([0, 0, 0]),
)
parser.add_argument(
    "-tu",
    "--text_upper",
    help="HSV upper bound for text",
    type=boundary,
    default=np.array([180, 255, 153]),
)
parser.add_argument(
    "-pl",
    "--page_lower",
    help="HSV lower bound for page",
    type=boundary,
    default=np.array([140, 0, 191]),
)
parser.add_argument(
    "-pu",
    "--page_upper",
    help="HSV upper bound for page",
    type=boundary,
    default=np.array([180, 76, 255]),
)

args = parser.parse_args()

image_rgb = cv2.imread(args.input_file)
image = auto_adjust_color(image_rgb)
im_name = os.path.basename(args.input_file)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mp_func = make_mask_proportion(
    args.text_lower, args.text_upper, args.page_lower, args.page_upper
)
crops = crop(hsv_image, mp_func, splits=4, threshold_mult=1.1, debug=True)

path = "output/{}".format(im_name)
cv2.imwrite(path, image_rgb[crops[0]:crops[1], crops[2]:crops[3]])
