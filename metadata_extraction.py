from typing import List
import pandas as pd

def extract_metadata(data, identifiers=True, equivalent_width=True, coordinates=True, redshifts=True, other_fields=None):
    if data.empty:
        raise Exception("Dataset is empty")
    
    metadata = pd.DataFrame()

    # Extract object identifiers
    if identifiers:
        if 'specObjID' in data.columns:
            metadata['object_id'] = data['specObjID']
        else:
            raise Exception("Missing 'specObjID' column in the provided DataFrame")

    # Extract equivalent_widths
    if equivalent_width:
        if 'h_beta_eqw' in data.columns:
            metadata['equivalent_width'] = data['h_beta_eqw']
        else:
            raise Exception("Missing 'h_beta_eqw' column in the provided DataFrame")

    # Extract object coordinates
    if coordinates:
        if 'ra' in data.columns and 'dec' in data.columns:
            metadata['coord.red_ascension'] = data['ra']
            metadata['coord.declination'] = data['dec']
        else:
            missing_columns = []
            if 'ra' not in data.columns:
                missing_columns.append("'ra'")
            if 'dec' not in data.columns:
                missing_columns.append("'dec'")
            raise Exception(f"Missing {', '.join(missing_columns)} column(s) in the provided DataFrame")

    # Extract redshifts
    if redshifts:
        if 'z' in data.columns:
            metadata['redshift'] = data['z']
        else:
            raise Exception("Missing 'z' column in the provided DataFrame")

    # Extract other specified fields
    if other_fields:
        for field in other_fields:
            if field in data.columns:
                metadata[field] = data[field]
            else:
                raise Exception(f"Missing '{field}' column in the provided DataFrame")

    return metadata
