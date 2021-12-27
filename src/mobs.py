import pygame
import math


class Mob:
    def __init__(self, pos, width, height, life, sprite_dict, initial_state):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.life = life
        self.sprite_dict = sprite_dict
        self.state = initial_state
        self.vel = pygame.Vector2(0)

    def draw(self, surface: pygame.Surface):
        surface.blit(next(self.sprite_dict(self.state)), self.pos)

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        # todo: check collisions in X axis

        self.pos.y += self.vel.y * dt
        # todo: check collision in Y axis

        """
        if not ground_under_its_feet:
        vel.y += some_gravity_value
        """

    def hurt(self, damage):
        self.life -= damage
        if self.life < 0:
            self.life = 0

    def kill(self):
        self.life = 0

    def change_state(self, new_state):
        self.state = new_state

    @property
    def alife(self):
        return bool(self.life)

    @property
    def pos(self):
        return pygame.Vector2(self.rect.topleft)

    @pos.setter
    def pos(self, value):
        self.rect.topleft = value

    @property
    def is_falling(self):
        return self.vel.y < 0

    @property
    def is_on_ground(self):
        return self.vel.y == 0


class Monster(Mob):
    def __init__(self, pos, width, height, life, sprite_dict, initial_state):
        super().__init__(pos, width, height, life, sprite_dict, initial_state)


class Player(Mob):
    JUMP_LIMIT = 2
    JUMP_STRENGHT = 10
    X_VEL_ACCELERATION = 1
    X_VEL_LIMIT = 20

    def __init__(self, pos, width, height, life, sprite_dict, initial_state):
        super().__init__(pos, width, height, life, sprite_dict, initial_state)
        self.jump_count = 0

    def jump(self):
        if self.jump_count >= self.JUMP_LIMIT:
            return
        self.vel.y += self.JUMP_STRENGHT
        self.jump_count += 1

    def move_right(self):
        if self.vel.x < 0:  # if it is moving left
            self.vel.x /= 2
            self.vel.x += self.X_VEL_ACCELERATION
        else:
            self.vel.x += self.X_VEL_ACCELERATION * abs(1 - self.vel.x / self.X_VEL_LIMIT)

    def move_left(self):
        if self.vel.x > 0:  # if it is moving left
            self.vel.x /= 2
            self.vel.x -= self.X_VEL_ACCELERATION
        else:
            self.vel.x -= self.X_VEL_ACCELERATION * abs(1 - self.vel.x / self.X_VEL_LIMIT)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                self.jump()

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        # todo: check collisions in X axis

        self.pos.y += self.vel.y * dt
        # todo: check collision in Y axis

        """
        if not ground_under_its_feet:
        vel.y += some_gravity_value
        """