# NEW META DATA EXTRACTION
from typing import List
import pandas as pd

def extract_metadata(data, identifiers=True, equivalent_width=True, coordinates=True, redshifts=True, other_fields=None):
    if data.empty:
        raise Exception("Dataset is empty")
    
    metadata = pd.DataFrame()

    # Extract object identifiers
    if identifiers:
        if 'SPECOBJID' in data.columns:
            metadata['specObjID'] = data['SPECOBJID']
        else:
            raise Exception("Missing 'specObjID' column in the provided DataFrame")

    # Extract equivalent_widths
    if equivalent_width:
        if 'LINEEW' in data.columns:
            metadata['equivalent_width'] = data['LINEEW']
        else:
            raise Exception("Missing 'LINEEW' column in the provided DataFrame")

    # Extract object coordinates
    if coordinates:
        if 'RA' in data.columns and 'DEC' in data.columns:
            metadata['coord.red_ascension'] = data['RA']
            metadata['coord.declination'] = data['DEC']
        else:
            missing_columns = []
            if 'RA' not in data.columns:
                missing_columns.append("'RA'")
            if 'DEC' not in data.columns:
                missing_columns.append("'DEC'")
            raise Exception(f"Missing {', '.join(missing_columns)} column(s) in the provided DataFrame")

    # Extract redshifts
    if redshifts:
        if 'Z' in data.columns:
            metadata['redshift'] = data['Z']
        else:
            raise Exception("Missing 'Z' column in the provided DataFrame")

    # Extract other specified fields
    if other_fields:
        for field in other_fields:
            if field in data.columns:
                metadata[field] = data[field]
            else:
                raise Exception(f"Missing '{field}' column in the provided DataFrame")

    return metadata
