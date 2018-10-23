from space_invaders import Game
import random


class Monkey:
    def __init__(self):
        self.DNA = []
        """Movement: [0]Shot perception height, [1]shot perception width, [2]shot weight, 
            [3]Barricade weight, [4]we, 
            Shooting: if [5]Invader velocity [6]lowest alien height [7]barricade distance is in [8] +- [9]"""

    def randomize_DNA(self):
        """Movement: [0]Shot perception height, [1]shot perception width, [2]shot weight,
                    [3]Barricade weight, [4]we,
                    Shooting: if [5]Invader velocity [6]lowest alien height [7]barricade distance is in [8] +- [9]"""
        self.DNA.append(random.randint(0, 700))     # 0
        self.DNA.append(random.randint(0, 1000))    # 1
        self.DNA.append(random.random() * 2 - 1)    # 2
        self.DNA.append(random.random() * 2 - 1)    # 3
        self.DNA.append(random.randint(0, 700))     # 4
        self.DNA.append(random.random() * 2 - 1)    # 5
        self.DNA.append(random.random() * 2 - 1)    # 6
        self.DNA.append(random.randint(0, 700))     # 7
        self.DNA.append(random.random() * 1000)     # 7
        self.DNA.append(random.random() * 300)      # 8

    def mutate(self):
        if random.random() < 0.3:
            self.DNA[random.randint(0, len(self.DNA)-1)] *= (random.random()+0.5)

    def move(self, game):
        closest_shot_height = 0
        closest_shot_x = 300
        for shot in game.shots:
            if shot.variant != 2:
                if 730 > shot.ypos > closest_shot_height and game.spaceship.ypos - shot.ypos < self.DNA[0] \
                        and abs(game.spaceship.xpos - shot.xpos) < self.DNA[1]:
                    closest_shot_height = shot.ypos
                    closest_shot_x = shot.xpos - game.spaceship.xpos
        shot_factor = self.DNA[2] * closest_shot_x

        closest_bar = 1000
        for bar in game.barricades:
            if bar is not None:
                if abs(bar.xpos + bar.width/2 - game.spaceship.xpos) < closest_bar:
                    closest_bar = bar.xpos + bar.width/2 - game.spaceship.xpos
        barricade_factor = self.DNA[3]

        steer = shot_factor + barricade_factor + self.DNA[4]
        if steer <= 0:
            return [-max(steer/1500, 1), 0]
        else:
            return [0, max(1, steer/1500)]

    def shoot(self, game):
        closest_bar = 1000
        for bar in game.barricades:
            if bar is not None and abs(bar.xpos + bar.width / 2 - game.spaceship.xpos) < closest_bar:
                closest_bar = bar.xpos + bar.width / 2 - game.spaceship.xpos
        if closest_bar < self.DNA[7]:
            return False
        lowest_invader_height = 1000
        for col in game.invaders:
            for inv in col:
                if inv.ypos > lowest_invader_height:
                    lowest_invader_height = inv.ypos
        return self.DNA[8] - self.DNA[9] < lowest_invader_height * self.DNA[6] + (game.invader_dir / game.invader_step) * self.DNA[5] < self.DNA[8] + self.DNA[9]


def calc_fitness(m):
    print("Calculating fitness")
    lives = 3
    score = 0
    while lives > 0:
        score, lives = run_game(lives, score, m)
    return score


def run_game(lives, score, monkey):
    game = Game(lives)
    while True:
        if game.leftmost_invader() == -1:
            return [score + game.score, game.spaceship.lives]
        left, right = monkey.move(game)
        space = True    # monkey.shoot(game)
        game.move_spaceship(left, right)
        game.spaceship_shoot(space)
        game.invader_shoot()
        game.move_invaders()
        game.move_shots()
        game.detect_shot_barricade()
        game.detect_shot_invader()
        game.detect_shot_shot()
        if game.detect_shot_spaceship():
            if game.spaceship.lives == 0:
                return [score + game.score, 0]
        if game.t > 1000000:
            return [score + game.score, 0]

def new_population(old_population):
    new_pop = []
    fitnesses = {}
    total_fitness = 0
    best_fitness = 0
    for monkey in old_population:
        fitnesses[monkey] = calc_fitness(monkey)
        total_fitness += fitnesses[monkey]
        if fitnesses[monkey] > best_fitness:
            best_fitness = fitnesses[monkey]
    if total_fitness == 0:
        for m in old_population:
            m.randomize_DNA()
        return old_population, 0
    for monkey in old_population:
        while True:
            monkey1 = old_population[random.randint(0, len(old_population)-1)]
            if float(fitnesses[monkey1])/total_fitness > random.random():
                break
        while True:
            monkey2 = old_population[random.randint(0, len(old_population)-1)]
            if float(fitnesses[monkey2]) / total_fitness > random.random():
                break
        new_monkey = crossover(monkey1, monkey2)
        new_monkey.mutate()
        new_pop.append(new_monkey)
    return new_pop, best_fitness


def crossover(monkey1, monkey2):
    new_monkey = Monkey()
    new_monkey.randomize_DNA()
    for a in range(len(monkey1.DNA)):
        if random.random() > 0.5:
            new_monkey.DNA[a] = monkey1.DNA[a]
        else:
            new_monkey.DNA[a] = monkey2.DNA[a]
    return new_monkey


def main():
    population = []
    for a in range(6):
        m = Monkey()
        population.append(m)
        m.randomize_DNA()
    for x in range(20):
        new_pop, best_fitness = new_population(population)
        population = new_pop
        print(best_fitness)


if __name__ == '__main__':
    main()