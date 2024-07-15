class Node:
    def __init__(self, data):
        self.number = data['number']
        self.neighbors = [(neighbor['neighbor'], neighbor['weight']) for neighbor in data['neighbors']]
        self.houses = [house for house in data['houses']]
        self.position = (data['position'][0], data['position'][1])
        