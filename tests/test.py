#!/usr/bin/env python3
import unittest
import numpy as np
from micropsi_lines.line_draw import LineDraw
from PIL import Image
from IPython import embed


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.ld = LineDraw()

    def tearDown(self):
        pass

    def test_img_in(self):
        self.assertEqual(self.ld.img.mode, "RGB")
        self.assertEqual(self.ld.img.size, (64, 64))

    def test_pix(self):
        self.assertIs(self.ld.pix_coords.dtype, np.dtype('int64'))
        self.assertIsInstance(self.ld.pix_coords, np.ndarray)
        self.assertEqual(np.unique(self.ld.pix_coords, axis=0).shape, (3, 2))
        self.assertTrue(0 <= self.ld.pix_coords.all() < 64)

    def test_get_pix(self):
        img_exp = Image.new("RGB", (64, 64))
        img_exp.putpixel((10, 10), (255, 0, 0))
        img_exp.putpixel((30, 30), (0, 255, 0))
        img_exp.putpixel((50, 50), (0, 0, 255))

        pix_coords_actual = self.ld.get_pix(img_exp)
        img_actual = Image.new("RGB", (64, 64))
        rgb_vals = (np.eye(3) * 255).astype(np.int64)
        for p, c in zip(pix_coords_actual, rgb_vals):
            img_actual.putpixel(tuple(p), tuple(c))
        self.assertEqual(img_actual, img_exp)

    def test_lines(self):
        self.assertIs(self.ld.lines.dtype, np.dtype('int64'))
        self.assertIsInstance(self.ld.lines, np.ndarray)

    def test_compute_lines(self):
        # Test vertical case
        pix_coords_exp_vert = np.array([[10, 10],
                                        [10, 30],
                                        [10, 50]])
        lines_exp_vert = np.concatenate([np.array([10 * np.ones(21, ), np.linspace(10, 30, 21)]).astype(np.int64),
                                         np.array([10 * np.ones(21, ), np.linspace(30, 50, 21)]).astype(np.int64),
                                         np.array([10 * np.ones(41, ), np.linspace(10, 50, 41)]).astype(np.int64)], 1)

        lines_actual_vert = self.ld.compute_lines(pix_coords_exp_vert)
        self.assertEqual(lines_actual_vert.tolist(), lines_exp_vert.tolist())

        # Test all the other cases
        pix_coords_exp = np.array([[10, 10],
                                   [30, 10],
                                   [50, 10]])
        lines_exp = np.concatenate([np.array([np.linspace(10, 30, 21), 10 * np.ones(21, )]).astype(np.int64),
                                    np.array([np.linspace(30, 50, 21), 10 * np.ones(21, )]).astype(np.int64),
                                    np.array([np.linspace(10, 50, 41), 10 * np.ones(41, )]).astype(np.int64)], 1)

        lines_actual = self.ld.compute_lines(pix_coords_exp)
        self.assertEqual(lines_actual.tolist(), lines_exp.tolist())

    def test_img_out_lines(self):
        img_out = self.ld.draw_lines(self.ld.img, self.ld.lines)
        self.assertEqual(img_out.mode, "RGB")
        self.assertEqual(img_out.size, (64, 64))

    def test_img_out(self):
        img_expected = Image.new("RGB", (64, 64))
        lines_expected = np.hstack([np.array([np.linspace(10, 20, 11), 10 * np.ones(11, )]).astype(np.int64),
                                    np.array([np.linspace(20, 30, 11), 10 * np.ones(11, )]).astype(np.int64)])

        img_actual = self.ld.draw_lines(img_expected, lines_expected)

        img_expected_arr = np.array(img_expected)
        img_expected_arr[lines_expected[0], lines_expected[1], :] = [255, 255, 255]
        img_expected = Image.fromarray(img_expected_arr, 'RGB')
        self.assertEqual(img_actual, img_expected)


if __name__ == '__main__':
    unittest.main()
