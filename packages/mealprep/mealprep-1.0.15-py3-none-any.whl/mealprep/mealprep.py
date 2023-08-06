import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def find_fruits_veg(df, type_of_out="categ", n_rows=100):
    """
    This function will drop row with NAs and find the index of columns with all
    numeric value or categorical value based on the specification.

    Parameters
    -----------
    df: pandas.core.frame.DataFrame
        Data frame that need to be proceed
    type_of_out: string
        Type of columns that we want to know index of, either 'categ' or 'num'
    n_rows: int
        The number of rows to check for each column. A higher value will ensure
        more accurate results, but will take longer to compute. By default, 100

    Returns
    -------
    list
        list of index of categorical or numerical values

    Example
    --------
    >>> df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    >>> find_fruits_veg(df, type_of_out = 'categ')
    [1]
    """
    list_of_categ = []
    list_of_num = []
    df_clean = df.dropna()
    if df_clean.shape[0] == 0:
        return "It is a empty data frame or too many missing data"
    num_rows_to_check = min(100, df_clean.shape[0])
    for i in np.arange(df_clean.shape[1]):
        is_str = []
        is_num = []
        for j in np.arange(num_rows_to_check):
            ij = df_clean.iloc[j, i]
            if isinstance(ij, str):
                is_str.append(True)
                is_num.append(False)
            elif (
                isinstance(ij, int)
                or isinstance(ij, float)
                or isinstance(ij, np.generic)
            ):
                is_str.append(False)
                is_num.append(True)
        # to be a numeric column, all values must be numeric
        if sum(is_num) == num_rows_to_check:
            list_of_num.append(i)
        # to be a string column, only one value must be str
        else:
            list_of_categ.append(i)
    if type_of_out == "categ":
        return list_of_categ
    elif type_of_out == "num":
        return list_of_num


def find_missing_ingredients(data):
    """
    For each column with missing values,
    this function will create a reference list of row indices,
    sum the number and calculate proportion of missing values

    Parameters
    -----------
    data: pandas.core.frame.DataFrame
        A dataframe that need to be processed

    Returns
    -------
    pandas.core.frame.DataFrame
        Data frame summarizing the indexes,
        count and proportion of missing values in each column

    Example
    --------
    >>> df = data.frame("letters" = c("a","b","c"),
                        "numbers" = c(1,2,3))
    >>> find_missing_ingredients(df)
    'There are no missing values'

    """
    if not isinstance(data, pd.core.frame.DataFrame):
        raise ValueError("`data` should be a pandas data frame")
    if data.shape[0] == 0:
        raise ValueError("The input data frame has no rows")

    if np.sum(np.sum(data.isna(), axis=0)) == 0:
        return "There are no missing values"

    counts = np.sum(data.isna(), axis=0)
    counts = counts[counts > 0]
    indices = []

    for column in data.columns:
        if np.sum(data[column].isna()):
            indices.append(data[column][data[column].isna()].index.values)

    else:
        report = pd.DataFrame(
            {
                "NaN count": counts,
                "NaN proportion": counts / data.shape[0],
                "NaN indices": indices,
            }
        ).reset_index()

        report["NaN proportion"] = pd.Series(
            ["{0:.1f}%".format(val * 100) for val in report["NaN proportion"]]
        )
        report = report.rename(columns={"index": "Column name"})

        return report


def find_bad_apples(df):
    """
    This function uses a univariate approach to outlier detection.
    For each column with outliers (values that are 2 or more
    standard deviations from the mean),
    this function will create a reference list of row indices with
    outliers, and the total number of outliers in that column.
    Note:
    This function works best for small datasets with
    unimodal variable distributions.
    Note:
    If your dataframe has duplicate column names,
    only the last of the duplicated columns will be checked.

    Parameters
    -----------
    df : pandas.core.frame.DataFrame
        A dataframe containing numeric data

    Returns
    -------
    bad_apples : pandas.DataFrame
        A dataframe showing 3 columns:
        Variable (column name),
        Indices (list of row indices with outliers), and
        Total Outliers (number of outliers in the column)

    Examples
    --------
    >>> df = pd.DataFrame({'A' : ['test', 1, 1, 1, 1])
    >>> find_bad_apples(df)
    ValueError: Every column in your dataframe must be numeric.
    >>> df = pd.DataFrame({'A' : [1, 1, 1, 1, 1],
    ...                    'B' : [10000, 1, 1, 1, 1]})
    >>> find_bad_apples(df)
    ValueError: Sorry, you don't have enough data.
    The dataframe needs to have at least 30 rows.
    >>> df = pd.DataFrame({'A' : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    ...                             1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ...                    'B' : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-100,
    ...                             1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,100],
    ...                    'C' : [1,1,1,1,1,19,1,1,1,1,1,1,1,1,19,1,1,1,1,
    ...                             1,1,1,1,1,1,1,19,1,1,1,1,1,1,1,1]})
    >>> find_bad_apples(df)
    Variable      Indices     Total Outliers
        B         [17, 34]          2
        C      [5, 14, 26]          3
    >>> df = pd.DataFrame({'A' : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    ...                             1,1,1,1,1,1,1,1,1,1,1,1,1],
    ...                    'B' : [1.000001, 1.000001, 1.000001, 1.000001,
    ...                           1.000001, 1.000001, 1.000001, 1.000001,
    ...                           1.000001, 1.000001, 1.000001, 1.000001,
    ...                           1.000001, 1.000001, 1.000001,
    ...                           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]})
    >>> find_bad_apples(df))
    Variable                Indices     Total Outliers
    No outliers detected        []              0
    """

    # Checks that every column in the dataframe is numeric
    if df.select_dtypes(include=["float", "int"]).shape[1] != df.shape[1]:
        raise ValueError("Every column in your dataframe must be numeric.")

    # Checks that there are at least 30 rows in the dataframe
    if df.shape[0] < 30:
        raise ValueError("Sorry, you don't have enough data. \
        The dataframe needs to have at least 30 rows.")

    columns = list(df)

    # Initializes empty dataframe
    output = pd.DataFrame(columns=["Variable", "Indices", "Total Outliers"])

    c = 0

    for column in columns:
        mean = round(df.mean(axis=0)[c], 3)
        sd = round(np.std(df.iloc[:, c]), 3)

        col = column
        ind = []
        tot = 0
        r = 0

        values = df.values[:, c]
        for value in values:
            if (mean - 2 * sd) <= value and value <= (mean + 2 * sd):
                r += 1
            else:
                ind.append(r)
                tot += 1
                r += 1
        c += 1

        if tot == 0:
            continue
        else:
            output = output.append(
                {"Variable": col, "Indices": ind, "Total Outliers": tot},
                ignore_index=True,
            )

    if len(output) == 0:
        output = output.append(
            {"Variable": "No outliers detected",
             "Indices": "x",
             "Total Outliers": tot},
            ignore_index=True,
        )
        return output
    else:
        return output


