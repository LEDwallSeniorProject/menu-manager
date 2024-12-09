from matrix_library import canvas as c, shapes as s, controller as con
import time
import sys

controller = con.Controller()

canvas = c.Canvas()

snake_pos = [16, 16]
snake_body = [[15, 16], [14, 16], [13, 16]]

snake_dir = [1, 0]

game_over = False

food_spawned = False
food_pos = [16, 8]


def exit_prog():
    del canvas
    sys.exit()


def move_up():
    global snake_dir
    snake_dir = [0, -1]


def move_down():
    global snake_dir
    snake_dir = [0, 1]


def move_left():
    global snake_dir
    snake_dir = [-1, 0]


def move_right():
    global snake_dir
    snake_dir = [1, 0]


controller.add_function("UP", move_up)
controller.add_function("DOWN", move_down)
controller.add_function("LEFT", move_left)
controller.add_function("RIGHT", move_right)
controller.add_function("START", exit_prog)

frame = 0
while not game_over:

    if snake_pos == food_pos:
        food_spawned = False

    # start = time.time()
    # while time.time() - start < 0.25:
    # if game_pad.active_keys() == [46]:
    #     snake_dir = [0, -1]
    # elif game_pad.active_keys() == [33]:
    #     snake_dir = [1, 0]
    # elif game_pad.active_keys() == [32]:
    #     snake_dir = [0, 1]
    # elif game_pad.active_keys() == [18]:
    #     snake_dir = [-1, 0]
    # elif game_pad.active_keys() == [24]:
    #     exit_prog()

    canvas.clear()

    for pos in snake_body:
        verts = s.get_polygon_vertices(4, 2, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        body = s.Polygon(verts, (0, 255, 0))
        body.rotate(45, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        canvas.add(body)

    if not game_over:
        snake_body.insert(0, snake_pos.copy())
        if snake_pos != food_pos:
            snake_body.pop()

    if not food_spawned:
        food_pos = [int(time.time()) % 32, int(time.time()) % 32]
        food_spawned = True

    food = s.Polygon(
        s.get_polygon_vertices(4, 2, ((food_pos[0] * 4) + 2, (food_pos[1] * 4) + 2)),
        (255, 0, 0),
    )

    canvas.add(food)

    canvas.draw()

    if frame % 2 == 0:
        snake_pos[0] += snake_dir[0]
        snake_pos[1] += snake_dir[1]

        if (
            snake_pos[0] < 0
            or snake_pos[0] >= 33
            or snake_pos[1] < 0
            or snake_pos[1] >= 33
        ):
            game_over = True

        if snake_pos in snake_body:
            game_over = True

    if game_over:
        canvas.clear()
        canvas.add(s.Phrase("GAME OVER", [32, 64], size=1))
        canvas.draw()
        time.sleep(2)
        break

    frame += 1
    # Add your code here
