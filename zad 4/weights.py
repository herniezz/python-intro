from typing import List, Optional
import numpy as np
from pymcdm import weights
import pandas as pd

def compute_weights_entropy(matrix: np.ndarray) -> List[float]:
    try:
        if matrix.size == 0:
            raise ValueError("Macierz decyzyjna jest pusta")
            
        if np.any(np.isnan(matrix)):
            raise ValueError("Macierz zawiera wartości NaN")
            
        if np.any(np.isinf(matrix)):
            raise ValueError("Macierz zawiera wartości nieskończone")
            
        w = weights.entropy_weights(matrix)
        return w.tolist()
        
    except Exception as e:
        raise ValueError(f"Błąd podczas obliczania wag: {str(e)}")

def create_consistent_comparison_matrix(n: int) -> np.ndarray:
    # Tworzymy wektor bazowych wag (od najważniejszego do najmniej ważnego)
    base_weights = np.array([1.0, 0.8, 0.6, 0.4, 0.2])
    
    if n > len(base_weights):
        base_weights = np.linspace(1.0, 0.2, n)
    else:
        base_weights = base_weights[:n]
    
    matrix = np.ones((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i,j] = base_weights[i] / base_weights[j]
    
    return matrix

def compute_weights_ahp(comparison_matrix: np.ndarray) -> List[float]:
    try:
        n = len(comparison_matrix)
        row_geometric_mean = np.power(np.prod(comparison_matrix, axis=1), 1/n)
        weights = row_geometric_mean / np.sum(row_geometric_mean)
        return weights.tolist()
        
    except Exception as e:
        raise ValueError(f"Błąd podczas obliczania wag AHP: {str(e)}")

def validate_weights(weights_list: List[float], n_criteria: int) -> None:
    if len(weights_list) != n_criteria:
        raise ValueError(f"Nieprawidłowa liczba wag: {len(weights_list)} (oczekiwano {n_criteria})")
        
    if not all(0 <= w <= 1 for w in weights_list):
        raise ValueError("Wagi muszą być z przedziału [0, 1]")
        
    if not np.isclose(sum(weights_list), 1.0):
        raise ValueError("Suma wag musi wynosić 1.0")

def calculate_weights(df: pd.DataFrame, method: str) -> np.ndarray:
    if method not in ['entropy', 'ahp']:
        raise ValueError(f"Nieprawidłowa metoda obliczania wag: {method}. Użyj 'entropy' lub 'ahp'")
    
    matrix = df.values
    n_criteria = matrix.shape[1]
    
    if method == 'entropy':
        return compute_weights_entropy(matrix)
    elif method == 'ahp':
        comparison_matrix = create_consistent_comparison_matrix(n_criteria)
        return compute_weights_ahp(comparison_matrix)
    
    return weights 