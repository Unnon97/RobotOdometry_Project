import pygame
import time

# Set up display
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
ROBOT_COLOR = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Gesture Simulation")

# Robot class
class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50

    def draw(self, screen):
        pygame.draw.circle(screen, ROBOT_COLOR, (self.x, self.y), self.size)

    def wave(self):
        self.x += 20 if self.x < WIDTH - self.size else -20

    def nod(self):
        self.y += 20 if self.y < HEIGHT - self.size else -20

def main():
    robot = Robot(WIDTH // 2, HEIGHT // 2)
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        robot.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate the robot's actions
        robot.wave()
        time.sleep(0.5)
        robot.nod()
        time.sleep(0.5)

    pygame.quit()

if __name__ == "__main__":
    main()
