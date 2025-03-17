from collections import defaultdict
import heapq



def p_walk_algorithm(trip_df, threshold):
    # שלב 1: חישוב מספר המופעים של כל צומת בכל שכבה
    hour_range_counts = trip_df.groupby('hour_range').size().to_dict()  # מספר נסיעות בטווח שעה
    duration_range_counts = trip_df.groupby('duration_range').size().to_dict()  # מספר נסיעות בטווח זמן
    start_station_counts = trip_df.groupby('start_station_id').size().to_dict()  # מספר נסיעות מתחנת התחלה

    # שלב 2: בניית יחסי הורה-ילד וילד-הורה בין שכבות הגרף
    parent_relations = defaultdict(list)  # יחסי הורה-ילד
    child_relations = defaultdict(list)  # יחסי ילד-הורה
    for _, trip in trip_df.iterrows():
        start_station = trip['start_station_id']
        duration_range = trip['duration_range']
        hour_range = trip['hour_range']
        
        # הורה (hour_range) מוביל לילד (duration_range)
        parent_relations[hour_range].append(duration_range)
        # הורה (duration_range) מוביל לילד (start_station)
        parent_relations[duration_range].append(start_station)
        
        # ילד (start_station) מוביל להורה (duration_range)
        child_relations[start_station].append(duration_range)
        # ילד (duration_range) מוביל להורה (hour_range)
        child_relations[duration_range].append(hour_range)
    
    # שלב 3: אתחול רשימת MUPs ותור עדיפויות לעיבוד צמתים
    mups = []  # רשימה לאחסון MUPs
    priority_queue = []  # תור עדיפויות (ערימה)
    visited = set()  # קבוצה כדי לעקוב אחר צמתים שכבר נבדקו
    
    # שלב 4: הגדרת פונקציית עדיפות
    def priority_score(node):
        # העדיפות נקבעת לפי מספר ההורים והילדים של הצומת
        return len(parent_relations.get(node, [])) + len(child_relations.get(node, []))
    
    # שלב 5: התחלה מצמתי העלים (start_station) והוספתם לתור העדיפויות
    for start_station in start_station_counts:
        heapq.heappush(priority_queue, (-priority_score(start_station), start_station, "start_station"))
    
    # שלב 6: עיבוד צמתים מתור העדיפויות
    while priority_queue:
        _, current_node, layer = heapq.heappop(priority_queue)  # שליפת הצומת עם העדיפות הגבוהה ביותר
        
        if current_node in visited:
            continue  # דלג אם הצומת כבר נבדק
        visited.add(current_node)  # סימון הצומת כנבדק
        
        # שלב 7: בדיקה לפי שכבה
        if layer == "start_station":
            count = start_station_counts[current_node]
            if count < threshold:
                # אם הצומת לא מכוסה, הוא MUP
                mups.append(current_node)
                # הוספת ההורים של הצומת לתור העדיפויות
                for duration_range in parent_relations[current_node]:
                    heapq.heappush(priority_queue, (-priority_score(duration_range), duration_range, "duration"))
            else:
                # אם הצומת מכוסה, גיזום כל ההורים שלו (כי הם גם חייבים להיות מכוסים)
                for duration_range in child_relations[current_node]:
                    if duration_range not in visited:
                        visited.add(duration_range)  # סימון ההורים כנגזמים
               
        elif layer == "duration":
            count = duration_range_counts[current_node]
            if count < threshold:
                # אם הצומת לא מכוסה, הוא MUP
                mups.append(current_node)
                # גיזום כל הילדים של הצומת (כי הם גם חייבים להיות לא מכוסים)
                for start_station in child_relations[current_node]:
                    if start_station not in visited:
                        visited.add(start_station)  # סימון הילדים כנגזמים
                # הוספת ההורים של הצומת לתור העדיפויות
                for hour_range in parent_relations[current_node]:
                    heapq.heappush(priority_queue, (-priority_score(hour_range), hour_range, "hour"))
            else:
                # אם הצומת מכוסה, גיזום כל ההורים שלו (כי הם גם חייבים להיות מכוסים)
                for hour_range in child_relations[current_node]:
                    if hour_range not in visited:
                        visited.add(hour_range)  # סימון ההורים כנגזמים
                # הוספת הילדים של הצומת לתור העדיפויות
                for duration_range in parent_relations[current_node]:
                    heapq.heappush(priority_queue, (-priority_score(duration_range), duration_range, "duration"))
        elif layer == "hour":
            count = hour_range_counts[current_node]
            if count < threshold:
                # אם הצומת לא מכוסה, הוא MUP
                mups.append(current_node)
                # גיזום כל הילדים של הצומת (כי הם גם חייבים להיות לא מכוסים)
                for duration_range in child_relations[current_node]:
                    if duration_range not in visited:
                        visited.add(duration_range)  # סימון הילדים כנגזמים
                
            else:
        
                # הוספת הילדים של הצומת לתור העדיפויות אם הצומת מכוסה, 
                for duration_range in child_relations[current_node]:
                    heapq.heappush(priority_queue, (-priority_score(duration_range), duration_range, "duration"))
    
    return mups  # החזרת רשימת MUPs
