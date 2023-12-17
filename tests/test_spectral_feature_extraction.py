import pytest
import pandas as pd
import numpy as np
from spectral_feature_extraction import *

sample_data = {
    'loglam': [1.0, 2.0, 3.0, 4.0],
    'flux': [10.0, 12.0, 8.0, 15.0],
    'model': [9.0, 11.0, 7.0, 14.0],
}
sample_df = pd.DataFrame(sample_data)

def test_extract_spectral_features():
    # Test case 1: Correct input
    emission, absorption, error = extract_spectral_features(sample_df)
    assert error is None
    assert isinstance(emission, np.ndarray)
    assert isinstance(absorption, np.ndarray)

    # Test case 2: Incorrect input type
    _, error = extract_spectral_features("not_a_dataframe")
    assert "Input must be a Pandas DataFrame." in error

    # Test case 3: Missing columns in DataFrame
    _, error = extract_spectral_features(pd.DataFrame({'incorrect_column': [1, 2, 3]}))
    assert "DataFrame must contain columns 'loglam', 'flux', and 'model'." in error