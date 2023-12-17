import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_spectrum(df: pd.DataFrame, continuum=True, emission_lines=None, absorption_lines=None):
    # Check if the input is a Pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")

    # Check if the required columns are present in the DataFrame
    required_columns = ['loglam', 'flux', 'model']
    if not all(column in df.columns for column in required_columns):
        raise ValueError("DataFrame must contain columns 'loglam', 'flux', and 'model'.")

    # Set larger figure size
    plt.figure(figsize=(10, 6))

    # Plot flux by wavelength in blue
    plt.plot(10**df['loglam'], df['flux'], color='blue', label='Measured Flux')

    # Add continuum annotations as vertical lines if continuum is True
    if continuum:
        plt.plot(10**df['loglam'], df['model'], color='red', label='Modeled Continuum')

    # Plot green vertical lines for emission lines if emission_lines is provided
    if emission_lines is not None:
        plt.vlines(emission_lines, ymin=0, ymax=df['flux'].max(), color='green', linestyle='--', label='Emission Lines')

    # Plot green vertical lines for absorption lines if absorption_lines is provided
    if absorption_lines is not None:
        plt.vlines(absorption_lines, ymin=0, ymax=df['flux'].max(), color='green', linestyle='--', label='Absorption Lines')

    # Set labels and title
    plt.xlabel('Wavelength (Angstroms)')
    plt.ylabel('Flux [10^-17 erg/cm^2/s/A]')
    plt.title("Spectrum Plot")  # Update title with meaningful information

    # Add legend
    plt.legend()

    # Set x-axis limits to the extremes of loglam
    plt.xlim(10**df['loglam'].min(), 10**df['loglam'].max())

    # Show the plot
    plt.show()