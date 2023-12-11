import requests
from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt

def plot_spectrum(plateid, mjd, fiberid, show_annotations=True):
    # Construct the URL for the FITS file
    fits_url = f"http://dr17.sdss.org/optical/spectrum/view/data/format=fits/spec=full?plateid={plateid}&mjd={mjd}&fiberid={fiberid}"

    # Download the FITS file
    response = requests.get(fits_url)
    fits_filename = "spectrum.fits"

    with open(fits_filename, "wb") as fits_file:
        fits_file.write(response.content)

    # Open the FITS file
    hdul = fits.open(fits_filename, ignore_missing_simple=True)

    # Get the data from the FITS file
    data = hdul[1].data

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Annotations data
    annotations_data = {
        "Line Name": ["Mg_II", "[O_II]", "[O_II]", "[Ne_III]", "H_epsilon", "[Ne_III]", "H_delta", "H_gamma", "[O_III]", "He_II", "H_beta", "[O_III]", "[O_III]", "He_II", "[O_I]", "[N_II]", "He_I", "[O_I]", "[S_III]", "[O_I]", "[N_II]", "H_alpha", "[N_II]", "[S_II]", "[S_II]", "[Ar_III]"],
        "Rest Wavelength [Å]": [2800.3, 3727.1, 3729.9, 3869.9, 3890.2, 3971.1, 4102.9, 4341.7, 4364.4, 4687.0, 4862.7, 4960.3, 5008.2, 5413.0, 5578.9, 5756.2, 5877.3, 6302.0, 6313.8, 6365.5, 6549.9, 6564.6, 6585.3, 6718.3, 6732.7, 7137.8],
        "Line z": [0.4078] * 26,
        "Line σ [km s^-1]": [588.2] * 20 + [153] * 6,
        "Line Flux [10^-17 erg/cm^2/s]": [6.08, 14.55, -19.36, -4.544, -2.225, -16.17, -0.3849, 0.5928, 0.4562, 1.164, -1.458, -0.4189, -1.269, -1.34, -1.211, -2.089, 1.091, 1.344, 2.004, -2.872, -0.06052, -2.803, 2.443, -13.49, -3.247, -20.2],
        "Continuum [10^-17 erg/cm^2/s/A]": [0.09896, 0.8686, 0.8591, 0.9047, 1.014, 1.234, 1.495, 1.709, 1.776, 2.168, 2.126, 2.382, 2.149, 2.4, 2.403, 2.559, 2.443, 2.419, 2.39, 2.455, 2.441, 2.41, 2.43, 2.329, 2.291, 2.354]
    }

    # Create a DataFrame for annotations
    annotations_df = pd.DataFrame(annotations_data)

    # Set larger figure size
    plt.figure(figsize=(10, 6))

    # Plot flux by wavelength in blue
    plt.plot(10**df['loglam'], df['flux'], color='blue', label='Flux')

    # Plot model in red
    plt.plot(10**df['loglam'], df['model'], color='red', label='Model')

    # Set labels and title
    plt.xlabel('Wavelength (Angstroms)')
    plt.ylabel('Flux [10^-17 erg/cm^2/s/A]')
    plt.title(f"Spectrum: plateid={plateid} mjd={mjd} fiberid={fiberid}")

    # Add legend
    plt.legend()

    # Add continuum annotations as vertical lines if show_annotations is True
    if show_annotations:
        for index, row in annotations_df.iterrows():
            wavelength = row['Rest Wavelength [Å]']
            continuum_value = row['Continuum [10^-17 erg/cm^2/s/Å]']
            line_name = row['Line Name']

            # Add vertical line in hot pink
            plt.axvline(x=wavelength, color='hotpink', linestyle='--', linewidth=0.5)

            # Add smaller text annotation with line name
            plt.text(wavelength, continuum_value, line_name, rotation=90, va='bottom', ha='right', fontsize=6, color='hotpink')

    # Set x-axis limits to the extremes of loglam
    plt.xlim(10**df['loglam'].min(), 10**df['loglam'].max())

    # Show the plot
    plt.show()

    # Close the FITS file
    hdul.close()

