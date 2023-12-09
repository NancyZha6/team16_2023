import pandas as pd
import pytest
from metadata_extractor import *

# Function to create a mock DataFrame with sample data
mock_data= pd.DataFrame({
        'identifier': [1, 2, 3],
        'coordinate_x': [10.0, 20.0, 30.0],
        'coordinate_y': [15.0, 25.0, 35.0],
        'chemical_abundance': [0.1, 0.2, 0.3],
        'redshift': [0.001, 0.002, 0.003],
        'other': ['info1', 'info2', 'info3']
    })

# Test to ensure metadata extraction is correct with all options enabled
def test_extract_metadata_all_options():
    result = extract_metadata(mock_data)

    # Verify that the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"

    # Verify that all columns are present
    expected_columns = mock_data.columns
    assert all([col in result.columns for col in expected_columns]), "All columns should be present in the result"

# Test to ensure metadata extraction is correct with specific options enabled
@pytest.mark.parametrize("identifiers, coordinates, chemical_abundances, redshifts, other_fields, expected_columns", [
    (True, False, False, False, None, ['identifier']),
    (False, True, False, False, None, ['coordinate_x', 'coordinate_y']),
    (False, False, True, False, None, ['chemical_abundance']),
    (False, False, False, True, None, ['redshift']),
    (False, False, False, False, ['other'], ['other']),
])
def test_extract_metadata_specific_options(identifiers, coordinates, chemical_abundances, redshifts, other_fields, expected_columns):

    result = extract_metadata(mock_data, identifiers=identifiers, coordinates=coordinates,
                              chemical_abundances=chemical_abundances, redshifts=redshifts,
                              other_fields=other_fields)

    # Verify that the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"

    # Verify that only the specified columns are present
    assert list(result.columns) == expected_columns, f"Unexpected columns present in the result"
