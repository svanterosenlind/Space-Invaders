from space_invaders import Game
import random


class Monkey:
    def __init__(self):
        self.DNA = []
        """Movement: [0]Shot perception height, [1]shot perception width, [2]shot weight, 
            [3]Barricade weight, [4]we, 
            Shooting: if [5]Invader velocity [6]lowest alien height [7]barricade distance is in [8] +- [9]"""
        self.DNA[0] = random.randint(0, 700)
        self.DNA[1] = random.randint(0, 1000)
        self.DNA[2] = random.random() * 2 - 1
        self.DNA[3] = random.random() * 2 - 1
        self.DNA[4] = random.randint(0, 700)
        self.DNA[5] = random.random() * 2 - 1
        self.DNA[6] = random.randint(0, 700)
        self.DNA[7] = random.randint(0, 700)
        self.DNA[8] = random.random() * 1000
        self.DNA[9] = random.random() * 300

    def calc_fitness(self):
        lives = 3
        score = 0
        while lives > 0:
            lives, score = run_game(lives, score, self.DNA)
        return score

    def move(self, game):
        closest_shot_height = 0
        closest_shot_x = 300
        for shot in game.shots:
            if shot.variant != 2:
                if 730 > shot.ypos > closest_shot_height and game.spaceship.ypos - shot.ypos < self.DNA[0] \
                        and abs(game.spaceship.xpos - shot.xpos) < self.DNA[1]:
                    closest_shot_height = shot.ypos
                    closest_shot_x = shot.xpos -game.spaceship.xpos
        shot_factor = self.DNA[2] * closest_shot_x

        closest_bar = 1000
        for bar in game.barricades:
            if abs(bar.xpos + bar.width/2 - game.spaceship.xpos) < closest_bar and bar is not None:
                closest_bar = bar.xpos + bar.width/2 - game.spaceship.xpos
        barricade_factor = self.DNA[3]

        steer = shot_factor + barricade_factor + self.DNA[4]
        if steer <= 0:
            return [-max(steer/1500, 1), 0]
        else:
            return [0, max(1,steer/1500)]

    def shoot(self, game):
        



def run_game(lives, score, DNA):
    invader_step = 20
    t = 0
    steps = 0
    left = False
    right = False
    space = False
    invader_dir = 1
    game = Game(lives)
    while True:
        if game.leftmost_invader() == -1:
            break
        #Set left, right and space here according to DNA
        if t % invader_step == 0:
            invader_dir = game.move_invaders(invader_dir)
            steps += 1
            if steps % 36 == 0 and invader_step > 2:
                invader_step -= 2
        game.move_spaceship(left, right)
        game.spaceship_shoot(space)
        game.invader_shoot()
        game.move_shots()
        game.detect_shot_barricade()
        game.detect_shot_invader()
        game.detect_shot_shot()
        if game.detect_shot_spaceship():
            if game.spaceship.lives == 0:
                return [score + game.score, 0]
    return [score + game.score, game.spaceship.lives]


def main():
    running = True
    score = 0
    lives = 3
    while running:
        [round_score, lives] = run_game(screen, images, font, lives, score)
        score += round_score
        if lives == 0:
            running = False
    highscores_read = open("highscores.txt")
    highscore_list = []
    added = False
    old_scores = highscores_read.readlines()
    for highscore1 in old_scores:
        highscorenum = int(highscore1.strip("\n"))
        if score > highscorenum and not added:
            highscore_list.append(score)
            added = True
        highscore_list.append(highscorenum)
    if not added:
        highscore_list.append(score)
    highscores_read.close()

    highscores_write = open("highscores.txt", "w")
    for highscore2 in highscore_list:
        highscores_write.write(str(highscore2) + "\n")
    highscores_write.close()