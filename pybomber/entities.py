#!usr/bin/python3

import pygame
import constants
import random

class Entity(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
    def next_step(self):
        pass
    def update(self, board):
        pass
    def is_collision(self, entity):
        return (abs(self.x - entity.x) < self.width) and \
        (abs(self.y - entity.y) < self.height)

class Player(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.bomb_amount = 5
        self.put_bomb = False
        self.img = pygame.image.load("icons/bomberman.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (int(self.width), int(self.height)))
        self.is_dead = False
        self.is_win = False
    def next_step(self, events, board):
        self.put_bomb = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_speed += -self.speed
                if event.key == pygame.K_RIGHT:
                    self.x_speed += self.speed
                if event.key == pygame.K_UP:
                    self.y_speed += -self.speed
                if event.key == pygame.K_DOWN:
                    self.y_speed += self.speed
                if event.key == pygame.K_SPACE:
                    self.put_bomb = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and abs(self.x_speed) > 0:
                    self.x_speed -= -self.speed
                if event.key == pygame.K_RIGHT and abs(self.x_speed) > 0:
                    self.x_speed -= self.speed
                if event.key == pygame.K_UP and abs(self.y_speed) > 0:
                    self.y_speed -= -self.speed
                if event.key == pygame.K_DOWN and abs(self.y_speed) > 0:
                    self.y_speed -= self.speed

        self.x += self.x_speed
        self.y += self.y_speed

    def update(self, board):
        if self.x < 0:
            self.x = 0
        if self.x > board.width - self.width:
            self.x = board.width - self.width
        if self.y < 0:
            self.y = 0
        if self.y > board.height - self.height:
            self.y = board.height - self.height

        for entity in board.entities:
            if super(Player, self).is_collision(entity) and \
            entity != self:
                if (isinstance(entity, Explosion) \
                or isinstance(entity, Monster)) \
                and self in board.entities:
                    self.is_dead = True
                if isinstance(entity, Bomb) and not entity.tangible:
                    continue
                if isinstance(entity, Exit):
                    self.is_win = True
                if abs(self.x - entity.x) >= abs(self.y - entity.y):
                    if self.x < entity.x:
                        self.x = entity.x - self.width
                    elif self.x > entity.x:
                        self.x = entity.x + self.width
                if abs(self.x - entity.x) <= abs(self.y - entity.y):
                    if self.y < entity.y:
                        self.y = entity.y - self.height
                    elif self.y > entity.y:
                        self.y = entity.y + self.height

        if self.put_bomb and self.bomb_amount > 0:
            x = self.x
            y = self.y
            if self.x % constants.SPRITE_W < constants.SPRITE_W / 2:
                x = self.x - self.x % constants.SPRITE_W
            else:
                x = self.x + constants.SPRITE_W - self.x % constants.SPRITE_W
            if self.y % constants.SPRITE_H < constants.SPRITE_H / 2:
                y = self.y - self.y % constants.SPRITE_H
            else:
                y = self.y + constants.SPRITE_H - self.y % constants.SPRITE_H
            board.entities.append(Bomb(x, y, self))
            self.bomb_amount -= 1


class Block(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/block.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (self.width, self.height))
    def next_step(self, events, board):
        pass
    def update(self, board):
        for entity in board.entities:
            if super(Block, self).is_collision(entity) and \
            entity != self and isinstance(entity, Explosion):
                board.entities.remove(self)
                break

class Wall(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/wall.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (self.width, self.height))
    def next_step(self, events, board):
        pass
    def update(self, board):
        pass

class Bomb(Entity):
    def __init__(self, x=0, y=0, bomber=None):
        super().__init__(x, y)
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/bomb.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (self.width, self.height))
        self.counter = 200
        self.bomber = bomber
        self.length = 2
        self.tangible = False
    def next_step(self, events, board):
        self.counter -= 1
    def update(self, board):
        is_player_above = False
        for entity in board.entities:
            if super(Bomb, self).is_collision(entity) and \
            entity != self:
                if isinstance(entity, Explosion):
                    self.counter = 0
                if isinstance(entity, Player) and not self.tangible:
                    is_player_above = True
        if not is_player_above:
            self.tangible = True
        if self.counter == 0:
            board.entities.remove(self)
            b_sound = pygame.mixer.Sound('sfx/bomb.wav')
            b_sound.play()
            self.place_explosion(board)
            self.bomber.bomb_amount += 1
    def place_explosion(self, board):
        board.entities.append(Explosion(self.x, self.y))
        for x in range(-self.length, 0)[::-1]:
            explosion = Explosion(
                self.x + x * self.width,
                self.y)

            board.entities.append(explosion)

            collision = False
            for entity in board.entities:
                if (isinstance(entity, Wall) or isinstance(entity, Block)) \
                and explosion.is_collision(entity):
                    collision = True
                    break
            if collision:
                break
        for x in range(1, self.length + 1):
            explosion = Explosion(
                self.x + x * self.width,
                self.y)

            board.entities.append(explosion)

            collision = False
            for entity in board.entities:
                if (isinstance(entity, Wall) or isinstance(entity, Block)) \
                and explosion.is_collision(entity):
                    collision = True
                    break
            if collision:
                break
        for y in range(-self.length, 0)[::-1]:
            explosion = Explosion(
                self.x,
                self.y + y * self.height)

            board.entities.append(explosion)

            collision = False
            for entity in board.entities:
                if (isinstance(entity, Wall) or isinstance(entity, Block)) \
                and explosion.is_collision(entity):
                    collision = True
                    break
            if collision:
                break
        for y in range(1, self.length + 1):
            explosion = Explosion(
                self.x,
                self.y + y * self.height)

            board.entities.append(explosion)

            collision = False
            for entity in board.entities:
                if (isinstance(entity, Wall) or isinstance(entity, Block)) \
                and explosion.is_collision(entity):
                    collision = True
                    break
            if collision:
                break

class Explosion(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/explosion.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (self.width, self.height))
        self.isimplodes = False
        self.counter = 20
    def next_step(self, events, board):
        self.counter -= 1
    def update(self, board):
        if self.counter == 0:
            board.entities.remove(self)

class Monster(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.x_speed = 0
        self.y_speed = 0
        self.direction = random.randint(0, 3)
        self.speed = 2
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/monster.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (int(self.width), int(self.height)))
        self.is_dead = False
        self.step_counter = 0
    def next_step(self, events, board):
        if self.step_counter > constants.SPRITE_W / self.speed:
            self.direction = random.randint(0, 3)
            self.step_counter = 0
        if self.direction == constants.LEFT:
            self.x_speed = -self.speed
            self.y_speed = 0
        if self.direction == constants.RIGHT:
            self.x_speed = self.speed
            self.y_speed = 0
        if self.direction == constants.DOWN:
            self.x_speed = 0
            self.y_speed = -self.speed
        if self.direction == constants.UP:
            self.x_speed = 0
            self.y_speed = self.speed

        # for entity in board.entities:
        #     if isinstance(entity, Player):
        #         mon_ind = constants.screen_to_matrix(self.x, self.y)
        #         play_ind = constants.screen_to_matrix(entity.x, entity.y)
        #         if mon_ind[0] == play_ind[0]:
        #             visible = True
        #             min_ind = min(mon_ind[1], play_ind[1])
        #             max_ind = max(mon_ind[1], play_ind[1])
        #             for index in range(min_ind, max_ind):

        #                 if board.matrix[mon_ind[0]][index] == 1 or \
        #                 board.matrix[mon_ind[0]][index] == 2:
        #                     visible = False
        #                     break

        #             if visible:
        #                 if play_ind[1] - mon_ind[1] > 0:
        #                     self.direction = constants.UP
        #                 else:
        #                     self.direction = constants.DOWN
        #                 self.x = constants.matrix_to_screen(play_ind[0], play_ind[1])[0]
        #                 self.step_counter = 0

        #         elif mon_ind[1] == play_ind[1]:
        #             visible = True
        #             min_ind = min(mon_ind[0], play_ind[0])
        #             max_ind = max(mon_ind[0], play_ind[0])
        #             for index in range(mon_ind[0], play_ind[0]):

        #                 if board.matrix[index][mon_ind[1]] == 1 or \
        #                 board.matrix[index][mon_ind[1]] == 2:
        #                     visible = False
        #                     break

        #             if visible:
        #                 if play_ind[0] - mon_ind[0] > 0:
        #                     self.direction = constants.RIGHT
        #                 else:
        #                     self.direction = constants.LEFT
        #                 self.y = constants.matrix_to_screen(play_ind[0], play_ind[1])[1]
        #                 self.step_counter = 0

        self.x += self.x_speed
        self.y += self.y_speed

        self.step_counter += 1

    def update(self, board):
        if self.x < 0:
            self.x = 0
        if self.x > board.width - self.width:
            self.x = board.width - self.width
        if self.y < 0:
            self.y = 0
        if self.y > board.height - self.height:
            self.y = board.height - self.height

        for entity in board.entities:
            if super(Monster, self).is_collision(entity) and \
            entity != self:
                if isinstance(entity, Explosion) and  self in board.entities:
                    self.is_dead = True
                    board.entities.remove(self)
                if isinstance(entity, Bomb) and not entity.tangible or \
                    isinstance(entity, Exit) or isinstance(entity, Player):
                    continue
                if abs(self.x - entity.x) >= abs(self.y - entity.y):
                    if self.x < entity.x:
                        self.x = entity.x - self.width
                    elif self.x > entity.x:
                        self.x = entity.x + self.width
                if abs(self.x - entity.x) <= abs(self.y - entity.y):
                    if self.y < entity.y:
                        self.y = entity.y - self.height
                    elif self.y > entity.y:
                        self.y = entity.y + self.height


class Exit(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.width = constants.SPRITE_W
        self.height = constants.SPRITE_H
        self.img = pygame.image.load("icons/exit.png")
        self.img = pygame.transform.smoothscale(
            self.img,
            (self.width, self.height))
    def next_step(self, events, board):
        pass
    def update(self, board):
        pass
