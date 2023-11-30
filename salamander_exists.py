from dataclasses import dataclass
from designer import *
from random import randint

SALAMANDER_SPEED = 10
MAX_OBJECTS = 7

# x position of hearts in corner
LEFT_HEART_X = 710
MIDDLE_HEART_X = 745
RIGHT_HEART_X = 780

# screen limit x max and min positions
MAX_X_POSITION = 650
MIN_X_POSITION = 150

# filenames for salamander hurt animation
NORMAL = "salamander_with_glasses.png"
RED = "hurt_salamander.png"

set_window_color('skyblue')

@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject

@dataclass
class TitleScreen:
    """ Welcome and instruction screen """
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
    """ Main gameplay """
    clouds: list[DesignerObject]
    building: DesignerObject
    windows: list[list[DesignerObject]]
    salamander: DesignerObject
    salamander_speed: int
    moving_left: bool
    moving_right: bool
    page_in_corner: DesignerObject
    page_count: int
    page_count_in_corner: DesignerObject
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
    """ Displays settings to adjust game difficulty """
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
    """
    Creates a Button with inner rectangle, outer rectangle, and text
    Args:
        message (str): Message on button
        x (int): x position of button
        y (int): y position of button
        length (int): how long rectangular button is
        width (int): how tall rectangular button is
        text_size (int): size of button text
        color (str): color of button background
    Returns:
        Button: collection of DesignerObjects to make a button
    """
    label = text('black', message, text_size, x, y, layer= 'top')
    return Button(rectangle(color, length, width, x, y),
                  rectangle('black', length, width, x, y, 1),
                  label)

def create_window(x: int, y: int) -> DesignerObject:
    """
    Creates window from image
    Args:
        x (int): x position of window
        y (int): y position of window
    Returns:
        DesignerObject: window image
    """
    window = image('window.png')
    grow(window, 0.15)
    window.x = x
    window.y = y
    return window

def create_window_list(x: int) -> list[DesignerObject]:
    """
    Creates a vertical column of windows
    Args:
        x (int): x position of windows
    Returns:
        list[DesignerObject]: list of window objects
    """
    window_column = []
    for number in [1,2,3,4,5,6,7]:
        window_column.append(create_window(x, number*100))
    return window_column

def move_windows_down(world: World):
    """
    Moves each individual window downward and wraps around
    Args:
        world (World): World instance
    """
    for window_list in world.windows:
        for window in window_list:
            window.y += 1
            window.y = window.y % get_window_height()

def create_cloud(x: int, y: int) -> DesignerObject:
    """
    Creates cloud for background in sky
    Args:
        x (int): x position of cloud
        y (int): y position of cloud
    Returns:
        DesignerObject: cloud image
    """
    cloud = image('cloud.png')
    grow(cloud, 0.5)
    cloud.x = x
    cloud.y = y
    return cloud

def move_clouds_down(world: World):
    """
    Moves each individual cloud downward and wraps around
    Args:
        world (World): World instance
    """
    for cloud in world.clouds:
        cloud.y += 1
        cloud.y = cloud.y % get_window_height()


def create_title_screen() -> TitleScreen:
    """
    Creates Title Screen with background, header, empty button with text instructions, and play button
    Returns:
        TitleScreen: TitleScreen instance
    """
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
    """
    Creates the world where actual gameplay occurs, background, salamander character,
    page count, hearts, settings button, and mode
    Returns:
        World: World instance
    """
    return World([create_cloud(100, 150), create_cloud(150, 400), create_cloud(700, 100), create_cloud(740, 500)],
                 create_building(),
                 [create_window_list(200), create_window_list(333), create_window_list(466), create_window_list(600)],
                 create_salamander(), 0, False, False,
                 show_page_in_corner(), 0,
                 show_page_count_in_corner(),
                 [create_heart(LEFT_HEART_X), create_heart(MIDDLE_HEART_X), create_heart(RIGHT_HEART_X)],
                 [], [], 3,
                 make_button("SETTINGS", 50, 40, 80, 40, 18, 'tan'),
                 'medium', 6, 8, 30,
                 text('black', "MODE:", 18, 50, 80),
                 text('black', "MEDIUM", 20, 50, 100)
                 )

def create_settings_screen() -> SettingsScreen:
    """
    Creates Settings to allow user to change difficulty with background, empty button for background,
    header, and three difficulty buttons
    Returns:
        SettingsScreen: SettingScreen instance
    """
    return SettingsScreen(background_image('city_background.jpg'),
                          make_button("", 400, 300, 640, 400, 0, 'cadetblue'),
                          text('black', "SETTINGS", 50, 400, 200),
                          make_button("EASY", 200, 350, 80, 50, 30, 'green'),
                          make_button("MEDIUM", 400, 350, 110, 50, 30, 'green'),
                          make_button("HARD", 600, 350, 80, 50, 30, 'green')
                          )

