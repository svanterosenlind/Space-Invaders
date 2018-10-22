import random

class Game:
    def __init__(self, lives):
        self.invader_grid_width = 90
        self.invader_grid_height = 70
        self.invader_space = (50, 1150)
        self.score = 0
        self.invader_dir = 1
        self.t = 0
        self.steps = 0
        self.invader_step = 20
        # Generate aliens
        aliencoords = [[(self.invader_grid_width * x, 150 + self.invader_grid_height * y) for y in range(5)]
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

        self.spaceship = Spaceship(lives)
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

    def move_invaders(self):
        """Move all invaders in the invader_dir specified by invader_dir. invader_dir = 1 signals right,
        and invader_dir = -1 signals left. If any invader moves out of the designated space, the opposite invader_dir is
        returned and the invaders are moved down. If they stay within the invader space,
        the same invader_dir is returned."""
        self.t += 1
        stepped = False
        if self.t % self.invader_step == 0:
            self.invader_dir = self.step_invaders(self.invader_dir)
            self.steps += 1
            if self.steps % 36 == 0 and self.invader_step > 2:
                self.invader_step -= 2
            stepped = True
        return stepped

    def step_invaders(self, invader_dir):
        if invader_dir == 1:
            for col in self.invaders:
                for inv in col:
                    if inv is not None:
                        inv.xpos += 8
            if self.rightmost_invader().xpos + self.invader_grid_width/2 > self.invader_space[1]:
                self.move_down_invaders()
                return -1
            else:
                return 1
        if invader_dir == -1:
            for col in self.invaders:
                for inv in col:
                    if inv is not None:
                        inv.xpos -= 8
            if self.leftmost_invader().xpos + self.invader_grid_width/2 < self.invader_space[0]:
                self.move_down_invaders()
                return 1
            else:
                return -1

    def move_down_invaders(self):
        for col in self.invaders:
            for inv in col:
                if inv is not None:
                    inv.ypos += 12

    def destroy_invader(self, inv):
        self.score += inv.variant

    def invader_shoot(self):
        for col in self.invaders:
            if random.random() > 0.997:
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

    def move_spaceship(self, left, right):
        self.spaceship.move(left, right)

    def spaceship_shoot(self, space):
        sh = self.spaceship.shoot(space)
        if sh is not None:
            self.shots.append(sh)

    def detect_shot_invader(self):
        destroyed = []
        for shot in self.shots[::-1]:
            if shot.variant == 2:
                for col in self.invaders:   # Player hits invaders
                    for invnum in range(len(col)):
                        if shot.detect_collision(col[invnum]):
                            destroyed.append((col[invnum].xpos, col[invnum].ypos))
                            self.destroy_invader(col[invnum])
                            col[invnum] = None
                            self.shots.remove(shot)
        return destroyed

    def detect_shot_shot(self):
        for shot1 in self.shots[::-1]:
            if shot1.variant == 2:
                for shot2 in self.shots[::-1]:
                    if shot2.variant in [1, 3]:
                        if shot1.detect_collision(shot2):
                            self.shots.remove(shot1)
                            self.shots.remove(shot2)

    def detect_shot_spaceship(self):
        for shot in self.shots[::-1]:
            if shot.variant in [1, 3]:
                if shot.detect_collision(self.spaceship):
                    self.spaceship.lives -= 1
                    self.shots = []
                    return True
        return False

    def detect_shot_barricade(self):
        for shot in self.shots[::-1]:
            for n in range(len(self.barricades)):
                if self.barricades[n] is not None:
                    if shot.detect_collision(self.barricades[n]):
                        self.barricades[n].hits_remaining -= 1
                        self.barricades[n].hits.append((shot.xpos, shot.ypos))
                        self.shots.remove(shot)
                        if self.barricades[n].hits_remaining <= 0:
                            self.barricades[n] = None


class Invader:
    def __init__(self, pos, variant):
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.variant = variant
        if variant == 1:
            self.width = 48
            self.height = 32
        elif variant == 2:
            self.width = 44
            self.height = 32
        elif variant == 3:
            self.width = 32
            self.height = 32

    def shoot(self):
        return Shot(self.xpos+self.width//2, self.ypos, 1)


class Shot:
    def __init__(self, xpos, ypos, variant):
        self.variant = variant
        self.xpos = xpos
        self.ypos = ypos
        if variant == 1:
            self.width = 12
            self.height = 28
            self.velocity = 6
        elif variant == 2:
            self.width = 4
            self.height = 12
            self.velocity = -12

    def detect_collision(self, obj):
        if obj is None:
            return False
        if self.variant == 2:    # Player shot
            return ((self.xpos + self.width >= obj.xpos) and (self.xpos <= obj.xpos + obj.width) and
                    (self.ypos + self.height >= obj.ypos) and (
                        self.ypos <= obj.ypos + obj.height))
        elif self.variant in [1, 3]:
            return ((self.xpos + self.width >= obj.xpos) and (self.xpos <= obj.xpos + obj.width) and
                    (self.ypos + self.height >= obj.ypos) and (
                            self.ypos <= obj.ypos + obj.height))
        return False


class Spaceship:
    def __init__(self, lives):
        self.xpos = 100
        self.ypos = 700
        self.width = 52
        self.height = 28
        self.max_velocity = 4
        self.lives = lives
        self.shot_timer = 0

    def move(self, left, right):
        if left == right:
            return
        elif left != 0:
            self.xpos -= left* self.max_velocity
        elif right !=0:
            self.xpos += right* self.max_velocity

        if self.xpos > 1200 - self.width:
            self.xpos = 1200 - self.width
        elif self.xpos < 0:
            self.xpos = 0

    def shoot(self, space):
        self.shot_timer -= 1
        if self.shot_timer < 0 and space != 0:
            self.shot_timer = 60
            return Shot(self.xpos + self.width//2, self.ypos - 12, 2)


class Barricade:
    def __init__(self, xpos, ypos):
        self.hits_remaining = 4
        self.width = 88
        self.height = 64
        self.xpos = xpos
        self.ypos = ypos
        self.hits = []


def invader_type(row):
    if row == 0:
        return 3
    elif row in [1, 2]:
        return 2
    elif row in [3, 4]:
        return 1

