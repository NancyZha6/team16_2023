# test_metadata_extraction.py
import pandas as pd
import pytest
from metadata_extraction import extract_metadata

# Function to create a mock DataFrame with sample data
mock_data = pd.DataFrame({
    'SPECOBJID': [1, 2, 3],
    'RA': [10.0, 20.0, 30.0],
    'DEC': [15.0, 25.0, 35.0],
    'LINEEW': [0.1, 0.2, 0.3],
    'Z': [0.001, 0.002, 0.003],
    'other': ['info1', 'info2', 'info3']
})

# Test to ensure metadata extraction is correct with all options enabled
def test_extract_metadata_all_options():
    result = extract_metadata(mock_data)

    # Verify that the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"

    # Verify that all columns are present
    expected_columns = ['specObjID', 'equivalent_width', 'coord.red_ascension', 'coord.declination', 'redshift']
    assert all([col in result.columns for col in expected_columns]), "All columns should be present in the result"

# Test to ensure metadata extraction is correct with specific options enabled
@pytest.mark.parametrize("identifiers, coordinates, equivalent_width, redshifts, other_fields, expected_columns", [
    (True, False, False, False, None, ['specObjID']),
    (False, True, False, False, None, ['coord.red_ascension', 'coord.declination']),
    (False, False, True, False, None, ['equivalent_width']),
    (False, False, False, True, None, ['redshift']),
    (False, False, False, False, ['other'], ['other']),
])
def test_extract_metadata_specific_options(identifiers, coordinates, equivalent_width, redshifts, other_fields, expected_columns):
    result = extract_metadata(mock_data, identifiers=identifiers, coordinates=coordinates,
                              equivalent_width=equivalent_width, redshifts=redshifts,
                              other_fields=other_fields)

    # Verify that the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"

    # Verify that only the specified columns are present
    assert list(result.columns) == expected_columns, f"Unexpected columns present in the result"
