## User Guide: Astronomical Research Library for Astronomical Data

This guide provides an overview and usage instructions for functions designed to work with astronomical data from the Sloan Digital Sky Survey (SDSS)

### 1. Data Query Module (Data Query in API diagram)

#### load_data_sql(adql_query: str = None) -> pd.DataFrame
This function retrieves SDSS data based on an ADQL query or identifiers. You can input your ADQL query as a string, and the function will return a pandas DataFrame containing the requested data.

**Parameters:**
- `adql_query` (str, optional): ADQL query to retrieve data. Default is None.

**Returns:**
- `pd.DataFrame`: DataFrame containing SDSS data defined by the query or identifiers.

**Usage:**
```python
adql_query = "SELECT top 10 plate, mjd, fiberid FROM dbo.SpecObj"
df = load_data_sql(adql_query)
```

#### load_data_file(file: str) -> dict
This function loads SDSS data from a FITS file. You need to provide the file path of a FITS file that meets the SDSS format, and the function will return a dictionary containing DataFrames for each Header Data Unit (HDU) in the FITS file.

**Parameters:**
- `file` (str): FITS file path that meets SDSS format.

**Returns:**
- `dict`: Dictionary containing DataFrames for each HDU in the FITS file.

**Usage:**
```python
fits_file_path = 'path/to/sdss_data.fits' # e.g. 'spectrum.fits'
dataframes = load_data_file(fits_file_path)
```

#### load_data_ids(ids_query: str = None) -> dict
This function retrieves SDSS data based on plateid, fiberid, and mjd. You can input an ADQL query to extract plateid, mjd, and fiberid, or provide a fits file that meets the SDSS format. The function returns a dictionary containing DataFrames for each HDU with extracted spectra.

**Parameters:**
- `ids_query` (str, optional): ADQL query to extract plateid, fiberid, and mjd. Default is None.

**Returns:**
- `dict`: Dictionary containing DataFrames for each HDU with extracted spectra.

**Usage:**
```python
ids_query = "SELECT plate, fiberid, mjd FROM dbo.SpecObj WHERE class IN ('STAR', 'GALAXY', 'QSO')"
dataframes = load_data_ids(ids_query)
```

#### load_data_constraints(constraints: dict) -> pd.DataFrame
This function retrieves SDSS data based on constraints provided in the form of a dictionary. You need to pass a dictionary of constraints to put in the WHERE statement of the query. The function constructs the query and returns a pandas DataFrame containing SDSS data defined by the constraints.

**Parameters:**
- `constraints (dict)`: Dictionary of constraints to put in the WHERE statement of the query.

**Returns:**
- `pd.DataFrame`: DataFrame containing SDSS data defined by the constraints.

**Usage:**
```python
constraints = {'column1': [value1, value2], 'column2': [value3, value4]}
df = load_data_constraints(constraints)
```


### 2. Data Preprocessing Module (Data Preprocessing in API diagram)

#### `load_data(adql_query: str) -> pd.DataFrame`
This function fetches data from the SDSS database using an Astronomical Data Query Language (ADQL) query. Simply input your query as a string.

**Parameters:**
- `adql_query` (str): The query string in ADQL format to retrieve data.

**Returns:**
- `pd.DataFrame`: A DataFrame containing the data fetched from SDSS based on the ADQL query.

**Usage:**
```python
myquery = 'select top 10 objid, ra, dec, r ' # note the space at the end of this string - important
myquery += 'from galaxy '
myquery += 'where clean = 1'
df=load_data(myquery)
```

#### `normalize(data: pd.DataFrame, exclude_columns=['objectid']) -> pd.DataFrame`
Normalizes the **numerical columns** in a DataFrame. It normalizes each numerical column by subtracting its mean and dividing by its standard deviation. If the standard deviation is zero, it only subtracts the mean. It will ignore non-numerical columns

**Parameters:**

- `data` (pd.DataFrame): DataFrame containing the spectral data to normalize.
- `exclude_columns` (list, optional): List of columns to exclude from normalization. Defaults to ['objectid'].

**Returns:**
- `pd.DataFrame`: A DataFrame containing the normalized spectral data.

**Usage:**
```python
# Exclude 'objectid' from normalization
normalized_data = normalize(data, exclude_columns=['objectid'])

# Resulting DataFrame with normalized spectral data
print(normalized_data)
```
**Note:** This function will throw an exception if the input DataFrame is empty. Ensure that the DataFrame contains the necessary spectral data before applying normalization.


#### `remove_outliers(data: pd.DataFrame, threshold: float, to_remove_columns: list) -> pd.DataFrame`
Removes outliers from the spectral data based on the specified percentile threshold for selected columns.

