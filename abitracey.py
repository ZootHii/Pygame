import pygame
import time
import random

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

crash_sound = pygame.mixer.Sound('crash.ogg')
pygame.mixer.music.load("music.ogg")

display_width = 600
display_height = 800
car_width = 80

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
thing_color = (78, 65, 166)

game_display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
pygame.display.set_caption("A bit Racey")
car_image = pygame.image.load("racecar.png")
pygame.display.set_icon(car_image)

pause = False


def game_quit():

    pygame.quit()
    quit()


def things_dodged(count):

    font_dodge = pygame.font.SysFont("comicsansms", 20)
    text = font_dodge.render("Dodge: " + str(count), True, black)
    game_display.blit(text, (0, 0))


def your_score(dodged):

    font_score = pygame.font.SysFont("comicsansms",20)
    TextSurf, TextRect = text_objects(str(dodged), font_score)
    TextRect.center = ((display_width * 0.50), (display_height * 0.50))
    game_display.blit(TextSurf, TextRect)


def things(tx, ty, tw, th, color):

    pygame.draw.rect(game_display, color, [tx, ty, tw, th])


def car(x, y):

    game_display.blit(car_image, (x, y))


def text_objects(text, font):

    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def massage_display(text):

    large_text = pygame.font.SysFont("comicsansms", 80)
    TextSurf, TextRect = text_objects(text, large_text)
    TextRect.center = ((display_width * 0.50), (display_height * 0.50))
    game_display.blit(TextSurf, TextRect)

    pygame.display.update()


def crash(dodged):

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    massage_display("YOU CRASHED")
    time.sleep(1)
    play_again(dodged)


def button(msg, x, y, b_width, b_height, i_color, a_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+b_width > mouse[0] > x and y+b_height > mouse[1] > y:
        pygame.draw.rect(game_display, a_color, (x, y, b_width, b_height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, i_color, (x, y, b_width, b_height))

    small_text = pygame.font.SysFont("comicsansms", 19)
    textSurf, textRect = text_objects(msg, small_text)
    textRect.center = ( (x+(b_width/2)), (y+(b_height/2)) )
    game_display.blit(textSurf, textRect)


def unpause():
    pygame.mixer.music.unpause()
    global pause
    pause = False


def paused():

    pygame.mixer.music.pause()

    while pause:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    unpause()

        # game_display.fill(white)
        large_text = pygame.font.SysFont("comicsansms", 90)
        TextSurf, TextRect = text_objects("Pause", large_text)
        TextRect.center = ((display_width * 0.50), (display_height * 0.30))
        game_display.blit(TextSurf, TextRect)

        button("Continue", 100, 415, 110, 70, green, bright_green, unpause)
        button("Quit", 380, 415, 110, 70, red, bright_red, game_quit)

        pygame.display.update()
        clock.tick(15)


def game_intro():

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        game_display.fill(white)
        large_text = pygame.font.SysFont("comicsansms", 90)
        TextSurf, TextRect = text_objects("A bit Racey", large_text)
        TextRect.center = ((display_width * 0.50), (display_height * 0.30))
        game_display.blit(TextSurf, TextRect)

        button("GO!", 100, 415, 110, 70, green, bright_green, game_loop)
        button("Quit", 380, 415, 110, 70, red, bright_red, game_quit)


        #pygame.draw.rect(game_display, thing_color, (198, 600, 200, 100))

        pygame.display.update()
        clock.tick(15)


def play_again(dodged):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        game_display.fill(white)
        large_text = pygame.font.SysFont("comicsansms", 90)
        TextSurf, TextRect = text_objects("A bit Racey", large_text)
        TextRect.center = ((display_width * 0.50), (display_height * 0.30))
        game_display.blit(TextSurf, TextRect)

        button("Play Again", 100, 415, 110, 70, green, bright_green, game_loop)
        button("Quit", 380, 415, 110, 70, red, bright_red, game_quit)
        button("Score: "+str(dodged), 240, 415, 110, 70, thing_color, thing_color, None)
        # pygame.draw.rect(game_display, thing_color, (198, 600, 200, 100))

        pygame.display.update()
        clock.tick(15)


def game_loop():

    global pause

    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.85)

    x_change = 0
    dodged = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 6
    thing_width = 100
    thing_height = 100

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    x_change = 7
                if event.key == pygame.K_LEFT:
                    x_change = -7
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        game_display.fill(white)

        # things(tx, ty, tw, th, color):
        things(thing_startx, thing_starty, thing_width, thing_height, thing_color)
        thing_starty += thing_speed

        car(x, y)

        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash(dodged)


        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(-75, display_width-75)
            dodged += 1
            thing_width += (dodged * 0.8)
            if dodged >= 7:
                thing_speed += 0.5
            elif dodged >= 14:
                thing_speed += 0.8

        if y < thing_starty + thing_height:
            if (x-10 > thing_startx and x+10 < thing_startx + thing_width) or (x-10 + car_width > thing_startx and x+10 + car_width < thing_startx + thing_width):
                crash(dodged)



        pygame.display.update()
        clock.tick(120)


game_intro()
game_loop()
game_quit()