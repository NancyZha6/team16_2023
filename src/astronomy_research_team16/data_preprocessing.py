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

# new normalize function (add exclude_columns for identifiers):
def normalize(data: pd.DataFrame, exclude_columns=['objectid']) -> pd.DataFrame:
    """
    Normalizes the spectral data in the DataFrame.
    Parameters:
    data: DataFrame containing the spectral data to normalize.
    exclude_columns: List of columns to exclude from normalization.
    Returns:
    DataFrame containing normalized data.
    """
    if data.empty:
        raise Exception("Dataset is empty")

    # exclude specified columns from normalization
    numerical_cols = data.select_dtypes(include='number').columns.difference(exclude_columns)

    # then apply normalization on these columns by subtracting mean and dividing by std
    for col in numerical_cols:
        std_dev = data[col].std()
        if std_dev != 0:
            data[col] = (data[col] - data[col].mean()) / std_dev
        else:
            # When std_dev is 0, subtract the mean without dividing
            data[col] = data[col] - data[col].mean()

    return data

def remove_outliers(data: pd.DataFrame, threshold: float, to_remove_columns: list) -> pd.DataFrame:
    """
    Removes outliers from the spectral data based on the specified threshold.
    
    Parameters:
    data: DataFrame containing the spectral data to remove outliers.
    threshold: The percentile threshold to remove outliers. 
               E.g. threshold=0.1: remove top and bottom 5% data as outliers.
    to_remove_columns: columns to perform outlier removal on
    
    Returns:
    DataFrame with outliers removed. 
    """
    if data.empty:
        raise Exception("Dataset is empty")
    
    # determine upper and lower threshold given user input
    lower_threshold=threshold/2
    upper_threshold=1-lower_threshold

    # convert it to data threshold 
    lower_percentiles = data[to_remove_columns].quantile(lower_threshold)
    upper_percentiles = data[to_remove_columns].quantile(upper_threshold) 

    # remove any data above or below the upper/lower data threshold
    cleaned_data=data.copy()
    cleaned_data[to_remove_columns]= data[to_remove_columns][(data[to_remove_columns] > lower_percentiles) & (data[to_remove_columns] < upper_percentiles)]
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


def correct_redshift(spectra, wavelenght_column='wavelength',redshift_column='redshift'):
    """
    Correct the redshift in the wavelengths of the spectra DataFrame. 
    z = (l_spectra - l)/l --> l = l_spectra/(z+1)

    Parameters:
    spectra: DataFrame containing 'wavelength' and 'flux' columns.
    wavelenght_column=column containing wavelength 
    redshift_column: Redshift value to correct the wavelengths.

    Returns:
    DataFrame with corrected wavelengths.
    """
    spectra[wavelenght_column] = spectra[wavelenght_column] * (1 + spectra[redshift_column])

    return spectra

