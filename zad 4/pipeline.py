import pandas as pd
from data_loader import load_data
from normalization import normalize
from weights import calculate_weights
from topsis import run_topsis
from spotis import run_spotis

def main():
    df = load_data("data/alternatives.csv")
    df_n = normalize(df, method="minmax")
    w = calculate_weights(df_n, method="entropy")
    
    
    r_t = run_topsis(df_n, w)
    r_s = run_spotis(df_n, w)
    

    results = pd.concat([r_t, r_s], axis=1, keys=["TOPSIS", "SPOTIS"])
    results.to_csv("results.csv")
    print("Results saved to results.csv")
    print("\nRankings:")
    print("\nTOPSIS:")
    print(r_t.sort_values(ascending=False))
    print("\nSPOTIS:")
    print(r_s.sort_values(ascending=False))

if __name__ == "__main__":
    main() 