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

    def __init__(self, name, count):
        # Get config parameters and access price
        config_file = get_config_name()
        config      = configreader(config_file)
        self.price  = config['tool'][name]['price']

        # Assign unique tool name. Let the store manage the
        # names of the tools, and the tool will keep track of itself
        self.tool_type = name
        self.tool_name = "{0} tool {1}".format(self.tool_type, count)
        print(self.tool_name)

class Customer:
    num_tools_rented = 0

    def __init__(self, name):
        config_file        = get_config_name()
        self.config        = configreader(config_file)
        self.max_num_tools = self.config['customer']['max_num_tools']
        self.name          = "Customer {0}".format(name)
        print(self.name)


    def create_rental(self):
        if self.num_tools_rented < self.max_num_tools:
            pass


class CasualCustomer(Customer):
    def __init__(self, name):
        super(CasualCustomer, self).__init__(name)
        self.num_tools  = self.config['customer']['casual']['num_tools']
        self.num_nights = self.config['customer']['casual']['num_nights']


class BusinessCustomer(Customer):
    def __init__(self, name):
        super(BusinessCustomer, self).__init__(name)
        self.num_tools  = self.config['customer']['business']['num_tools']
        self.num_nights = self.config['customer']['business']['num_nights']

class RegularCustomer(Customer):
    def __init__(self, name):
        super(RegularCustomer, self).__init__(name)
        self.num_tools  = self.config['customer']['regular']['num_tools']
        self.num_nights = self.config['customer']['regular']['num_nights']

class CustomerFactory:
    def __init__(self):
        config_file         = get_config_name()
        self.config         = configreader(config_file)
        self.customer_types = self.config['customer']['types']    # list of all possible customer types

    def get_customer(self, type, name):
        if   type == "casual":   return CasualCustomer(name)
        elif type == "business": return BusinessCustomer(name)
        elif type == "regular":  return RegularCustomer(name)

    def random_customer(self, name):
        random_type_index = random.randint(0, len(self.customer_types)-1)
        customer_type     = self.customer_types[random_type_index]
        return self.get_customer(customer_type, name)


class Store:

    def __init__(self):
        config_file         = get_config_name()
        config              = configreader(config_file)
        self.num_customers  = config['customer']['num_customers']


    def generate_inventory(self):
        self.inventory = []

        self.inventory.append([Tool("painting", i+1) for i in range(4)])
        self.inventory.append([Tool("concrete", i+1) for i in range(4)])
        self.inventory.append([Tool("plumbing", i+1) for i in range(4)])
        self.inventory.append([Tool("woodwork", i+1) for i in range(4)])
        self.inventory.append([Tool("yardwork", i+1) for i in range(4)])

    def generate_customers(self):
        self.customers  = []
        customerfactory = CustomerFactory()
        self.customers.append([customerfactory.random_customer(i+1) for i in range(self.num_customers)])

    def cycle_day(self):
        pass


class Rental:

    tools = []
    price = 0

    def __init__(self, rental_begin_day, tools):
        self.days_remaining = rental_begin_day

    def add_tool(self, tool):
        pass



def main():
    config_file = get_config_name()
    config = configreader(config_file)
    store = Store()
    store.generate_inventory()
    store.generate_customers()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()


if __name__ == '__main__':
    main()
