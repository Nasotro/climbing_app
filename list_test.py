import pygame
import sys
import random
from tkinter import messagebox


# Initialize Pygame
pygame.init()
pygame.font.init()

# Create the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 840, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FONT = "font2.ttf"

button_texts = ["Bloc 1", "Bloc 2", "Bloc 3", "Bloc 4", "Bloc 5", "Bloc 6", "Bloc 7", "Bloc 8", "Bloc 9", "Bloc 10","11","12","13","14","15","16","17","18","19","20"]

x_start_pos = 150
y_start_pos = 40

button_width = 150
button_height = 80
x_pos = x_start_pos
y_pos = y_start_pos
button_spacing = 30

nb_holds = 11*16

class Button:
    def __init__(self, text, x, y, width, height, color, text_color, index):
        self.index = index
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color

    def draw(self, screen, x = None, y = None):
        
        if x is not None: self.x = x
        if y is not None: self.y = y
            
        # Draw the button
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Create a font object
        font = pygame.font.Font(FONT, 24)

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
    
    def button_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print("test button" + str(self.index))
            if self.is_over(pygame.mouse.get_pos()):
                # messagebox.showinfo('button clicked', f'you clicked on button {self.index}')
                return True  # Button was clicked
        return False  # Button was not clicked

def draw_button_list_scene(screen, buttons, page, nb_buttons = 6):
    screen.fill((30, 30, 30))

    button_spacing = 10
    y_pos = 50

    start_index = page * nb_buttons
    end_index = min(start_index + nb_buttons, len(buttons))

    for i in range(start_index, end_index):
        buttons[i].draw(screen, y= y_start_pos + (button_height + button_spacing)*(i-start_index))
        # print(i,y_pos)
        y_pos += buttons[i].height + button_spacing
        
def handle_left_arrow_click(page):
    if page > 0:
        page -= 1
    return page

def handle_right_arrow_click(page, num_pages):
    if page < num_pages - 1:
        page += 1
    return page

def draw_info_current_bloc(screen):
    if(selected_bloc == -1): return
    font = pygame.font.Font(FONT, 24)

    # Create a text surface
    text_surface = font.render(f'The bloc {button_texts[selected_bloc]} is active', True, WHITE)

    # Get the text rectangle
    text_rect = text_surface.get_rect()
    text_rect.center = (600,150)
    screen.blit(text_surface, text_rect)
    pass

def create_buttons(button_texts, x_start_pos, y_start_pos, button_width, button_height, button_spacing):
    buttons = []
    x_pos = x_start_pos
    y_pos = y_start_pos
    for i, text in enumerate(button_texts):
        button = Button(text, x_pos, y_pos, button_width, button_height, WHITE, BLUE, i)
        buttons.append(button)
        y_pos += button_height + button_spacing
    return buttons

buttons = create_buttons(button_texts, x_start_pos, y_start_pos, button_width, button_height, button_spacing)

left_arrow = Button("<", 20, SCREEN_HEIGHT // 2, 30, 30, WHITE, BLUE, -1)
right_arrow = Button(">", SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2, 30, 30, WHITE, BLUE, -1)

start_index = 0

num_buttons = len(button_texts)
num_pages = (num_buttons - 1) // 5 + 1
current_page = 0

current_scene = 'button_list'
selected_bloc = -1



def set_random_blocs(n):
    bloc_holds = []
    for i in range(n):
        bloc_holds.append([random.randint(0, nb_holds) for _ in range(random.randint(7, 15))])
    return bloc_holds

bloc_holds = set_random_blocs(len(buttons))
selected_bloc_holds = []



def set_bloc(i):
    global selected_bloc, selected_bloc_holds
    selected_bloc = i
    selected_bloc_holds = bloc_holds[i]
    print("bloc " + str(i) + " selected")
    
import neopixel
import board

pin = board.D18
num_leds = 300
pixels = neopixel.NeoPixel(pin, num_leds, brightness=0.2, auto_write=False)

class AllLeds:
    def __init__(self, num_leds):
        self.num_leds = num_leds
        self.leds = [0] * num_leds

    def set_led(self, i, color):
        self.leds[i] = color

    def set_bloc(self, bloc_holds = None, color=(0, 255, 0)):
        if(bloc_holds is None):
            bloc_holds = list(range(self.num_leds))
        for hold in bloc_holds:
            for i in hold:
                self.leds[i] = color

    def show(self):
        for i, color in enumerate(self.leds):
            pixels[i] = color
        pixels.show()
    

LEDs = AllLeds(num_leds)

def show_leds():
    global selected_bloc_holds, LEDs
    LEDs.set_bloc(selected_bloc_holds)





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == 'button_list':
            # Check if the left arrow button was clicked
            if left_arrow.button_clicked(event):
                current_page = handle_left_arrow_click(current_page)

            # Check if the right arrow button was clicked
            if right_arrow.button_clicked(event):
                current_page = handle_right_arrow_click(current_page, num_pages)
                
            for button in buttons:
                if button.button_clicked(event):
                    set_bloc(button.index)
                    pass

    if current_scene == 'button_list':
        draw_button_list_scene(screen, buttons, current_page)
        draw_info_current_bloc(screen)
        show_leds()
        left_arrow.draw(screen)
        right_arrow.draw(screen)


    pygame.display.flip()

