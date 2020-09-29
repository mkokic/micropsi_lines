#!/usr/bin/env python3
import numpy as np
from PIL import Image
import os
from IPython import embed


def line_params(x1, y1, x2, y2):
    # For vertical line compute only points on y-axis
    if x1 == x2:
        points = np.array([np.ones(abs(y2 - y1) + 1, ) * x1,
                           np.linspace(y1, y2, abs(y2 - y1) + 1)]).astype(np.int64)

    # For all the other cases compute slope and intercept
    else:
        # Slope
        a = (y2 - y1) / (x2 - x1)
        # Inctercept
        b = y1 - a * x1

        # Generate points on a line
        xs = np.linspace(x1, x2, abs(x2 - x1) + 1)
        points = np.array([xs, a * xs + b]).astype(np.int64)
    return points


class LineDraw(object):
    def __init__(self):
        # Load an image from the data folder
        self.path = os.path.dirname(__file__) + '/data/'
        self.img = Image.open(self.path + 'mpsi_task.png').convert("RGB")

        # Extract pixels coordinates
        self.pix_coords = self.get_pix(self.img)
        # Compute lines connecting the pixels
        self.lines = self.compute_lines(self.pix_coords)
        # Draw the lines on the input image and save
        self.img_out = self.draw_lines(self.img, self.lines)

    @staticmethod
    def get_pix(img):
        # Get coordinates of the red, green and blue pixel
        rgb_vals = (np.eye(3) * 255).astype(np.uint8)
        pix_coords = np.array(
            [list(divmod([i for i, pixel in enumerate(img.getdata()) if pixel == tuple(col)][0], img.size[0])) for col
             in rgb_vals]).reshape(3, 2)

        return pix_coords

    @staticmethod
    def compute_lines(pix_coords):
        # Get coordinates of the three pixels
        x1, y1 = pix_coords[0, 0], pix_coords[0, 1]
        x2, y2 = pix_coords[1, 0], pix_coords[1, 1]
        x3, y3 = pix_coords[2, 0], pix_coords[2, 1]

        # Generate points on the lines connecting three pixels
        points_r2g = line_params(x1, y1, x2, y2)
        points_g2b = line_params(x2, y2, x3, y3)
        points_r2b = line_params(x1, y1, x3, y3)
        lines = np.concatenate((points_r2g, points_g2b, points_r2b), 1)

        return lines

    # Draw the lines on the input image
    def draw_lines(self, img, lines):
        img_arr = np.array(img)
        img_arr[lines[0], lines[1], :] = [255, 255, 255]
        img_out = Image.fromarray(img_arr, 'RGB')
        # Save the new image
        img_out.save(self.path + 'mpsi_task_out.png')

        return img_out


if __name__ == '__main__':
    LineDraw()
