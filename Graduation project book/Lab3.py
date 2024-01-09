import pygame
import sys
import Labnomenu as CF
from time import sleep
pygame.init()   # Initialize Pygame


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crowd-Funding app")


# Load background image
background_image = pygame.image.load(r'C:\Users\hp\Desktop\pythonLabs\background.jpg')
background_image = pygame.transform.scale(background_image, (width, height))

background_image2 = pygame.image.load(r'C:\Users\hp\Desktop\pythonLabs\images.png')
background_image2 = pygame.transform.scale(background_image2, (width, height))


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
current_screen = "menu"  # Initial screen

# Fonts
font = pygame.font.Font(None, 36)

all_screens={0:'menu',1:'reg',2:'login',3:'Create Project'}

# Function to draw buttons
def draw_button(text, rect, active):
    color = gray if not active else white
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, black, rect, 2)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_menu_screen():
    screen.blit(background_image, (0, 0))
        # Draw buttons
    button_rects = []
    button_texts = ["Register", "Login", "Create Project", "View Projects", "Edit Project", "Delete Project", "Search Projects", "Exit"]
    for i, text in enumerate(button_texts, start=1):
        button_rect = pygame.Rect(50, 50 * i, 200, 40)
        draw_button(text, button_rect, button_rect.collidepoint(mouse_x, mouse_y))
        button_rects.append((button_rect, i))


        # Handle events
    print("lets handle evensts.")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("===================================")
            for rect, choice in button_rects:
                if rect.collidepoint(mouse_x, mouse_y):
                    print(f"Selected option: {choice}",f"selected screen : {all_screens[choice]}")
                    print("not menu")
                    sleep(10)
                    global current_screen 
                    current_screen= all_screens[choice]
                break
        break
    return current_screen
    
    
            #return all_screens[choice]
                            



    # text = font.render("Menu Screen (Press Space to Start)", True, black)
    # text_rect = text.get_rect(center=(width // 2, height // 2))
    # screen.blit(text, text_rect) 

def draw_login_window():

    screen.blit(background_image2, (0, 0))
        # Draw buttons
    button_rects = []
    button_texts = ["Register", "Login", "Create Project", "View Projects", "Edit Project", "Delete Project", "Search Projects", "Exit"]
    for i, text in enumerate(button_texts, start=1):
        button_rect = pygame.Rect(50, 50 * i, 200, 40)
        draw_button(text, button_rect, button_rect.collidepoint(mouse_x, mouse_y))
        button_rects.append((button_rect, i))


        # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, choice in button_rects:
                if rect.collidepoint(mouse_x, mouse_y):
                    print(f"Selected option: {choice}")
                    if all_screens[choice] != 'login':
                        print("not login")
                        pass
    return all_screens[choice]
                        


# Main 
current_screen = 'menu'
#draw_menu_screen()
while True:
    current_screen = 'menu'
    mouse_x, mouse_y = pygame.mouse.get_pos()

    print("main loop ",current_screen)
    
    if current_screen == 'menu':
        current_screen = draw_menu_screen()
        print("stell menu =",current_screen)

    elif current_screen == 'reg':
        draw_login_window()
        print("Not menu =",current_screen)
        
    pygame.display.flip()
