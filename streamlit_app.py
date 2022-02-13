import streamlit as st
import pandas as pd
from pathlib import Path
import os, sys
import altair as alt
import matplotlib.pyplot as plt
import utils
PATH = Path.cwd()

st.title('January 2022 Fitness Challenge')

SCORE_FILENAME = "scores.csv"
TOTALS_FILENAME = "totals.csv"

def load_data():
    score = pd.read_csv(PATH / SCORE_FILENAME, header=0)
    totals = pd.read_csv(PATH / TOTALS_FILENAME, header=0)
    return score, totals

score, totals= load_data()
pointsystem = utils.load_pointsystem(PATH / "pointsystem.csv")
max_points = utils.get_max_points(pointsystem)

st.subheader("Challenge Description")
st.write("Based on the pointsystem show below, contestants could earn points daily. No points were awareded on day in which contenstants drank alcohol or smoked. Whoever earned the most points by the end of the month would be declared the winner.")

st.subheader("Pointsystem")
score_card = pd.read_csv(PATH / "pointsystem.csv")

st.table(score_card.style.format(formatter={'PointPerUnit':"{:.2f}"}))
st.subheader("Strength Training")
st.write("""Points are awarded per repetition. All variations are counted the same i.e. Wide-grip Pull-Ups are Pull-Ups and diamond-cutter Push-Ups are Push-Ups. You can earn 0.010 additional points per 10 pounds added to your bodyweight for Pull-Ups, Chin-Ups, Push-Ups and Squats.""")

st.subheader("Cardio")
st.write("Points are awarded by minute.")

st.subheader("Recovery")
st.write("You can still earn up to 20 points daily for yoga routines on recovery day. You cannot earn Strength Training points and Recovery points on the same day. You can follow any routine you like, guided routines on YouTube for example.")

st.subheader("Sleeep")
st.write("""7:50 sleep time = 8 hours  
7:49 sleep time = 7 hours""")

st.subheader("Hydration")
st.write("Water intake measured in liters.")

st.subheader("Hot/Cold Bath/Shower")
st.write("Points are awarded per minute under cold water. Alternate between hot and cold every minute.")

st.subheader("Penalties")
st.write("If you smoke, drink, shoot, snort, butt-chug or by any other means take in toxic enjoyables, you cannot score points for that day.")

st.subheader("Fitness Test")
st.write("""Set a performance benchmark by completing a fitness test before the challenge starts. An identical fitness test will be completed at the end of the competition. For push-ups and pull-ups you are welcome to 'rest', so long as you don't leave the bar or exist the push-up position i.e. lose four points of contact with the floor.

Push-Ups: Max reps  
Pull-Ups: Max reps  
Squats (60lb Kettlebell): Max reps

""")


st.markdown("""---""")
st.title("Results")
st.subheader("Quantities by Category")
st.dataframe(totals.style.format(formatter={'PULL_UP':"{:.2f}",
                                           'CHIN_UP':"{:.2f}",
                                           'PUSH_UP':"{:.2f}",
                                           'SQUAT':"{:.2f}",
                                           'HR_105-132':"{:.2f}", 
                                           'HR_133-166':"{:.2f}",
                                           'HR_167+':"{:.2f}",
                                           'MINS_RECOVERY':"{:.2f}",
                                           'HRS_SLEEP':"{:.2f}", 
                                           'LITERS_H2O':"{:.2f}",
                                           'MINS_HOT/COLD':"{:.2f}",
                                           'DISTANCE_KM':"{:.2f}",
                                           'MOOD':"{:.2f}",
                                           'REP_TOTAL':"{:.2f}"}))

st.subheader("Points by Category")
st.dataframe(score.style.format(formatter={'PULL_UP':"{:.2f}",
                                           'CHIN_UP':"{:.2f}",
                                           'PUSH_UP':"{:.2f}",
                                           'SQUAT':"{:.2f}",
                                           'HR_105-132':"{:.2f}", 
                                           'HR_133-166':"{:.2f}",
                                           'HR_167+':"{:.2f}",
                                           'MINS_RECOVERY':"{:.2f}",
                                           'HRS_SLEEP':"{:.2f}", 
                                           'LITERS_H2O':"{:.2f}",
                                           'MINS_HOT/COLD':"{:.2f}",
                                           'DISTANCE_KM':"{:.2f}",
                                           'MOOD':"{:.2f}",
                                           'POINT_TOTAL':"{:.2f}"}))

total_points = score["POINT_TOTAL"].max()
exercise_days = len(totals[totals["REP_TOTAL"] != 0.0])
x_days = len(score[score["POINT_TOTAL"] == 0.0])
no_exercise = len(totals[totals["REP_TOTAL"] == 0.0])-1
daily_scores = score["POINT_TOTAL"].tolist()
daily_scores.sort(reverse=True)
daily_high_score = daily_scores[1]
points_by_cat = score.iloc[31]
st.markdown("""---""")

st.header("Insights")
temp = score[score["POINT_TOTAL"] == total_points].index
best_day_date = score.iloc[temp]["DATE"].get(1)
col1, col2, col3, col4 = st.columns(4)
col1.metric("NO EXERCISE DAYS", no_exercise)
col2.metric("EXERCISE DAYS", exercise_days)
col3.metric("0-POINT DAYS", x_days)
col4.metric("TOTAL SCORE", f"{total_points:.2f}")

col_a, col_b = st.columns(2)
col_a.metric("HIGHEST DAILY", f"{daily_high_score:.2f}")
col_b.metric("% of all points earned", f"{(total_points/sum(max_points.values()))*100:.2f}")
st.markdown("""---""")


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
st.subheader("Fig. 1 - Points by Category")
st.write("Shows all the points I earned by category as a percentage.")
labels = 'Pull-Ups', 'Chin-Ups', 'Push-Ups', 'Squats', 'Cardio', 'Recovery', 'Sleep', 'H20'
sizes = [20.60, 34.35, 107.55, 65.55, 33.0, 20.0, 53.50, 66]
explode = (0, 0, 0.1, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

st.subheader("Fig. 2 - Daily Points Earned by Category")
st.write("This stacked bar chart shows the make up (by category) of total daily points earned across the month.")
stack_data = utils.build_stacked_barchat_data(score)
st.write(alt.Chart(stack_data).mark_bar().encode(
    x='date',
    y='sum(points)',
    color='category'
))

st.subheader("Fig. 3 - Points Earned of Total Available by Category")
st.write("This chart shows how much of the available points for a category I earned.")
temp = utils.build_percentage_chart_data(points_by_cat, max_points)
# st.dataframe(temp)
st.write(alt.Chart(temp).mark_bar().encode(
    x='category',
    y='points',
    color='status'
).properties(
    width=800,
    height=450
))


st.markdown("""---""")
st.header("Post-Challenge Fitness Test Results")
col1, col2, col3 = st.columns(3)
col1.metric("PULL-UPS", "12", "3")
col2.metric("PUSH-UPS", "37", "7")
col3.metric("SQUATS", "31", "6")