def make_recipe(
    X,
    y,
    recipe="ohe_and_standard_scaler",
    splits_to_return="train_test",
    random_seed=None,
    train_valid_prop=0.8,
):
    """
    The `make_recipe()` function is used to quickly apply common data
    preprocessing techniques

    Parameters
    ----------
    X : pandas.DataFrame
        A dataframe containing training, validation, and testing features.
    y : pandas.DataFrame
        A dataframe containing training, validation, and testing response.
    recipe : str
        A string specifying which recipe to apply to the data. The only recipe
        currently available is "ohe_and_standard_scaler". More recipes are
        under development. By default "ohe_and_standard_scaler"
    splits_to_return : str, optional
        "train_test" to return train and test splits, "train_test_valid" to
        return train, test, and validation data, "train" to return all data
        without splits. By default "train_test".
    random_seed : int, optional
        The random seed to set for splitting data to create reproducible
        results. By default None.
    train_valid_prop : float, optional
        The proportion to split the data by. Should range between 0 to 1. For
        example, if 0.8, than the trainin data would make up 0.8, while the
        test data would make up 0.2. By default = 0.8.

    Returns
    -------
    Tuple
        A tuple of pandas dataframes and numpy arrays. The X_ objects are
        pandas dataframes, while the y_ objects are numpy arrays.
        (X_train, X_valid, X_test, y_train, y_valid, y_test)

    Example
    --------
    >>> from vega_datasets import data
    >>> from mealprep.mealprep import make recipe
    >>> df = pd.read_json(data.cars.url).drop(columns=["Year"])
    >>> X = df.drop(columns=["Name"])
    >>> y = df[["Name"]]
    >>> X_tr X_va, X_te, y_tr, y_va, y_te = mealprep.make_recipe(
    ...        X=X, y=y, recipe="ohe_and_standard_scaler",
    ...        splits_to_return="train_test")
    """

    # validate inputs
    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y should have the same number of rows.")
    if recipe not in ["ohe_and_standard_scaler"]:
        raise ValueError("Please select a valid string option for recipe.")
    if splits_to_return not in ["train_test", "train_test_valid", "train"]:
        raise ValueError("Please enter a valid string for splits_to_return.")

    # clean input data
    y = y.to_numpy().ravel()

    # split data
    if splits_to_return == "train_test":
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=1 - train_valid_prop, random_state=random_seed
        )
        X_valid = None
        y_valid = None
    elif splits_to_return == "train_test_valid":
        X_train_valid, X_test, y_train_valid, y_test = train_test_split(
            X, y, test_size=1 - train_valid_prop, random_state=random_seed
        )
        X_train, X_valid, y_train, y_valid = train_test_split(
            X_train_valid,
            y_train_valid,
            test_size=1 - train_valid_prop,
            random_state=random_seed,
        )
    elif splits_to_return == "train":
        X_train = X
        y_train = y
        X_test = None
        y_test = None
        X_valid = None
        y_valid = None

    # determine column type
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    categorics = ["object"]
    numeric_features = list(X_train.select_dtypes(include=numerics).columns)
    categorical_features = list(
        X_train.select_dtypes(include=categorics).columns
    )

    # preprocess data
    if recipe == "ohe_and_standard_scaler":
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    X_train = preprocessor.fit_transform(X_train)
    if splits_to_return == "train_test":
        X_test = preprocessor.transform(X_test)
    if splits_to_return == "train_test_valid":
        X_valid = preprocessor.transform(X_valid)

    # get column names back and convert back to a DataFrame
    categorical_features_transformed = preprocessor.transformers_[1][
        1
    ].get_feature_names()
    features_transformed = list(numeric_features) + list(
        categorical_features_transformed
    )
    X_train = pd.DataFrame(data=X_train, columns=features_transformed)
    if splits_to_return == "train_test":
        X_test = pd.DataFrame(data=X_test, columns=features_transformed)
    if splits_to_return == "train_test_valid":
        X_valid = pd.DataFrame(data=X_valid, columns=features_transformed)

    return (X_train, X_valid, X_test, y_train, y_valid, y_test)
