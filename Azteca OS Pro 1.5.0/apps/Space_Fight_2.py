import pygame
import random
import os

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ALIEN_COLOR = (0, 255, 0)  # Green color for aliens

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plane Shooter Game")

# Load player image
plane_image = pygame.image.load("Space_Fight_2_A/player_plane.png")  # Replace with your player image file
plane_image = pygame.transform.scale(plane_image, (100, 100))  # Scale to appropriate size

# Bullet images
bullet_image = pygame.Surface((5, 10))  # Bullet can still be a colored surface
bullet_image.fill(WHITE)

alien_bullet_image = pygame.Surface((5, 10))  # Alien bullet can still be a colored surface
alien_bullet_image.fill((255, 0, 0))  # Red color for alien bullets

# High score file
high_score_file = "high_score.txt"

# Load high score
def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read())
    return 0  # Return 0 if the file does not exist

# Save high score
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Reset high score
def reset_high_score():
    save_high_score(0)

# Load sound effects
kill_sound = pygame.mixer.Sound('Space_Fight_2_A/kill_sound.wav')  # Your specified sound file
level_up_sound = pygame.mixer.Sound('Space_Fight_2_A/level_up_sound.wav')  # Your specified sound file
death_sound = pygame.mixer.Sound('Space_Fight_2_A/death_sound.wav')  # Your specified sound file

# Load background music
pygame.mixer.music.load("Space_Fight_2_A/background_music.mp3")  # Replace with your background music file
pygame.mixer.music.set_volume(0.5)  # Set volume for background music (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely


# Classes for game objects
class Plane:
    def __init__(self):
        self.image = plane_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Alien:
    def __init__(self, x, y):
        self.position = [x, y]  # Store position as a list for easy modification
        self.speed = 1  # Speed of alien movement
        self.direction = 1  # 1 for moving right, -1 for moving left
        self.shoot_timer = random.randint(30, 60)  # Random timer for shooting

    def move(self):
        # Move the alien horizontally and change direction at edges
        self.position[0] += self.speed * self.direction
        if self.position[0] >= SCREEN_WIDTH - 20 or self.position[0] <= 20:
            self.direction *= -1  # Reverse direction when reaching screen edges
            self.position[1] += 20  # Drop down slightly when direction reverses

    def draw(self, surface):
        pygame.draw.circle(surface, ALIEN_COLOR, self.position, 20)  # Draw a green circle for the alien

    def shoot(self):
        # Create an alien bullet at the alien's position
        return AlienBullet(self.position[0], self.position[1] + 20)  # Slightly below the alien

class AlienBullet:
    def __init__(self, x, y):
        self.image = alien_bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Display the loading screen
def show_loading_screen():
    font = pygame.font.Font(None, 74)
    title_text = font.render("Space Fight", True, WHITE)
    copyright_text = pygame.font.Font(None, 36).render("© Azteca", True, WHITE)

    start_ticks = pygame.time.get_ticks()  # Get the starting time
    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(copyright_text, (SCREEN_WIDTH // 2 - copyright_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()

        # Check for the time elapsed
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate elapsed seconds
        if seconds >= 5:  # Show the loading screen for 5 seconds
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Display the menu
def show_menu(high_score):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Plane Shooter", True, WHITE)
    play_text = pygame.font.Font(None, 36).render("Press Enter to Play", True, WHITE)
    reset_text = pygame.font.Font(None, 36).render("Press R to Reset High Score", True, WHITE)
    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(reset_text, (SCREEN_WIDTH // 2 - reset_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    return
                if event.key == pygame.K_r:  # Reset high score
                    reset_high_score()
                    high_score = load_high_score()  # Reload high score after reset

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    plane = Plane()
    bullets = []
    alien_bullets = []
    score = 0
    level = 1
    high_score = load_high_score()  # Load high score at the start of the game

    # Function to spawn aliens
    def spawn_aliens(level):
        return [Alien(x * 100 + 50, y * 50 + 50) for y in range(3) for x in range(8)]  # Position aliens in a grid

    # Spawn initial aliens
    aliens = spawn_aliens(level)

    # Initialize joystick (if available)
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            plane.move(-plane.speed)
        if keys[pygame.K_d]:  # Move right
            plane.move(plane.speed)
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # Limit number of bullets on screen
                bullets.append(Bullet(plane.rect.centerx, plane.rect.top))

        # Joystick movement (if available)
        if joystick:
            axis_x = joystick.get_axis(0)  # Horizontal axis of the joystick
            if axis_x < -0.5:
                plane.move(-plane.speed)  # Move left
            elif axis_x > 0.5:
                plane.move(plane.speed)  # Move right

            # Joystick shooting
            if joystick.get_button(0):  # Button 0 is typically the fire button
                if len(bullets) < 5:
                    bullets.append(Bullet(plane.rect.centerx, plane.rect.top))

        # Move aliens and bullets
        for alien in aliens:
            alien.move()

        for alien_bullet in alien_bullets:
            alien_bullet.move()
            if alien_bullet.rect.y > SCREEN_HEIGHT:
                alien_bullets.remove(alien_bullet)
            # Check for collision between alien bullets and plane
            if pygame.sprite.collide_mask(plane, alien_bullet):
                death_sound.play()  # Play death sound effect
                running = False  # End the game if plane collides with an alien bullet

        # Move bullets and check for collisions
        for bullet in bullets:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
            for alien in aliens:
                alien_rect = pygame.Rect(alien.position[0] - 20, alien.position[1] - 20, 40, 40)  # Create a rect for the alien
                if bullet.rect.colliderect(alien_rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1
                    kill_sound.play()  # Play kill sound effect
                    break

        # Check if all aliens are defeated
        if not aliens:
            level += 1
            level_up_sound.play()  # Play level-up sound effect
            aliens = spawn_aliens(level)  # Spawn new aliens for the next level
            print(f"Level up! Now at level {level}")

        # Randomly allow aliens to shoot
        if random.randint(1, 100) <= 3:  # 3% chance for each alien to shoot
            alien = random.choice(aliens)
            alien_bullets.append(alien.shoot())

        # Clear the screen
        screen.fill(BLACK)

        # Draw objects
        plane.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for alien_bullet in alien_bullets:
            alien_bullet.draw(screen)
        for alien in aliens:
            alien.draw(screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw level
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Game Over screen
    if score > high_score:
        high_score = score
        save_high_score(high_score)  # Update high score if player got a new high score

    return high_score  # Return the final score

# Main program
show_loading_screen()  # Display loading screen before the menu
show_menu(load_high_score())  # Display the menu after loading screen
game_loop()  # Start the game loop
pygame.quit()  # Quit Pygame when game is over