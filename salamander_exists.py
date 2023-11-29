from dataclasses import dataclass
from designer import *
from random import randint

SALAMANDER_SPEED = 10
MAX_OBJECTS = 10

# x position of hearts in corner
LEFT_HEART_X = 710
MIDDLE_HEART_X = 745
RIGHT_HEART_X = 780

# screen limit x positons
MAX_X_POSITION = 670
MIN_X_POSITION = 128

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
    settings_button: Button
    settings_mode: str
    page_speed: int
    bomb_speed: int
    spawn_rate: int
    display_mode: DesignerObject
    display_difficulty: DesignerObject

@dataclass
class SettingsScreen:
    """ Displays settings to switch game difficulty """
    background: DesignerObject
    rectangle: DesignerObject
    heading: DesignerObject
    easy_button: Button
    medium_button: Button
    hard_button: Button

@dataclass
class EndScreen:
    """ Works as game over screen """
    background: DesignerObject
    message: DesignerObject
    quit_button: Button
    play_again_button: Button

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

def create_world() -> World:
    """ Create the world where actual gameplay occurs """
    return World(background_image('background.png'),
                 create_salamander(400, 360), 0, False, False, create_page_emoji(), 0,
                 show_page_count_text(),
                 [create_heart(LEFT_HEART_X), create_heart(MIDDLE_HEART_X), create_heart(RIGHT_HEART_X)],
                 [], [], 3,
                 make_button("SETTINGS", 50, 40, 80, 40, 18, 'tan'),
                 'medium', 6, 8, 30,
                 text('black', "MODE:", 18, 50, 80),
                 text('black', "MEDIUM", 20, 50, 100)
                 )

def create_settings_screen() -> SettingsScreen:
    """ Settings to allow user to change difficulty """
    return SettingsScreen(background_image('city_background.jpg'),
                          make_button("", 400, 300, 640, 400, 0, 'cadetblue'),
                          text('black', "SETTINGS", 50, 400, 200),
                          make_button("EASY", 200, 350, 80, 50, 30, 'green'),
                          make_button("MEDIUM", 400, 350, 110, 50, 30, 'green'),
                          make_button("HARD", 600, 350, 80, 50, 30, 'green')
                          )

def create_end_screen(final_page_count: int) -> EndScreen:
    """ Shows background, game over message with final score, quit button to end program, and play again button to redirect to world """
    game_over_message = "GAME OVER! SCORE:  " + str(final_page_count)
    return EndScreen(background_image('background.png'),
                     make_button(game_over_message, get_width()/2, 270, 450, 90, 40, 'oldlace'),
                     make_button("QUIT", 300, 350, 80, 50, 30, 'skyblue'),
                     make_button("PLAY AGAIN", 450, 350, 160, 50, 30, 'skyblue')
                     )

def handle_title_buttons(world: TitleScreen):
    """ When user presses play button, scene changes to world """
    if colliding_with_mouse(world.play_button.background):
        change_scene('world')

def handle_world_buttons(world: World):
    """ Push settings scene when settings button is clicked """
    if colliding_with_mouse(world.settings_button.background):
        push_scene('settings')

def handle_settings_buttons(world: SettingsScreen):
    """When user presses a difficulty mode, that mode is selected and sent back to world when scene is popped """
    if colliding_with_mouse(world.easy_button.background):
        pop_scene(difficulty = 'easy')
    if colliding_with_mouse(world.medium_button.background):
        pop_scene(difficulty = 'medium')
    if colliding_with_mouse(world.hard_button.background):
        pop_scene(difficulty = 'hard')

def handle_end_buttons(world: EndScreen):
    """ When user clicks quit button, application closes
     or if play again is pressed, it takes you back to world"""
    if colliding_with_mouse(world.quit_button.background):
        quit()
    if colliding_with_mouse(world.play_again_button.background):
        change_scene('world')

def resume_from_settings(world: World, difficulty: str):
    """ Used when settings is closed and world resumes. Updates difficulty in world """
    world.settings_mode = difficulty
    update_difficulty_mode(world)

