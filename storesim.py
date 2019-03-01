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
        for customer in self.customers:
            rental        = customer.create_rental(self.inventory)
            self.revenue += rental.price

    def print_summary(self):
        print("Tools currently in the store (not rented):")
        for tool in self.inventory:
            print(tool.tool_name)
        print("{} tools are currently in the store".format(len(self.inventory)))
        print("======================================")
        print("Amount of money the store made: ${}".format(self.revenue))
        print("======================================")
        print("Summaries of returned rentals:")

        for rental in self.returned_rentals:
            tools = rental.tools
            print("Tools rented: {}".format(", ".join(tool.tool_name for tool in tools)))
            print("Total price of rental: {}".format(rental.price))
            print("Name of renter: {}".format(rental.customer_name))
            print("======================================")

        print("Summaries of current rentals:")
        for customer in self.customers:
            for rental in customer.rentals:
                tools = rental.tools
                print("Tools rented: {}".format(", ".join(tool.tool_name for tool in tools)))
                print("Total price of rental: {}".format(rental.price))
                print("Name of renter: {}".format(rental.customer_name))
                print("======================================")



class Rental:

    def __init__(self, days_remaining, tools, customer_name):
        self.days_remaining = days_remaining
        self.rental_length  = days_remaining
        self.tools          = tools
        self.price          = sum([tool.price*days_remaining for tool in tools])
        self.customer_name  = customer_name

class Customer:
    num_tools_rented = 0
    rentals = []

    def __init__(self, type, id):
        config_file        = get_config_name()
        self.config        = configreader(config_file)
        self.max_num_tools = self.config['customer']['max_num_tools']
        self.name          = "{0} Customer {1}".format(type, id)

    def create_rental(self, tools):
        can_rent = self.max_num_tools - self.num_tools_rented
        if can_rent > 0 and can_rent <= len(tools):
			#num_tools = random.randint(1, can_rent)
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
			#days = random.randint(1,7)
            # again, we should pick preferred_num_nights
            days = random.choice(self.preferred_num_nights)
            rental = Rental(days, rental_tools, self.name)
            self.rentals.append(rental)
            return rental
        else:
            return Rental(0, [], '')


    def check_returns(self):
        returned_tools   = []
        returned_rentals = []
        for rental in self.rentals:
            rental.days_remaining -= 1
            if rental.days_remaining <= 0:
                returned_tools   += rental.tools
                returned_rentals.append(rental)
                self.rentals.remove(rental)

        return returned_tools, returned_rentals

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
