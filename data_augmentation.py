import pandas as pd 
import numpy as np
from typing import Tuple
from typing import List
from astroquery.sdss import SDSS
from scipy.special import gamma


def standard_derivative(data):
    """
    Calculate the standard derivative of the given data.

    Args:
    data (numpy.ndarray): A numpy array of data to differentiate.

    Returns:
    numpy.ndarray: The derivative of the input data.
    """
    return np.gradient(data, axis=0)


def grunwald_letnikov(f, order, h=1e-5):
    """
    Calculate the fractional derivative of a function using the Grünwald-Letnikov approach.

    Args:
    f (numpy.ndarray): The function (as a numpy array) to differentiate.
    order (float): The order of the derivative (fractional).
    h (float): The step size for numerical differentiation (default is 1e-5).

    Returns:
    numpy.ndarray: The fractional derivative of the function.
    """
    N = len(f)
    d = np.zeros(N)
    coeffs = [((-1) ** k) * (gamma(order + 1) / (gamma(k + 1) * gamma(order - k + 1))) for k in range(N)]

    for n in range(N):
        for k in range(min(n + 1, N)):
            d[n] += coeffs[k] * f[n - k] if n - k >= 0 else 0

    return d * (1 / h ** order)


def fractional_derivative(data, order):
    """
    Apply the fractional derivative computation to each column of the input DataFrame.

    Args:
    data (numpy.ndarray): The data as a numpy array.
    order (float): The order of the fractional derivative.

    Returns:
    numpy.ndarray: The fractional derivative of the data.
    """
    return np.apply_along_axis(grunwald_letnikov, axis=0, arr=data, order=order)


def augment_data(data: pd.DataFrame, methods: List, frac_order: float) -> pd.DataFrame:
    """
    Computes derivatives and fractional derivatives, appending them to each preprocessed spectra.

    Parameters:
    data (pd.DataFrame): The DataFrame containing spectral data to augment.
    methods (List): A list of callable functions that define the augmentation methods to be applied.
    frac_order (float): The order of the fractional derivative.

    Returns:
    pd.DataFrame: The augmented DataFrame.
    """
    augmented_data = data.copy()

    for method in methods:
        if method == 'standard_derivative':
            for col in data.columns:
                # Apply the standard_derivative function to each column
                derivative_data = standard_derivative(augmented_data[col].values)
                augmented_data[col + '_std_deriv'] = derivative_data
        elif method == 'fractional_derivative':
            for col in data.columns:
                # Apply the fractional_derivative function to each column
                fractional_derivative_data = fractional_derivative(augmented_data[col].values, frac_order)
                augmented_data[col + '_frac_deriv'] = fractional_derivative_data

    return augmented_data


