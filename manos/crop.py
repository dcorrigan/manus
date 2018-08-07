import matplotlib
matplotlib.use("Agg")
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools


def crop(
    image,
    test_func,
    splits=64,
    threshold_mult=1.4,
    backoff=True,
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

    def working_tiers(matrix):
        return [index for index, tier in enumerate(matrix) if tier.mean() > threshold]

    def continuous_ranges(arr):
        uniq = []
        for k, g in itertools.groupby(enumerate(arr), key=lambda iv: iv[0] - iv[1]):
            uniq.append([j for i, j in g])
        return uniq

    def corner(arrs):
        for arr in arrs:
            if len(arr) > round(splits * 0.1):
                return arr[0]

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


    rows = continuous_ranges(working_tiers(results_coll))
    top_edge = corner(rows) or 0
    bottom_edge = corner([list(reversed(i)) for i in reversed(rows)]) or splits - 1

    cols = continuous_ranges(working_tiers(results_coll.T))
    left_edge = corner(cols) or 0
    right_edge = corner([list(reversed(i)) for i in reversed(cols)]) or splits - 1

    top = top_edge * height_unit
    bottom = (bottom_edge * height_unit) + 1 # add one to make it inclusive for numpy slice
    left = left_edge * width_unit
    right = (right_edge * width_unit) + 1 # add one to make it inclusive for numpy slice

    if backoff:
        if top != 0:
            top -= height_unit
        if bottom != 0:
            bottom += height_unit
        if left != 0:
            left -= width_unit
        if right != 0:
            right += width_unit

    return (top, bottom, left, right)
