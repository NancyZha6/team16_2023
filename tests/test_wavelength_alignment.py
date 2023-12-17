import pandas as pd
import numpy as np
import pytest
from wavelength_alignment import align_wavelength
from data_query import *

def sample_data():
    adql_query = """
    SELECT top 20 plate,mjd,fiberid
    FROM dbo.SpecObj
    """
    data = load_data_ids(adql_query)
    table = data['hdu_1'][['flux', 'loglam']]
    return table

#def sample_data():
    # Create a sample DataFrame for testing
#    data = pd.DataFrame({
#        'loglam': np.linspace(3.0, 4.0, 10),
#        'flux': np.random.rand(10),
#    })
#    return data

def test_align_wavelength_within_range():
    data = sample_data()
    # Test aligning within a specified wavelength range
    wavelength_range = (3.2, 3.8)
    aligned_data = align_wavelength(data, wavelength_range)

    # Check if only data within the range is present
    assert (aligned_data['loglam'] >= wavelength_range[0]).all()
    assert (aligned_data['loglam'] <= wavelength_range[1]).all()

def test_align_wavelength_no_interpolation():
    data = sample_data()
    # Test aligning without interpolation
    wavelength_range = (3.2, 3.8)
    aligned_data = align_wavelength(data, wavelength_range, interpolation=False)

    # Check if interpolation is not applied
    assert aligned_data['flux'].isna().sum() == 0

def test_align_wavelength_interpolation():
    data = sample_data()
    # Test aligning with interpolation
    wavelength_range = (3.2, 3.8)
    aligned_data = align_wavelength(data, wavelength_range, interpolation=True)

    # Check if interpolation is applied
    assert aligned_data['flux'].isna().sum() == 0  # No missing values after interpolation
    assert aligned_data['flux'].equals(data['flux']) == False  # Values should be different after interpolation

