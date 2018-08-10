import numpy as np
import scipy.stats as stats


# must be a binary image
def edge_proportion(edges):
    uniq, counts = np.unique(edges, return_counts=True)
    counts = dict(zip(uniq, counts))
    pix = counts.get(True, 0)
    return pix / (edges.shape[0] * edges.shape[1])


# must be a colorspace that has a value channel
def contrast_entropy(img, value_channel=0):
    channel = img[:, :, value_channel]
    hist, bins = np.histogram(channel, bins=256)
    return stats.entropy(hist)
