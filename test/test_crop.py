import numpy as np
import cv2

from manos.crop import crop

# this is a hard-coded (4,4,3) numpy array that mimics a boolean
# image with a "center" area; should crop to a (2,2,3) image
_FIXTURE_DATA = np.array(
   [
       [[ False,  False,  False],
        [ False,  False,  False],
        [ False,  False,  False],
        [ False, False, False]],

       [[False, False, False],
        [True, True, True],
        [True, True, True],
        [False, False, False]],

       [[False, False, False],
        [True, True, True],
        [True, True, True],
        [False, False, False]],

       [[False, False, False],
        [False, False, False],
        [False, False, False],
        [False, False, False]]
    ]
)

def binary_crop_func(img):
    if img.all():
        return 1
    else:
        return 0.1

def test_basic_crop():
    crops = crop(_FIXTURE_DATA, binary_crop_func, splits=4, threshold_mult=1, backoff=False)
    assert crops == (1, 3, 1, 3)

def white_proportion_crop(img):
    count = np.sum(np.all(img > 225, axis=2))
    size = img.shape[0] * img.shape[1]
    return count / size

def test_white_proportion_crop():
    image = cv2.imread("test/fixtures/books.jpg")
    # crazy overfit example
    crops = crop(image, white_proportion_crop, splits=32, threshold_mult=0.24)
    assert crops == (152, 837, 336, 1153)
