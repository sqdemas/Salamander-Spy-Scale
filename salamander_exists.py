from dataclasses import dataclass
from designer import *
from random import randint

SALAMANDER_SPEED = 10
PAGE_SPEED = 6
BOMB_SPEED = 7

@dataclass
class World:
    salamander: DesignerObject
    salamander_speed: int
    moving_left: bool
    moving_right: bool
    page: DesignerObject
    page_count: int
    show_page_text: DesignerObject
    heart1: DesignerObject
    heart2: DesignerObject
    heart3: DesignerObject
    pages: list[DesignerObject]
    bombs: list[DesignerObject]

def create_world() -> World:
    """ Create the world """
    return World(create_salamander(), 0, False, False, create_page_emoji(), 0,
                 show_page_count_text(), create_heart1(), create_heart2(), create_heart3(),
                 [], [])

def create_salamander() -> DesignerObject:
    """ Create salamander """
    salamander = image("salamander_with_glasses.png")
    salamander.y = get_height() * 0.5
    grow(salamander, 0.2)
    return salamander

def create_page_emoji() -> DesignerObject:
    """ Create page emoji to go next to counter in corner"""
    page = emoji("📃")
    page.y = 30
    page.x = get_width() - 30
    grow(page, 0.8)
    return page

def show_page_count_text() -> DesignerObject:
    """ Show number in corner representing number of pages collected"""
    number = text("black", "0", 30)
    number.y = 30
    number.x = get_width() - 60
    return number

def create_heart1() -> DesignerObject:
    """ Create rightmost heart in corner"""
    heart1 = image("heart_icon.png")
    heart1.y = 70
    heart1.x = get_width() - 30
    grow(heart1, 0.04)
    return heart1

def create_heart2() -> DesignerObject:
    """ Create middle heart in corner"""
    heart2 = image("heart_icon.png")
    heart2.y = 70
    heart2.x = get_width() - 70
    grow(heart2, 0.04)
    return heart2

def create_heart3() -> DesignerObject:
    """ Create leftmost heart in corner"""
    heart3 = image("heart_icon.png")
    heart3.y = 70
    heart3.x = get_width() - 110
    grow(heart3, 0.04)
    return heart3


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
    """ Check to see if key is pressed """
    if key == "right":
        world.moving_right = True
    elif key == "left":
        world.moving_left = True

def keys_not_pressed(world: World, key: str) :
    """ Check to see if key is pressed """
    if key == "right":
        world.moving_right = False
    elif key == "left":
        world.moving_left = False

def salamander_direction(world: World):
    """ Salamander moves horizontally depending on keys and only within screen limit """
    if world.moving_right and world.salamander.x < get_width() - 31:
        move_right(world)
    elif world.moving_left and world.salamander.x > 25:
        move_left(world)
    else:
        world.salamander_speed = 0

def create_page_object() -> DesignerObject:
    """ Create page DesignerObject """
    page = emoji("📃")
    grow(page, 0.8)
    page.anchor = "midtop"
    page.x = randint(0, get_width())
    page.y = 0
    return page

def make_pages(world: World):
    """ Create page randomly if there aren't enough currently"""
    not_enough_pages = len(world.pages) < 7
    random_chance = randint(1,50) == 1
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
    keep_pages = []
    for page in world.pages:
        if colliding(page, world.salamander):
            destroy(page)
            world.page_count += 1
        else:
            keep_pages.append(page)
    world.pages = keep_pages

def update_score_text(world: World):
    """ Score is shown and updated """
    world.show_page_text.text = str(world.page_count)

def create_bomb() -> DesignerObject:
    """ Create bomb DesignerObject """
    bomb = emoji("💣")
    bomb.anchor = "midtop"
    bomb.x = randint(0, get_width())
    bomb.y = 0
    return bomb

def make_bombs(world: World):
    """ Create bomb randomly if there aren't enough currently"""
    not_enough_bombs = len(world.bombs) < 5
    random_odds = randint(1,70) == 1
    if not_enough_bombs and random_odds:
        world.bombs.append(create_bomb())

def move_bombs_down(world: World):
    """ Move each bomb down """
    for bomb in world.bombs:
        bomb.y += BOMB_SPEED

def destroy_bomb_on_ground(world: World):
    """ Destroy bombs that touch the ground """
    keeps = []
    for bomb in world.bombs:
        if bomb.y < get_height():
            keeps.append(bomb)
        else:
            destroy(bomb)
        world.bombs = keeps

def salamander_bombs_collide(world: World):
    """ When salamander and bombs collide:
    Filters and destroys bombs,
    then subtracts from score if possible (score must stay >= 0)
    removes a heart """
    keep_bombs = []
    for bomb in world.bombs:
        if colliding(bomb, world.salamander):
            destroy(bomb)
            if world.page_count >= 2:
                world.page_count -= 2
            else:
                world.page_count = 0
        else:
            keep_bombs.append(bomb)
    world.bombs = keep_bombs

# pages on bombs should not spawn on top of each other, nor pages together or bombs together

when('starting', create_world)
when('updating', move_salamander)
when('typing', keys_pressed)
when('done typing', keys_not_pressed)
when('updating', salamander_direction)
when('updating', make_pages)
when('updating', move_pages_down)
when('updating', destroy_page_on_ground)
when('updating',destroy_when_page_collide)
when('updating', update_score_text)
when('updating', make_bombs)
when('updating', move_bombs_down)
when('updating', destroy_bomb_on_ground)
when('updating',salamander_bombs_collide)
start()