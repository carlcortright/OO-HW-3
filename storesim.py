import json
import random
import argparse


#
# BEGIN SECTION: static methods that don't need a class
# These are implemented to reduce coupling between retrieving
# command line args and config settings and the objects using them
#
def get_config_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', help='config json file')
    args = parser.parse_args()
    return args.configfile


def configreader(configfile):
    with open(configfile) as file:
        config = json.load(file)
    return config

#
# END SECTION: Static methods that don't need a class
#


# After dicussion, we decided to put all tools into a single
# class, since we decided that we were using new tools as
# subclasses for specialization, rather than a new functionality.
# Our subclasses were basically data holders, which is now managed
# by the Tool superclass
class Tool:

    def __init__(self, type_str, count):
        # Get config parameters and access price
        config_file = get_config_name()
        config      = configreader(config_file)
        self.price  = config['tool'][type_str]['price']

        # Assign unique tool name. Let the store manage the
        # names of the tools, and the tool will keep track of itself
        self.tool_type = type_str
        self.tool_name = "{0} tool {1}".format(self.tool_type, count)

    def get_name(self):
        return self.tool_name

    def __eq__(self, other):
        return self.tool_name == other.tool_name


class Store:

    def __init__(self):
        self.build_inventory()
        self.create_customers()
        self.returned_rentals = []
        self.revenue = 0.0

    def create_customers(self):
        self.customers = []
        self.customers += [CasualCustomer(i+1) for i in range(3)]
        self.customers += [RegularCustomer(i+1) for i in range(3)]
        self.customers += [BusinessCustomer(i+1) for i in range(4)]

    def build_inventory(self):
        self.inventory = []
        self.inventory += [Tool("painting", i+1) for i in range(4)]
        self.inventory += [Tool("concrete", i+1) for i in range(4)]
        self.inventory += [Tool("plumbing", i+1) for i in range(4)]
        self.inventory += [Tool("woodwork", i+1) for i in range(4)]
        self.inventory += [Tool("yardwork", i+1) for i in range(4)]

    def cycle_day(self):
        # First return all of the remaining tools
        for customer in self.customers:
            returned_tools, returned_rentals = customer.check_returns()
            self.inventory += returned_tools
            self.returned_rentals += returned_rentals

        # Then create new rentals for the next day
        random.shuffle(self.customers)
        for customer in self.customers:
            rental        = customer.create_rental(self.inventory)
            self.revenue += rental.get_price()

    def print_summary(self):
        
        print("Summaries of returned rentals:")
        for rental in self.returned_rentals:
            tools = rental.get_tools()
            print("Tools rented: {}".format(", ".join(tool.get_name() for tool in tools)))
            print("Total price of rental: {}".format(rental.get_price()))
            print("Name of renter: {}".format(rental.get_customer()))
            print("======================================")

        print("Summaries of current rentals:")
        for customer in self.customers:
            customer.print_current_rentals()

        print("Tools currently in the store (not rented):")
        for tool in self.inventory:
            print(tool.get_name())
        print("{} tools are currently in the store".format(len(self.inventory)))
        print("======================================")
        print("Amount of money the store made: ${:.2f}".format(self.revenue))
        


# A class that dumbly holds and gives back information about a rental.
# Also decrements the number of days remaining for a rental. This
# Mostly helps the customer keep track of their multiple rentals
class Rental:

    def __init__(self, days_remaining, tools, customer_name):
        self.__days_remaining = days_remaining
        self.rental_length  = days_remaining
        self.tools          = tools
        self.price        = sum([tool.price*days_remaining for tool in tools])
        self.customer_name  = customer_name

    @property
    def days_remaining(self):
        return self.__days_remaining

    def decrement_days(self):
        self.__days_remaining -= 1

    def get_price(self):
        return self.price

    def get_tools(self):
        return self.tools

    def get_customer(self):
        return self.customer_name


class Customer:
    num_tools_rented = 0
    rentals = []

    def __init__(self, type, id):
        config_file        = get_config_name()
        self.config        = configreader(config_file)
        self.max_num_tools = self.config['customer']['max_num_tools']
        self.name          = "{0} Customer {1}".format(type, id)

    def get_rentals(self):
        return self.rentals

    # 
    # Creates a rental for the customer using their specific desired quantities. 
    # Returns that rental so the caller can account for any tools that have been
    # rented.
    # 
    def create_rental(self, tools):
        can_rent = self.max_num_tools - self.num_tools_rented
        if can_rent > 0 and can_rent <= len(tools):
            # pick a preferred number of tools based on customer type
            # to follow requirements of assignment
            num_tools = random.choice(self.preferred_num_tools)
            while num_tools > can_rent:
                num_tools -= 1

            rental_tools = []
            for i in range(num_tools):
                tool = random.choice(tools)
                tools.remove(tool)
                rental_tools.append(tool)
            # again, we should pick preferred_num_nights
            days = random.choice(self.preferred_num_nights)
            rental = Rental(days, rental_tools, self.name)
            self.rentals.append(rental)
            return rental
        else:
            return Rental(0, [], '')

    # 
    # Method that has the customer check if any of their rentals need to be returned. 
    # If a rental needs to be returned it is removed from the rentals and the tools 
    # are returned. 
    # 
    def check_returns(self):
        returned_tools   = []
        returned_rentals = []
        for rental in self.rentals:
            rental.decrement_days()
            if rental.days_remaining <= 0:
                returned_tools   += rental.tools
                returned_rentals.append(rental)
                self.rentals.remove(rental)

        return returned_tools, returned_rentals

    def print_current_rentals(self):
        for rental in self.get_rentals():
            tools = rental.get_tools()
            print("Tools rented: {}".format(", ".join(tool.get_name() for tool in tools)))
            print("Total price of rental: {}".format(rental.get_price()))
            print("Name of renter: {}".format(rental.get_customer()))
            print("======================================")


class CasualCustomer(Customer):
    def __init__(self, id):
        super(CasualCustomer, self).__init__("Casual", id)
        self.preferred_num_tools  = self.config['customer']['casual']['preferred_num_tools']
        self.preferred_num_nights = self.config['customer']['casual']['preferred_num_nights']


class BusinessCustomer(Customer):
    def __init__(self, id):
        super(BusinessCustomer, self).__init__("Business", id)
        self.preferred_num_tools  = self.config['customer']['business']['preferred_num_tools']
        self.preferred_num_nights = self.config['customer']['business']['preferred_num_nights']


class RegularCustomer(Customer):
    def __init__(self, id):
        super(RegularCustomer, self).__init__("Regular", id)
        self.preferred_num_tools  = self.config['customer']['regular']['preferred_num_tools']
        self.preferred_num_nights = self.config['customer']['regular']['preferred_num_nights']


def main():
    config_file = get_config_name()
    config = configreader(config_file)
    store = Store()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()
    store.print_summary()

if __name__ == '__main__':
    main()
