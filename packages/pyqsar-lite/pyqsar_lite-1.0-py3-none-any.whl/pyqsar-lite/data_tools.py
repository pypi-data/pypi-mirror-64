#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def rmNaN(X_data) :
    """
    Remove feature that has 'NaN' as value

    Parameters
    ----------
    X_data : pandas DataFrame , shape = (n_samples, n_features)

    Returns
    -------
    X_data that removed feature has 'NaN' as value
    """
    header = list(X_data.columns.values)
    A = X_data.isnull().any()
    for fact in enumerate(A) :
        if fact[1] == True :
            col_Nan = header[fact[0]]
            del X_data[col_Nan]
    return X_data


def rm_empty_feature(X_data) :
    """
    Remove feature that has same value for all sample(data)

    Parameters
    ----------
    X_data : pandas DataFrame , shape = (n_samples, n_features)

    Returns
    -------
    X_data that removed feature that has same value for all sample(data)
    """
    zero_desc = []
    header = list(X_data.columns.values)
    for i in header :
        flag = 0
        ch = X_data[i]
        ch = list(ch)
        stan = ch[0]
        for d in ch :
            if d != stan :
                flag = 1
                break
        if flag == 0 :
            zero_desc.append(i)
    X_data = X_data.drop(zero_desc, axis=1)
    return X_data


def rmNaN_corrmtx(X_data) :
    """
    Remove feature that has 'NaN' as value when calculating correlation coefficients

    Parameters
    ----------
    X_data : pandas DataFrame , shape = (n_samples, n_features)

    Returns
    -------
    X_data that removed feature that has 'NaN' when calculating correlation coefficients
    """
    drop_box = []
    corr_mtx = abs(X_data.corr())
    header = list(corr_mtx.columns.values)
    A = corr_mtx.isnull().sum()
    for fact in enumerate(A) :
        if fact[1] == len(header) :
            col_Nan = header[fact[0]]
            del corr_mtx[col_Nan]
            drop_box.append(col_Nan)
    X_data = X_data.drop(drop_box)
    return X_data

def train_scaler(X_data) :
    """
    Transforms features by scaling each feature to a given range.
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    X_scaled = X_std * (max - min) + min
    (https://github.com/scikit-learn/scikit-learn/blob/f3320a6f/sklearn/preprocessing/data.py#L190)

    Parameters
    ----------
    X_data : pandas DataFrame , shape = (n_samples, n_features)

    Returns
    -------
    X_scaled
    """
    header = list(X_data.columns.values)
    scaler = MinMaxScaler()
    X_data_scaled = scaler.fit_transform(X_data)
    X_data_scaled = pd.DataFrame(X_data_scaled , columns=header)
    return X_data_scaled

def rm_star(X_data) :
    """
    Strip off the '**' marker from a value

    Parameters
    ----------
    X_data : pandas DataFrame , shape = (n_samples, n_features)

    Returns
    -------
    X_data that removed '**' marker
    """
    # for 'Rapidmind' data
    po = []
    v = np.array(X_data)
    n = 0
    header = list(X_data.columns.values)
    for l in v:
        nn = 0
        for c in l :
            if '**' in str(c) :
                po.append(nn)
                cc = c[:-2]
                v[n][nn] = cc
            nn = nn+1
        n = n+1
    vv = pd.DataFrame(v, columns=header)
    return vv
