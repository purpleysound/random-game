import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("game")
clock = pygame.time.Clock()


class Entity:
    def __init__(self, coordinates: tuple[int]) -> None:
        self.x_pos, self.y_pos = coordinates
        self.x_vel, self.y_vel = 0, 0
        self.min_vel, self.max_vel = -64, 64
        self.speed = 64
        
    def update_pos(self) -> None:
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
            print("not in range")
            self.x_pos -= self.x_vel * delta_time
        self.y_pos += self.y_vel * delta_time
        if 16 > self.y_pos or self.y_pos > 464:
            print("not in range")
            self.y_pos -= self.y_vel * delta_time

        self.rect.center = (self.x_pos, self.y_pos)


class Player(Entity):
    def __init__(self, coordinates: tuple[int]) -> None:
        super().__init__(coordinates)
        self.image = pygame.image.load("textures/player.png")
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update_pos(self) -> None:
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

        super().update_pos()
        

def update_screen():
    screen.fill((192, 192, 192))
    screen.blit(player.image, player.rect)
    pygame.display.update()

player = Player((64, 64))
delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player.update_pos()
    update_screen()
    delta_time = clock.tick(60)/1000

pygame.quit()
exit()
