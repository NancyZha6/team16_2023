import pandas as pd
import numpy as np
import pytest
from data_preprocessing import *
from wavelength_alignment import align_wavelength

def test_align_wavelength_no_interpolation():
    # test data with varied wavelengths and flux values
    data = pd.DataFrame({
        'wavelength': [500, 510, 520, 530],
        'flux': [1.0, 2.0, 3.0, 4.0]
    })

    # align wavelengths within specified range without interpolation
    aligned_data = align_wavelength(data, wavelength_range=(505, 525), interpolation=False)

    # check if aligned wavelengths are within specified range
    assert aligned_data['wavelength'].min() >= 505
    assert aligned_data['wavelength'].max() <= 525

    # get the flux values corresponding to the aligned wavelengths
    aligned_flux = aligned_data['flux'].values

    # check if the flux values remain the same (no interpolation)
    np.testing.assert_array_equal(aligned_flux, data[data['wavelength'].isin(aligned_data['wavelength'])]['flux'].values)

def test_align_wavelength_with_interpolation():
    # test data with varied wavelengths and flux values
    data = pd.DataFrame({
        'wavelength': [500, 510, 520, 530],
        'flux': [1.0, 2.0, 3.0, 4.0]
    })

    # align wavelengths within specified range with interpolation
    aligned_data = align_wavelength(data, wavelength_range=(505, 525), interpolation=True)

    # check if aligned wavelengths are within specified range
    assert aligned_data['wavelength'].min() >= 505
    assert aligned_data['wavelength'].max() <= 525

    # check if there are interpolated values for aligned wavelengths
    assert not aligned_data['flux'].isna().any()
