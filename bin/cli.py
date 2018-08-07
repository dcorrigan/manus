import os
import argparse
import cv2


def base_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the file to crop")
    parser.add_argument("-o", "--output", help="the output file")
    parser.add_argument(
        "-t",
        "--tiles",
        help="the numbers of tiles to apply when cropping",
        type=int,
        default=64,
    )
    parser.add_argument("-d", "--debug", help="print debugging figure", action='store_true')
    return parser


def crop_args(args):
    return {"debug": args.debug, "splits": args.tiles}


class ImageIO():

    def __init__(self, args):
        self.args = args
        self.image_name = os.path.basename(args.input_file)
        self.content = cv2.imread(self.args.input_file)

    @property
    def output(self):
        return self.args.output or "output/{}".format(self.image_name)

    def write_output(self, image):
        cv2.imwrite(self.output, image)
        return True