def create_salamander(x: int, y: int) -> DesignerObject:
    """ Create salamander DesignerObject"""
    salamander = image("salamander_with_glasses.png")
    salamander.x = x
    salamander.y = y
    grow(salamander, 0.22)
    return salamander

def create_red_salamander() -> DesignerObject:
    red_salamander = image('hurt_salamander.png')
    red_salamander.x = 400
    red_salamander.y = 360
    grow(red_salamander, 0.22)
    return red_salamander

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
    random_chance = randint(1, world.spawn_rate) == 1
    if not_enough_pages and random_chance:
        world.pages.append(create_page_object())

def move_pages_down(world: World):
    """ Move each page downward """
    for page in world.pages:
        page.y += world.page_speed

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
    random_odds = randint(1, world.spawn_rate) == 1
    if not_enough_bombs and random_odds:
        world.bombs.append(create_bomb())

def move_bombs_down(world: World):
    """ Move each bomb down """
    for bomb in world.bombs:
        bomb.y += world.bomb_speed

def destroy_bomb_on_ground(world: World):
    """ Destroy bombs that touch the ground """
    keep = []
    for bomb in world.bombs:
        if bomb.y < get_height():
            keep.append(bomb)
        else:
            destroy(bomb)
        world.bombs = keep
"""
def salamander_show_damage(world: World):
    "" When Salamander collides with bomb, it is moved back to center
     and sequence animation flashes red""
    #destroy(world.salamander)
    salamander_hurt_sequence = [create_salamander(400, 360), create_red_salamander(), create_salamander(400, 360)]
    sequence_animation(create_salamander(400,360), 'filename', salamander_hurt_sequence, 3.0, 3, False, None, False)
    #world.salamander = create_salamander(400, 360)
"""
def salamander_bombs_collide(world: World):
    """ When salamander and bombs collide,
    filter and destroy bombs,
    subtracts from score
    removes a heart """
    keep = []
    for bomb in world.bombs:
        if colliding(bomb, world.salamander):
            destroy(bomb)
            #salamander_show_damage(world)
            remove_heart(world)
            # score must stay >= 0
            if world.page_count >= 2:
                world.page_count -= 2
            else:
                world.page_count = 0
        else:
            keep.append(bomb)
    world.bombs = keep
def salamander_fall_animation(world: World):
    """ pauses falling objects and prevents new ones from spawning,
    salamander spins and falls offscreen """
    world.page_speed = 0
    world.bomb_speed = 0
    world.spawn_rate = 10000
    linear_animation(world.salamander, 'angle', 0, 360, 2.0, True, None, False)
    linear_animation(world.salamander, 'y', 360, 700, 2.0, True, None, False)

def game_over(world: World):
    """ When the game is over, Salamander fall animation, and changes scene """
    salamander_fall_animation(world)
    if world.salamander.y >= 600:
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

def update_difficulty_mode(world: World):
    """ Adjusts speed and spawn rate of bombs and pages depending on selected difficulty mode,
     updates display with current difficulty level """
    if world.settings_mode == 'easy':
        world.display_difficulty.text = "EASY"
        world.page_speed = 4
        world.bomb_speed = 6
        world.spawn_rate = 60
    elif world.settings_mode == 'medium':
        world.display_difficulty.text = "MEDIUM"
        world.page_speed = 6
        world.bomb_speed = 8
        world.spawn_rate = 30
    elif world.settings_mode == 'hard':
        world.display_difficulty.text = "HARD"
        world.page_speed = 8
        world.bomb_speed = 10
        world.spawn_rate = 20

when("starting: title", create_title_screen)
when("clicking: title", handle_title_buttons)

when('starting: world', create_world)
when('clicking: world', handle_world_buttons)
when('entering: world', resume_from_settings)

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

when('starting: settings', create_settings_screen)
when('clicking: settings', handle_settings_buttons)

when('starting: end', create_end_screen)
when('clicking: end', handle_end_buttons)

start()
debug(scene = 'title')