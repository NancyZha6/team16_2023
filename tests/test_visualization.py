import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytest
from visualization import plot_spectrum

@pytest.fixture
def example_dataframe():
    # Create an example DataFrame for testing
    data = {'loglam': np.linspace(1, 2, 100),
            'flux': np.random.rand(100),
            'model': np.random.rand(100)}
    return pd.DataFrame(data)

def test_plot_spectrum_input_type(example_dataframe):
    # Test if the function raises a TypeError for non-DataFrame input
    with pytest.raises(TypeError):
        plot_spectrum(None)

def test_plot_spectrum_missing_columns(example_dataframe):
    # Test if the function raises a ValueError for missing columns
    df = example_dataframe.drop(columns=['model'])
    with pytest.raises(ValueError):
        plot_spectrum(df)

def test_plot_spectrum_plotting(example_dataframe):
    # Test if the function generates a plot without errors
    plot_spectrum(example_dataframe)

def test_plot_spectrum_annotations(example_dataframe):
    # Test if the function generates a plot with continuum, emission lines, and absorption lines
    plt.figure(figsize=(10, 6))
    plt.plot(10**example_dataframe['loglam'], example_dataframe['flux'], color='blue', label='Measured Flux')
    plt.plot(10**example_dataframe['loglam'], example_dataframe['model'], color='red', label='Modeled Continuum')
    plt.vlines([1.5, 1.8], ymin=0, ymax=example_dataframe['flux'].max(), color='green', linestyle='--', label='Emission Lines')
    plt.vlines([1.3, 1.6], ymin=0, ymax=example_dataframe['flux'].max(), color='green', linestyle='--', label='Absorption Lines')
    plt.xlabel('Wavelength (Angstroms)')
    plt.ylabel('Flux [10^-17 erg/cm^2/s/A]')
    plt.title("Spectrum Plot")
    plt.legend()
    plt.xlim(10**example_dataframe['loglam'].min(), 10**example_dataframe['loglam'].max())
    plt.show()