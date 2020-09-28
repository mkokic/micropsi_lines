#!/usr/bin/env python3
import unittest
import numpy as np
from lines import line_draw
from PIL import Image


def slope_inercept(xs, ys):
    xs_centered = [x - np.mean(xs) for x in xs]
    ys_centered = [y - np.mean(ys) for y in ys]
    b1_num = sum([x * y for x, y in zip(xs_centered, ys_centered)])
    b1_den = sum([(x - np.mean(xs)) ** 2 for x in xs])
    b1 = b1_num / b1_den
    b0 = np.mean(ys) - (b1 * np.mean(xs))
    return b1, b0


class MyTestCase(unittest.TestCase):
    ld = line_draw.LineDraw()
    im = ld.img
    line_r2g = ld.line_r2g
    line_g2b = ld.line_g2b
    pix_coords = ld.pix_coords
    im_out = ld.img_out

    def test_in_image(self):
        self.assertEqual(self.im.mode, "RGB")
        self.assertEqual(self.im.size, (64, 64))

    def test_pixels(self):
        self.assertIs(self.pix_coords.dtype, np.dtype('int64'))
        self.assertIsInstance(self.pix_coords, np.ndarray)
        self.assertEqual(self.pix_coords.shape, (3, 2))
        self.assertGreaterEqual(self.pix_coords.all(), 0)
        self.assertLess(self.pix_coords.all(), 64)

    def test_image_pix(self):
        im_expected = Image.new("RGB", (64, 64))
        im_expected.putpixel((self.pix_coords[0, 1], self.pix_coords[0, 0]), (255, 0, 0))
        im_expected.putpixel((self.pix_coords[1, 1], self.pix_coords[1, 0]), (0, 255, 0))
        im_expected.putpixel((self.pix_coords[2, 1], self.pix_coords[2, 0]), (0, 0, 255))
        self.assertEqual(im_expected, self.im)

    def test_lines(self):
        # Test that lines are int and array
        self.assertIs(self.line_r2g.dtype, np.dtype('int64'))
        self.assertIs(self.line_g2b.dtype, np.dtype('int64'))
        self.assertIsInstance(self.line_r2g, np.ndarray)
        self.assertIsInstance(self.line_g2b, np.ndarray)

        # Test lines shape
        self.assertEqual(self.line_r2g.shape, (2, abs(self.pix_coords[0, 0] - self.pix_coords[1, 0]) + 1))
        self.assertEqual(self.line_g2b.shape, (2, abs(self.pix_coords[1, 0] - self.pix_coords[2, 0]) + 1))

        # Test slope and intercept
        # Line r2g
        slope_r2g_expected = self.ld.slope_r2g
        intercept_r2g_expected = self.ld.intercept_r2g
        slope_r2g_actual, intercep_r2g_actual = slope_inercept(self.line_r2g[0, :], self.line_r2g[1, :])
        self.assertAlmostEqual(slope_r2g_actual, slope_r2g_expected, -1)
        self.assertAlmostEqual(intercep_r2g_actual, intercept_r2g_expected, -1)
        # Line g2b
        slope_g2b_expected = self.ld.slope_g2b
        intercept_g2b_expected = self.ld.intercept_g2b
        slope_g2b_actual, intercep_g2b_actual = slope_inercept(self.line_g2b[0, :], self.line_g2b[1, :])
        self.assertAlmostEqual(slope_g2b_actual, slope_g2b_expected, -1)
        self.assertAlmostEqual(intercep_g2b_actual, intercept_g2b_expected, -1)

    def test_out_image(self):
        self.assertEqual(self.im_out.mode, "RGB")
        self.assertEqual(self.im_out.size, (64, 64))

        im_expected = Image.new("RGB", (64, 64))
        im_expected_arr = np.array(im_expected)
        im_expected_arr[self.line_r2g[0], self.line_r2g[1], :] = [255, 255, 255]
        im_expected_arr[self.line_g2b[0], self.line_g2b[1], :] = [255, 255, 255]
        im_expected = Image.fromarray(im_expected_arr, 'RGB')
        self.assertEqual(self.im_out, im_expected)


if __name__ == '__main__':
    unittest.main()
