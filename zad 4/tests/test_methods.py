import pytest
import pandas as pd
import numpy as np
from data_loader import load_data
from normalization import normalize
from weights import calculate_weights
from topsis import run_topsis
from spotis import run_spotis

@pytest.fixture
def sample_data():
    data = {
        'C1': [1, 2, 3],
        'C2': [4, 5, 6]
    }
    return pd.DataFrame(data, index=['A1', 'A2', 'A3'])

def test_load_data(tmp_path):
    # Create a temporary CSV file
    data = {
        'C1': [1, 2, 3],
        'C2': [4, 5, 6],
        'C3': [7, 8, 9]
    }
    df = pd.DataFrame(data, index=['A1', 'A2', 'A3'])
    csv_path = tmp_path / "test_data.csv"
    df.to_csv(csv_path)
    
    # Test loading
    loaded_df = load_data(str(csv_path))
    pd.testing.assert_frame_equal(df, loaded_df)
    
    # Test invalid file
    with pytest.raises(FileNotFoundError):
        load_data("nonexistent.csv")

def test_normalize(sample_data):
    normalized = normalize(sample_data, method="minmax")
    assert normalized.min().min() >= 0
    assert normalized.max().max() <= 1
    assert normalized.shape == sample_data.shape
    
 
    normalized = normalize(sample_data, method="zscore")
    assert abs(normalized.mean().mean()) < 1e-10
    assert all(abs(normalized.std() - 1) < 1e-10)
    assert normalized.shape == sample_data.shape
    
    with pytest.raises(ValueError):
        normalize(sample_data, method="invalid")

def test_calculate_weights(sample_data):
    weights = calculate_weights(sample_data, method="entropy")
    assert len(weights) == len(sample_data.columns)
    assert abs(sum(weights) - 1.0) < 1e-10
    assert all(0 <= w <= 1 for w in weights)
    
    # ahp weights
    weights = calculate_weights(sample_data, method="ahp")
    assert len(weights) == len(sample_data.columns)
    assert abs(sum(weights) - 1.0) < 1e-10
    assert all(0 <= w <= 1 for w in weights)
    
    with pytest.raises(ValueError):
        calculate_weights(sample_data, method="invalid")

def test_topsis(sample_data, sample_weights):
    weights = sample_weights[:len(sample_data.columns)]
    scores = run_topsis(sample_data, weights)
    assert len(scores) == len(sample_data)
    assert all(0 <= score <= 1 for score in scores)
    assert scores.index.equals(sample_data.index)
    
    
    assert scores['A3'] > scores['A2'] > scores['A1']

def test_spotis(sample_data, sample_weights):
    weights = sample_weights[:len(sample_data.columns)]
    scores = run_spotis(sample_data, weights)
    assert len(scores) == len(sample_data)
    assert all(0 <= score <= 1 for score in scores)
    assert scores.index.equals(sample_data.index)
    assert scores['A3'] > scores['A2'] > scores['A1']

def test_ranking_consistency(sample_data, sample_weights):
    weights = sample_weights[:len(sample_data.columns)]
    topsis_scores = run_topsis(sample_data, weights)
    spotis_scores = run_spotis(sample_data, weights)
    
    topsis_rank = topsis_scores.rank(ascending=False)
    spotis_rank = spotis_scores.rank(ascending=False)
    correlation = topsis_rank.corr(spotis_rank)
    assert correlation > 0.5  