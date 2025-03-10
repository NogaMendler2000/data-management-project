from collections import defaultdict, deque


def bottom_up_algorithm(trip_df, threshold):
    # שלב 1: חישוב מספר המופעים של כל צומת בכל שכבה
    start_station_counts = trip_df.groupby('start_station_id').size().to_dict()  # מספר נסיעות מתחנת התחלה
    duration_range_counts = trip_df.groupby('duration_range').size().to_dict()  # מספר נסיעות בטווח זמן
    hour_range_counts = trip_df.groupby('hour_range').size().to_dict()  # מספר נסיעות בטווח שעה

    # שלב 2: בניית יחסי הורה-ילד בין שכבות הגרף
    parent_relations = defaultdict(list)
    for _, trip in trip_df.iterrows():
        start_station = trip['start_station_id']
        duration_range = trip['duration_range']
        hour_range = trip['hour_range']
        
        # הורה (hour_range) מוביל לילד (duration_range)
        parent_relations[hour_range].append(duration_range)
        # הורה (duration_range) מוביל לילד (start_station)
        parent_relations[duration_range].append(start_station)
    
    # שלב 3: אתחול רשימת MUPs ותור לעיבוד צמתים
    mups = []  # רשימה לאחסון MUPs
    queue = deque()  # תור לעיבוד צמתים
    visited = set()  # קבוצה כדי לעקוב אחר צמתים שכבר נבדקו
    
    # שלב 4: התחלה מצמתי העלים (start_station) ועבודה כלפי מעלה
    for start_station in start_station_counts:
        queue.append((start_station, "start_station"))  # הוספת צומת התחלה לתור
    
    # שלב 5: עיבוד צמתים בתור
    while queue:
        current_node, layer = queue.popleft()  # שליפת הצומת הבא מהתור
        
        if current_node in visited:
            continue  # דלג אם הצומת כבר נבדק
        visited.add(current_node)  # סימון הצומת כנבדק
        
        # שלב 6: בדיקה לפי שכבה
        if layer == "start_station":
            count = start_station_counts[current_node]
            if count < threshold:
                # אם הצומת לא עובר את הסף, הוא MUP
                mups.append(current_node)
                # הוספת הורים (duration_range) לתור
                for duration_range in parent_relations[current_node]:
                    queue.append((duration_range, "duration"))
        elif layer == "duration":
            count = duration_range_counts[current_node]
            if count < threshold:
                # אם הצומת לא עובר את הסף, הוא MUP
                mups.append(current_node)
                # הוספת הורים (hour_range) לתור
                for hour_range in parent_relations[current_node]:
                    queue.append((hour_range, "hour"))
        elif layer == "hour":
            count = hour_range_counts[current_node]
            if count < threshold:
                # אם הצומת לא עובר את הסף, הוא MUP
                mups.append(current_node)
    
    return mups  # החזרת רשימת MUPs