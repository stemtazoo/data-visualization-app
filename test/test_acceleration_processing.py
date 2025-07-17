import unittest
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_processing import rotate_xy, calc_accel_metrics

class TestAccelerationProcessing(unittest.TestCase):
    def test_rotate_xy(self):
        df = pd.DataFrame({'x':[1,0], 'y':[0,1]})
        rotated = rotate_xy(df, 'x', 'y', 90)
        self.assertAlmostEqual(rotated['x_rot'].iloc[0], 0, places=5)
        self.assertAlmostEqual(rotated['y_rot'].iloc[0], 1, places=5)
    def test_calc_metrics(self):
        s = pd.Series([1, -1, 1, -1])
        metrics = calc_accel_metrics(s)
        self.assertAlmostEqual(metrics['rms'], 1, places=5)
        self.assertEqual(metrics['max'], 1)
        self.assertEqual(metrics['min'], -1)
        self.assertEqual(metrics['p2p'], 2)

if __name__ == '__main__':
    unittest.main()
