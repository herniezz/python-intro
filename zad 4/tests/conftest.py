import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_data():
    data = {
        'C1': [1, 2, 3],
        'C2': [4, 5, 6],
        'C3': [7, 8, 9]
    }
    return pd.DataFrame(data, index=['A1', 'A2', 'A3'])

@pytest.fixture
def sample_weights():
    """Create sample weights for testing."""

    return np.array([0.3, 0.3, 0.4]) 