**Parameters:**
- `data` (pd.DataFrame): DataFrame containing the spectral data to remove outliers.
- `threshold` (float): The percentile threshold to remove outliers. For example, threshold=0.1 removes the top and bottom 5% of data as outliers.
to_remove_columns (list): List of columns to perform outlier removal on.
- `to_remove_columns` (list): a list of columns to perform outlier removal on 

**Returns:**
- `pd.DataFrame`: The DataFrame with outliers removed.

**Usage:**
```python
# Remove outliers from 'flux_A' and 'flux_B'
cleaned_data = remove_outliers(data, threshold=0.1, to_remove_columns=['flux_A', 'flux_B'])
```
**Note:** This function will throw an exception if the input DataFrame is empty. 


#### `interpolate(spectra, flux_column='flux', wavelength_column='wavelength') -> pd.DataFrame`
Interpolates values in the spectra DataFrame.

**Parameters:**

- `spectra` (pd.DataFrame): DataFrame containing flux and wavelength columns.
- `flux_column` (str, optional): Name of the flux column.
- `wavelength_column` (str, optional): Name of the wavelength column.

**Returns:**

- `pd.DataFrame`: Interpolated and subsampled DataFrame.

**Usage:**
```python
interpolated_df = interpolate(spectra)
```

#### `correct_redshift(spectra, wavelenght_column='wavelength', redshift_column='redshift') -> pd.DataFrame`
Corrects the redshift in the wavelengths of the spectra DataFrame.

**Parameters:**

- `spectra` (pd.DataFrame): DataFrame containing 'wavelength' and 'flux' columns.
- `wavelenght_column` (str): name of the column in spectra datafram that contains wavelength
- `redshift_column` (str, optional): Name of the redshift column.

**Returns:**

- `pd.DataFrame`: DataFrame with corrected wavelengths.

**Usage:**
```python
corrected_df = correct_redshift(spectra)
```

### 3. Metadata Extraction Module (Metadata Extraction in API diagram)

#### `extract_metadata(data: pd.DataFrame, identifiers=True, equivalent_width=True, coordinates=True, redshifts=True, other_fields=None) -> pd.DataFrame`
Extracts metadata from a DataFrame containing spectral data based on specified parameters.

**Parameters:**

- `data` (pd.DataFrame): DataFrame containing spectral data.
- `identifiers` (bool, optional): If True, extract object identifiers. Defaults to True.
- `equivalent_width` (bool, optional): If True, extract equivalent widths. Defaults to True.
- `coordinates` (bool, optional): If True, extract object coordinates (red ascension and declination). Defaults to True.
- `redshifts` (bool, optional): If True, extract redshifts. Defaults to True.
- `other_fields` (List[str], optional): List of other fields to extract from the DataFrame. Defaults to None.

**Returns:**

- `pd.DataFrame`: DataFrame containing the extracted metadata.

**Usage:**
```python
# Extract metadata with default parameters
metadata_default = extract_metadata(spectral_data)

# Optionally, customize the extraction
metadata_customized = extract_metadata(spectral_data, equivalent_width=False, redshifts=False, other_fields=['field1', 'field2'])
```

### 4. Wavelength Alignment Module (Wavelength Alignment in API diagram)
#### `align_wavelength(data: pd.DataFrame, wavelength_range: Tuple[float, float], interpolation: bool = False) -> pd.DataFrame`
Aligns the wavelength for all spectra within a predefined range in a DataFrame.

**Parameters:**

- `data` (pd.DataFrame): DataFrame containing 'wavelength' and 'flux' columns.
- `wavelength_range (Tuple[float, float])`: Tuple representing the range of wavelengths to align.
- `interpolation (bool, optional)`: If True, perform interpolation. Default is False.

**Returns:**

- `pd.DataFrame`: DataFrame with aligned wavelength spectra.

**Usage:**
```python
# Align the wavelength within the specified range without interpolation
aligned_data = align_wavelength(data, wavelength_range=(505, 525), interpolation=False)

# Optionally, align with interpolation
aligned_data_interpolated = align_wavelength(data, wavelength_range=(505, 525), interpolation=True)
```

### 5. Data Augmentation Module (Data Augmentation in API diagram)

#### standard_derivative(flux: numpy.ndarray, wavelength: numpy.ndarray) -> numpy.ndarray
This function calculates the standard derivative of flux with respect to wavelength.

**Parameters:**

- `flux` (numpy.ndarray): A numpy array of flux data.
- `wavelength` (numpy.ndarray): A numpy array of wavelength data.

**Returns:**

- `numpy.ndarray`: The derivative of flux with respect to wavelength.

**Usage:**
```python
augmented_data_deriv = augment_data(corrected_data, ['standard_derivative'])
```

#### fractional_derivative(flux: numpy.ndarray, wavelength: numpy.ndarray, order: float, h: float = 1e-5, max_terms: int = 50) -> numpy.ndarray
This function calculates the fractional derivative of flux with respect to wavelength using the Grünwald-Letnikov approach.

**Parameters:**

