import random
from typing import List, Dict
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[
        1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def SnakeSafe(data, x, y):
    for asmr in data['board']['hazards']:
        if asmr['x'] == x and asmr['y'] == y:
            return False
    for bmi in data['board']['snakes']:
        for _ in bmi['body']:
            if _['x'] == x and _['y'] == y:
                return False
    return True


def avoid_myself(my_head: Dict[str, int], data, my_body: List[dict],
                 possible_moves: List[str]) -> List[str]:
    print("AVOID MYSELF")
    for _ in data['board']['snakes']:
        for n in _['body']:
            if n['x'] == my_head['x'] - 1 and n['y'] == my_head[
                    'y'] and 'left' in possible_moves:
                possible_moves.remove('left')
                print(possible_moves)
                print(my_head['x'] - 1)
                print(n['x'])
            elif n['x'] == my_head['x'] + 1 and n['y'] == my_head[
                    'y'] and 'right' in possible_moves:
                possible_moves.remove('right')
                print(possible_moves)
                print(my_head['x'] + 1)
                print(n['x'])
            elif n['y'] == my_head['y'] - 1 and n['x'] == my_head[
                    'x'] and 'down' in possible_moves:
                possible_moves.remove('down')
                print(possible_moves)
                print(my_head['y'] - 1)
                print(n['y'])
            elif n['y'] == my_head['y'] + 1 and n['x'] == my_head[
                    'x'] and 'up' in possible_moves:
                possible_moves.remove('up')
                print(possible_moves)
                print(my_head['y'] + 1)
                print(n['y'])
    return possible_moves


def D(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def SnakeFood(data):
    x, y = 0, 0
    hx = data["you"]["head"]["x"]
    hy = data["you"]["head"]["y"]
    foods = data["board"]["food"]
    min_d = None
    for food in foods:
        dx = food["x"]
        dy = food["y"]
        dist = D(hx, hy, dx, dy)
        if min_d is None or dist < min_d:
            min_d = dist
            x, y = dx, dy
    return x, y


def SnakeNeck(data):
    headx = data["you"]["body"][0]["x"]
    heady = data["you"]["body"][0]["y"]
    neckx = data["you"]["body"][1]["x"]
    necky = data["you"]["body"][1]["y"]
    if headx < neckx:
        return "right"
    if headx > neckx:
        return "left"
    if heady < necky:
        return "up"
    if heady > necky:
        return "down"


def food(my_head, data, my_body, possible_moves):
    mov = None
    if len(data['board']['food']) > 0:
        if 'right' in avoid_myself(
                my_head, data, my_body,
                possible_moves) and SnakeFood(data)[0] > my_head['x']:
            mov = 'right'
        elif 'left' in avoid_myself(
                my_head, data, my_body,
                possible_moves) and SnakeFood(data)[0] < my_head['x']:
            mov = 'left'
        elif 'down' in avoid_myself(
                my_head, data, my_body,
                possible_moves) and SnakeFood(data)[1] < my_head['y']:
            mov = 'down'
        elif 'up' in avoid_myself(
                my_head, data, my_body,
                possible_moves) and SnakeFood(data)[1] > my_head['y']:
            mov = 'up'
        else:
            mov = choose_move(data)
    else:
        mov = choose_move(data)
    return mov


def avoid_borders(data, possible_moves):
    my_head = data['you']['head']
    print('border code')
    if my_head['x'] == data['board']['width'] - 1:
        possible_moves.remove('right')
        print(possible_moves)
    if my_head['x'] == 0:
        possible_moves.remove('left')
        print(possible_moves)
    if my_head['y'] == data['board']['height'] - 1:
        possible_moves.remove('up')
        print(possible_moves)
    if my_head['y'] == 0:
        possible_moves.remove('down')
        print(possible_moves)

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"][
        "head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"][
        "body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(
    #     f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~"
    # )
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    possible_moves = avoid_borders(data, possible_moves)
    possible_moves = avoid_myself(my_head, data, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    # board_height = ?
    # board_width = ?

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    print(my_head)
    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}"
    )

    return move
