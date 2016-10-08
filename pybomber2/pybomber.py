#!usr/bin/python3

import pygame
from entities import Player, Monster
from board import Board
import os.path

def main():
    pygame.init()

    clock = pygame.time.Clock()

    current_map = 1

    board = Board()
    board.read_map("maps/" + str(current_map) + ".map")
    board.add_entities()

    gray = (109, 67, 56)

    game_display = pygame.display.set_mode(
        (board.width, board.height),
        pygame.HWSURFACE | pygame.DOUBLEBUF)

    pygame.display.set_caption("PyBomber")

    crashed = False

    pygame.mixer.music.load('music/background.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    score = 0

    level_finished = False

    while not crashed:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                crashed = True

        game_display.fill(gray)
        for entity in board.entities:
            entity.next_step(events, board)
        for entity in board.entities[::-1]:
            entity.update(board)
            if isinstance(entity, Player):
                if entity.is_dead:
                    score = 0
                    level_finished = True
                    break
                elif entity.is_win:
                    level_finished = True
                    score += 500
                    break
            elif isinstance(entity, Monster):
                if entity.is_dead:
                    score += 100
            game_display.blit(entity.img, (entity.x, entity.y))
        if level_finished:
            board = Board()
            if score == 0 or not os.path.isfile("maps/" + str(current_map + 1) + ".map"):
                current_map = 1
                game_display.fill(gray)
                font = pygame.font.SysFont("Typewriter.ttf", 40)
                level_text = font.render(
                    "GAME OVER. Your score is: %s" % score, 1, (255, 255, 255))
                game_display.blit(
                    level_text, (5, 5))
                pygame.display.update()
                pygame.time.delay(5000)
                crashed = True
            else:
                current_map += 1
                game_display.fill(gray)
                font = pygame.font.SysFont("Typewriter.ttf", 40)
                level_text = font.render(
                    "Level: %s" % current_map, 1, (255, 255, 255))
                game_display.blit(
                    level_text, (5, 5))
                pygame.display.update()
                clock.tick_busy_loop(1)
            try:
                board.read_map("maps/" + str(current_map) + ".map")
            except Exception:
                pass
            game_display = pygame.display.set_mode(
                (board.width, board.height),
                pygame.HWSURFACE | pygame.DOUBLEBUF)
            board.add_entities()
            level_finished = False
        font = pygame.font.SysFont("Typewriter.ttf", 30)
        score_text = font.render("Score: %s" % score, 1, (255, 255, 255))
        game_display.blit(score_text, (5, 5))
        pygame.display.update()
        clock.tick_busy_loop(60)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