- `flux` (numpy.ndarray): The flux data (as a numpy array).
- `wavelength` (numpy.ndarray): The wavelength data (as a numpy array).
- `order` (float): The order of the derivative (fractional).
- `h` (float): The step size for numerical differentiation (default is 1e-5).
- `max_terms` (int): Maximum number of terms to include in the sum (default is 50).

**Returns:**
- `numpy.ndarray`: The fractional derivative of flux with respect to wavelength.

**Usage:**
```python
augmented_data_frac = augment_data(corrected_data, ['fractional_derivative'], 0.5)
```

#### augment_data(data: pd.DataFrame, methods: list, frac_order: float = None) -> pd.DataFrame
This function computes derivatives and fractional derivatives of flux with respect to wavelength, appending them to each preprocessed spectrum in the DataFrame.

**Parameters:**

- `data` (pd.DataFrame): The DataFrame containing spectral data to augment. Assumes 'flux' and 'wavelength' columns are present.
- `methods` (list): A list of callable functions that define the augmentation methods to be applied.
- `frac_order` (float): The order of the fractional derivative.

**Returns:**
- `pd.DataFrame`: The augmented DataFrame.

**Usage:**
```python
augmented_data = augment_data(corrected_data, ['standard_derivative','fractional_derivative'], 0.5)
```


### 6. Machine Learning Module (Additional Feature 1, Astronomical Classifier in API diagram)

#### prepare_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]
This function prepares the data for machine learning by cleaning, normalizing, and splitting it into training, validation, and testing sets.

**Parameters:**

- `data` (pd.DataFrame): The DataFrame containing spectral data.

**Returns:**
- `Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]`: Tuple containing X_train, X_val, y_train, y_val, and X_test.

**Usage:**
```python
X_train, X_val, y_train, y_val, X_test = prepare_data(data3)
```
#### fit_model(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> RandomForestClassifier
This function fits a RandomForestClassifier model to the training data and evaluates it using the validation data. It also visualizes the confusion matrix.

**Parameters:**

- `X_train` (pd.DataFrame): The training data features.
- `y_train` (pd.Series): The training data labels.
- `X_val` (pd.DataFrame): The validation data features.
- `y_val` (pd.Series): The validation data labels.

**Returns:**
- `RandomForestClassifier`: The trained Random Forest classifier model.

**Usage:**
```python
model=fit_model(X_train,y_train,X_val,y_val)
```

#### predict_class(model: RandomForestClassifier, data: pd.DataFrame) -> pd.Series
This function predicts class labels for samples in the given data using the trained model.

**Parameters:**

- `model` (RandomForestClassifier): The trained Random Forest classifier model.
- `data` (pd.DataFrame): The data for which class labels need to be predicted.

**Returns:**
- `pd.Series`: Predicted class labels.

**Usage:**
```python
prediction=predict_class(model,X_test)
```

#### predict_proba(model: RandomForestClassifier, data: pd.DataFrame) -> pd.DataFrame
This function predicts class probabilities for samples in the given data using the trained model.

**Parameters:**

- `model` (RandomForestClassifier): The trained Random Forest classifier model.
- `data` (pd.DataFrame): The data for which class probabilities need to be predicted.

**Returns:**
- `pd.DataFrame`: DataFrame containing predicted class probabilities.

**Usage:**
```python
prediction_prob=predict_proba(model,X_test)
```

### 7. Spectral Feature Extraction (Additional Feature 2, Feature Extractor in API diagram)

#### extract_spectral_features(data: pd.DataFrame) -> np.array, np.array, None
This function identifies emission and absorption lines based on residuals in the provided DataFrame.
    
**Parameters:**
- `data` (pd.DataFrame): The data with columns 'loglam', 'flux', and 'model'.

**Returns:**
- `np.array`: The first array is provided: wavelengths with emission
- `np.array`: The second array is provided: wavelengths with absorption

**Usage:**
```python
emission_wavelengths, absorption_wavelengths = extract_spectral_features(data)
```

### 8. Visualization Module (Spectral Visualizer in API diagram)

#### plot_spectrum(df: pd.DataFrame, continuum=True, emission_lines=None, absorption_lines=None) -> None
This function uses matplotlib to create static plots of the spectral data with options for overlay of the continuum data and annotations of emission and absorption spectra.

**Parameters:**
- `data` (pd.DataFrame): The data with columns 'loglam', 'flux', and 'model'.

**Usage:**
```python
plot_spectrum(data, emission_lines = emission_wavelengths, absorption_lines = absorption_wavelength)
```
---

### Important Notes:
- Ensure you have the necessary packages (`numpy`, `pandas` and `astroquery`) installed in your Python environment.
- These functions are specifically designed for processing astronomical data and may not be suitable for other types of data without modifications.
- Handle the data responsibly, especially when it comes to managing large datasets or sensitive information.
