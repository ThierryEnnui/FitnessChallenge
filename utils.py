import pandas as pd

def load_pointsystem(point_system_filepath):
    data = pd.read_csv(point_system_filepath)
    rules = {}
    metrics = data["Metric"].tolist()
    points = data["PointPerUnit"]
    maxes = data["DailyMax"]

    for metric, point, my_max in zip(metrics, points, maxes):
        rules[metric] = {"PPU": point, "MAX": my_max}
    return rules

def get_max_points(pointsystem):
    max_points = {}
    for key, val in pointsystem.items():
        if key != "WEIGHT":
            max_points[key] = val["MAX"] * 31
    return max_points
        
def clean_data(data, pointsystem):
        for column in data.columns:
            if column in pointsystem.keys():
                data[column] = data[column].apply(lambda x: x if x > 0 else 0.0)

def calculate_score(df, pointsystem):
    data = df.copy()
    result = {}
    for column in data.columns:
        if column in pointsystem.keys():
            multiplier = float(pointsystem[column].get("PPU"))
            max_val = float(pointsystem[column].get("MAX"))
            data[column] = data[column].apply(lambda x: x*multiplier if x*multiplier <= max_val else max_val)
        elif column in ("SQUAT_LBS", "PULL_UP_LBS", "CHIN_UP_LBS", "PUSH_UP_LBS"):
            data[column] = data[column].apply(lambda x: x*pointsystem["WEIGHT"].get("PPU"))
            data[column] = data[column].apply(lambda x: x if x != 0 else 1.0)
    # data.drop(["DATE"], axis=1, inplace=True)
    for column in data.columns:
        if column in ("SQUAT", "PULL_UP", "CHIN_UP", "PUSH_UP"):
            multiplier = float(pointsystem[column].get("PPU"))
            max_val = float(pointsystem[column].get("MAX"))
            data[column] = data[column] * data[f"{column}_LBS"]
            data[column] = data[column].apply(lambda x: x if x <= max_val else max_val)
    daily_totals = []
    data.drop(["PULL_UP_LBS", "CHIN_UP_LBS", "PUSH_UP_LBS", "SQUAT_LBS"], axis=1, inplace=True)
    for row in data.iterrows():
        daily_total = 0.0
        for column in data.columns:
            if column not in ["DATE", "MOOD", "DISTANCE"]:
                daily_total += row[1][column]
        daily_totals.append(daily_total)
    data["POINT_TOTAL"] = daily_totals
    best_day = data["POINT_TOTAL"].max()
    for column in data.columns:
        if column == "DATE":
            result[column] = "TOTAL:"
        elif column == "MOOD":
            result[column] = data[column].mean()
        else:
            result[column] = data[column].sum()
    data.loc[len(data.index)] = result
    data.rename({'FAT_BURN':'HR_105-132',
                 'CARDIO':'HR_133-166',
                 'RED_LINE':'HR_167+',
                 'RECOVERY':'MINS_RECOVERY',
                 'SLEEP':'HRS_SLEEP',
                 'H2O':'LITERS_H2O',
                 'HOT/COLD':'MINS_HOT/COLD',
                 'DISTANCE':'DISTANCE_KM'},axis=1, inplace=True)
    return data, best_day

def calculate_totals(df):
    data = df.copy()
    tally = {}
    daily_totals = []
    data.drop(["PULL_UP_LBS", "CHIN_UP_LBS", "PUSH_UP_LBS", "SQUAT_LBS"], axis=1, inplace=True)
    for row in data.iterrows():
        daily_total = 0.0
        for column in data.columns:
            if column in ["PULL_UP", "CHIN_UP", "PUSH_UP", "SQUAT"]:
                daily_total += row[1][column]
        daily_totals.append(daily_total)
    data["REP_TOTAL"] = daily_totals
    for column in data.columns:
        if column == "DATE":
            tally[column] = "TOTAL:"
        elif column == "MOOD":
            tally[column] = data[column].mean()
        else:
            tally[column] = data[column].sum()
    data.loc[len(data.index)] = tally
    data.rename({'FAT_BURN':'HR_105-132',
                 'CARDIO':'HR_133-166',
                 'RED_LINE':'HR_167+',
                 'RECOVERY':'MINS_RECOVERY',
                 'SLEEP':'HRS_SLEEP',
                 'H2O':'LITERS_H2O',
                 'HOT/COLD':'MINS_HOT/COLD',
                 'DISTANCE':'DISTANCE_KM'},axis=1, inplace=True)
    return data

def build_stacked_barchat_data(a_df):
    df = a_df.drop(31, axis=0)
    dates = df["DATE"].tolist()
    results = []
    for column in df.columns:
        if column not in ["DATE", "MOOD", "DISTANCE_KM", "POINT_TOTAL"]:
            for date, entry in zip(dates, df[column].tolist()):
                temp = {}
                temp["date"] = date
                temp["points"] = entry
                temp["category"] = column
                results.append(temp)
    new = pd.DataFrame(results)
    return new

def build_percentage_chart_data(point_totals, max_points):
    series = point_totals.drop(["MOOD", "DISTANCE_KM", "POINT_TOTAL", "DATE"])
    total_rows = []
    for key, val, my_score in zip(max_points.keys(), max_points.values(), series):
        temp = {}
        temp["points"] = (int(val) - int(my_score))
        temp["category"] = key
        temp["status"] =  "UNEARNED"
        total_rows.append(temp)

        temp2 = {}
        temp2["points"] = my_score
        temp2["category"] = key
        temp2["status"] =  "EARNED"
        total_rows.append(temp2)
    new = pd.DataFrame(total_rows)
    return new
    


    
    
            
    