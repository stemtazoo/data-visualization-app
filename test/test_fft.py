import unittest
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.data_processing import compute_fft, compute_fft_segments

class TestFFT(unittest.TestCase):
    def test_compute_fft_peak(self):
        t = np.linspace(0, 1, 256, endpoint=False)
        df = pd.DataFrame({
            'X': np.sin(2*np.pi*10*t),
            'Y': np.sin(2*np.pi*20*t),
            'Z': np.sin(2*np.pi*30*t),
            'Time': t
        })
        freqs, amp_df, _ = compute_fft(df, 0.0, 256)
        self.assertAlmostEqual(freqs[np.argmax(amp_df['X'])], 10, places=6)
        self.assertAlmostEqual(freqs[np.argmax(amp_df['Y'])], 20, places=6)
        self.assertAlmostEqual(freqs[np.argmax(amp_df['Z'])], 30, places=6)

    def test_compute_fft_segments_shape(self):
        t = np.linspace(0, 1, 128, endpoint=False)
        df = pd.DataFrame({'X': np.sin(2*np.pi*10*t), 'Time': t})
        freqs, times, spec_dict, _ = compute_fft_segments(df, 32)
        self.assertEqual(spec_dict['X'].shape, (17, 4))
        self.assertAlmostEqual(times[-1], 0.75, places=6)

if __name__ == '__main__':
    unittest.main()
