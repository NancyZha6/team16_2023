import pandas as pd 
from astroquery.sdss import SDSS
from typing import Tuple
from data_preprocessing import *

def align_wavelength(data: pd.DataFrame, wavelength_range: Tuple[float, float], interpolation: bool = False) -> pd.DataFrame:
    """
    Aligns the wavelength for all spectra within a predefined range.

    Parameters:
    data (pd.DataFrame): DataFrame containing 'wavelength' and 'flux' columns.
    wavelength_range (Tuple[float, float]): Tuple representing the range of wavelengths to align.
    interpolation (bool, optional): If True, perform interpolation. Default is False.

    Returns:
    - pd.DataFrame: DataFrame with aligned wavelength spectra.
    """
    # Filter data within specified wavelength range
    # add .copy() not to change the original dataframe
    aligned_data = data[(data['waveMin'] >= wavelength_range[0]) & (data['waveMax'] <= wavelength_range[1])].copy()

    if interpolation:
        # Interpolate flux values for aligned wavelengths
        aligned_data['flux'] = aligned_data['flux'].interpolate()

    return aligned_data

