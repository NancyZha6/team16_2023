import numpy as np
import pandas as pd
from scipy.special import gamma

def standard_derivative(flux, wavelength):
    """
    Calculate the standard derivative of flux with respect to wavelength.

    Args:
    flux (numpy.ndarray): A numpy array of flux data.
    wavelength (numpy.ndarray): A numpy array of wavelength data.

    Returns:
    numpy.ndarray: The derivative of flux with respect to wavelength.
    """
    d_flux = np.gradient(flux)
    d_wavelength = np.gradient(wavelength)
    return d_flux / d_wavelength


def fractional_derivative(flux, wavelength, order, h=1e-5, max_terms=50):
    """
    Calculate the fractional derivative of flux with respect to wavelength using a manual implementation
    of the Grünwald-Letnikov approach.

    Args:
    flux (numpy.ndarray): The flux data (as a numpy array).
    wavelength (numpy.ndarray): The wavelength data (as a numpy array).
    order (float): The order of the derivative (fractional).
    h (float): The step size for numerical differentiation (default is 1e-5).
    max_terms (int): Maximum number of terms to include in the sum (default is 50).

    Returns:
    numpy.ndarray: The fractional derivative of flux with respect to wavelength.
    """
    N = len(flux)
    d_flux = np.zeros(N)
    max_terms = min(max_terms, N)  # Limit the number of terms to avoid computational issues

    coeffs = []
    for k in range(max_terms):
        if order - k >= 0:
            coeffs.append(((-1) ** k) * gamma(order + 1) / (gamma(k + 1) * gamma(order - k + 1)))
        else:
            coeffs.append(0)  # Avoid negative values in the gamma function

    for n in range(N):
        sum_term = sum(coeffs[k] * flux[n - k] if n - k >= 0 else 0 for k in range(max_terms))
        d_flux[n] = sum_term

    d_wavelength = np.gradient(wavelength)
    return d_flux * (1 / h ** order) / d_wavelength



def augment_data(data: pd.DataFrame, methods: list, frac_order: float = None) -> pd.DataFrame:
    """
    Computes derivatives and fractional derivatives of flux with respect to wavelength,
    appending them to each preprocessed spectra.

    Parameters:
    data (pd.DataFrame): The DataFrame containing spectral data to augment.
                         Assumes 'flux' and 'wavelength' columns are present.
    methods (list): A list of callable functions that define the augmentation methods to be applied.
    frac_order (float): The order of the fractional derivative.

    Returns:
    pd.DataFrame: The augmented DataFrame.
    """
    augmented_data = data.copy()
    flux = data['flux'].values
    wavelength = data['loglam'].values

    for method in methods:
        if method == 'standard_derivative':
            derivative_data = standard_derivative(flux, wavelength)
            augmented_data['flux_std_deriv'] = derivative_data
        elif method == 'fractional_derivative':
            fractional_derivative_data = fractional_derivative(flux, wavelength, frac_order)
            augmented_data['flux_frac_deriv'] = fractional_derivative_data

    return augmented_data
