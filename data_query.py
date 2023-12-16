import requests
from astropy.io import fits
import pandas as pd
from astroquery.sdss import SDSS
from astropy.table import Table

def load_data_sql(adql_query: str = None) -> pd.DataFrame:
    """
    Retrieves SDSS data based on an ADQL query or identifiers.

    Parameters:
    adql_query (str, optional): ADQL query to retrieve data. Default is None.

    Returns:
    pd.DataFrame: DataFrame containing SDSS data defined by the query or identifiers.
    """
    try:
        # Use ADQL query to retrieve data
        result = SDSS.query_sql(adql_query).to_pandas()
    except Exception as e:
        print(e)

    return result

def load_data_file(file=None):
    """
    Loads SDSS data from a FITS file.

    Parameters:
    file (str): FITS file path that meets SDSS format.

    Returns:
    dict: Dictionary containing DataFrames for each HDU in the FITS file.
    """

    if file is None:
      raise Exception("You need to provide a fits file that meets SDSS format")
    HDUs = fits.open(file, ignore_missing_simple=True)
    # Initialize an empty dictionary to store DataFrames
    dataframes = {}
    # Iterate over all HDUs in the result
    identifiers=Table(HDUs[2].data)[['CLASS','SPECOBJID',"Z"]].to_pandas()
    for i in range(4):
        try:
            # convert to table
            hdu=HDUs[i]
            if i==2:
              data_table=Table(hdu.data)[['Z','RA','DEC','CLASS','SPECOBJID','OBJID']]
            else:
              data_table = Table(hdu.data)
            # Convert to dataframe
            df = data_table.to_pandas()
            # add identifiers to all tables except for hdu_2 since it already has them
            if i !=2:
              repeats=len(df)
              df_identifier = pd.concat([identifiers] * repeats, ignore_index=True)
              df = pd.concat([df, df_identifier], axis=1)
            # Save the DataFrame in the dictionary with a unique key
            dataframes[f"hdu_{i}"] = df
        except Exception as e:
            pass

    return dataframes


def load_data_ids(ids_query=None) -> pd.DataFrame:
    """
    Retrieves SDSS data based on plateid, fiberid, and mjd.

    Parameters:
    ids_query (str, optional): ADQL query to extract plateid, fiberid, and mjd. Default is None.

    Returns:
    dict: Dictionary containing DataFrames for each HDU with extracted spectra.
    """

    if ids_query is None:
      raise Exception("You need to provide a query to extract plateid, mjd, and fiberid, or a fits file that meets SDSS format")

    ids = SDSS.query_sql(ids_query).to_pandas()
    dataframes={}
    for index, row in ids.iterrows():
      try:
        result = SDSS.get_spectra(plate=row['plate'], fiberID=row['fiberid'], mjd=row['mjd'])
        HDUs=result[0]
        identifiers=Table(HDUs[2].data)[['CLASS','SPECOBJID','Z']].to_pandas()
        for i in range(1,4):
            # convert to table
            hdu=HDUs[i]
            if i==2:
              data_table=Table(hdu.data)[['Z','RA','DEC','CLASS','SPECOBJID','OBJID']]
            else:
              data_table = Table(hdu.data)
            # Convert to dataframe
            df = data_table.to_pandas()
            # add identifiers to all tables except for hdu_2 since it already has them
            if i !=2:
              repeats=len(df)
              df_identifier = pd.concat([identifiers] * repeats, ignore_index=True)
              df = pd.concat([df, df_identifier], axis=1)
            # Save the DataFrame in the dictionary with a unique key
            if f"hdu_{i}" in dataframes.keys(): dataframes[f"hdu_{i}"]=pd.concat(objs=[dataframes[f"hdu_{i}"],df])
            else: dataframes[f"hdu_{i}"] =df
      except Exception as e:
        print(e)
    return dataframes



def load_data_constraints(constraints: dict) -> pd.DataFrame:
    """
    Retrieves SDSS data based on constraints provided in the form of a dictionary.

    Parameters:
    constraints (dict): Dictionary of constraints to put in the WHERE statement of the query.

    Returns:
    pd.DataFrame: DataFrame containing SDSS data defined by the constraints.
    """
    query = f"SELECT * FROM SpecObj WHERE "
    query += " AND ".join([f"{key}={value}" for key, value in constraints.items()])

    result = SDSS.query_sql(query)
    data = result.get_fits_spectrum().to_pandas()
    return data
