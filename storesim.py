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


class Tool:
    def __init__(self, name):
        config_file = get_config_name()
        config = configreader(config_file)
        self.price = config['tool'][name]['price']

    def set_price(self, price):
        self.price = price


class Painting(Tool):
    num_tools = 0

    def __init__(self):
        self.name = "painting"
        super(Painting, self).__init__(self.name)
        self.num_tools += 1
        self.tool_name = "Painting tool {}".format(self.num_tools)


class Concrete(Tool):
    num_tools = 0

    def __init__(self):
        self.name = "concrete"
        super(Concrete, self).__init__(self.name)
        self.num_tools += 1
        self.tool_name = "Concrete tool {}".format(self.num_tools)


class Plumbing(Tool):
    num_tools = 0

    def __init__(self):
        self.name = "plumbing"
        super(Plumbing, self).__init__(self.name)
        self.num_tools += 1
        self.tool_name = "Plumbing tool {}".format(self.num_tools)


class Woodwork(Tool):
    num_tools = 0

    def __init__(self):
        self.name = "woodwork"
        super(Woodwork, self).__init__(self.name)
        self.num_tools += 1
        self.tool_name = "Woodwork tool {}".format(self.num_tools)


class Yardwork(Tool):
    num_tools = 0

    def __init__(self):
        self.name = "yardwork"
        super(Yardwork, self).__init__(self.name)
        self.num_tools += 1
        self.tool_name = "Yardwork tool {}".format(self.num_tools)


class Store:
    def build_inventory(self):
        self.inventory = []

        PaintingTools = self.inventory.append([Painting() for _ in range(4)])
        ConcreteTools = self.inventory.append([Concrete() for _ in range(4)])
        PlumbingTools = self.inventory.append([Plumbing() for _ in range(4)])
        WoodworkTools = self.inventory.append([Woodwork() for _ in range(4)])
        YardworkTools = self.inventory.append([Yardwork() for _ in range(4)])

    def cycle_day(self):
        pass


class Rental:
    pass


if __name__ == '__main__':
    config_file = get_config_name()
    config = configreader(config_file)
    store = Store()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()
