class GameOfLife():
    def __init__(self):
        self.life_map = []
        self.mirror_map = []
        self.rules_alive = []
        self.rules_born = []
        self.map_len = 0
        self.row_len = 0

    def set_rules(self, alive=[], born=[]):
        self.rules_alive = alive
        self.rules_born = born
    
    def get_rules(self):
        return {"alive": self.rules_alive, "born": self.rules_born}

    def generate_random(self, row_len=None, map_len=None):
        from random import randint as rd

        if (not self.life_map) and (row_len and map_len):
            self.row_len = row_len
            self.map_len = map_len

        self.life_map = [rd(0, 1) for x in range(map_len)]
        self.mirror_map = [0 for x in self.life_map]

    def import_existing(self, source=[], row_len=None):
        if row_len and (len(source) % row_len == 0):
            self.life_map = [x for x in source]
            self.mirror_map = [0 for x in source]
            self.row_len = row_len
            self.map_len = len(source)

    def evaluate_cell(self, cell_index):
        if not self.life_map:
            return None
        
        state = self.life_map[cell_index]
        life_around = 0

        neighbors = [
            -(self.row_len - 1),
            -self.row_len,
            -(self.row_len + 1),
            -1,
            +1,
            +(self.row_len - 1),
            +self.row_len,
            +(self.row_len + 1)
        ]

        if cell_index < self.row_len:
            neighbors[0], neighbors[1], neighbors[2] = None, None, None
        if cell_index >= self.map_len - self.row_len:
            neighbors[5], neighbors[6], neighbors[7] = None, None, None
        if cell_index % self.row_len == 0:
            neighbors[0], neighbors[3], neighbors[5] = None, None, None
        if cell_index % self.row_len == self.row_len - 1: 
            neighbors[2], neighbors[4], neighbors[7] = None, None, None

        for nb in neighbors:
            if nb:
                life_around += self.life_map[cell_index + nb]
        
        if state and life_around in self.rules_alive:
            return 1
        elif (not state) and life_around in self.rules_born:
            return 1
        else:
            return 0
    
    def next_iteration(self):
        from copy import deepcopy as dc
        
        self.mirror_map = [self.evaluate_cell(idx) for idx in range(len(self.life_map))]
        self.life_map = dc(self.mirror_map)
    
    def get_map(self):
        return self.life_map
        
    def get_row_len(self):
        return self.row_len
