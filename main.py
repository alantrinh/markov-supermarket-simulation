import numpy as np
import pandas as pd
from datetime import timedelta
from time import sleep

from supermarket import Supermarket

if __name__ == '__main__':
    
    supermarket = Supermarket()
    supermarket.open()

    # for loop that checks if the supermarket is before 21:50
    #   If so then incerement one minute and simulate generation/movement of customers
    #   Else close store and send current customers to checkout

    transition_matrix = pd.read_csv('./data/transition_matrix.csv')
    transition_matrix.set_index('location', inplace=True)
    transition_matrix = transition_matrix.transpose()

    NEW_CUSTOMERS_PER_MIN = {7: 1.6333333333333333, #data should come from data. To implemented
                        8: 2.35,                
                        9: 1.5166666666666666,
                        10: 1.3166666666666667,
                        11: 1.1166666666666667,
                        12: 1.3166666666666667,
                        13: 1.7666666666666666,
                        14: 1.6166666666666667,
                        15: 1.3333333333333333,
                        16: 1.7833333333333334,
                        17: 1.8833333333333333,
                        18: 2.1666666666666665,
                        19: 2.5,
                        20: 1.6,
                        21: 0.9333333333333333}
    
    
    id = 1
    
    for i in range(899):
        supermarket.time = supermarket.time + timedelta(minutes=1) #increment by 1 minute
        if supermarket.time <= timedelta(hours=21, minutes=50): #if before closing time
            key = supermarket.time.seconds // 3600 #takes hour from time as key for dict
            no_of_customers = round(np.random.normal(NEW_CUSTOMERS_PER_MIN[key])) #generated customers per min
            for no in range(no_of_customers): #adds generated customers to list
                customer = supermarket.generate_new_customer(id)
                id = id + 1
            for location_name, location in supermarket.locations.items():
                if location_name != 'checkout':
                    for customer in location.customers:
                        sleep(0.05)
                        customer.next_state(transition_matrix, supermarket.time, supermarket.locations)
        else:
            supermarket.close()
