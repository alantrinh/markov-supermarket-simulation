import pandas as pd

def get_avg_customers_per_min():
    """
    This function get the dictionary for the average customers per min per opening hour.
    The dictionary is used for the simulation to create a random number of customers per min.
    """

    data = pd.read_csv('./data/supermarket_data.csv')
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # create hour column
    data['hour'] = data['timestamp'].dt.hour

    # ged rid of the multiple customer_no's
    data = data.drop_duplicates(subset=['customer_no'], keep='first')

    # get the average number of customers per specific hour
    # diveded by 60, to get average per minute
    # diveded by 5, because the data is for 5 days
    per_min_avg = data.groupby('hour')['customer_no'].count()/60/5

    # make it to a dict
    per_min_avg = dict(per_min_avg)

    return per_min_avg
