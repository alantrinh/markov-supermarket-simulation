

class Location:
    def __init__(self, name):
        self.name = name
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer_id):
        self.customers = [customer for customer in self.customers if customer.id != customer_id]