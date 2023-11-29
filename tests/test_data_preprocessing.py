import pytest
import pandas as pd
import numpy as np
from data_preprocessing import *

def test_load_data():
	# test with a valid file path
	df = load_data('valid_query.txt')
	assert not df.isnull().values.any(), "Function should not return to null"""

def test_normalize():
    # test DataFrame with numerical and non-numerical columns
    data = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': ['X', 'Y', 'Z']
    })

    # check if empty data
    with pytest.raises(Exception, match="Dataset is empty"):
        normalize(pd.DataFrame())

    # test normalization
    normalized_data = normalize(data[['A', 'B']])
    
    # expect mean close to 0 and sd close to 1
    assert np.allclose(normalized_data.mean(), 0)
    assert np.allclose(normalized_data.std(), 1)

    # expect non-numerical columns not affected
    normalized_data2 = normalize(data)
    assert data['C'].equals(normalized_data2['C'])

    # test normalization with all 0s
    zero_data = pd.DataFrame({
        'A': [0, 0, 0],
        'B': [0, 0, 0]
    })
    normalized_zero_data = normalize(zero_data)
    # still 0s
    assert np.allclose(normalized_zero_data, 0)

def test_remove_outliers():
    # DataFrame with numerical columns
    data = pd.DataFrame({
        'A': [1, 2, 3, 100],
        'B': [4, 5, 6, 200],
        'C': [7, 8, 9, 300]
    })

    # test 1: remove outliers with threshold = 0.25
    cleaned_data = remove_outliers(data, 0.25)
    # expect outliers (100, 200, 300) are removed
    assert cleaned_data.shape == (2, 3)

    # test 2: remove outliers with a threshold of 0.5
    cleaned_data_50 = remove_outliers(data, 0.5)
    # expect half of the data is removed (top and bottom 25%)
    assert cleaned_data_50.shape == (2, 3)

    # test 3: remove outliers from DataFrame with same values
    constant_data = pd.DataFrame({
        'A': [1, 1, 1],
        'B': [1, 1, 1],
        'C': [1, 1, 1]
    })
    # expect result an empty DataFrame
    assert remove_outliers(constant_data, 0.1).empty

def test_interpolation():
    # Data with NaN values in both columns
    data_with_nans = pd.DataFrame({
        'wavelength': [1, np.nan, 3, 4, 5],
        'flux': [10, np.nan, 30, 40, 50]
    })

    # Perform interpolation
    interpolated_data = interpolate(data_with_nans)

    # Check if NaN values in both columns are filled
    assert not (interpolated_data['wavelength'].isna().any())
    assert not (interpolated_data['flux'].isna().any())

    # Data without NaN values
    clean_data = pd.DataFrame({
        'wavelength': [1, 2, 3, 4, 5],
        'flux': [10, 20, 30, 40, 50]
    })

    # Perform interpolation on clean data
    result_data = interpolate(clean_data)

    # Check if data remains unchanged when no NaNs are present
    pd.testing.assert_frame_equal(result_data, clean_data)

    # Additional test: Check interpolated values (assuming linear interpolation)
    # This part depends on the interpolation method used (here we assume linear)
    expected_interpolated_values = pd.DataFrame({
        'wavelength': [1, 2, 3, 4, 5],
        'flux': [10, 20, 30, 40, 50]
    })
    pd.testing.assert_frame_equal(interpolated_data, expected_interpolated_values)

def test_redshift_correction():
    # Test data with varied redshift values including zero
    test_data = pd.DataFrame({
        'wavelength': [100, 200, 300, 400],
        'redshift': [0.5, 1, 0, 1.5]
    })

    # Expected results after redshift correction
    expected_data = pd.DataFrame({
        'wavelength': [150, 400, 300, 1000],  # Corrected values
        'redshift': [0.5, 1, 0, 1.5]
    })

    # Perform redshift correction
    corrected_data = correct_redshift(test_data)

    # Check if the corrected wavelengths are as expected
    pd.testing.assert_frame_equal(corrected_data, expected_data)
