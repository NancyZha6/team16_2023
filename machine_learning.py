from data_query import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from data_preprocessing import normalize, remove_outliers
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def prepare_data(data:pd.DataFrame):
    data_pre=data['hdu_1'][['flux','loglam','CLASS']]
    cleaned_data=remove_outliers(data_pre,to_remove_columns=['flux','loglam'],threshold=0.1)
    normalized_data=normalize(cleaned_data)
    X=normalized_data[['flux','loglam']]
    y=normalized_data['CLASS']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
    return X_train, X_val, y_train, y_val, X_test


def fit_model(X_train: pd.DataFrame, y_train: pd.DataFrame, X_val: pd.DataFrame,y_val: pd.DataFrame):
    # Fit the model to the training data.
    model=RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    prediction=model.predict(X_val)
    conf_matrix = confusion_matrix(y_val, prediction, labels=["STAR", "GALAXY", "QSO"])

    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)  # Adjust the font size
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False, square=True,
                xticklabels=["Predicted Star", "Predicted Galaxy", "QSO"],
                yticklabels=["Actual Star", "Actual Galaxy","Actual QSO"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()
    return model


def predict_class(model: RandomForestClassifier,data: pd.DataFrame) -> pd.Series:
    # Predict class labels for samples in data.
    prediction=pd.Series(model.predict(data))

    return prediction


def predict_proba(model: RandomForestClassifier, data: pd.DataFrame) -> pd.DataFrame:
    # Predict class probabilities for samples in data.
    return pd.DataFrame(model.predict_proba(data))