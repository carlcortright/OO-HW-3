import json
import argparse
import random


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

	def __eq__(self, other):
		return self.tool_name == other.tool_name


class Store:

	def __init__(self):
		self.build_inventory()
		self.create_customers()
		self.rentals = list()
		self.revenue = 0.0

	def create_customers(self):
		self.customers = []
		self.customers += [CasualCustomer() for i in range(3)]
		self.customers += [RegularCustomer() for i in range(3)]
		self.customers += [BusinessCustomer() for i in range(4)]

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
			self.inventory += customer.check_returns()
		# Then create new rentals for the next day
		for customer in self.customers:
			rental = customer.create_rental(self.inventory)
			self.revenue += rental.price

class Rental:

	def __init__(self, days_remaining, tools):
		self.days_remaining = days_remaining
		self.tools = tools     # tools is a list of Tools
		self.price = sum([tool.price*days_remaining for tool in tools])
	


class Customer:
	num_tools_rented = 0
	rentals = []

	def __init__(self):
		config_file = get_config_name()
		self.config = configreader(config_file)
		self.max_num_tools = self.config['customer']['max_num_tools']

	def create_rental(self, tools):
		can_rent = self.max_num_tools - self.num_tools_rented
		if can_rent > 0 and can_rent <= len(tools):
			num_tools = random.randint(1, can_rent)
			rental_tools = []
			for i in range(num_tools):
				tool = random.choice(tools)
				tools.remove(tool)
				rental_tools.append(tool)
			days = random.randint(1,7)
			rental = Rental(days, rental_tools)
			self.rentals.append(rental)
			return rental
		else:
			return Rental(0, [])
			  
	
	def check_returns(self):
		returned_tools = []
		for rental in self.rentals:
			rental.days_remaining -= 1
			if rental.days_remaining <= 0:
				returned_tools += rental.tools
				self.rentals.remove(rental)
		return returned_tools

class CasualCustomer(Customer):
    def __init__(self):
        super(CasualCustomer, self).__init__()
        self.num_tools = self.config['customer']['casual']['num_tools']
        self.num_nights = self.config['customer']['casual']['num_nights']


class BusinessCustomer(Customer):
    def __init__(self):
        super(BusinessCustomer, self).__init__()
        self.num_tools  = self.config['customer']['business']['num_tools']
        self.num_nights = self.config['customer']['business']['num_nights']


class RegularCustomer(Customer):
    def __init__(self):
        super(RegularCustomer, self).__init__()
        self.num_tools  = self.config['customer']['regular']['num_tools']
        self.num_nights = self.config['customer']['regular']['num_nights']


def main():
	config_file = get_config_name()
	config = configreader(config_file)
	store = Store()
	store.build_inventory()
	for _ in range(config['simulation']['num_days']):
		store.cycle_day()
	print(store.revenue)


if __name__ == '__main__':
    main()
