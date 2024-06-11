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

blocs = {'bloc1': [1,2,3,4,5,6,7,8,9,10], 'bloc2': [11,12,13,14,15,16,17,18,19,20]}

x_start_pos = 150
y_start_pos = 40

button_width = 150
button_height = 80
x_pos = x_start_pos
y_pos = y_start_pos
button_spacing = 30

nb_holds = 11*16
font = pygame.font.Font(FONT, 24)


class _text_():
    def __init__(self, font, size, text, antialias, colour, background, x, y):
        self.font = font
        self.size = size
        self.text = text
        self.antialias = antialias
        self.colour = colour
        self.background = background 
        self.x = x
        self.y = y
        texts = pygame.font.SysFont(self.font, self.size)
        self.text = texts.render(self.text, self.antialias, self.colour, self.background)
    def _textblit_(self, screen):
        screen.blit(self.text, (self.x, self.y))
        
class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
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
    if(selected_bloc == ''): return
    font = pygame.font.Font(FONT, 24)

    # Create a text surface
    text_surface = font.render(f'The bloc {selected_bloc} is active', True, WHITE)

    # Get the text rectangle
    text_rect = text_surface.get_rect()
    text_rect.center = (600,150)
    screen.blit(text_surface, text_rect)
    
    show_leds_lettres()
    
    pass

def create_buttons(button_names, x_start_pos, y_start_pos, button_width, button_height, button_spacing):
    buttons = []
    x_pos = x_start_pos
    y_pos = y_start_pos
    for i, name in enumerate(button_names):
        button = Button(name, x_pos, y_pos, button_width, button_height, WHITE, BLUE)
        buttons.append(button)
        y_pos += button_height + button_spacing
    return buttons


bloc_names = list(blocs.keys())
buttons = create_buttons(bloc_names, x_start_pos, y_start_pos, button_width, button_height, button_spacing)

left_arrow = Button("<", 20, SCREEN_HEIGHT // 2, 30, 30, WHITE, BLUE)
right_arrow = Button(">", SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2, 30, 30, WHITE, BLUE)

start_index = 0

num_buttons = len(bloc_names)
num_pages = (num_buttons - 1) // 5 + 1
current_page = 0

current_scene = 'button_list'
# current_scene = 'addbloc'

selected_bloc = ""


def set_bloc(name):
    global selected_bloc
    selected_bloc = name
    print("bloc " + name + " selected")


num_leds = 300
def show_leds_lettres(sequence_lettres):
    # pixels.fill((0, 0, 0))
    # pixels.show()
    
    pass


input_sequence = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False

# Set up the button
button_rect = pygame.Rect(100, 200, 140, 32)
button_color = pygame.Color('green')

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

input_sequence = InputBox(400, 100, 140, 32)
input_name = InputBox(100, 100, 140, 32)
button_submit = Button("Submit", 100, 200, 140, 32, WHITE, BLUE)
text_name = _text_(FONT, 24, "nom du bloc", True, WHITE, BLUE, 100, 50)
text_seqence = _text_(FONT, 24, "s?quence du bloc", True, WHITE, BLUE, 400, 50)

button_add_bloc = Button("Add Bloc", 500, 500, 140, 32, WHITE, BLUE)


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
                    set_bloc(button.text)
            
            if(button_add_bloc.button_clicked(event)):
                current_scene = 'addbloc'
                pass
            
            
        if current_scene == 'addbloc':
            input_sequence.handle_event(event)
            input_name.handle_event(event)
            if(button_submit.button_clicked(event)):
                if(input_sequence.text != ''):
                    sequence = input_sequence.text.replace(' ', '').replace('\r','').split(',')
                    name = input_name.text
                    blocs[name] = sequence
                    print(blocs)
                    input_sequence.text = ''
                    buttons = create_buttons(list(blocs.keys()), x_start_pos, y_start_pos, button_width, button_height, button_spacing)
                    screen.fill((30, 30, 30))
                    current_scene = 'button_list'
                    pass

    if current_scene == 'button_list':
        screen.fill((30, 30, 30))
        draw_button_list_scene(screen, buttons, current_page)
        draw_info_current_bloc(screen)
        show_leds()
        left_arrow.draw(screen)
        right_arrow.draw(screen)
        button_add_bloc.draw(screen)
        
    if current_scene == 'addbloc':
        screen.fill((30, 30, 30))
        input_sequence.update()
        input_sequence.draw(screen)
        input_name.update()
        input_name.draw(screen)
        text_name._textblit_(screen)
        text_seqence._textblit_(screen)
        button_submit.draw(screen)
        

    pygame.display.flip()

