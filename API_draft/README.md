# API_draft README

## Overview
This folder contains the draft of the Application Programming Interface (API) for the astronomical research library. The library aims to assist in the classification of astronomical objects, specifically stars, galaxies, and QSOs, by interfacing with Sloan Digital Sky Survey (SDSS) services.

## Modules, Classes, and Functions

### 1. Data Preprocessing Module
- **Class: DataPreprocessing**
  - **Function: load_data(adql_query: str) -> DataFrame:**
    - Accepts an ADQL query as a string format and retrieves data from Sloan Digital Sky Survey (SDSS) database.
    - Parameters:
      - `adql_query`: the query to retrieve data in string format
    - Returns: Dataframe containing SDSS data defined via the query. 
    
  - **Function: normalize(data: DataFrame) -> DataFrame:**
    - Normalizes the spectral data.
    - Parameters:
      - `data`: the data to normalize
    - Returns: Dataframe containing normalized data.

  - **Function: remove_outliers(data: DataFrame, threshold: float) -> DataFrame:**
    - Removes outliers above/below specific threshold from the spectral data 
    - Parameters:
      - `data`: the data to remove outliers
      - `threshold`: the percentile threshold to remove outliers. E.g. threshold=0.9: remove top and bottom 10% data as outliers 
    - Returns: Dataframe containing data with outliers removed.  

  - **Function: interpolate(data: DataFrame) -> DataFrame:**
    - Performs interpolation on the spectral data.
    - Parameters:
      - `data`: data to perform interpolation on 
    - Returns: Dataframe containing interpolated data 

  - **Function: correct_redshift(data: DataFrame) -> DataFrame:**
    - Corrects redshift in the spectral data.
    - Parameters:
      - `data`: the data to correct red shift on 
    - Returns: Dataframe containing data with red shift corrected.

### 2. Metadata Extraction Module
- **Class: MetadataExtractor**
  - **Function: extract_metadata(data: DataFrame, identifiers: bool = True, coordinates: bool = True, chemical_abundances: bool = True, redshifts: bool = True, other_fields: List[str] = None) -> DataFrame:**
    - Extracts metadata from the spectral data based on user-defined parameters.
      - Parameters:
        - `data`: the data to extract metadata from
        - `identifiers`: If True, extract object identifiers.
        - `coordinates`: If True, extract object coordinates.
        - `chemical_abundances`: If True, extract chemical abundances.
        - `redshifts`: If True, extract redshifts.
        - `other_fields`: A list of other fields to extract if specified.
      - Returns: Dataframe containing the extracted metadata.

### 3. Wavelength Alignment Module
- **Class: WavelengthAlignment**
  - **Function: align_wavelength(data: DataFrame, wavelength_range: Tuple[float, float], interpolation = False) -> DataFrame:**
    - Aligns the wavelength for all spectra within a predefined range
    - If needed, add interpolation. Default: no interpolation (interpolation = False)
    - Returns: DataFrame with aligned wavelength spectra.

### 4. Visualization Module
- **Class: SpectralVisualizer**
  - **Function: visualize_spectrum(data: DataFrame, continuum_overlay: bool = True) -> None:**
    - Uses matplotlib to create static plots of the spectral data with options for overlays and annotations.
    - Parameters:
      - `data`: The DataFrame containing spectral data to be plotted.
      - `continuum_overlay`: A boolean indicating whether a continuum overlay should be added to the plot.
    - Returns: A matplotlib Figure object of the plotted data.

### 5. Data Augmentation Module
- **Class: DataAugmentation**
  - **Function: augment_data(data: DataFrame, methods:List) -> DataFrame:**
    - Computes derivatives and fractional derivatives, appending them to each preprocessed spectra.
    - Parameters:
       - `data`: The DataFrame containing spectral data to augment.
       - `method`: A list of callable functions that define the augmentation methods to be applied.
    - Returns: The augmented DataFrame.

### 6. Machine Learning Module (Additional Feature 1)
- **Class: AstronomicalClassifier**
  - **Function: fit(X_train: DataFrame, y_train: DataFrame) -> None:**
    - Trains a machine learning model to distinguish between Stars, Galaxies, and QSOs.
    - Parameters:
      - `X_train` Training data with spectral features.
      - `y_train` Target labels (Stars, Galaxies, QSOs).

  - **Function: predict(data: DataFrame) -> Series:**
    - Predicts based on spectral data of astronomical objects.
    - Parameters:
      - `data` Data to predict on using the trained model
    - Returns: A series of predicted labels.

  - **Function: predict_proba(data: DataFrame) -> DataFrame:**
    - Prediction probabilities.
    - Parameters:
      - `data` Data to predict on using the trained model
    - Returns: Predicted probabilities for each class label.

### 7. Spectral Feature Extraction (Additional Feature 2)
- **Class: FeatureExtractor**
  - **Function: extract_spectral_features(data: DataFrame, continuum: DataFrame, sigma_level:float) -> DataFrame:**
    - Extracts spectral features defining emission and absorption lines.
    - Parameters:
      - `data`: The DataFrame containing the observed spectral data which includes flux values for various wavelengths.
      - `continuum`: The DataFrame containing the estimated continuum levels corresponding to the wavelength.
      - `sigma_level`: The number of standard deviations used to identify significant deviations from the continuum.
    - Returns: DataFrame containing the identified spectral features.

## Implementation Specifications
- Developers will select and implement at least two additional features from Annex B.
- The methodology used should be flexible for future changes without compromising library functions.

## Documentation and Reporting
- All design and implementation details will be documented and reviewed with the client prior to the final submission.

