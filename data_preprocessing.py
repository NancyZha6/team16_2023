import pandas as pd 
from astroquery.sdss import SDSS

def  load_data(adql_query: str) -> pd.DataFrame:
    """
    Retrieves data from the Sloan Digital Sky Survey (SDSS) database using an ADQL query.
    
    Parameters:
    adql_query: The query to retrieve data in string format.

    Returns:
    DataFrame containing SDSS data defined via the query.
    """
    df = SDSS.query_sql(adql_query).to_pandas()
    return df

def normalize(data: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes the spectral data in the DataFrame.
    
    Parameters:
    data: DataFrame containing the spectral data to normalize.
    
    Returns:
    DataFrame containing normalized data.
    """
    if data.empty:
        raise Exception("Dataset is empty")
    # normalize only numerical columns:
    numerical_cols= data.select_dtypes(include='number').columns
    # then apply normalization on these columns by subtracting mean and dividing by std 
    for col in numerical_cols:
        std_dev = data[col].std()
        if std_dev != 0:
            data[col] = (data[col] - data[col].mean()) / std_dev
        else:
            # When std_dev is 0, subtract the mean without dividing
            data[col] = data[col] - data[col].mean()
    return data

def remove_outliers(data: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Removes outliers from the spectral data based on the specified threshold.
    
    Parameters:
    data: DataFrame containing the spectral data to remove outliers.
    threshold: The percentile threshold to remove outliers. 
               E.g. threshold=0.1: remove top and bottom 5% data as outliers.
    
    Returns:
    DataFrame with outliers removed. 
    """
    if data.empty:
        raise Exception("Dataset is empty")
    
    # determine upper and lower threshold given user input
    lower_threshold=threshold/2
    upper_threshold=1-lower_threshold

    # convert it to data threshold 
    lower_percentiles = data.quantile(lower_threshold)
    upper_percentiles = data.quantile(upper_threshold) 

    # remove any data above or below the upper/lower data threshold
    cleaned_data = data[(data > lower_percentiles) & (data < upper_percentiles)]
    cleaned_data.dropna(inplace=True)
    cleaned_data.reset_index(inplace=True,drop=True)
    return cleaned_data

def interpolate(spectra, flux_column='flux', wavelength_column='wavelength'):
    """
    Interpolate values in the spectra DataFrame.

    Parameters:
    spectra: DataFrame containing flux and wavelength columns.
    flux_column (optional): Name of the flux column.
    wavelength_column (optional): Name of the wavelength column.
    #wavelengths (optional): List of predefined wavelengths for subsampling.

    Returns:
    Interpolated and subsampled DataFrame.

    """
    #if wavelengths is not None:
    #    spectra = spectra[spectra[wavelength_column].isin(wavelengths)]

    # Interpolate NaN values in both flux and wavelength columns
    spectra[flux_column] = spectra[flux_column].interpolate()
    spectra[wavelength_column] = spectra[wavelength_column].interpolate()

    return spectra


def correct_redshift(spectra, redshift_column='redshift'):
    """
    Correct the redshift in the wavelengths of the spectra DataFrame. 
    z = (l_spectra - l)/l --> l = l_spectra/(z+1)

    Parameters:
    spectra: DataFrame containing 'wavelength' and 'flux' columns.
    redshift: Redshift value to correct the wavelengths.

    Returns:
    DataFrame with corrected wavelengths.
    """
    spectra['wavelength'] = spectra['wavelength'] * (1 + spectra[redshift_column])

    return spectra

