from data_query import load_data_sql, load_data_file, load_data_ids, load_data_constraints

def test_load_data_sql():
    # Test with a valid ADQL query
    adql_query = "SELECT top 10 plate, mjd, fiberid FROM dbo.SpecObj"
    result_df = load_data_sql(adql_query)
    assert result_df is not None
    assert len(result_df) > 0

    # Test with an invalid ADQL query
    invalid_adql_query = "INVALID QUERY"
    try:
        result_df = load_data_sql(invalid_adql_query)
        # Ensure that the function raised an exception for the invalid query
        assert False, f"Expected an exception for an invalid query. Got result: {result_df}"
    except Exception as e:
        # Ensure that the exception contains the expected part of the error message
        expected_error_message = "must be a select statement:  INVALID"
        assert expected_error_message in str(e)


def test_load_data_file():
    # Test with a valid FITS file
    valid_fits_file = "spectrum.fits"
    result_dict = load_data_file(valid_fits_file)
    assert result_dict is not None
    assert all(key.startswith('hdu_') and len(value) > 0 for key, value in result_dict.items())

    # Test with an invalid FITS file
    invalid_fits_file = "spectrum.fits"
    try:
        load_data_file(invalid_fits_file)
    except Exception as e:
        assert str(e) == "Expected Exception"

def test_load_data_ids():
    # Test with a valid ADQL query for plateid, fiberid, and mjd
    ids_query = "SELECT top 10 plate, fiberid, mjd FROM dbo.SpecObj"
    result_dict = load_data_ids(ids_query)
    assert result_dict is not None
    assert all(key.startswith('hdu_') and len(value) > 0 for key, value in result_dict.items())

    # Test with an invalid ADQL query
    invalid_ids_query = "INVALID QUERY"
    try:
        load_data_ids(invalid_ids_query)
    except Exception as e:
        assert str(e) == "Expected Exception"

def test_load_data_constraints():
    # Test case 1: Valid constraints
    constraints_1 = {"class": ["STAR", "GALAXY", "QSO"]}
    try:
        result_df_1 = load_data_constraints(constraints_1)
        print("Test Case 1:")
        print(result_df_1)
    except ValueError as e:
        print(f"Error: {e}")

    # Test case 2: Empty constraints
    constraints_2 = {}
    try:
        result_df_2 = load_data_constraints(constraints_2)
        print("\nTest Case 2:")
        print(result_df_2)
    except ValueError as e:
        print(f"Error: {e}")

    # Test case 3: Invalid constraints
    constraints_3 = {"invalid_key": ["value"]}
    try:
        result_df_3 = load_data_constraints(constraints_3)
        print("\nTest Case 3:")
        print(result_df_3)
    except ValueError as e:
        print(f"Error: {e}")

    # Test case 4: No constraints provided
    constraints_4 = None
    try:
        result_df_4 = load_data_constraints(constraints_4)
        print("\nTest Case 4:")
        print(result_df_4)
    except ValueError as e:
        print(f"Error: {e}")

    # Test case 5: Valid constraints with additional constraint
    constraints_5 = {"class": ["STAR", "GALAXY", "QSO"], "fiberID": [1, 2, 3]}
    try:
        result_df_5 = load_data_constraints(constraints_5)
        print("\nTest Case 5:")
        print(result_df_5)
    except ValueError as e:
        print(f"Error: {e}")

# Run the test cases
test_load_data_constraints()


if __name__ == "__main__":
    test_load_data_sql()
    test_load_data_file()
    test_load_data_ids()
    test_load_data_constraints()
    print("All tests passed!")
