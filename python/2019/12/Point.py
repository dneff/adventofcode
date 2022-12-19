class Point():
    def __init__(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0

    def findGravity(self, a, b):
        if a > b:
            return -1
        elif a == b:
            return 0
        elif a < b:
            return 1
    
    def getEnergy(self):
        pot = abs(self.pos_x) + abs(self.pos_y) + abs(self.pos_z)
        kin = abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)
        return pot * kin

    def updateVelocity(self, other):
        self.vel_x += self.findGravity(self.pos_x, other.pos_x)
        self.vel_y += self.findGravity(self.pos_y, other.pos_y)
        self.vel_z += self.findGravity(self.pos_z, other.pos_z)
    
    def updatePosition(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.pos_z += self.vel_z

    def __eq__(self, other):
        return all([
            self.pos_x == other.pos_x,
            self.pos_y == other.pos_y,
            self.pos_z == other.pos_z
        ])

    def __iter__(self):
        return (x for x in [self.pos_x, self.pos_y, self.pos_z])

    def __str__(self):
        s = "Point("
        s += f"x={self.pos_x}, "
        s += f"y={self.pos_y}, "
        s += f"z={self.pos_z}"
        s += ")"
        return s

    def __repr__(self):
        s = "Point("
        s += f"x={self.pos_x}, "
        s += f"y={self.pos_y}, "
        s += f"z={self.pos_z}"
        s += ")"
        return s    

