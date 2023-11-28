import pytest
import pandas as pd
from data_preprocessing import *

def test_load_data():
	# test with a valid file path
	df = load_data('valid_query.txt')
	assert not df.isnull().values.any(), "Function should not return to null"""