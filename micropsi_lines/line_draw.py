#!/usr/bin/env python3
import numpy as np
from PIL import Image


def slope_intercept(x1, y1, x2, y2):
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


class LineDraw(object):
    def __init__(self):
        self.path = '../data/'
        self.img = Image.open(self.path + 'mpsi_task.png').convert("RGB")
        self.pix_coords = self.get_pix(self.img)
        self.draw_lines()

    @staticmethod
    def get_pix(img):
        rgb_vals = (np.eye(3) * 255).astype(np.uint8)
        pix_coords = np.array(
            [list(divmod([i for i, pixel in enumerate(img.getdata()) if pixel == tuple(col)][0], img.size[0])) for col
             in rgb_vals]).reshape(3, 2)
        return pix_coords

    def draw_lines(self):
        x1, y1 = self.pix_coords[0, 0], self.pix_coords[0, 1]
        x2, y2 = self.pix_coords[1, 0], self.pix_coords[1, 1]
        x3, y3 = self.pix_coords[2, 0], self.pix_coords[2, 1]

        # Compute a line between the first (red) and the second (green) dot
        self.slope_r2g, self.intercept_r2g = slope_intercept(x1, y1, x2, y2)
        x_r2g = np.linspace(x1, x2, abs(x2 - x1) + 1)
        self.line_r2g = np.array([x_r2g,
                                  self.slope_r2g * x_r2g + self.intercept_r2g]).astype(np.int64)

        # Compute a line between the second (green) and the third (blue) dot
        self.slope_g2b, self.intercept_g2b = slope_intercept(x2, y2, x3, y3)
        x_g2b = np.linspace(x2, x3, abs(x3 - x2) + 1)
        self.line_g2b = np.array([x_g2b,
                                  self.slope_g2b * x_g2b + self.intercept_g2b]).astype(np.int64)

        white_lines = np.hstack((self.line_r2g, self.line_g2b))

        # Draw the lines
        img_arr = np.array(self.img)
        img_arr[white_lines[0], white_lines[1], :] = [255, 255, 255]
        self.img_out = Image.fromarray(img_arr, 'RGB')
        # self.img_out.show()
        self.img_out.save(self.path + 'mpsi_task_out.png')


if __name__ == '__main__':
    LineDraw()
