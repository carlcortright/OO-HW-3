import json
import argparse

def configreader(configfile):
    with open(configfile) as file:
        config = json.load(file)
    return config


class Tool:
    pass

class Painting(Tool):
    PRICE = config['tool']['painting']['price']

class Concrete(Tool):
    PRICE = config['tool']['concrete']['price']

class Plumbing(Tool):
    PRICE = config['tool']['plumbing']['price']

class Woodwork(Tool):
    PRICE = config['tool']['woodwork']['price']

class Yardwork(Tool):
    PRICE = config['tool']['yardwork']['price']


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
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', help='config json file')
    args = parser.parse_args()
    config = configreader(args.configfile)
    store = Store()
    for _ in range(config['simulation']['num_days']):
        store.cycle_day()
