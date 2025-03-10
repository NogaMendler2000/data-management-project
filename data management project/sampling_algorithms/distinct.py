import pandas as pd
from collections import defaultdict
import random  


def distinct_sampler(df, columns, f, p, S):
    samples = []
    reservoirs = defaultdict(list)
    weights = {}  # מילון לשמירת המשקלים של הרשומות

    for _, row in df.iterrows():
        key = tuple(row[col] for col in columns)
        
        if len(reservoirs[key]) < f:
            # שלב 1: שמירת ה-f הראשונות באופן ודאי
            reservoirs[key].append(row)
            weights[key] = weights.get(key, []) + [1.0]  # משקל 1 ל-f הראשונות
        else:
            if len(reservoirs[key]) < f + S:
                # שלב 2: שמירת רשומות נוספות במאגר
                reservoirs[key].append(row)
                weights[key] = weights.get(key, []) + [(len(reservoirs[key]) - f) / S]  # משקל פרופורציונלי
            else:
                if random.random() < p:
                    # שלב 3: דגימה אקראית עם הסתברות p
                    reservoirs[key].append(row)
                    weights[key] = weights.get(key, []) + [1.0 / p]  # משקל 1/p

    # איסוף הדגימות עם המשקלים
    for key in reservoirs:
        for i, row in enumerate(reservoirs[key]):
            row['weight'] = weights[key][i]  # הוספת עמודת weight לרשומה
            samples.append(row)
    
    return pd.DataFrame(samples)