def create_end_screen(final_page_count: int) -> EndScreen:
    """
    Game over screen with background, message and final score, quit button, and play again button
    Args:
         final_page_count (int): number of pages user collected, passed in from World
    Returns:
        EndScreen: EndScreen instance
    """
    game_over_message = "GAME OVER! SCORE:  " + str(final_page_count)
    return EndScreen(background_image('city_background.jpg'),
                     make_button(game_over_message, 400, 270, 450, 90, 40, 'oldlace'),
                     make_button("QUIT", 300, 350, 80, 50, 30, 'skyblue'),
                     make_button("PLAY AGAIN", 450, 350, 160, 50, 30, 'skyblue')
                     )

def handle_title_buttons(world: TitleScreen):
    """
    When user presses play button, scene changes to world
    Args:
        world (TitleScreen): TitleScreen instance
    """
    if colliding_with_mouse(world.play_button.background):
        change_scene('world')

def handle_world_buttons(world: World):
    """
    When user presses settings button, settings scene is pushed
    Args:
        world (World): World instance
    """
    if colliding_with_mouse(world.settings_button.background):
        push_scene('settings')

def handle_settings_buttons(world: SettingsScreen):
    """
    When user presses a difficulty button, settings scene is popped and a string
    representing the difficulty is passed as a keyword argument back to World
    Args:
        world (TitleScreen): SettingsScreen instance
    """
    if colliding_with_mouse(world.easy_button.background):
        pop_scene(difficulty = 'easy')
    if colliding_with_mouse(world.medium_button.background):
        pop_scene(difficulty = 'medium')
    if colliding_with_mouse(world.hard_button.background):
        pop_scene(difficulty = 'hard')

def handle_end_buttons(world: EndScreen):
    """
    When user clicks quit button, application closes
    When user clicks play again button, scene changes to world
    Args:
        world (EndScreen): EndScreen instance
    """
    if colliding_with_mouse(world.quit_button.background):
        quit()
    if colliding_with_mouse(world.play_again_button.background):
        change_scene('world')

def resume_from_settings(world: World, difficulty: str):
    """
    Called when settings scene is closed and world resumes.
    Updates difficulty in world
    Args:
        world (World): World instance
        difficulty (str): string representing chosen difficulty setting
    """
    world.settings_mode = difficulty
    update_difficulty_mode(world)

def create_building() -> DesignerObject:
    """
    Creates brown rectangle representing building
    Returns:
        DesignerObject: brown rectangle
    """
    building = rectangle('saddlebrown', 570, 600)
    return building

def create_salamander() -> DesignerObject:
    """
    Create salamander character
    Returns:
        DesignerObject: image of salamander
    """
    salamander = image("salamander_with_glasses.png")
    salamander.x = 400
    salamander.y = 360
    grow(salamander, 0.22)
    return salamander

def show_page_in_corner() -> DesignerObject:
    """
    Create page to be displayed in corner
    Returns:
        DesignerObject: page emoji
    """
    page = emoji("📃")
    page.y = 30
    page.x = get_width() - 30
    grow(page, 0.8)
    return page

def show_page_count_in_corner() -> DesignerObject:
    """
    Display number of pages collected in corner
    Returns:
        DesignerObject: text displaying page count
    """
    number = text("black", "0", 30)
    number.y = 30
    number.x = get_width() - 60
    return number

def create_heart(x: int) -> DesignerObject:
    """
    Create heart to be displayed in corner
    Args:
        x (int): x position of heart
    Returns:
        DesignerObject: heart image
    """
    heart = image("heart_icon.png")
    heart.y = 70
    heart.x = x
    grow(heart, 0.037)
    return heart

def move_salamander(world: World):
    """
    Changes speed to move salamander horizontally left and right
    Args:
        world (World): World instance
    """
    world.salamander.x += world.salamander_speed

def move_right(world: World):
    """
    Salamander moves right
    Args:
        world (World): World instance
    """
    world.salamander_speed = SALAMANDER_SPEED

def move_left(world: World):
    """
    Salamander moves left
    Args:
        world (World): World instance
    """
    world.salamander_speed = -SALAMANDER_SPEED

def keys_pressed(world: World, key: str):
    """
    Checks to see if key is pressed
    Args:
        world (World): World instance
        key (str): name of key being pressed
    """
    if key == "right":
        world.moving_right = True
    elif key == "left":
        world.moving_left = True

def keys_not_pressed(world: World, key: str):
    """
    Checks to see if key is pressed
    Args:
        world (World): World instance
        key (str): name of key being pressed
    """
    if key == "right":
        world.moving_right = False
    elif key == "left":
        world.moving_left = False

def salamander_direction(world: World):
    """
    Checks if a key is pressed and if Salamander is within screen limit,
    then move horizontally or not at all
    Args:
        world (World): World instance
    """
    if world.moving_right and world.salamander.x < MAX_X_POSITION:
        move_right(world)
    elif world.moving_left and world.salamander.x > MIN_X_POSITION:
        move_left(world)
    else:
        world.salamander_speed = 0

def create_page() -> DesignerObject:
    """
    Creates page that falls down screen
    Returns:
        DesignerObject: page emoji
    """
    page = emoji("📃")
    grow(page, 0.8)
    page.anchor = "midtop"
    page.x = randint(MIN_X_POSITION, MAX_X_POSITION)
    page.y = 0
    return page

