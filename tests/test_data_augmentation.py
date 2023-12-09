import pandas as pd
import numpy as np
import pytest
from data_augmentation import *

def test_standard_derivative():
    # Create a sample data array
    data = np.array([1, 2, 3, 4, 5])
    # Expected derivative of a linear function is constant
    expected = np.ones_like(data)
    # Call the standard_derivative function
    derivative = standard_derivative(data)
    # Assert that the result is as expected
    assert np.array_equal(derivative, expected)


def test_grunwald_letnikov():
    # Create a sample function
    f = np.array([1, 2, 3, 4, 5])
    order = 0.5
    h = 1e-5
    # Call the grunwald_letnikov function
    result = grunwald_letnikov(f, order, h)
    # Assert the result is a numpy array of the same length as f
    assert isinstance(result, np.ndarray) # Result should be a numpy array
    assert len(result) == len(f) # Result array should be the same length as input function


def test_fractional_derivative():
    # Create a sample DataFrame
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [6, 7, 8, 9, 10]})
    order = 0.5
    # Call the fractional_derivative function
    result = fractional_derivative(df.to_numpy(), order)
    # Assert the result has the same shape as the input DataFrame
    assert result.shape == df.shape  # The shape of the result should match the shape of the input DataFrame.


def test_augment_data():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [6, 7, 8, 9, 10]})
    frac_order = 0.75  # Define the order of the fractional derivative here
    methods = ['standard_derivative', 'fractional_derivative']

    augmented_df = augment_data(df, methods, frac_order)

    assert 'A_std_deriv' in augmented_df.columns  # New column for A's standard derivative should be present.
    assert 'B_std_deriv' in augmented_df.columns  # New column for B's standard derivative should be present.
    assert 'A_frac_deriv' in augmented_df.columns  # New column for A's fractional derivative should be present.
    assert 'B_frac_deriv' in augmented_df.columns  # New column for B's fractional derivative should be present.
