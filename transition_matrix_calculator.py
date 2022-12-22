import pandas as pd
import numpy as np
from datetime import timedelta

from pandas._libs.tslibs.offsets import Day

# add initial timestamp for each customer with location 'entry'
def add_location_entry(df):
    df_entry = pd.DataFrame(df.groupby('customer_no').first()['timestamp'] - timedelta(minutes=1)) # find each customer's first timestamp and go back 1 minute
    df_entry['location'] = 'entry' # add location entry for all timestamps
    df_entry.reset_index(inplace=True) # reset index to get 'customer_no' column back

    df_with_entry = pd.concat([df, df_entry]).sort_values(['timestamp', 'location']) # concat and sort by timestamp
    
    return df_with_entry

def create_missing_checkout(df):
    """
    For some of last customers are the checkouts missing. This function adds them.
    """
    timestamp = df['timestamp'].iloc[-1] + timedelta(minutes=1) #selecting the last timestamp in the df for date and time and adds 3 minutes
    
    data_checkout = df.loc[df['location'] == 'checkout']
    customers_with_checkout = data_checkout['customer_no'].unique()
    customers_ids = df['customer_no'].unique()
    customers_without_checkout = np.setxor1d(customers_with_checkout, customers_ids) # function, which compares to arrays for no matching values
    
    for ids in customers_without_checkout:
        new_row = pd.DataFrame({'timestamp':timestamp, 'customer_no':ids, 'location':'checkout'}, index =[0])
        df = pd.concat([df, new_row]).reset_index(drop = True)
        
    return df

# forward fill with granularity of minutes
def fill_minutes(df):
    df_filled_mins = df.set_index('timestamp')
    df_filled_mins = df_filled_mins.groupby('customer_no').resample('T').first().ffill()
    df_filled_mins.drop('customer_no', axis=1, inplace=True) # drop 'customer_no' column as it is in index after grouping
    df_filled_mins.reset_index(inplace=True) # reset index to get 'timestamp' and 'customer_no' back
    df_filled_mins = df_filled_mins.sort_values(['timestamp', 'location']) # sort

    return df_filled_mins

def replace_customer_ids(df, day_ids):
    """
    The customer id 'customer_no' resets each day. This functions makes it unique for all days. The daily IDs are needed.
    """
    value = 1
    for i, _ in enumerate(day_ids):
        df.loc[df['customer_no'] == value, 'customer_no'] = day_ids[i]
        value += 1
    
    return df

def calculate_transition_matrix(df):
    # add 'next_location' 
    df['next_location'] = df[['location', 'customer_no']].groupby('customer_no').shift(-1)
    # where 'location' is 'checkout', 'next_location' is NaN so fill these with 'checkout'
    df.loc[df['location'] == 'checkout', 'next_location'] = 'checkout'

    P = pd.crosstab(
        df['location'],
        df['next_location'],
        normalize='index'
    )

    return P

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

days_data = {day: pd.read_csv(f'data/{day}.csv', sep=';') for day in days}
for key in days_data:
    # convert timestamps from string to datetime
    days_data[key]['timestamp'] = pd.to_datetime(days_data[key]['timestamp'])

days_ids = {}

for i, current_day in enumerate(days):
    if current_day == 'monday':
        days_ids[current_day] = np.array(days_data[current_day]['customer_no'])
    else:
        previous_day = days[i - 1]
        if current_day == 'tuesday':
            days_ids[current_day] = np.arange((
                days_data[previous_day]['customer_no'].max()) + 1,
                days_data[previous_day]['customer_no'].max() + days_data[current_day]['customer_no'].max() + 1
            )
        else:
            days_ids[current_day] = np.arange(
                days_ids[previous_day][-1] + 1,
                days_ids[previous_day][-1] + days_data[current_day]['customer_no'].max() + 1
            )

tmp = []
for day in days:
    current_day_data = add_location_entry(days_data[day])
    current_day_data = create_missing_checkout(current_day_data)
    current_day_data = fill_minutes(current_day_data)
    if day != 'monday':
        current_day_data = replace_customer_ids(current_day_data, days_ids[day])
    tmp.append(current_day_data)

data = pd.concat(tmp, ignore_index=True)

transition_matrix = calculate_transition_matrix(data)
transition_matrix.to_csv("./data/transition_matrix.csv")

data.to_csv("./data/supermarket_data.csv", index=False)
