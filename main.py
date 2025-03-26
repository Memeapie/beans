def intro(fullscreen):
    import moviepy.editor as e
    clip = e.VideoFileClip('assets/intro_video.mp4')

    if fullscreen:
        clip.preview(fullscreen=True)
    else:
        clip.preview()

def game_init():
    # Example file showing a basic pygame "game loop"

    import pygame as p

    GAME_FULLSCREEN = False
    SKIP_INTRO = False
    RUNNING = True

    p.init()

    if GAME_FULLSCREEN:
        screen = p.display.set_mode((1920, 1080), p.FULLSCREEN)
    else:
        screen = p.display.set_mode((1920, 1080), p.RESIZABLE)

    if not SKIP_INTRO:
        intro(GAME_FULLSCREEN)

    clock = p.time.Clock()

    while RUNNING:
        for event in p.event.get():
            if event.type == p.QUIT:
                RUNNING = False


        screen.fill("green")

        p.display.flip()

        clock.tick(60)

    p.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_init()
