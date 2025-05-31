import numpy as np
import pandas as pd

def run_topsis(df: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    """
    Run TOPSIS (Technique for Order Preference by Similarity to an Ideal Solution) method.
    
    Args:
        df (pd.DataFrame): Normalized decision matrix
        weights (np.ndarray): Criteria weights
        
    Returns:
        pd.Series: Ranking scores for each alternative
    """
    # Convert to numpy array
    matrix = df.values
    
    # Calculate ideal and anti-ideal solutions
    ideal = np.max(matrix, axis=0)
    anti_ideal = np.min(matrix, axis=0)
    
    # Calculate distances to ideal and anti-ideal solutions
    d_plus = np.sqrt(np.sum(weights * (matrix - ideal) ** 2, axis=1))
    d_minus = np.sqrt(np.sum(weights * (matrix - anti_ideal) ** 2, axis=1))
    
    # Calculate relative closeness
    scores = d_minus / (d_plus + d_minus)
    
    # Create Series with alternative names as index
    return pd.Series(scores, index=df.index, name='TOPSIS_Score') 