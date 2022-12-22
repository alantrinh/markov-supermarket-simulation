from datetime import timedelta

from location import Location
from timestamp import Timestamp
from customer import Customer

class Supermarket:
    def __init__(self):
        location_names = ['entry', 'dairy', 'drinks', 'fruit', 'spices', 'checkout']
        self.locations = {location_name: Location(location_name) for location_name in location_names}

    def open(self):
        self.time = timedelta(hours=7)

    def generate_new_customer(self, id):
        customer = Customer(id, self.time, self.get_entry_location())
        self.locations['entry'].add_customer(customer)
        print(f'{customer.id} is at {customer.get_last_location()} at time {customer.get_last_timestamp().time}')

        return customer

    def close(self):
        """
        Every customer, who did not check out, is send to checkout
        """
        for location_name, location in self.locations.items():
            #send remaining customers to checkout
            if location_name != 'checkout':
                for customer in location.customers:
                    customer.history.append(Timestamp(self.time, self.locations['checkout']))
                    print(f'{customer.id} is at {customer.get_last_location()} at time {customer.get_last_timestamp().time}')
                #empty customers from location
                location.customers = []


    def get_entry_location(self):
        return self.locations['entry']

