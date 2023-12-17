# API_draft README

## Overview
This folder contains the draft of the Application Programming Interface (API) for the astronomical research library. The library aims to assist in the classification of astronomical objects, specifically stars, galaxies, and QSOs, by interfacing with Sloan Digital Sky Survey (SDSS) services.

## Modules, Classes, and Functions

### 1. Data Query Module 
   - **Function: load_data_sql(adql_query: str = None) -> DataFrame**
     - Retrieves SDSS data based on an ADQL query or identifiers.
     - Parameters:
        - `adql_query`: ADQL query to retrieve data. Default is None.
     - Returns: DataFrame containing SDSS data defined by the query or identifiers.
     
   - **Function: load_data_file(file: fits) -> dict:**
     - Accepts a fits file and just open it and load data.
     - Parameters:
        - `file`: FITS file path that meets SDSS format.
     - Returns: Dictionary containing DataFrames for each HDU in the FITS file.

   - **Function: load_data_ids(ids_query: str = None) -> dict:**
     - Retrieves SDSS data based on plateid, fiberid, and mjd.
     - Parameters:
        - `ids_query`: ADQL query to extract plateid, fiberid, and mjd. Default is None.
     - Returns: Dictionary containing DataFrames for each HDU with extracted spectra.
   
   - **Function: load_data_constraints(constraints: dictionary) -> DataFrame:**
      - Retrieves SDSS data based on constraints provided in the form of a dictionary.
      - Parameters:
        - `constraints`: constraints to put in the where statement of the query to get data  
      - Returns: Dataframe containing SDSS data defined via the query. 

### 2. Data Preprocessing Module (Data Preprocessing in API diagram)
   - **Function: load_data(adql_query: str) -> DataFrame:**
      - Retrieves SDSS data using an ADQL query as a string.
      - Parameters:
        - `adql_query` (str): The query string in ADQL format to retrieve data.
      - Returns: DataFrame containing the data fetched from SDSS based on the ADQL query.

  - **Function: normalize(data: DataFrame, exclude_columns: List[str] = ['objectid']) -> DataFrame:**
    - Normalizes the spectral data in the DataFrame.
    - Parameters:
      - `data` (pd.DataFrame): DataFrame containing the spectral data to normalize.
      - `exclude_columns` (List[str], optional): List of columns to exclude from normalization. Default is `['objectid']`.
    - Returns: DataFrame containing normalized data.

  - **Function: remove_outliers(data: pd.DataFrame, threshold: float, to_remove_columns: list) -> DataFrame:**
    - Removes outliers above/below specific threshold from the spectral data 
    - Parameters:
      - `data`: the data to remove outliers
      - `threshold`: the percentile threshold to remove outliers. E.g. threshold=0.9: remove top and bottom 10% data as outliers 
      - `to_remove_columns`: a list of column names to remove the outliers
    - Returns: Dataframe containing data with outliers removed.  

  - **Function: interpolate(spectra: DataFrame, flux_column='flux', wavelength_column='wavelength') -> DataFrame:**
    - Performs interpolation on the spectral data.
    - Parameters:
      - `spectra`: DataFrame containing flux and wavelength columns perform interpolation.
      -  `flux_column`: Name of the flux column.
      -  `wavelength_column`: Name of the wavelength column.
    - Returns: Dataframe containing interpolated data 

  - **Function: correct_redshift(spectra: DataFrame, wavelenght_column='wavelength',redshift_column='redshift') -> DataFrame:**
    - Corrects redshift in the spectral data.
    - Parameters:
      - `spectra`: DataFrame containing 'wavelength' and 'flux' columns to perform redshift correction.
      - `wavelenght_column`: name of wavelength column
      - `redshift_column`: name of redshift column
    - Returns: Dataframe containing data with red shift corrected.

### 3. Metadata Extraction Module (Metadata Extraction in API diagram)
  - **Function: extract_metadata(data: DataFrame, identifiers: bool = True, coordinates: bool = True, redshifts: bool = True, other_fields: List[str] = None) -> DataFrame:**
    - Extracts user-defined parameters of metadata from the spectral data.
    - Parameters:
      - `data`: the pandas dataframe of the data to extract metadata from
      - `identifiers`: If True, extract object identifier: Spectral Object ID (SPECOBJID).
      - `coordinates`: If True, extract object coordinates: right ascension (RA), declination (DEC).
      - `redshifts`: If True, extract redshift (Z).
      - `other_fields`: A list of other fields to extract if specified.
    - Returns: Dataframe containing the extracted metadata.

