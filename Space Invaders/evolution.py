from space_invaders import Game
import random

class Monkey:
    def __init__(self):
        self.DNA = []
        """Movement: [0]Shot perception height, [1]shot perception width, [2]shot weight, 
        """
        for gene in range(9):
            self.DNA.append(random.random())
        range[]

    def calc_fitness(self):
        lives = 3
        score = 0
        while lives > 0:
            lives, score = run_game(lives, score, self.DNA)
        return score


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