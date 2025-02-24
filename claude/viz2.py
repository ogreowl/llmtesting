import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.Surface((screen_width, screen_height))
background.fill((0, 0, 30))  # Dark blue background

# Create stars for the background
for i in range(100):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    radius = random.randint(1, 2)
    brightness = random.randint(100, 255)
    pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), radius)

# Title and Icon
pygame.display.set_caption("Space Shooter")

# Player
class Player:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 20
        self.speed = 5
        self.color = (0, 255, 0)  # Green
        self.shoot_cooldown = 0
        self.health = 100
        self.score = 0

    def draw(self):
        # Draw ship body
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y),  # Top
            (self.x, self.y + self.height),  # Bottom left
            (self.x + self.width, self.y + self.height)  # Bottom right
        ])
        
        # Draw cockpit
        pygame.draw.circle(screen, (100, 100, 255), 
                          (self.x + self.width // 2, self.y + self.height // 2), 10)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Boundary check
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullets.append(Bullet(self.x + self.width // 2, self.y))
            self.shoot_cooldown = 15
        
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

# Enemy
class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(50, 200)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2)
        self.speed_y = random.uniform(0.2, 0.5)
        self.color = (255, 0, 0)  # Red
        self.health = 30
        self.shoot_timer = random.randint(30, 120)
    
    def draw(self):
        # Draw enemy ship
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y + self.height),  # Bottom
            (self.x, self.y),  # Top left
            (self.x + self.width, self.y)  # Top right
        ])
        
        # Draw alien eyes
        eye_radius = 5
        eye_distance = 15
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x + self.width // 2 - eye_distance), int(self.y + 20)), eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x + self.width // 2 + eye_distance), int(self.y + 20)), eye_radius)
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Boundary check for left and right
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.speed_x *= -1
        
        # If enemy reaches bottom, reset position
        if self.y > screen_height:
            self.reset()
    
    def shoot(self):
        if self.shoot_timer <= 0:
            enemy_bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height))
            self.shoot_timer = random.randint(60, 180)
        else:
            self.shoot_timer -= 1
    
    def reset(self):
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(-100, -50)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2)
        self.speed_y = random.uniform(0.2, 0.5)

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 7
        self.color = (0, 255, 255)  # Cyan
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Add glow effect
        pygame.draw.circle(screen, (100, 200, 255), (int(self.x), int(self.y)), self.radius + 2, 1)
    
    def move(self):
        self.y -= self.speed
    
    def is_off_screen(self):
        return self.y < 0
    
    def collides_with(self, enemy):
        distance = math.sqrt((self.x - enemy.x - enemy.width // 2) ** 2 + 
                            (self.y - enemy.y - enemy.height // 2) ** 2)
        return distance < self.radius + enemy.width // 2

# Enemy Bullet
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 4
        self.speed = 5
        self.color = (255, 100, 0)  # Orange
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > screen_height
    
    def collides_with(self, player):
        # Check if bullet collides with player's ship
        if (self.x > player.x and self.x < player.x + player.width and
            self.y > player.y and self.y < player.y + player.height):
            return True
        return False

# Explosion
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.growth_rate = 2
        self.fade_speed = 10
        self.color = (255, 200, 0)  # Yellow-orange
        self.alpha = 255
    
    def draw(self):
        # Create a surface for the explosion with transparency
        explosion_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(explosion_surface, (*self.color, self.alpha), 
                          (self.radius, self.radius), self.radius)
        screen.blit(explosion_surface, (self.x - self.radius, self.y - self.radius))
    
    def update(self):
        self.radius += self.growth_rate
        self.alpha -= self.fade_speed
        return self.alpha <= 0

# Power-up
class PowerUp:
    def __init__(self):
        self.width = 25
        self.height = 25
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height
        self.speed = 2
        self.type = random.choice(["health", "speed", "weapon"])
        if self.type == "health":
            self.color = (0, 255, 0)  # Green
        elif self.type == "speed":
            self.color = (0, 255, 255)  # Cyan
        else:
            self.color = (255, 255, 0)  # Yellow
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw an icon based on power-up type
        if self.type == "health":
            # Draw plus sign
            pygame.draw.line(screen, (255, 255, 255), 
                            (self.x + self.width // 2, self.y + 5), 
                            (self.x + self.width // 2, self.y + self.height - 5), 3)
            pygame.draw.line(screen, (255, 255, 255), 
                            (self.x + 5, self.y + self.height // 2), 
                            (self.x + self.width - 5, self.y + self.height // 2), 3)
        elif self.type == "speed":
            # Draw arrow
            pygame.draw.polygon(screen, (255, 255, 255), [
                (self.x + self.width // 2, self.y + 5),
                (self.x + 5, self.y + self.height - 5),
                (self.x + self.width - 5, self.y + self.height - 5)
            ])
        else:
            # Draw star
            pygame.draw.circle(screen, (255, 255, 255), 
                              (self.x + self.width // 2, self.y + self.height // 2), 5)
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > screen_height
    
    def collides_with(self, player):
        if (self.x < player.x + player.width and self.x + self.width > player.x and
            self.y < player.y + player.height and self.y + self.height > player.y):
            return True
        return False

# Create player
player = Player()

# Lists to store entities
enemies = []
bullets = []
enemy_bullets = []
explosions = []
power_ups = []

# Create initial enemies
for _ in range(5):
    enemies.append(Enemy())

# Game variables
game_over = False
enemy_spawn_timer = 0
power_up_spawn_timer = 0
score = 0
level = 1
font = pygame.font.SysFont(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()
FPS = 60

while running:
    # Fill the screen with background
    screen.blit(background, (0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
    
    if not game_over:
        # Player controls
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        player.move(dx, dy)
        player.update()
        
        # Update bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if bullet.collides_with(enemy):
                        enemy.health -= 10
                        explosions.append(Explosion(bullet.x, bullet.y))
                        if enemy.health <= 0:
                            score += 100
                            explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                            enemies.remove(enemy)
                            if random.random() < 0.2:  # 20% chance to drop power-up
                                power_up = PowerUp()
                                power_up.x = enemy.x
                                power_up.y = enemy.y
                                power_ups.append(power_up)
                        if bullet in bullets:
                            bullets.remove(bullet)
        
        # Update enemy bullets
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.is_off_screen():
                enemy_bullets.remove(enemy_bullet)
            elif enemy_bullet.collides_with(player):
                player.health -= 10
                explosions.append(Explosion(enemy_bullet.x, enemy_bullet.y))
                enemy_bullets.remove(enemy_bullet)
                if player.health <= 0:
                    game_over = True
        
        # Update enemies
        for enemy in enemies:
            enemy.move()
            enemy.shoot()
        
        # Update explosions
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
        
        # Update power-ups
        for power_up in power_ups[:]:
            power_up.move()
            if power_up.is_off_screen():
                power_ups.remove(power_up)
            elif power_up.collides_with(player):
                if power_up.type == "health":
                    player.health = min(100, player.health + 25)
                elif power_up.type == "speed":
                    player.speed += 1
                else:  # weapon upgrade
                    # Here you could implement different weapon types
                    pass
                power_ups.remove(power_up)
        
        # Spawn new enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 180 and len(enemies) < 5 + level:  # Spawn every 3 seconds
            enemies.append(Enemy())
            enemy_spawn_timer = 0
        
        # Spawn power-ups
        power_up_spawn_timer += 1
        if power_up_spawn_timer >= 600:  # Spawn every 10 seconds
            power_ups.append(PowerUp())
            power_up_spawn_timer = 0
        
        # Level progression
        if score >= level * 1000:
            level += 1
    
    # Draw everything
    # Draw player
    if not game_over:
        player.draw()
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw()
    
    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw()
    
    # Draw explosions
    for explosion in explosions:
        explosion.draw()
    
    # Draw power-ups
    for power_up in power_ups:
        power_up.draw()
    
    # Draw HUD (Heads-Up Display)
    # Health bar
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    pygame.draw.rect(screen, (255, 0, 0), (150, 15, 200, 20))  # Red background
    pygame.draw.rect(screen, (0, 255, 0), (150, 15, player.health * 2, 20))  # Green health
    
    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width - 200, 10))
    
    # Level
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (screen_width - 200, 50))
    
    # Game over message
    if game_over:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 180, screen_height // 2 - 36))
        
        restart_font = pygame.font.SysFont(None, 36)
        restart_text = restart_font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width // 2 - 120, screen_height // 2 + 50))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            game_over = False
            player = Player()
            enemies = []
            bullets = []
            enemy_bullets = []
            explosions = []
            power_ups = []
            for _ in range(5):
                enemies.append(Enemy())
            enemy_spawn_timer = 0
            power_up_spawn_timer = 0
            score = 0
            level = 1
    
    # Update display
    pygame.display.update()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()