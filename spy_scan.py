#@title Weekly Highs and Lows by Day of Week
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from tabulate import tabulate

def get_day_name(day_number):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return days[day_number]

# Fetch SPY data for the last 5 years
spy = yf.Ticker("SPY")
data = spy.history(period="5y")

# Ensure the data is sorted by date
data = data.sort_index()

# Add a column for the day of the week (0 = Monday, 1 = Tuesday, ..., 4 = Friday)
data['Day_of_Week'] = data.index.dayofweek

# Resample to weekly data to find high and low of each week
weekly_data = data.resample('W').agg({'High': 'max', 'Low': 'min'})

# Initialize dictionaries to store the results
high_dates = {i: [] for i in range(5)}
low_dates = {i: [] for i in range(5)}

# Iterate over each week to find highs and lows for each day of the week
for week_start in weekly_data.index:
    week_data = data.loc[week_start - pd.Timedelta(days=6):week_start]

    if not week_data.empty:
        # Get the high and low of the week
        week_high = week_data['High'].max()
        week_low = week_data['Low'].min()

        # Check which day the high of the week occurred
        high_day = week_data[week_data['High'] == week_high].iloc[0]
        if high_day['Day_of_Week'] < 5:  # Exclude Saturday and Sunday
            high_dates[high_day['Day_of_Week']].append(high_day.name.date())

        # Check which day the low of the week occurred
        low_day = week_data[week_data['Low'] == week_low].iloc[0]
        if low_day['Day_of_Week'] < 5:  # Exclude Saturday and Sunday
            low_dates[low_day['Day_of_Week']].append(low_day.name.date())

# Function to calculate average days between occurrences
def calculate_average_days(dates):
    if len(dates) < 2:
        return 'N/A'
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    return sum(diffs) / len(diffs)

# Create a DataFrame for all dates
all_dates_data = []
for day in range(5):
    day_name = get_day_name(day)
    high_dates_recent = ', '.join(map(str, high_dates[day][-10:]))  # Only the ten most recent
    low_dates_recent = ', '.join(map(str, low_dates[day][-10:]))  # Only the ten most recent
    all_dates_data.append({'Day': day_name,
                           'High Dates': high_dates_recent,
                           'Low Dates': low_dates_recent})

all_dates_df = pd.DataFrame(all_dates_data)

# Calculate days from today for the last occurrence
today = pd.Timestamp(datetime.now().date())
last_occurrence_data = []

for day in range(5):
    day_name = get_day_name(day)
    last_high = max(high_dates[day]) if high_dates[day] else None
    last_low = max(low_dates[day]) if low_dates[day] else None

    days_since_high = (today - pd.Timestamp(last_high)).days if last_high else 'N/A'
    days_since_low = (today - pd.Timestamp(last_low)).days if last_low else 'N/A'

    average_days_between_highs = calculate_average_days(high_dates[day])
    average_days_between_lows = calculate_average_days(low_dates[day])

    last_occurrence_data.append({
        'Day': day_name,
        'Days Since Last High': days_since_high,
        'Days Since Last Low': days_since_low,
        'Number of Highs': len(high_dates[day]),
        'Number of Lows': len(low_dates[day]),
        'Average Days Between Highs': average_days_between_highs,
        'Average Days Between Lows': average_days_between_lows
    })

last_occurrence_df = pd.DataFrame(last_occurrence_data)

# Format the table using tabulate with custom formatting
headers = ['Day', 'High Dates', 'Low Dates']
table_data = all_dates_df.values.tolist()

# Add padding to make the columns more readable
formatted_table = tabulate(table_data, headers, tablefmt="grid", numalign="center", stralign="left")

print(f"\nAll dates when weekly high and low occurred for each day of the week for ticker: {spy.ticker}")
print(formatted_table)

# Format the second table using tabulate
headers_stats = ['Day', 'Days Since Last High', 'Days Since Last Low', 'Number of Highs', 'Number of Lows', 'Average Days Between Highs', 'Average Days Between Lows']
table_data_stats = last_occurrence_df.values.tolist()

# Create the formatted table for statistics
formatted_table_stats = tabulate(table_data_stats, headers_stats, tablefmt="grid", numalign="center", stralign="center")

print("\nStatistics for weekly highs and lows by day:")
print(formatted_table_stats)

# Create side-by-side bar chart
fig = go.Figure()

days = last_occurrence_df['Day']
highs = last_occurrence_df['Number of Highs']
lows = last_occurrence_df['Number of Lows']
days_since_high = last_occurrence_df['Days Since Last High']
days_since_low = last_occurrence_df['Days Since Last Low']
avg_days_between_highs = last_occurrence_df['Average Days Between Highs']
avg_days_between_lows = last_occurrence_df['Average Days Between Lows']

fig.add_trace(go.Bar(x=days, y=highs, name='Number of Highs'))
fig.add_trace(go.Bar(x=days, y=lows, name='Number of Lows'))
fig.add_trace(go.Bar(x=days, y=days_since_high, name='Days Since Last High'))
fig.add_trace(go.Bar(x=days, y=days_since_low, name='Days Since Last Low'))
fig.add_trace(go.Bar(x=days, y=avg_days_between_highs, name='Avg Days Between Highs', marker_color='rgba(255, 127, 80, 0.6)'))
fig.add_trace(go.Bar(x=days, y=avg_days_between_lows, name='Avg Days Between Lows', marker_color='rgba(100, 149, 237, 0.6)'))

fig.update_layout(barmode='group',
                  title='Statistics for Weekly Highs and Lows by Day of the Week',
                  xaxis_title='Day of the Week',
                  yaxis_title='Count/Days',
                  legend_title='Metric',
                  xaxis={'categoryorder':'array', 'categoryarray': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']})

fig.show()
