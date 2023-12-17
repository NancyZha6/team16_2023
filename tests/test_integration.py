# NEW INTEGRATION TEST 
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_query import load_data_sql, load_data_file, load_data_ids, load_data_constraints
import data_preprocessing 
import metadata_extraction 
import wavelength_alignment 
import data_augmentation
import machine_learning
import spectral_feature_extraction
import visualization

# Sample ADQL query for testing
ADQL_QUERY = """
SELECT TOP 30 s.specObjID, s.z, s.ra, s.dec, s.waveMin, s.waveMax, s.class, s.spectroFlux_u, g.h_beta_eqw 
FROM dbo.SpecObj AS s
JOIN GalSpecLine AS g ON s.specobjid = g.specobjid
WHERE s.class IN ('STAR', 'GALAXY', 'QSO')
"""
# Integration Test
def test_data_processing_pipeline():

    # Step 0: Load data using the new data query module
    data_query_result = load_data_sql(ADQL_QUERY)
    assert isinstance(data_query_result, pd.DataFrame), "load_data_sql should return a DataFrame"

    # Step 0.1: Load data from FITS file
    fits_file = "tests/spectrum.fits"
    data_file_result = load_data_file(fits_file)
    assert isinstance(data_file_result, dict), "load_data_file should return a dictionary of DataFrames"

    # Step 0.2: Load data based on plateid, fiberid, and mjd
    ids_query = "SELECT top 10 plate, fiberid, mjd FROM dbo.SpecObj"
    data_ids_result = load_data_ids(ids_query)
    metadata_1 = data_ids_result['hdu_2']
    metadata_2 = data_ids_result['hdu_3']
    metadata_2 = pd.merge(metadata_1, metadata_2, left_index=True, right_index=True)
    metadata_1 = data_ids_result['hdu_1']
    merged_meta = pd.merge(metadata_1, metadata_2, left_index=True, right_index=True)
    assert isinstance(data_ids_result, dict), "load_data_ids should return a dictionary of DataFrames"

    # Test case 0.3: Valid constraints with additional constraint
    constraints_5 = {"class": ["STAR", "GALAXY", "QSO"], "fiberID": [1, 2, 3]}
    with pytest.raises(ValueError, match="No data found."):
        result_df_5 = load_data_constraints(constraints_5)

    # Step 1: Load and preprocess data
    data = data_preprocessing.load_data(ADQL_QUERY)
    assert isinstance(data, pd.DataFrame), "load_data should return a DataFrame"
    # check that data is returned 
    assert not data.empty, "load_data should return non-empty DataFrame"

    normalized_data = data_preprocessing.normalize(merged_meta)
    assert isinstance(normalized_data, pd.DataFrame), "normalize should return a DataFrame"
    
    data_no_outliers = data_preprocessing.remove_outliers(normalized_data, threshold=0.1,to_remove_columns=["flux"])
    assert isinstance(data_no_outliers, pd.DataFrame), "remove_outliers should return a DataFrame"
    
    interpolated_data = data_preprocessing.interpolate(data_no_outliers,flux_column='flux', wavelength_column='loglam')
    assert isinstance(interpolated_data, pd.DataFrame), "interpolate should return a DataFrame"
    
    redshift_corrected_data = data_preprocessing.correct_redshift(interpolated_data,wavelenght_column='loglam',redshift_column='Z')
    assert isinstance(redshift_corrected_data, pd.DataFrame), "correct_redshift should return a DataFrame"

    # check that data is returned 
    assert not redshift_corrected_data.empty, "data preprocessing should return non-empty DataFrame"
    
    # Step 2: Extract metadata
    # Assuming 'data' is a Pandas DataFrame
    extracted_metadata = metadata_extraction.extract_metadata(redshift_corrected_data, identifiers = True, 
                                                                                        coordinates = True,
                                                                                            equivalent_width = True,
                                                                                            redshifts = True,
                                                                                            other_fields = None)
    assert isinstance(extracted_metadata, pd.DataFrame), "extract_metadata should return a DataFrame"

    # Step 3: Wavelength alignment
    aligned_data = wavelength_alignment.align_wavelength(redshift_corrected_data, wavelength_range=(-0.5, 2), interpolation=True)
    assert isinstance(aligned_data, pd.DataFrame), "align_wavelength should return a DataFrame"

    # Step 4: Data Augmentation
    # augmented dataframe with both methods
    augmented_data = data_augmentation.augment_data(aligned_data, ['standard_derivative', 'fractional_derivative'], 0.5)
    assert isinstance(augmented_data, pd.DataFrame),"data_augmentation should return a DataFrame"
    assert 'flux_std_deriv' in augmented_data.columns
    assert 'flux_frac_deriv' in augmented_data.columns

    # Step5: Machine Learning Module
    X_train, X_val, y_train, y_val, X_test = machine_learning.prepare_data(data_ids_result)
    assert not X_train.empty
    assert not X_val.empty
    assert not y_train.empty
    assert not y_val.empty
    assert not X_test.empty

    model = machine_learning.fit_model(X_train, y_train, X_val, y_val)
    assert model is not None

    prediction = machine_learning.predict_class(model, X_test)
    assert len(prediction) == len(X_test)

    prediction_prob = machine_learning.predict_proba(model, X_test)
    assert prediction_prob.shape == (len(X_test), model.n_classes_)
    
    # Step6: Spectral Feature Extraction
    emission, absorption, error = spectral_feature_extraction.extract_spectral_features(merged_meta)
    assert error is None
    assert isinstance(emission, np.ndarray)
    assert isinstance(absorption, np.ndarray) 
    
    # Step7: Visualization
    visualization.plot_spectrum(merged_meta)
    plot1 = plt.gcf()
    assert plot1 is not None, "No figure has been created"
    
    visualization.plot_spectrum(merged_meta, emission_lines=emission, absorption_lines=absorption)
    plot2 = plt.gcf()
    assert plot2 is not None, "No figure has been created"
