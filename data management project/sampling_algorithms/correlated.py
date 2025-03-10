import pandas as pd
import hashlib  


def correlated_sampler(df, join_column, p):
    samples = []
    
    for _, row in df.iterrows():
        hash_value = int(hashlib.sha256(str(row[join_column]).encode()).hexdigest(), 16) / (2**256)
        
        if hash_value < p:
            samples.append(row)
    
    return pd.DataFrame(samples)