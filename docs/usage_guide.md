## User Guide: Astronomical Research Library for Astronomical Data

This guide provides an overview and usage instructions for functions designed to work with astronomical data from the Sloan Digital Sky Survey (SDSS)

### 1. Data Preprocessing Module (Data Preprocessing in API diagram)

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

### 2. Metadata Extraction Module (Metadata Extraction in API diagram)

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

### 3. Wavelength Alignment Module (Wavelength Alignment in API diagram)
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

### 4. Visualization Module (Spectral Visualizer in API diagram)


### 5. Data Augmentation Module (Data Augmentation in API diagram)

#### `augment_data(data: DataFrame, methods:List) -> DataFrame:`
Computes derivatives and fractional derivatives, appending them to each preprocessed spectra.

**Parameters:**

- `data`: The DataFrame containing spectral data to augment.
- `method`: A list of callable functions that define the augmentation methods to be applied.
- `frac_order`: The order of the fractional derivative.

**Returns:**

- `pd.DataFrame`: The augmented DataFrame.

**Usage:**
```python
augmented_df = augment_data(spectra, methods=['standard_derivative', 'fractional_derivative'], frac_order=0.75)
```

---

### Important Notes:
- Ensure you have the necessary packages (`pandas` and `astroquery`) installed in your Python environment.
- These functions are specifically designed for processing astronomical data and may not be suitable for other types of data without modifications.
- Handle the data responsibly, especially when it comes to managing large datasets or sensitive information.
