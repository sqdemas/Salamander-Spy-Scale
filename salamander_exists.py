from dataclasses import dataclass
from designer import *

SALAMANDER_SPEED = 8

@dataclass
class World:
    salamander: DesignerObject
    salamander_speed: int
    moving_left: bool
    moving_right: bool
    page: DesignerObject
    page_count: int
    show_page_text: DesignerObject

def create_world() -> World:
    """ Create the world """
    return World(create_salamander(), 0, False, False, create_page_emoji(), 0,
                 show_page_count_text())

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

def screen_limit(world: World):
    """ Salamander stops moving when it touches screen edge """
    if world.salamander.x > get_width() - 25 or world.salamander.x < 25:
        world.salamander_speed = 0

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
    """ Salamander moves horizontally depending on keys """
    if world.moving_right:
        move_right(world)
    elif world.moving_left:
        move_left(world)
    else:
        world.salamander_speed = 0

when('starting', create_world)
when('updating', move_salamander)
when('updating', screen_limit)
when('typing', keys_pressed)
when('done typing', keys_not_pressed)
when('updating', salamander_direction)
start()