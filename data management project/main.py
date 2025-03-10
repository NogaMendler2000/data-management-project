import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import io
import time  
import sys
import os

# הוספת התיקייה algorithms למערכת הנתיבים
from algorithms.bottom_up import bottom_up_algorithm
from algorithms.top_down import top_down_algorithm
from algorithms.walking import p_walk_algorithm
from sampling_algorithms.distinct import distinct_sampler
from sampling_algorithms.correlated import correlated_sampler


# שינוי encoding של הפלט ל-UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# נתיב היעד הכללי
destination_path = r"C:\Users\mendl\data management project"

# טעינת קבצי Bike Share
def load_bike_share_files():
    bike_files = ["trip.csv"]  # נטען רק את קובץ הנסיעות
    dataframes = {}
    
    for file in bike_files:
        file_path = os.path.join(destination_path, file)
        if os.path.exists(file_path):
            # טעינת רק 100,000 רשומות ראשונות
            df = pd.read_csv(file_path, nrows=100000)
            dataframes[file] = df
            print(f"Loaded {file} with columns: {df.columns.tolist()}")
        else:
            print(f"Warning: {file} not found in {destination_path}")
    
    return dataframes

# קריאת קבצי SF Bay Area Bike Share
bike_data = load_bike_share_files()

# נטען את 100,000 הרשומות הראשונות
trip_df = bike_data["trip.csv"]

# פונקציה לקביעת טווח זמן השכרה (עד 500 דקות)
def get_duration_range(duration):
    ranges = [
        (60, "0-60"),
        (120, "61-120"),
        (180, "121-180"),
        (240, "181-240"),
        (300, "241-300"),
        (360, "301-360"),
        (420, "361-420"),
        (480, "421-480"),
        (500, "481-500")
    ]
    for max_duration, label in ranges:
        if duration <= max_duration:
            return label
    return "481-500"

# פונקציה לקביעת טווח שעת ההשכרה
def get_hour_range(start_date):
    hour = pd.to_datetime(start_date).hour
    if 6 <= hour < 12:
        return "6-12"
    elif 12 <= hour < 18:
        return "12-18"
    else:
        return "18-24"

# יצירת העמודות hour_range ו-duration_range לפני החישובים
trip_df['duration_range'] = trip_df['duration'].apply(get_duration_range)
trip_df['hour_range'] = trip_df['start_date'].apply(get_hour_range)

# חישוב מספר הצמתים בכל שכבה
unique_hour_ranges = trip_df['hour_range'].nunique()
unique_duration_ranges = trip_df['duration_range'].nunique()
unique_start_stations = trip_df['start_station_id'].nunique()


# קביעת טווחי ספים (thresholds) מ-20 עד 1000 בקפיצות של 20
thresholds = list(range(20, 301, 20))

# רשימות לאחסון מספר ה-MUPs עבור כל סף
bottom_up_mup_counts = []
p_walk_mup_counts_ops = []
top_down_mup_counts = []

# רשימות לאחסון זמן הריצה עבור כל סף
bottom_up_runtimes = []
p_walk_runtimes = []
top_down_runtimes = []

# הפעלת האלגוריתם Bottom-Up עבור כל סף
for threshold in thresholds:
    start_time = time.time()  # התחלת מדידת זמן
    mups = bottom_up_algorithm(trip_df, threshold)
    end_time = time.time()  # סיום מדידת זמן
    bottom_up_mup_counts.append(len(mups))
    bottom_up_runtimes.append(end_time - start_time)  # שמירת זמן הריצה

# הפעלת האלגוריתם P-WALK עבור כל סף
for threshold in thresholds:
    start_time = time.time()  # התחלת מדידת זמן
    mups = p_walk_algorithm(trip_df, threshold)
    end_time = time.time()  # סיום מדידת זמן
    p_walk_mup_counts_ops.append(len(mups))
    p_walk_runtimes.append(end_time - start_time)  # שמירת זמן הריצה

# הפעלת האלגוריתם Top-Down עבור כל סף
for threshold in thresholds:
    start_time = time.time()  # התחלת מדידת זמן
    mups = top_down_algorithm(trip_df, threshold)
    end_time = time.time()  # סיום מדידת זמן
    top_down_mup_counts.append(len(mups))
    top_down_runtimes.append(end_time - start_time)  # שמירת זמן הריצה

