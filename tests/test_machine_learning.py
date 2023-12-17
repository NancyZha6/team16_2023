from machine_learning import *
from data_query import *
from data_preprocessing import *
import pytest
import pandas as pd


# Sample data for testing
def generate_sample_data():
    adql_query = """
    SELECT top 20 plate,mjd,fiberid
    FROM dbo.SpecObj
    """
    data = load_data_ids(adql_query)
    return data


# test machine learning module
def test_machine_learning():
    # Test for prepare_data function
    sample_data = generate_sample_data()
    X_train, X_val, y_train, y_val, X_test = prepare_data(sample_data)
    assert not X_train.empty
    assert not X_val.empty
    assert not y_train.empty
    assert not y_val.empty
    assert not X_test.empty

    # Test for fit_model function
    model = fit_model(X_train, y_train, X_val, y_val)
    assert model is not None

    # Test for predict_class function
    predictions = predict_class(model, X_test)
    assert not predictions.empty

    # Test for predict_proba function
    proba = predict_proba(model, X_test)
    assert not proba.empty
