import pytest
import pandas as pd
import data_preprocessing 
import metadata_extraction 
import wavelength_alignment 
import data_augumentation

# Sample ADQL query for testing
ADQL_QUERY = """
SELECT TOP 30 s.specObjID, s.z, s.ra, s.dec, s.waveMin, s.waveMax, s.class, s.spectroFlux_u, g.h_beta_eqw, 
FROM dbo.SpecObj AS s
JOIN GalSpecLine AS g ON s.specobjid = g.specobjid
WHERE s.class IN ('STAR', 'GALAXY', 'QSO')
"""
# Integration Test
def test_data_processing_pipeline():

    # Step 1: Load and preprocess data
    data = data_preprocessing.load_data(ADQL_QUERY)
    assert isinstance(data, pd.DataFrame), "load_data should return a DataFrame"
    # check that data is returned 
    assert not data.isempty(), "load_data should return non-empty DataFrame"

    normalized_data = data_preprocessing.normalize(data)
    assert isinstance(normalized_data, pd.DataFrame), "normalize should return a DataFrame"
    
    data_no_outliers = data_preprocessing.remove_outliers(normalized_data, threshold=0.1,to_remove_columns=["spectroFlux_u"])
    assert isinstance(data_no_outliers, pd.DataFrame), "remove_outliers should return a DataFrame"
    
    interpolated_data = data_preprocessing.interpolate(data_no_outliers,flux_column='spectroFlux_u', wavelength_column='waveMin')
    assert isinstance(interpolated_data, pd.DataFrame), "interpolate should return a DataFrame"
    
    redshift_corrected_data = data_preprocessing.correct_redshift(interpolated_data,wavelenght_column='waveMin',redshift_column='z')
    assert isinstance(redshift_corrected_data, pd.DataFrame), "correct_redshift should return a DataFrame"

    # check that data is returned 
    assert not redshift_corrected_data.isempty(), "data preprocessing should return non-empty DataFrame"
    
    # Step 2: Extract metadata
    extracted_metadata = metadata_extraction.extract_metadata(redshift_corrected_data, identifiers = True, 
                                                                                        coordinates = True,
                                                                                            equivalent_width = True,
                                                                                            redshifts = True,
                                                                                            other_fields = None)
    assert isinstance(extracted_metadata, pd.DataFrame), "extract_metadata should return a DataFrame"

    # Step 3: Wavelength alignment
    aligned_data = wavelength_alignment.align_wavelength(redshift_corrected_data, wavelength_range=(400, 700))
    assert isinstance(aligned_data, pd.DataFrame), "align_wavelength should return a DataFrame"

    # Step 5: Data augumentation
    augumented_data = data_augumentation.augment_data(aligned_data, methods = ['standard_derivative', 'fractional_derivative'], frac_order = 0.75)
    assert isinstance(aligned_data, pd.DataFrame), "augment_data should return a DataFrame"

    # Optionally, you can include additional assertions to verify the content of the dataframes
    # For example, you can check if certain expected columns are present in the dataframes

