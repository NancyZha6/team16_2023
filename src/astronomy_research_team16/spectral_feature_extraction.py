import pandas as pd
import numpy as np

def extract_spectral_features(df: pd.DataFrame):
    """
    Identify emission and absorption lines based on residuals in the provided DataFrame.
    Parameters:
    - df: Pandas DataFrame with columns 'loglam', 'flux', and 'model'.
    Returns:
    - Tuple containing emission and absorption arrays.
    - Error message if any issues are encountered.
    """
    # Check if the input is a Pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        return None, "Input must be a Pandas DataFrame."

    # Check if the required columns are present in the DataFrame
    required_columns = ['loglam', 'flux', 'model']
    if not all(column in df.columns for column in required_columns):
        return None, "DataFrame must contain columns 'loglam', 'flux', and 'model'."

    # Calculate residuals
    residuals = np.array(df['flux']) - np.array(df['model'])

    # Calculate threshold
    threshold = 2 * np.std(residuals)

    # Identify emission and absorption lines
    emission_array = np.array(df['loglam'])[residuals > threshold]
    absorption_array = np.array(df['loglam'])[residuals < -threshold]

    return 10**emission_array, 10**absorption_array, None