### 4. Wavelength Alignment Module (Wavelength Alignment in API diagram)
  - **Function: align_wavelength(data: pd.DataFrame, wavelength_range: Tuple[float, float], interpolation: bool = False) -> DataFrame:**
    - Aligns the wavelength for all spectra within a predefined range.
    - If needed, add interpolation. Default: no interpolation (interpolation = False)
    - Parameters:
       - `data`: DataFrame containing 'wavelength' and 'flux' columns.
       - `wavelength_range`: Tuple representing the range of wavelengths to align.
       - `interpolation`: If True, perform interpolation. Default is False.
    - Returns: DataFrame with aligned wavelength spectra.

### 5. Data Augmentation Module (Data Augmentation in API diagram)
  - **Function: standard_derivative(flux: numpy.ndarray, wavelength: numpy.ndarray) -> array:**
    - Calculates the standard derivative of flux with respect to wavelength.
    - Parameters:
      - `flux`:  A numpy array of flux data.
      - `wavelength`: A numpy array of wavelength data.
    - Returns: The derivative of flux with respect to wavelength.

  - **Function: fractional_derivative(flux: numpy.ndarray, wavelength: numpy.ndarray, order: float, h: float = 1e-5, max_terms: int = 50) -> array:**
    - Calculates the fractional derivative of flux with respect to wavelength using the Grünwald-Letnikov approach.
    - Parameters:
      - `flux`: The flux data (as a numpy array).
      - `wavelength`: The wavelength data (as a numpy array).
      - `order`: The order of the derivative (fractional).
      - `h`: The step size for numerical differentiation (default is 1e-5).
      - `max_terms`: Maximum number of terms to include in the sum (default is 50).
    - Returns: The fractional derivative of flux with respect to wavelength.
  
  - **Function: augment_data(data: pd.DataFrame, methods: list, frac_order: float = None) -> DataFrame:**
   - Computes derivatives and fractional derivatives of flux with respect to wavelength, appending them to each preprocessed spectrum in the DataFrame.
   - Parameters:
      - `data`: The DataFrame containing spectral data to augment. Assumes 'flux' and 'wavelength' columns are present.
      - `methods`: A list of callable functions that define the augmentation methods to be applied.
      - `frac_order`: The order of the fractional derivative.
   - Returns: The augmented DataFrame.

### 6. Machine Learning Module (Additional Feature 1, Astronomical Classifier in API diagram)
  - **Function: prepare_data(data: pd.DataFrame) -> Tuple:**
   - Prepares the data for machine learning by cleaning, normalizing, and splitting it into training, validation, and testing sets.
   - Parameters:
     - `data`: The DataFrame containing spectral data.  
   - Returns: Tuple containing X_train, X_val, y_train, y_val, and X_test. 

  - **Function: fit_model(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> RandomForestClassifier:**
   - Fits a RandomForestClassifier model to the training data and evaluates it using the validation data. It also visualizes the confusion matrix.
   - Parameters:
     - `X_train`: The training data features.
     - `y_train`: The training data labels.
     - `X_val`: The validation data features.
     - `y_val`: The validation data labels.
   - Returns: The trained Random Forest classifier model.

  - **Function: predict_class(model: RandomForestClassifier, data: pd.DataFrame) -> Series:**
   - Predicts class labels for samples in the given data using the trained model.
   - Parameters:
     - `model`: The trained Random Forest classifier model.
     - `data`: The data for which class labels need to be predicted.
   - Returns: Predicted class labels.

  - **Function: predict_proba(model: RandomForestClassifier, data: pd.DataFrame) -> DataFrame:**
   - Predicts class probabilities for samples in the given data using the trained model.
   - Parameters:
     - `model`: The trained Random Forest classifier model.
     - `data`: The data for which class probabilities need to be predicted.
   - Returns: DataFrame containing predicted class probabilities.

### 7. Spectral Feature Extraction (Additional Feature 2, Feature Extractor in API diagram)
  - **Function: extract_spectral_features(data: pd.DataFrame) -> array:**
    - Extract spectral features defining emission and absorption lines as those with flux levels exceeding 2 sigma from the continuum.
    - Parameters:
      - `data`: The DataFrame containing the observed spectral data which includes `flux`, `loglam` (log of wavelength), and `model` (continuum).
    - Returns: Array 1 containing the wavelength of emission, array 2 containing the wavelengh of absorption, and array 3 is the potential error message.

### 8. Visualization Module (Spectral Visualizer in API diagram)
  - **Function: visualize_spectrum(data: DataFrame, continuum_overlay: bool = True) -> None:**
    - Uses matplotlib to create static plots of the spectral data with options for overlays and annotations.
    - Parameters:
      - `data`: The DataFrame containing spectral data to be plotted.
      - `continuum_overlay`: A boolean indicating whether a continuum overlay should be added to the plot.
    - Returns: A matplotlib Figure object of the plotted data.

## Implementation Specifications
- Developers will select and implement at least two additional features from Annex B.
- The methodology used should be flexible for future changes without compromising library functions.

## Documentation and Reporting
- All design and implementation details will be documented and reviewed with the client prior to the final submission.
