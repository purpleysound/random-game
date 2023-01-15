import pygame
pygame.init()
MAX_X, MAX_Y = 640, 480
screen = pygame.display.set_mode((MAX_X, MAX_Y))
pygame.display.set_caption("game")
clock = pygame.time.Clock()
import math
import random

class Entity:
    def __init__(self, coordinates: tuple[int]) -> None:
        self.x_pos, self.y_pos = coordinates
        self.x_vel, self.y_vel = 0, 0
        self.min_vel, self.max_vel = -64, 64
        self.speed = 64

        self._obj_attributes = {
            "weapon": None
        }
    
    @property
    def weapon(self):
        return self._obj_attributes["weapon"]

    def set_weapon(self, weapon) -> None:
        self._obj_attributes["weapon"] = weapon

    def update(self) -> None:
        if self.x_vel > self.max_vel:
            self.x_vel = self.max_vel
        elif self.x_vel < self.min_vel:
            self.x_vel = self.min_vel

        if self.y_vel > self.max_vel:
            self.y_vel = self.max_vel
        elif self.y_vel < self.min_vel:
            self.y_vel = self.min_vel

        self.x_pos += self.x_vel * delta_time
        if 16 > self.x_pos or self.x_pos > 624:
            self.x_pos -= self.x_vel * delta_time
        self.y_pos += self.y_vel * delta_time
        if 16 > self.y_pos or self.y_pos > 464:
            self.y_pos -= self.y_vel * delta_time

        self.rect.center = (self.x_pos, self.y_pos)

        self.weapon.update()

    def death(self) -> None:
        if self in enemies:
            enemies.remove(self)
        enemies.append(Enemy((random.randint(32, 608), random.randint(32, 448))))


class Player(Entity):
    def __init__(self, coordinates: tuple[int]) -> None:
        super().__init__(coordinates)
        self.image = pygame.image.load("textures/player.png")
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.min_vel, self.max_vel = -96, 96
        self.speed = 96
        self.set_weapon(Gun(self))

    def update(self) -> None:
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.y_vel -= self.speed
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.y_vel += self.speed
        else:
            self.y_vel = 0

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x_vel -= self.speed
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x_vel += self.speed
        else:
            self.x_vel = 0

        self.weapon.rotation = math.atan2(mouse_pos[1] - self.y_pos, mouse_pos[0] - self.x_pos)
        if mouse_pressed[0]:
            self.weapon.shoot()

        super().update()

class Enemy(Entity):
    def __init__(self, coordinates: tuple[int]) -> None:
        super().__init__(coordinates)
        self.image = pygame.image.load("textures/enemy.png")
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.set_weapon(Gun(self))

    def update(self) -> None:
        self.x_vel, self.y_vel = unit_vector((player.x_pos - self.x_pos, player.y_pos - self.y_pos))
        self.x_vel *= self.speed
        self.y_vel *= self.speed
        for projectile in player.weapon.projectiles:
            if projectile.rect.colliderect(self.rect):
                player.weapon.projectiles.remove(projectile)
                self.death()

        super().update()


class Weapon:
    def __init__(self, entity: Entity) -> None:
        self.x_pos, self.y_pos = entity.x_pos, entity.y_pos
        self.rotation = 0
        self.projectile = Projectile
        self.projectiles = []
        self.max_cooldown = 0.5
        self.cooldown = 0


        self._obj_attributes = {
            "entity": entity
        }

    @property
    def entity(self) -> Entity:
        return self._obj_attributes["entity"]

    def update(self) -> None:
        self.x_pos, self.y_pos = self.entity.x_pos+10, self.entity.y_pos
        if self.cooldown > 0:
            self.cooldown -= delta_time
            if self.cooldown < 0:
                self.cooldown = 0
        self.rect.center = (self.x_pos, self.y_pos)
        for projectile in self.projectiles:
            projectile.update()

    def shoot(self) -> None:
        if self.cooldown == 0:
            self.cooldown = self.max_cooldown
            self.projectiles.append(self.projectile(self, self.rotation))


class Gun(Weapon):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.image = pygame.image.load("textures/gun.png")
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.projectile = Bullet


class Projectile:
    def __init__(self, weapon: Weapon, angle: float) -> None:
        self.x_pos, self.y_pos = weapon.x_pos+5, weapon.y_pos
        self.x_vel, self.y_vel = 0, 0
        self.speed = 128
        self.x_vel, self.y_vel = math.cos(angle) * self.speed, math.sin(angle) * self.speed

        self._obj_attributes = {
            "weapon": weapon
        }

    @property
    def weapon(self) -> Weapon:
        return self._obj_attributes["weapon"]

    def update(self):
        self.x_pos += self.x_vel * delta_time
        self.y_pos += self.y_vel * delta_time
        self.rect.center = (self.x_pos, self.y_pos)


class Bullet(Projectile):
    def __init__(self, weapon: Weapon, angle: float) -> None:
        super().__init__(weapon, angle)
        self.image = pygame.image.load("textures/bullet.png")
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

def update_screen():
    screen.fill((255, 255, 255))
    screen.blit(player.image, player.rect)
    screen.blit(player.weapon.image, player.weapon.rect)
    for projectile in player.weapon.projectiles:
        screen.blit(projectile.image, projectile.rect)
    for enemy in enemies: 
        screen.blit(enemy.image, enemy.rect)
        screen.blit(enemy.weapon.image, enemy.weapon.rect)
        for projectile in enemy.weapon.projectiles:
            screen.blit(projectile.image, projectile.rect)
    pygame.display.update()


def unit_vector(vector: tuple[float]) -> tuple[float]:
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if magnitude == 0:
        return 0, 0
    return (vector[0] / magnitude, vector[1] / magnitude)


player = Player((MAX_X//2, MAX_Y//2))
enemies = [Enemy((128, 128))]
delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    player.update()
    for enemy in enemies: enemy.update()
    update_screen()
    delta_time = clock.tick(60)/1000

pygame.quit()
exit()