# יצירת גרפים נפרדים עבור Bottom-Up, P-WALK ו-Top-Down (מספר MUPs)
plt.figure(figsize=(12, 6))
plt.plot(thresholds, bottom_up_mup_counts, marker='o', linestyle='-', color='b', label='Bottom-Up')
plt.plot(thresholds, p_walk_mup_counts_ops, marker='o', linestyle='-', color='g', label='P-WALK')
plt.plot(thresholds, top_down_mup_counts, marker='o', linestyle='-', color='r', label='Top-Down')
plt.xlabel("Threshold")
plt.ylabel("Number of MUPs")
plt.title("Number of MUPs for Different Thresholds (Bottom-Up vs P-WALK vs Top-Down)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# יצירת גרף זמן הריצה עבור Bottom-Up, P-WALK ו-Top-Down
plt.figure(figsize=(12, 6))
plt.plot(thresholds, bottom_up_runtimes, marker='o', linestyle='-', color='b', label='Bottom-Up Runtime')
plt.plot(thresholds, p_walk_runtimes, marker='o', linestyle='-', color='g', label='P-WALK Runtime')
plt.plot(thresholds, top_down_runtimes, marker='o', linestyle='-', color='r', label='Top-Down Runtime')
plt.xlabel("Threshold")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime for Different Thresholds (Bottom-Up vs P-WALK vs Top-Down)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# קביעת טווחי ספים (thresholds) מ-100 עד 1000 בקפיצות של 100
thresholds = list(range(100, 1001, 100))

# רשימות לאחסון מספר ה-MUPs עבור כל סף
p_walk_mup_counts = []
distinct_sampler_mup_counts = []
correlated_sampler_mup_counts = []

# רשימות לאחסון דיוק (accuracy) עבור כל סף
distinct_sampler_accuracy = []
correlated_sampler_accuracy = []

# הפעלת האלגוריתם P-WALK על הדגימות השונות
for threshold in thresholds:
    # P-WALK על הנתונים המלאים
    mups_full = p_walk_algorithm(trip_df, threshold)
    p_walk_mup_counts.append(len(mups_full))
    
    # דגימה עם Distinct Sampler המקורי
    sampled_df_distinct = distinct_sampler(trip_df, ['hour_range', 'duration_range'], f=500, p=0.35, S=10000)
    mups_distinct = p_walk_algorithm(sampled_df_distinct, threshold)
    distinct_sampler_mup_counts.append(len(mups_distinct))
    
    # דגימה עם Correlated Sampling Method
    sampled_df_correlated = correlated_sampler(trip_df, join_column='start_station_id', p=0.35)
    mups_correlated = p_walk_algorithm(sampled_df_correlated, threshold)
    correlated_sampler_mup_counts.append(len(mups_correlated))
    
    # חישוב דיוק (accuracy) עבור Distinct Sampler ו-Correlated Sampling
    if len(mups_full) > 0:
        distinct_sampler_accuracy.append(len(mups_full) / len(mups_distinct))
        correlated_sampler_accuracy.append(len(mups_correlated) / len(mups_full))
    else:
        distinct_sampler_accuracy.append(0)
        correlated_sampler_accuracy.append(0)

# יצירת גרפים נפרדים עבור P-WALK, Distinct Sampler ו-Correlated Sampling Method
plt.figure(figsize=(12, 6))
plt.plot(thresholds, p_walk_mup_counts, marker='o', linestyle='-', color='b', label='P-WALK (Full Data)')
plt.plot(thresholds, distinct_sampler_mup_counts, marker='o', linestyle='-', color='g', label='P-WALK (Distinct Sampler)')
plt.plot(thresholds, correlated_sampler_mup_counts, marker='o', linestyle='-', color='r', label='P-WALK (Correlated Sampling)')
plt.xlabel("Threshold")
plt.ylabel("Number of MUPs")
plt.title("Number of MUPs for Different Thresholds (P-WALK with Sampling)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# יצירת גרף דיוק (accuracy) עבור Distinct Sampler ו-Correlated Sampling
plt.figure(figsize=(12, 6))
plt.plot(thresholds, distinct_sampler_accuracy, marker='o', linestyle='-', color='g', label='Distinct Sampler Accuracy')
plt.plot(thresholds, correlated_sampler_accuracy, marker='o', linestyle='-', color='r', label='Correlated Sampling Accuracy')
plt.xlabel("Threshold")
plt.ylabel("Accuracy")
plt.title("Accuracy of Distinct Sampler and Correlated Sampling (Compared to Full Data)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# ערכי p לדגימה
p_values = [0.35, 0.3, 0.2, 0.1, 0.05]

# ספים (thresholds) למדידה
thresholds_to_measure = [100, 400, 800]

# רשימות לאחסון זמן הריצה עבור כל p וכל סף
distinct_sampler_runtimes = {p: [] for p in p_values}

# מדידת זמן הריצה של Distinct Sampler עבור כל p וכל סף
for p in p_values:
    for threshold in thresholds_to_measure:
        start_time = time.time()  # התחלת מדידת זמן
        sampled_df = distinct_sampler(trip_df, ['hour_range', 'duration_range'], f=500, p=p, S=10000)
        mups = p_walk_algorithm(sampled_df, threshold)
        end_time = time.time()  # סיום מדידת זמן
        distinct_sampler_runtimes[p].append(end_time - start_time)  # שמירת זמן הריצה

# יצירת גרף עמודות עבור זמן הריצה של Distinct Sampler
plt.figure(figsize=(12, 6))
x = range(len(p_values))  # מיקומי העמודות על ציר X
width = 0.2  # רוחב העמודות

# יצירת עמודות עבור כל סף
for i, threshold in enumerate(thresholds_to_measure):
    runtimes = [distinct_sampler_runtimes[p][i] for p in p_values]
    plt.bar([pos + i * width for pos in x], runtimes, width=width, label=f'Threshold = {threshold}')

# הגדרות הגרף
plt.xlabel("p values")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime of Distinct Sampler for Different p Values and Thresholds")
plt.xticks([pos + width for pos in x], p_values)  # תוויות ציר X
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ערכי p לדגימה
p_values = [0.35, 0.3, 0.2, 0.1, 0.05]

# ספים (thresholds) למדידה
thresholds_to_measure = [100, 400, 800]

# רשימות לאחסון זמן הריצה עבור כל p וכל סף
correlated_sampler_runtimes = {p: [] for p in p_values}

# מדידת זמן הריצה של Correlated Sampler עבור כל p וכל סף
for p in p_values:
    for threshold in thresholds_to_measure:
        start_time = time.time()  # התחלת מדידת זמן
        sampled_df = correlated_sampler(trip_df, join_column='start_station_id', p=p)
        mups = p_walk_algorithm(sampled_df, threshold)
        end_time = time.time()  # סיום מדידת זמן
        correlated_sampler_runtimes[p].append(end_time - start_time)  # שמירת זמן הריצה

# יצירת גרף עמודות עבור זמן הריצה של Correlated Sampler
plt.figure(figsize=(12, 6))
x = range(len(p_values))  # מיקומי העמודות על ציר X
width = 0.2  # רוחב העמודות

# יצירת עמודות עבור כל סף
for i, threshold in enumerate(thresholds_to_measure):
    runtimes = [correlated_sampler_runtimes[p][i] for p in p_values]
    plt.bar([pos + i * width for pos in x], runtimes, width=width, label=f'Threshold = {threshold}')

# הגדרות הגרף
plt.xlabel("p values")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime of Correlated Sampler for Different p Values and Thresholds")
plt.xticks([pos + width for pos in x], p_values)  # תוויות ציר X
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# פונקציה לחישוב מספר ה-MUPs בכל שכבה
def count_mups_by_layer(mups, trip_df):
    # יצירת מילון לאחסון מספר ה-MUPs בכל שכבה
    mups_by_layer = {
        'hour_range': set(),
        'duration_range': set(),
        'start_station_id': set()
    }
    
    # עבור כל MUP, נבדוק לאיזו שכבה הוא שייך
    for mup in mups:
        if mup in trip_df['hour_range'].unique():
            mups_by_layer['hour_range'].add(mup)
        elif mup in trip_df['duration_range'].unique():
            mups_by_layer['duration_range'].add(mup)
        elif mup in trip_df['start_station_id'].unique():
            mups_by_layer['start_station_id'].add(mup)
    
    # מחזירים את מספר ה-MUPs בכל שכבה
    return {layer: len(mups) for layer, mups in mups_by_layer.items()}

# קביעת טווחי ספים (thresholds) מ-20 עד 200 בקפיצות של 20
thresholds = list(range(20, 301, 20))

# רשימות לאחסון מספר ה-MUPs בכל שכבה עבור כל סף
hour_range_mup_counts = []
duration_range_mup_counts = []
start_station_mup_counts = []

# הפעלת האלגוריתם P-WALK עבור כל סף וחישוב מספר ה-MUPs בכל שכבה
for threshold in thresholds:
    mups = p_walk_algorithm(trip_df, threshold)
    mups_by_layer = count_mups_by_layer(mups, trip_df)
    
    hour_range_mup_counts.append(mups_by_layer['hour_range'])
    duration_range_mup_counts.append(mups_by_layer['duration_range'])
    start_station_mup_counts.append(mups_by_layer['start_station_id'])

# יצירת גרף המציג את מספר ה-MUPs בכל שכבה עבור כל סף
plt.figure(figsize=(12, 6))
plt.plot(thresholds, hour_range_mup_counts, marker='o', linestyle='-', color='b', label='Hour Range MUPs')
plt.plot(thresholds, duration_range_mup_counts, marker='o', linestyle='-', color='g', label='Duration Range MUPs')
plt.plot(thresholds, start_station_mup_counts, marker='o', linestyle='-', color='r', label='Start Station MUPs')
plt.xlabel("Threshold")
plt.ylabel("Number of MUPs")
plt.title("Number of MUPs in Each Layer for Different Thresholds (P-WALK)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

