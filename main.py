import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("game")
clock = pygame.time.Clock()
import math

class Entity:
    def __init__(self, coordinates: tuple[int]) -> None:
        self.x_pos, self.y_pos = coordinates
        self.x_vel, self.y_vel = 0, 0
        self.min_vel, self.max_vel = -64, 64
        self.speed = 64

        self._obj_attributes = {
            "weapon": None
        }

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

    @property
    def weapon(self):
        return self._obj_attributes["weapon"]

    def set_weapon(self, weapon) -> None:
        self._obj_attributes["weapon"] = weapon


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
        self.x_pos, self.y_pos = weapon.x_pos, weapon.y_pos
        self.x_vel, self.y_vel = 0, 0
        self.speed = 128
        self.x_vel, self.y_vel = math.cos(angle) * self.speed, math.sin(angle) * self.speed

        self._obj_attributes = {
            "weapon": weapon
        }

    def update(self):
        self.x_pos += self.x_vel * delta_time
        self.y_pos += self.y_vel * delta_time
        self.rect.center = (self.x_pos, self.y_pos)

    @property
    def weapon(self) -> Weapon:
        return self._obj_attributes["weapon"]


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
    pygame.display.update()


player = Player((64, 64))
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
    update_screen()
    delta_time = clock.tick(60)/1000

pygame.quit()
exit()
