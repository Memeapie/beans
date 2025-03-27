_GAME_FULLSCREEN = False
_SKIP_INTRO = True
_HOLDING_READY = False
_OBJECTS = []
_NO_BEANS = 9
_BEANS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

import pygame as p
import moviepy.editor as e

if _GAME_FULLSCREEN:
    screen = p.display.set_mode((1920, 1080), p.FULLSCREEN)
else:
    screen = p.display.set_mode((1920, 1080), p.RESIZABLE)

font = p.font.SysFont('Arial', 20)

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
            'normal': '#5adbb5',
            'hover': '#5dbea3',
            'pressed': '#33b249',
        }

        self.buttonSurface = p.Surface((self.width, self.height))
        self.buttonRect = p.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(button_text, True, (20, 20, 20))

        _OBJECTS.append(self)

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

class AmountSlider:
    def __init__(self, x, y, width, height, amount, bean, iteration):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.amount = amount
        self.bean = bean
        self.pressed = False
        self.iteration = str(iteration+1)

        self.sliderImage = p.image.load("assets/" + self.bean + "-" + self.iteration + ".png")
        self.sliderRect = p.Rect(self.x, self.y, self.width, self.height)
        self.sliderText = font.render(self.amount + " BEAN", True, (255, 255, 255))
        self.fontSizeWidth, self.fontSizeHeight = font.size(self.amount + " BEAN")
        self.sliderTextRect = p.Rect(self.x + (self.width / 2) - (self.fontSizeWidth / 2), self.y + (self.height / 2) - (self.fontSizeHeight / 2), self.width, self.height)

        _OBJECTS.append(self)

    def process(self):
        mouse_pos = p.mouse.get_pos()
        if self.sliderRect.collidepoint(mouse_pos):
            if p.mouse.get_pressed(num_buttons=3)[0]:
                self.pressed = True

        if not self.pressed:
            screen.blit(self.sliderImage, self.sliderRect)
            screen.blit(self.sliderText, self.sliderTextRect)



def intro():
    clip = e.VideoFileClip('assets/intro_video.mp4')

    if _GAME_FULLSCREEN:
        clip.preview(fullscreen=True)
    else:
        clip.preview()

def ready_up():
    global _HOLDING_READY
    _HOLDING_READY = True

def holding_screen():
    global _HOLDING_READY
    clock = p.time.Clock()

    Button(screen.get_width() / 2 - 100, screen.get_height() / 2 - 50, 200, 100, 'Ready!', ready_up)

    while not _HOLDING_READY:
        for event in p.event.get():
            if event.type == p.QUIT:
                _HOLDING_READY = False

        screen.fill("grey")

        for object in _OBJECTS:
            object.process()

        p.display.flip()
        clock.tick(60)

    _OBJECTS.clear()

def game_loop():
    clock = p.time.Clock()

    beanCounter = 0
    for bean in _BEANS:
        AmountSlider(screen.get_width()-375, beanCounter * 100, 375, 87, bean, "red", beanCounter)
        print("Created Red Slider " + bean)
        beanCounter += 1

    beanCounter = 0
    while not (beanCounter == _NO_BEANS):
        AmountSlider(0, beanCounter * 100, 375, 87, "NO", "blue", beanCounter)
        print("Created Blue Slider " + str(beanCounter))
        beanCounter += 1

    bg_image = p.image.load('assets/background.jpg')
    logo = p.image.load('assets/logo.png')

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        screen.blit(p.transform.scale(bg_image, (screen.get_width(), screen.get_height())), (0, 0))
        screen.blit(logo, ((screen.get_width() / 2) - (logo.get_width() / 2), (screen.get_height() / 2) - (logo.get_height() / 4)))

        for object in _OBJECTS:
            object.process()

        p.display.flip()

        clock.tick(60)

def game_init():
    p.init()
    holding_screen()

    if not _SKIP_INTRO:
        intro()

    game_loop()
    p.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_init()
