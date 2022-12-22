import numpy as np
from timestamp import Timestamp


class Customer:
    def __init__(self, id, entry_time, entry_location):
        self.id = id
        self.history = [Timestamp(entry_time, entry_location)]

    def next_state(self, transition_matrix, time, locations):
        """
        This function implements Markov Chain Simulation, and
        returns the next state given an initial state
        """
        #remove customer from current location
        current_location_name = self.get_last_location()
        locations[current_location_name].remove_customer(self.id)

        #generate new location from probability matrix
        next_location_name = np.random.choice(
            a = transition_matrix.index,
            p = transition_matrix[self.get_last_location()]
        )

        #add timestamp to customer and customer to new location
        next_location = locations[next_location_name]
        self.history.append(Timestamp(time, next_location))
        next_location.add_customer(self)

        print(f'{self.id} is at {self.get_last_location()} at time {self.get_last_timestamp().time}')

    def get_last_timestamp(self):
        return self.history[-1]

    def get_last_location(self):
        return self.get_last_timestamp().location.name

