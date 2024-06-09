import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        # Draw the button
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Create a font object
        font = pygame.font.Font(None, 24)

        # Create a text surface
        text_surface = font.render(self.text, True, self.text_color)

        # Get the text rectangle
        text_rect = text_surface.get_rect()

        # Center the text on the button
        text_rect.center = (self.x + (self.width / 2), self.y + (self.height / 2))

        # Draw the text on the button
        screen.blit(text_surface, text_rect)

    def is_over(self, pos):
        # Check if the mouse is over the button
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pygame.mouse.get_pos()):
                return True  # Button was clicked
        return False  # Button was not clicked

# Create a button
button = Button("Click me!", 50, 50, 100, 50, WHITE, BLUE)

current_scene = 'menu' 


def draw_game_scene(screen):
    screen.fill((0, 128, 0))
    
def draw_menu_scene(screen):
    screen.fill((30, 30, 30))
    button.draw(screen)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == 'menu':
            # Check if the button was clicked
            if button.handle_event(event):
                current_scene = 'game'  # Switch to the game scene

    if current_scene == 'menu':
        draw_menu_scene(screen)
    elif current_scene == 'game':
        draw_game_scene(screen)
        
    # Update the new window display
    pygame.display.flip()

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Change the button color if the mouse is over it
    if button.is_over(mouse_pos):
        button.color = GREEN
    else:
        button.color = WHITE

    # Draw the button
    button.draw(screen)

    # Update the display
    pygame.display.flip()
