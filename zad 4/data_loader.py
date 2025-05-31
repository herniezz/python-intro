import json
from typing import List, Tuple

import numpy as np
import pandas as pd


def load_decision_matrix(path: str) -> np.ndarray:
    try:
        df = pd.read_csv(path, index_col=0)
        return df.to_numpy()
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    except Exception as e:
        raise ValueError(f"Błąd podczas ładowania macierzy decyzyjnej: {str(e)}")

def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, index_col=0)
        for col in df.columns:
            if not all(ord(c) < 128 for c in col):
                raise ValueError(f"kolumna '{col}' ma nieprawidłowe znaki")
        
        if not all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns):
            raise ValueError("Wszystkie kolumny muszą zawierać wartości numeryczne")
        
        if df.isnull().any().any():
            raise ValueError("Dane zawierają brakujące wartości")
            
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Plik jest pusty: {path}")
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

def load_criteria_info(path: str) -> Tuple[List[str], List[float], List[str]]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict) or 'criteria' not in data:
            raise ValueError("Invalid JSON format")
            
        criteria = data['criteria']
        names = []
        weights = []
        types = []
        
        for criterion in criteria:
            if not all(k in criterion for k in ['name', 'weight', 'type']):
                raise ValueError("Missing required fields in criterion")
                
            names.append(criterion['name'])
            weights.append(float(criterion['weight']))
            
            criterion_type = criterion['type'].lower()
            if criterion_type not in ['max', 'min']:
                raise ValueError(f"Invalid criterion type: {criterion_type}")
            types.append(criterion_type)
            
        return names, weights, types
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Error loading criteria info: {str(e)}")

 