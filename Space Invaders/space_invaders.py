import random

class Game:
    def __init__(self):
        self.invader_grid_width = 70
        self.invader_grid_height = 70
        self.invader_space = (100, 1100)
        # Generate aliens
        aliencoords = [[(self.invader_grid_width * x, self.invader_grid_height * y) for y in range(5)]
                       for x in range(11)]  # aliencoords[0] is first column TODO: adjust coordinates to match game
        self.invaders = [[None for y in range(5)] for x in range(11)]
        for col in range(len(aliencoords)):
            for row in range(len(aliencoords[col])):
                inv = Invader(aliencoords[col][row], invader_type(row))
                self.invaders[col][row] = inv
                inv.xpos += self.invader_space[0] + (self.invader_grid_width - inv.width)/2

        # Generate barricades
        self.barricades = []
        for bar in range(4):
            gridpoint = 100 + 1000//4 * bar + (1000//4-88)//2
            self.barricades.append(Barricade(gridpoint, 600))

        self.spaceship = Spaceship()
        self.shots = []

    def leftmost_invader(self):
        """Find the first column of invaders that contains living invaders. Return the first invader in that column.
        If all invaders are dead, return -1."""
        for col in self.invaders:
            for inv in col:
                if inv is not None:
                    return inv
        return -1

    def rightmost_invader(self):
        """Find the last column of invaders that contains living invaders. Return the last invader found in that column,
        or -1 if all invaders are dead."""
        for col in self.invaders[::-1]:
            for inv in col:
                if inv is not None:
                    return inv
        return -1

    def move_invaders(self, invader_dir):
        """Move all invaders in the invader_dir specified by invader_dir. invader_dir = 1 signals right,
        and invader_dir = -1 signals left. If any invader moves out of the designated space, the opposite invader_dir is
        returned and the invaders are moved down. If they stay within the invader space,
        the same invader_dir is returned."""
        if invader_dir == 1:
            for col in self.invaders:
                for inv in col:
                    if inv is not None:
                        inv.xpos += 4
            if self.rightmost_invader().xpos + self.invader_grid_width/2 > self.invader_space[1]:
                self.move_down_invaders()
                return -1
            else:
                return 1
        if invader_dir == -1:
            for col in self.invaders:
                for inv in col:
                    if inv is not None:
                        inv.xpos -= 4
            if self.leftmost_invader().xpos + self.invader_grid_width/2 < self.invader_space[0]:
                self.move_down_invaders()
                return 1
            else:
                return -1

    def move_down_invaders(self):
        for col in self.invaders:
            for inv in col:
                if inv is not None:
                    inv.ypos += 8

    def destroy_invader(self):
        pass

    def invader_shoot(self):
        for col in self.invaders:
            if random.random() > 0.999:
                for inv in col[::-1]:
                    if inv is not None:
                        self.shots.append(inv.shoot())
                        break

    def move_shots(self):
        delete_shots = []
        for k in range(len(self.shots)):
            s = self.shots[k]
            s.ypos += s.velocity
            if s.ypos > 800 or s.ypos < 0:
                delete_shots.append(k)
        for l in delete_shots[::-1]:
            self.shots.pop(l)


class Invader:
    def __init__(self, pos, variant):
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.variant = variant
        if variant == 1:
            self.width = 48
        elif variant == 2:
            self.width = 44
        elif variant == 3:
            self.width = 32

    def shoot(self):
        return Shot(self.xpos+self.width//2, self.ypos, 1, 1)


class Shot:
    def __init__(self, xpos, ypos, velocity, variant):
        self.variant = variant
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = velocity
        self.width = 2
        self.height = 6


class Spaceship:
    def __init__(self):
        self.xpos = 100
        self.ypos = 700
        self.width = 52
        self.max_velocity = 4
        self.lives = 3


class Barricade:
    def __init__(self, xpos, ypos):
        self.hits_remaining = 5
        self.width = 88
        self.xpos = xpos
        self.ypos = ypos


def invader_type(row):
    if row == 0:
        return 3
    elif row in [1, 2]:
        return 2
    elif row in [3, 4]:
        return 1