def make_pages(world: World):
    """
    Creates page randomly if there aren't enough currently
    Args:
        world (World): World instance
    """
    not_enough_pages = len(world.pages) < MAX_OBJECTS
    random_chance = randint(1, world.spawn_rate) == 1
    if not_enough_pages and random_chance:
        world.pages.append(create_page())

def move_pages_down(world: World):
    """
    Moves each page downward
    Args:
        world (World): World instance
    """
    for page in world.pages:
        page.y += world.page_speed

def destroy_page_on_ground(world: World):
    """
    Destroy pages that touch the ground
    Args:
        world (World): World instance
    """
    keep = []
    for page in world.pages:
        if page.y < get_height():
            keep.append(page)
        else:
            destroy(page)
        world.pages = keep

def destroy_when_page_collide(world: World):
    """
    Filters and destroys pages that collide with Salamander, then adds to score
    Args:
        world (World): World instance
    """
    keep = []
    for page in world.pages:
        if colliding(page, world.salamander):
            destroy(page)
            world.page_count += 1
        else:
            keep.append(page)
    world.pages = keep

def update_score(world: World):
    """
    Score is updated to world
    Args:
        world (World): World instance
    """
    world.page_count_in_corner.text = str(world.page_count)

def create_bomb() -> DesignerObject:
    """
    Create bomb that falls down screen
    Returns:
        DesignerObject: bomb emoji
    """
    bomb = emoji("💣")
    bomb.anchor = "midtop"
    bomb.x = randint(MIN_X_POSITION, MAX_X_POSITION)
    bomb.y = 0
    return bomb

def make_bombs(world: World):
    """
    Create bomb randomly if there aren't enough currently
    Args:
        world (World): World instance
    """
    not_enough_bombs = len(world.bombs) < MAX_OBJECTS
    random_odds = randint(1, world.spawn_rate) == 1
    if not_enough_bombs and random_odds:
        world.bombs.append(create_bomb())

def move_bombs_down(world: World):
    """
    Move each bomb down
    Args:
        world (World): World instance
    """
    for bomb in world.bombs:
        bomb.y += world.bomb_speed

def destroy_bomb_on_ground(world: World):
    """
    Destroy bombs that touch the ground
    Args:
        world (World): World instance
    """
    keep = []
    for bomb in world.bombs:
        if bomb.y < get_height():
            keep.append(bomb)
        else:
            destroy(bomb)
        world.bombs = keep


def salamander_show_damage(world: World):
    """
    Sequence animation flashes red
    Args:
        world (World): World instance
    """
    salamander_hurt_sequence = [NORMAL, RED, NORMAL]
    sequence_animation(world.salamander, 'filename', salamander_hurt_sequence,
                       1, 2)

def subtract_from_score(world: World):
    """
    Subtract 2 from score if possible. Score must stay above 0
    Args:
        world (World): World instance
    """
    if world.page_count >= 2:
        world.page_count -= 2
    else:
        world.page_count = 0

def salamander_bombs_collide(world: World):
    """
    When salamander and bombs collide, filter and destroy bombs, salamander show hurt,
    remove_heart, and subtracts from score
    Args:
        world (World): World instance
    """
    keep = []
    for bomb in world.bombs:
        if colliding(bomb, world.salamander):
            destroy(bomb)
            salamander_show_damage(world)
            remove_heart(world)
            subtract_from_score(world)
        else:
            keep.append(bomb)
    world.bombs = keep

def salamander_fall_animation(world: World):
    """
    Stops objects from falling and spawning, animation for salamander to spin offscreen
    Args:
        world (World): World instance
    """
    world.page_speed = 0
    world.bomb_speed = 0
    world.spawn_rate = 10000
    world.salamander.flip_y = True
    linear_animation(world.salamander, 'angle', 0, 360, 2.0, True, None, False)
    linear_animation(world.salamander, 'y', 360, 700, 2.0, True, None, False)

def when_game_over(world: World):
    """
    When the game is over, change scene to EndScreen
    Args:
        world (World): World instance
    """
    if world.salamander.y >= 600:
        change_scene('end', final_page_count = world.page_count)

def remove_heart(world: World):
    """
    Subtract from heart count, destroys heart, and update hearts in world
    Args:
        world (World): World instance
    """
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
        salamander_fall_animation(world)

def update_difficulty_mode(world: World):
    """
    Adjusts speed and spawn rate of bombs and pages depending on selected difficulty mode,
    then updates display with current difficulty level
    Args:
        world (World): World instance
    """
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
when('updating: world', update_score)
when('updating: world', make_bombs)
when('updating: world', move_bombs_down)
when('updating: world', destroy_bomb_on_ground)
when('updating: world',salamander_bombs_collide)
when('updating: world', when_game_over)
when('updating: world', move_windows_down)
when('updating: world', move_clouds_down)

when('starting: settings', create_settings_screen)
when('clicking: settings', handle_settings_buttons)

when('starting: end', create_end_screen)
when('clicking: end', handle_end_buttons)

start()
debug(scene = 'title')