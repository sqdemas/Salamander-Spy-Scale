from dataclasses import dataclass
from designer import *
from random import randint

SALAMANDER_SPEED = 10
PAGE_SPEED = 6
BOMB_SPEED = 8
LEFT_HEART_X = 710
MIDDLE_HEART_X = 745
RIGHT_HEART_X = 780
SPAWN_RATE = 30
MAX_OBJECTS = 10
MAX_X_POSITION = 670
MIN_X_POSITION = 128

@dataclass
class World:
    background: DesignerObject
    salamander: DesignerObject
    salamander_speed: int
    moving_left: bool
    moving_right: bool
    page: DesignerObject
    page_count: int
    show_page_text: DesignerObject
    hearts: list[DesignerObject]
    pages: list[DesignerObject]
    bombs: list[DesignerObject]
    hearts_remaining: int

@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject

@dataclass
class TitleScreen:
    background: DesignerObject
    header: DesignerObject
    instruction_background: DesignerObject
    instruction_line1: DesignerObject
    instruction_line2: DesignerObject
    instruction_line3: DesignerObject
    instruction_line4: DesignerObject
    instruction_line5: DesignerObject
    play_button: Button

@dataclass
class EndScreen:
    """ Works as game over screen """
    background: DesignerObject
    message: DesignerObject
    quit_button: Button

def make_button(message: str, x: int, y: int, length: int, width: int, text_size: int, color: str) -> Button:
    """ Creates object with inner rectangle, outer rectangle, and text """
    label = text('black', message, text_size, x, y, layer= 'top')
    return Button(rectangle(color, length, width, x, y),
                  rectangle('black', length, width, x, y, 1),
                  label)

def create_title_screen() -> TitleScreen:
    """ Title Screen has background, text in a box, and a play button """
    instruction1 = "You are SuperSpy Salamander, the only spy with the ability to scale walls!"
    instruction2 = "Your mission is to collect pages of top secret documents"
    instruction3 = "by maneuvering SuperSpy Salamander with the left and right arrow keys."
    instruction4 = "Beware of bombs left by enemy agents! If SuperSpy Salamander is hit three times,"
    instruction5 = "he will lose his grip and fall."
    return TitleScreen(background_image('city_background.jpg'),
                       text('black', "Welcome to Salamander Spy Scale", 50, 400, 90),
                       make_button("", get_width()/2, 240, 650, 180, 20, 'oldlace'),
                       text('black', instruction1, 20, 400, 180),
                       text('black', instruction2, 20, 400, 210),
                       text('black', instruction3, 20, 400, 240),
                       text('black', instruction4, 20, 400, 270),
                       text('black', instruction5, 20, 400, 300),
                       make_button("PLAY", get_width()/2, 400, 80, 50, 30, 'chartreuse'))

def handle_title_buttons(world: TitleScreen):
    """ When user presses play button, scene changes to world """
    if colliding_with_mouse(world.play_button.background):
        change_scene('world')

def create_world() -> World:
    """ Create the world """
    return World(background_image('background.png'),
                 create_salamander(400, 360), 0, False, False, create_page_emoji(), 0,
                 show_page_count_text(),
                 [create_heart(LEFT_HEART_X), create_heart(MIDDLE_HEART_X), create_heart(RIGHT_HEART_X)],
                 [], [], 3)

def create_salamander(x: int, y: int) -> DesignerObject:
    """ Create salamander DesignerObject"""
    salamander = image("salamander_with_glasses.png")
    salamander.x = x
    salamander.y = y
    grow(salamander, 0.22)
    return salamander

def create_page_emoji() -> DesignerObject:
    """ Create page for display in corner"""
    page = emoji("📃")
    page.y = 30
    page.x = get_width() - 30
    grow(page, 0.8)
    return page

def show_page_count_text() -> DesignerObject:
    """ Show number of pages collected in corner """
    number = text("black", "0", 30)
    number.y = 30
    number.x = get_width() - 60
    return number

def create_heart(x: int) -> DesignerObject:
    """ Create heart DesignerObject """
    heart = image("heart_icon.png")
    heart.y = 70
    heart.x = x
    grow(heart, 0.037)
    return heart

def move_salamander(world: World):
    """ Move salamander horizontally left and right """
    world.salamander.x += world.salamander_speed

def move_right(world: World):
    """ Salamander moves right """
    world.salamander_speed = SALAMANDER_SPEED

def move_left(world: World):
    """ Salamander moves left """
    world.salamander_speed = -SALAMANDER_SPEED

def keys_pressed(world: World, key: str) :
    """ Check to see if key is pressed
    Args:
        key(str): name of key being pressed """
    if key == "right":
        world.moving_right = True
    elif key == "left":
        world.moving_left = True

def keys_not_pressed(world: World, key: str) :
    """ Check to see if key is pressed
    Args:
        key(str): name of key being pressed """
    if key == "right":
        world.moving_right = False
    elif key == "left":
        world.moving_left = False

def salamander_direction(world: World):
    """ Salamander moves horizontally depending on keys and only within screen limit """
    if world.moving_right and world.salamander.x < MAX_X_POSITION:
        move_right(world)
    elif world.moving_left and world.salamander.x > MIN_X_POSITION:
        move_left(world)
    else:
        world.salamander_speed = 0

