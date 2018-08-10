import matplotlib
matplotlib.use("Agg")
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
from scipy.ndimage import measurements, generate_binary_structure, binary_dilation


def crop(
    image,
    test_func,
    splits=64,
    threshold_mult=1.4,
    dilate=1,
    debug=False,
    debug_title=lambda r: round(r, 4),
):
    score = test_func(image)
    threshold = score * threshold_mult
    height_unit = int(image.shape[0] / splits)
    width_unit = int(image.shape[1] / splits)

    def grid_subsection(t, l):
        top = t * height_unit
        left = l * width_unit
        return image[top:(top + height_unit), left:(left + width_unit)]

    results_coll = np.ndarray(shape=(splits, splits))

    if debug:
        debug_fig, debug_axes = plt.subplots(
            nrows=splits, ncols=splits, sharex=True, sharey=True
        )

    # print to a map where we can measure difference
    for ttb in range(0, splits):
        for rtl in range(0, splits):
            section = grid_subsection(ttb, rtl)
            rate = test_func(section)
            results_coll[ttb, rtl] = rate

            if debug:
                tile = debug_axes[ttb][rtl]
                tile.imshow(section)
                tile.set_title(debug_title(rate))
                tile.axis("off")

    if debug:
        plt.tight_layout()
        plt.savefig("debug.png")

    binary = results_coll > threshold
    for _n in range(dilate):
        binary = binary_dilation(binary)

    struct = generate_binary_structure(2,2)
    # applies numeric labels to contiguous clusters of True values
    labeled_arr, _num_features = measurements.label(binary, structure=struct)
    # determines the area of every labeled cluster
    cluster_sizes = measurements.sum(binary, labeled_arr, index=np.arange(labeled_arr.max() + 1))
    # finds the cluster label with the greatest area
    label = cluster_sizes.argmax()
    # returns the coordinates for every tile within the largest cluster
    indices = np.where(labeled_arr == label)

    # find the outermost perimeter of the cluster
    top_edge = indices[0].min()
    bottom_edge = indices[0].max()
    left_edge = indices[1].min()
    right_edge = indices[1].max()

    top = top_edge * height_unit
    bottom = (bottom_edge * height_unit) + 1 # add one to make it inclusive for numpy slice
    left = left_edge * width_unit
    right = (right_edge * width_unit) + 1 # add one to make it inclusive for numpy slice

    return (top, bottom, left, right)
