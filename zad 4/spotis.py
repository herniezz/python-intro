import numpy as np
import pandas as pd

def run_spotis(df: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    matrix = df.values
    ideal = np.max(matrix, axis=0)
    distances = np.sqrt(np.sum(weights * (matrix - ideal) ** 2, axis=1))
    scores = 1 - (distances / np.max(distances))
    return pd.Series(scores, index=df.index, name='SPOTIS_Score') 