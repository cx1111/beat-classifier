"""
Module to make reading WFDB data easier
"""
import numpy as np
import pandas as pd


def ann_to_df(ann, keep_sym=None, rm_sym=None):
    """
    Get a pandas df from wfdb annotation.

    Filter by symbols by specifying what to keep or remove.
    Only specify one of keep_sym and rm_sym.
    """
    df = pd.DataFrame({'sample':ann.sample, 'symbol':ann.symbol})

    if keep_sym and rm_sym:
        raise Exception('Specify either symbols to keep or remove')
    if keep_sym:
        df = df.loc[df['symbol'].isin(keep_sym)]
    elif rm_sym:
        df = df.loc[-df['symbol'].isin(rm_sym)]
    return df
