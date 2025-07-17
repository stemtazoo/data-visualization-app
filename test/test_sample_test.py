# test/test_sample_data.py
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.sample_data import load_simple_sample_data, load_timeseries_sample_data

class TestSampleData(unittest.TestCase):
    def test_load_simple_sample_data(self):
        df = load_simple_sample_data()
        self.assertEqual(df.shape, (5, 3))
        self.assertIn('X軸', df.columns)

    def test_load_timeseries_sample_data(self):
        df = load_timeseries_sample_data()
        self.assertEqual(df.shape[0], 100)
        self.assertIn('日付', df.columns)

if __name__ == '__main__':
    unittest.main()
