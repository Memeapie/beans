_GAME_FULLSCREEN = False
_SKIP_INTRO = True
objects = []

import pygame as p
import moviepy.editor as e

if _GAME_FULLSCREEN:
    screen = p.display.set_mode((1920, 1080), p.FULLSCREEN)
else:
    screen = p.display.set_mode((1920, 1080), p.RESIZABLE)

font = p.font.SysFont('Arial', 40)

def test_func():
    print('Button Pressed')

class Button:
    def __init__(self, x, y, width, height, button_text='Button', onclick_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclick_function
        self.onePress = one_press
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = p.Surface((self.width, self.height))
        self.buttonRect = p.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(button_text, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mouse_pos = p.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if p.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def intro():
    clip = e.VideoFileClip('assets/intro_video.mp4')

    if _GAME_FULLSCREEN:
        clip.preview(fullscreen=True)
    else:
        clip.preview()

def game_loop():
    clock = p.time.Clock()

    Button(30, 30, 400, 100, 'Button One (onePress)', test_func)
    Button(30, 140, 400, 100, 'Button Two (multiPress)', test_func, True)

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        screen.fill("green")

        for object in objects:
            object.process()

        p.display.flip()

        clock.tick(60)

def game_init():
    p.init()
    if not _SKIP_INTRO:
        intro()

    game_loop()
    p.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_init()
