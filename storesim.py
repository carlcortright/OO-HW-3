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
        config = configreader(config_file)
        self.price = config['tool'][type_str]['price']

        # Assign unique tool name. Let the store manage the
        # names of the tools, and the tool will keep track of itself
        self.tool_type = type_str
        self.tool_name = "{0} tool {1}".format(self.tool_type, count)

class Customer:
    num_tools_rented = 0

    def __init__(self, type, id):
        config_file        = get_config_name()
        self.config        = configreader(config_file)
        self.max_num_tools = self.config['customer']['max_num_tools']
        self.name          = "{0} Customer {1}".format(type, id)


    def create_rental(self):
        if self.num_tools_rented < self.max_num_tools:
            pass

    def cycle_day(self):
        pass


class CasualCustomer(Customer):
    def __init__(self, id):
        super(CasualCustomer, self).__init__("Casual", id)
        self.num_tools  = self.config['customer']['casual']['num_tools']
        self.num_nights = self.config['customer']['casual']['num_nights']


class BusinessCustomer(Customer):
    def __init__(self, id):
        super(BusinessCustomer, self).__init__("Business", id)
        self.num_tools  = self.config['customer']['business']['num_tools']
        self.num_nights = self.config['customer']['business']['num_nights']

class RegularCustomer(Customer):
    def __init__(self, id):
        super(RegularCustomer, self).__init__("Regular", id)
        self.num_tools  = self.config['customer']['regular']['num_tools']
        self.num_nights = self.config['customer']['regular']['num_nights']

class Store:

	def __init__(self):
		self.build_inventory()
		self.create_customers()
		self.rentals = list()

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
		for customer in self.customers:
			customer.cycle_day()


class Rental:

    tools = []
    price = 0

    def __init__(self, rental_begin_day):
        self.days_remaining = rental_begin_day

    def add_tool(self, tool):
        pass




def main():
    config_file = get_config_name()
    config = configreader(config_file)
    store = Store()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()


if __name__ == '__main__':
    main()
