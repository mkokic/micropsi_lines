#!/usr/bin/env python3
import unittest
import numpy as np
from PIL import Image
from micropsi_lines.line_draw import LineDraw


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.ld = LineDraw()

    def tearDown(self):
        pass

    # Test the mode and the size of the input image
    def test_img_in(self):
        self.assertEqual(self.ld.img.mode, "RGB")
        self.assertEqual(self.ld.img.size, (64, 64))

    # Test that extracted pixels are an int array of 3x2 points between 0 and 64
    def test_pix(self):
        self.assertIs(self.ld.pix_coords.dtype, np.dtype('int64'))
        self.assertIsInstance(self.ld.pix_coords, np.ndarray)
        self.assertEqual(np.unique(self.ld.pix_coords, axis=0).shape, (3, 2))
        self.assertTrue(0 <= self.ld.pix_coords.all() < 64)

    # Test that the coordinates and colors of extracted pixels values are correct
    def test_get_pix(self):
        # Expected image with pixels in specified locations
        img_exp = Image.new("RGB", (64, 64))
        img_exp.putpixel((10, 10), (255, 0, 0))  # Red
        img_exp.putpixel((30, 30), (0, 255, 0))  # Green
        img_exp.putpixel((50, 50), (0, 0, 255))  # Blue

        # Extract pixels coordinates from the expected image
        pix_coords_actual = self.ld.get_pix(img_exp)

        # Generate an actual image with computed pixel coordinates
        img_actual = Image.new("RGB", (64, 64))
        rgb_vals = (np.eye(3) * 255).astype(np.int64)
        for p, c in zip(pix_coords_actual, rgb_vals):
            img_actual.putpixel(tuple(p), tuple(c))

        self.assertEqual(img_actual, img_exp)

    # Test that lines are an array of integers
    def test_lines(self):
        self.assertIs(self.ld.lines.dtype, np.dtype('int64'))
        self.assertIsInstance(self.ld.lines, np.ndarray)

    # Test that the lines computed from pixels are correct
    def test_compute_lines(self):
        # Test vertical case
        # x1 = x2 = x3; y1 = 10, y2 = 30, y3 = 50
        pix_coords_exp_vert = np.array([[10, 10],
                                        [10, 30],
                                        [10, 50]])
        lines_exp_vert = np.concatenate([np.array([[10] * 21, np.linspace(10, 30, 21)]),
                                         np.array([[10] * 21, np.linspace(30, 50, 21)]),
                                         np.array([[10] * 41, np.linspace(10, 50, 41)])], 1).astype(np.int64)

        lines_actual_vert = self.ld.compute_lines(pix_coords_exp_vert)
        self.assertEqual(lines_actual_vert.tolist(), lines_exp_vert.tolist())

        # Test all the other cases
        # x1 = 10, x2 = 30, x3 = 50; y1 = 10, y2 = 10, y3 = 10
        pix_coords_exp = np.array([[10, 10],
                                   [30, 10],
                                   [50, 10]])
        lines_exp = np.concatenate([np.array([np.linspace(10, 30, 21), [10] * 21]),
                                    np.array([np.linspace(30, 50, 21), [10] * 21]),
                                    np.array([np.linspace(10, 50, 41), [10] * 41])], 1).astype(np.int64)

        lines_actual = self.ld.compute_lines(pix_coords_exp)
        self.assertEqual(lines_actual.tolist(), lines_exp.tolist())

    # Test the mode and the size of the output image
    def test_img_out(self):
        self.assertEqual(self.ld.img_out.mode, "RGB")
        self.assertEqual(self.ld.img_out.size, (64, 64))

    # Test that the output image contains white lines connecting the pixels
    def test_draw_lines(self):
        img_exp = Image.new("RGB", (64, 64))
        lines_exp = np.concatenate([np.array([np.linspace(10, 30, 21), [10] * 21]),
                                    np.array([np.linspace(30, 50, 21), [10] * 21]),
                                    np.array([np.linspace(10, 50, 41), [10] * 41])], 1).astype(np.int64)

        img_actual = self.ld.draw_lines(img_exp, lines_exp)

        img_expected_arr = np.array(img_exp)
        img_expected_arr[lines_exp[0], lines_exp[1], :] = [255, 255, 255]
        img_expected = Image.fromarray(img_expected_arr, 'RGB')
        self.assertEqual(img_actual, img_expected)


if __name__ == '__main__':
    unittest.main()
