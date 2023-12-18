from data_augmentation import *
from data_query import load_data_sql, load_data_file, load_data_ids, load_data_constraints


def generate_sample_data():
    adql_query = """
    SELECT top 5 plate,mjd,fiberid
    FROM dbo.SpecObj
    """
    data = load_data_ids(adql_query)
    table = data['hdu_1'][['flux', 'loglam']]
    return table

def test_standard_derivative():
    data = generate_sample_data()
    derivative = standard_derivative(data['flux'].values, data['loglam'].values)
    assert len(derivative) == len(data['flux'])

def test_fractional_derivative():
    data = generate_sample_data()
    result = fractional_derivative(data['flux'].values, data['loglam'].values, 0.5)
    assert len(result) == len(data['flux'])

def test_augment_data():
    df = generate_sample_data()
    frac_order = 0.75
    methods = ['standard_derivative', 'fractional_derivative']

    augmented_df = augment_data(df, methods, frac_order)

    assert 'flux_std_deriv' in augmented_df.columns  # Check for standard derivative column
    assert 'flux_frac_deriv' in augmented_df.columns  # Check for fractional derivative column
    # Ensure the new columns are the correct length
    assert len(augmented_df['flux_std_deriv']) == len(df['flux'])
    assert len(augmented_df['flux_frac_deriv']) == len(df['flux'])

