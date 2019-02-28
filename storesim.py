import json
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
        config = configreader(config_file)
        self.price = config['tool'][name]['price']

        # Assign unique tool name. Let the store manage the
        # names of the tools, and the tool will keep track of itself
        self.tool_type = name
        self.tool_name = "{0} tool {1}".format(self.tool_type, count)
        print(self.tool_name)


class Store:
    def build_inventory(self):
        self.inventory = []

        self.inventory.append([Tool("painting", i+1) for i in range(4)])
        self.inventory.append([Tool("concrete", i+1) for i in range(4)])
        self.inventory.append([Tool("plumbing", i+1) for i in range(4)])
        self.inventory.append([Tool("woodwork", i+1) for i in range(4)])
        self.inventory.append([Tool("yardwork", i+1) for i in range(4)])

    def cycle_day(self):
        pass


class Rental:

    def __init__(self, days_remaining, tools):
        self.days_remaining = days_remaining
        self.tools = tools     # tools is a list of Tools


class Customer:
    max_num_tools    = config['customer']['max_num_tools']
    num_tools_rented = 0

    def create_rental(self):
        if self.num_tools_rented < max_num_tools:
        

class CasualCustomer(Customer):
    num_tools  = config['customer']['casual']['num_tools']
    num_nights = config['customer']['casual']['num_nights']

class BusinessCustomer(Customer):
    num_tools  = config['customer']['business']['num_tools']
    num_nights = config['customer']['business']['num_nights']

class RegularCustomer(Customer):
    num_tools  = config['customer']['regular']['num_tools']
    num_nights = config['customer']['regular']['num_nights']


def main():
    config_file = get_config_name()
    config = configreader(config_file)
    store = Store()
    store.build_inventory()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()


if __name__ == '__main__':
    main()
