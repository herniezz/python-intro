from typing import List, Dict
import numpy as np
from pymcdm import normalizations
import pandas as pd

NORMALIZATION_METHODS = {
    'vector': normalizations.vector_normalization,
    'minmax': normalizations.minmax_normalization,
    'linear': normalizations.linear_normalization,
    'max': normalizations.max_normalization,
    'sum': normalizations.sum_normalization
}

def normalize_matrix(matrix: np.ndarray, method: str) -> np.ndarray:
    try:
        if method not in NORMALIZATION_METHODS:
            available = ', '.join(NORMALIZATION_METHODS.keys())
            raise ValueError(f"Nieprawidłowa metoda normalizacji: {method}. Dostępne metody: {available}")
            
        if matrix.size == 0:
            raise ValueError("Macierz decyzyjna jest pusta")
            
        if np.any(np.isnan(matrix)):
            raise ValueError("Macierz zawiera wartości NaN")
            
        if np.any(np.isinf(matrix)):
            raise ValueError("Macierz zawiera wartości nieskończone")
            

        normalized = NORMALIZATION_METHODS[method](matrix)
        return normalized
        
    except Exception as e:
        raise ValueError(f"Błąd podczas normalizacji macierzy: {str(e)}")

def get_available_methods() -> List[str]:

    return list(NORMALIZATION_METHODS.keys())

def normalize(df: pd.DataFrame, method: str) -> pd.DataFrame:
    """
    Normalize the decision matrix using the specified method.
    
    Args:
        df (pd.DataFrame): Input decision matrix
        method (str): Normalization method ('minmax' or 'zscore')
        
    Returns:
        pd.DataFrame: Normalized decision matrix
        
    Raises:
        ValueError: If invalid method is specified
    """
    if method not in ['minmax', 'zscore']:
        raise ValueError(f"Invalid normalization method: {method}. Use 'minmax' or 'zscore'")
    
    matrix = df.values
    
    if method == 'minmax':
        # Min-max normalization to [0,1]
        min_vals = np.min(matrix, axis=0)
        max_vals = np.max(matrix, axis=0)
        normalized = (matrix - min_vals) / (max_vals - min_vals)
    else:  # zscore
        # Z-score normalization
        mean_vals = np.mean(matrix, axis=0)
        std_vals = np.std(matrix, axis=0, ddof=1)  # Use ddof=1 for sample standard deviation
        # Handle case where std_vals is 0
        std_vals = np.where(std_vals == 0, 1, std_vals)
        normalized = (matrix - mean_vals) / std_vals
    
    return pd.DataFrame(normalized, index=df.index, columns=df.columns)