def create_page_object() -> DesignerObject:
    """ Create page DesignerObject """
    page = emoji("📃")
    grow(page, 0.8)
    page.anchor = "midtop"
    page.x = randint(MIN_X_POSITION, MAX_X_POSITION)
    page.y = 0
    return page

def make_pages(world: World):
    """ Create page randomly if there aren't enough currently """
    not_enough_pages = len(world.pages) < MAX_OBJECTS
    random_chance = randint(1, SPAWN_RATE) == 1
    if not_enough_pages and random_chance:
        world.pages.append(create_page_object())

def move_pages_down(world: World):
    """ Move each page downward """
    for page in world.pages:
        page.y += PAGE_SPEED

def destroy_page_on_ground(world: World):
    """ Destroy pages that touch the ground """
    keep = []
    for page in world.pages:
        if page.y < get_height():
            keep.append(page)
        else:
            destroy(page)
        world.pages = keep

def destroy_when_page_collide(world: World):
    """ Filters and destroys pages that collide with Salamander, then adds to score"""
    keep = []
    for page in world.pages:
        if colliding(page, world.salamander):
            destroy(page)
            world.page_count += 1
        else:
            keep.append(page)
    world.pages = keep

def update_score_text(world: World):
    """ Score is shown and updated """
    world.show_page_text.text = str(world.page_count)

def create_bomb() -> DesignerObject:
    """ Create bomb DesignerObject """
    bomb = emoji("💣")
    bomb.anchor = "midtop"
    bomb.x = randint(MIN_X_POSITION, MAX_X_POSITION)
    bomb.y = 0
    return bomb

def make_bombs(world: World):
    """ Create bomb randomly if there aren't enough currently """
    not_enough_bombs = len(world.bombs) < MAX_OBJECTS
    random_odds = randint(1, SPAWN_RATE) == 1
    if not_enough_bombs and random_odds:
        world.bombs.append(create_bomb())

def move_bombs_down(world: World):
    """ Move each bomb down """
    for bomb in world.bombs:
        bomb.y += BOMB_SPEED

def destroy_bomb_on_ground(world: World):
    """ Destroy bombs that touch the ground """
    keep = []
    for bomb in world.bombs:
        if bomb.y < get_height():
            keep.append(bomb)
        else:
            destroy(bomb)
        world.bombs = keep

def salamander_show_damage(world: World):
    """ Sequence animation to show Salamander hurt when collides with bomb """
    #sequence_animation(world.salamander, )

def salamander_bombs_collide(world: World):
    """ When salamander and bombs collide,
    filter and destroy bombs,
    subtracts from score
    removes a heart """
    keep = []
    for bomb in world.bombs:
        if colliding(bomb, world.salamander):
            destroy(bomb)
            #salamander_show_damage()
            remove_heart(world)
            # score must stay >= 0
            if world.page_count >= 2:
                world.page_count -= 2
            else:
                world.page_count = 0
        else:
            keep.append(bomb)
    world.bombs = keep

def game_over(world: World):
    """ When there are no lives, the game is over.
     Salamander should fall off screen
     Then scene is changed """
    # linear_animation(world.salamander, 'y', world.salamander.y, 600, 3.0)
    change_scene('end', final_page_count = world.page_count)

def remove_heart(world: World):
    """ Subtracts from heart count, destroys heart, updating hearts in world """
    world.hearts_remaining -= 1
    for heart in world.hearts:
        destroy(heart)
    if (world.hearts_remaining == 3):
        world.hearts = [create_heart(LEFT_HEART_X), create_heart(MIDDLE_HEART_X), create_heart(RIGHT_HEART_X)]
    elif (world.hearts_remaining == 2):
        world.hearts = [create_heart(MIDDLE_HEART_X), create_heart(RIGHT_HEART_X)]
    elif (world.hearts_remaining == 1):
        world.hearts = [create_heart(RIGHT_HEART_X)]
    elif (world.hearts_remaining == 0):
        world.hearts = []
        game_over(world)

def create_end_screen(final_page_count: int) -> EndScreen:
    """ Shows background, game over message with final score, and quit button to end program """
    game_over_message = "GAME OVER! SCORE:  " + str(final_page_count)
    return EndScreen(background_image('background.png'),
                     make_button(game_over_message, get_width()/2, 270, 450, 90, 40, 'oldlace'),
                     make_button("QUIT", get_width()/2, 350, 80, 50, 30, 'skyblue')
                     )

def handle_end_buttons(world: EndScreen):
    """ When user clicks quit button, application closes """
    if colliding_with_mouse(world.quit_button):
        quit()

when("starting: title", create_title_screen)
when("clicking: title", handle_title_buttons)

when('starting: world', create_world)
when('updating: world', move_salamander)
when('typing: world', keys_pressed)
when('done typing: world', keys_not_pressed)
when('updating: world', salamander_direction)
when('updating: world', make_pages)
when('updating: world', move_pages_down)
when('updating: world', destroy_page_on_ground)
when('updating: world',destroy_when_page_collide)
when('updating: world', update_score_text)
when('updating: world', make_bombs)
when('updating: world', move_bombs_down)
when('updating: world', destroy_bomb_on_ground)
when('updating: world',salamander_bombs_collide)

when('starting: end', create_end_screen)
when('clicking: end', handle_end_buttons)

start()
debug(scene = 'title')