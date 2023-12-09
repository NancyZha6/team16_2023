## User Guide: Data Processing Functions for Astronomical Data

This guide provides an overview and usage instructions for functions designed to work with astronomical data from the Sloan Digital Sky Survey (SDSS)

### 1. `load_data(adql_query: str) -> pd.DataFrame`

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

### 2. `normalize(data: pd.DataFrame) -> pd.DataFrame`

Normalizes the **numerical columns** in a DataFrame. It normalizes each numerical column by subtracting its mean and dividing by its standard deviation. If the standard deviation is zero, it only subtracts the mean. It will ignore non-numerical columns

**Parameters:**
- `data` (pd.DataFrame): The DataFrame containing the data to be normalized.

**Returns:**
- `pd.DataFrame`: The DataFrame with numerical columns normalized.

**Usage:**
```python
normalized_df = normalize(df)
```
**Note:** This function will throw an exception if the input DataFrame is empty. 


### 3. `remove_outliers(data: pd.DataFrame, threshold: float) -> pd.DataFrame`

Removes outliers from a DataFrame based on the specified percentile threshold. It removes outliers as values below the lower percentile threshold and above the upper percentile threshold. The threshold will be split into 2 half to cover both the top and bottom outliers. 

**Parameters:**
- `data` (pd.DataFrame): The DataFrame containing the data from which to remove outliers.
- `threshold` (float): The percentile threshold to identify outliers (e.g., 0.1 for top and bottom 5%).
- `to_remove_columns` (list): a list of columns to perform outlier removal on 

**Returns:**
- `pd.DataFrame`: The DataFrame with outliers removed.

**Usage:**
```python
cleaned_df = remove_outliers(df, 0.1)
```

**Note:** This function will throw an exception if the input DataFrame is empty. 


### 4. `interpolate(spectra, flux_column='flux', wavelength_column='wavelength') -> pd.DataFrame`
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

### 5. `correct_redshift(spectra, redshift_column='redshift') -> pd.DataFrame`
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

---

### Important Notes:
- Ensure you have the necessary packages (`pandas` and `astroquery`) installed in your Python environment.
- These functions are specifically designed for processing astronomical data and may not be suitable for other types of data without modifications.
- Handle the data responsibly, especially when it comes to managing large datasets or sensitive information.
