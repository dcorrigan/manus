from math import sqrt
import cv2

def write_hsv(path, img):
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_HSV2RGB))

# opencv represents HSV like this:
# H: 0 - 180, S: 0 - 255, V: 0 - 255

# gimp represents HSV like this:
# H = 0-360, S = 0-100 and V = 0-100

def gimp2opencv(arr):
    arr[0] = int(arr[0] / 360 * 180)
    arr[1] = int(arr[1] / 100 * 255)
    arr[2] = int(arr[2] / 100 * 255)
    return arr

def opencv2gimp(arr):
    arr[0] = arr[0] * 2
    arr[1] = int(arr[1] / 255 * 100)
    arr[2] = int(arr[2] / 255 * 100)
    return arr


# equalize rgb histogram
def auto_adjust_color(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)


# limit 1 and limit 2 are width and height (answers must fit a rectangle
# smaller than the width and height) and area of the area to get valid factors
# for


def image_area_factors(l1, l2, area):
    collect = []
    for i in range(1, int(sqrt(area)) + 1):
        if area % i == 0:
            j = area // i
            if (i <= l1 and j <= l2) or (j <= l1 and i <= l2):
                collect.append((i, j))
    return collect


# given, say, a 4x4 grid, how many valid, smaller sizes can fit within it


def smaller_sizes(l1, l2):
    collect = set()
    for i in range(1, l1):
        for j in range(1, l2):
            collect.add(((l1 - i), l2))
            collect.add((l2, (l1 - i)))
            collect.add(((l2 - j), l1))
            collect.add((l1, (l2 - j)))
            collect.add(((l2 - j), (l1 - i)))
            collect.add(((l1 - i), (l2 - j)))
    l = list(collect)
    l.sort(key=lambda p: p[0]*p[1])
    l.reverse()
    return l


def possible_positions_for_size(width, height, l1, l2):
    collect = set()

    def _iter(ch, cw):
        for i in range(0, cw + 1):
            ltr = i + cw
            if ltr > width:
                break

            for j in range(0, ch + 1):
                ttb = j + ch
                if ttb > height:
                    break

                collect.add((i, ltr, j, ttb))

    _iter(l1, l2)
    _iter(l2, l1)
    return collect
