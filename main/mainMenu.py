import sys
from matrix_library import shapes as s, canvas as c
import time
from evdev import InputDevice, categorize, ecodes
import os

gamepad = InputDevice("/dev/input/event2")

# Initialize the canvas
canvas = c.Canvas()

# Create shapes and phrases for main menu
square = s.Polygon(s.get_polygon_vertices(4, 60, (0, 100)), (90, 200, 90))
headerline = s.Line((3, 28), (115, 28), (255, 255, 255), thickness=1)
menuheader = s.Phrase("MENU", (2, 0), (255, 255, 255), size=3.5, auto_newline=True)
demoheader = s.Phrase("Demos", (0, 33), (255, 255, 255), size=3, auto_newline=True)
gamesheader = s.Phrase("Games", (0, 60), (255, 255, 255), size=3, auto_newline=True)
creatornames = s.Phrase("created by Alex Ellie and Palmer", (0, 100), (255, 255, 255), size=1)

# Countdown setup
countdown_value = 16
countdown_display = s.Phrase(str(countdown_value), (110, 119), (255, 255, 255), size=1, auto_newline=True)
countdown_expired = False

# Main menu options and selection
options = [demoheader, gamesheader]
selected_index = 0
actions = [lambda: demo_action(), lambda: games_action()]

# selector box for selection
selector_box = s.Polygonselector(s.get_polygon_vertices(4, 20, (-100, -100)), (0, 255, 0), 1)

# Games scene to manage game folders
class GamesScene:
    def __init__(self):
        self.game_folders = self.load_game_folders()
        self.selected_index = 0
        self.page_index = 0
        self.items_per_page = 7

    def load_game_folders(self):
        current_dir = os.path.dirname(__file__)  # Get the directory of the current file
        games_dir = os.path.join(current_dir, "games")  # Path to the 'games' folder
        return [folder for folder in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, folder))]

    def get_current_page(self):
        start = self.page_index * self.items_per_page
        end = start + self.items_per_page
        return self.game_folders[start:end]

    def next_page(self):
        if (self.page_index + 1) * self.items_per_page < len(self.game_folders):
            self.page_index += 1
            self.selected_index = 0

    def previous_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.selected_index = 0

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.get_current_page())

    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.get_current_page())

    def get_selected_game(self):
        current_page = self.get_current_page()
        return current_page[self.selected_index] if current_page else None

# Scene management
main_scene = True
games_scene = GamesScene()

def demo_action():
    print("demos")
    canvas.clear()
    canvas.draw()
    del canvas
    sys.exit(0)

def games_action():
    global main_scene
    main_scene = False

def main_action():
    global main_scene
    main_scene = True

def shutdown():
    print("shutdown")
    canvas.clear()
    canvas.draw()
    del canvas
    sys.exit(0)

# Keyboard event handlers
def on_key_w():
    global selected_index, countdown_value, countdown_expired
    if main_scene:
        selected_index = (selected_index - 1) % len(options)
    else:
        games_scene.select_previous()
    countdown_value = 16
    countdown_expired = False

def on_key_s():
    global selected_index, countdown_value, countdown_expired
    if main_scene:
        selected_index = (selected_index + 1) % len(options)
    else:
        games_scene.select_next()
    countdown_value = 16
    countdown_expired = False

def on_key_x():
    global countdown_value, countdown_expired
    if main_scene:
        actions[selected_index]()
    else:
        selected_game = games_scene.get_selected_game()
        if selected_game:
            print(f"games/{selected_game}")
    countdown_value = 16
    countdown_expired = False

def on_key_a():
    if not main_scene:
        games_scene.previous_page()

def on_key_d():
    if not main_scene:
        games_scene.next_page()

def on_key_c():
    if not main_scene:
        main_action()

# keyboard.on_press_key("w", lambda _: on_key_w())
# keyboard.on_press_key("s", lambda _: on_key_s())
# keyboard.on_press_key("x", lambda _: on_key_x())
# keyboard.on_press_key("a", lambda _: on_key_a())
# keyboard.on_press_key("d", lambda _: on_key_d())
# keyboard.on_press_key("c", lambda _: on_key_c())

# Main loop
fps = 15
frame_time = 1 / fps
last_frame_time = time.time()

while True:
    current_time = time.time()
    elapsed_time = current_time - last_frame_time

    if elapsed_time >= frame_time:
        last_frame_time = current_time
        canvas.clear()
        
        if main_scene:

            if gamepad.active_keys() == [46]:
                on_key_w()
            if gamepad.active_keys() == [32]:
                on_key_s()
            if gamepad.active_keys() == [23]:
                on_key_x()
            if gamepad.active_keys() == [49]:
                shutdown()

            selected_option = options[selected_index]
            box_x = selected_option.position[0] - 2  # Add a small margin
            box_y = selected_option.position[1] - 2
            box_width = selected_option.get_width() + 4
            box_height = selected_option.size * 8 + 4

            # Set vertices for the selector box
            selector_box.vertices = s.get_polygon_vertices(4, 20, (box_x + 142, box_y + 15))

            # Update scrolling creator names
            creatornames.translate(-2, 0)
            if creatornames.get_width() + creatornames.position[0] < 0:
                creatornames.set_position([128, 100])

            # Countdown Timer Logic
            if countdown_value > 0:
                countdown_value -= 2 / fps  # Decrease countdown_value based on frame rate
            else:
                if not countdown_expired:
                    demo_action()  # Call demo action only once
                    countdown_expired = True  # Set flag to prevent repeated calls

            # Update countdown display text and position
            countdown_display.set_text(str(int(countdown_value)))  # Update the display text
            if countdown_value < 10:
                countdown_display.set_position((114, 119))  # Move to the right if single-digit
            else:
                countdown_display.set_position((110, 119))  # Keep original position for double-digit

            # Draw everything
            canvas.add(square)
            canvas.add(headerline)
            canvas.add(menuheader)
            canvas.add(demoheader)
            canvas.add(gamesheader)
            canvas.add(creatornames)
            canvas.add(countdown_display)  # Draw the countdown display
            canvas.add(selector_box)  # Add the green selector box
        
        else:
            game_names = games_scene.get_current_page()
            for i, game in enumerate(game_names):
                game_phrase = s.Phrase(game, (8, 7 + i * 15), (255, 255, 255), size=1)
                canvas.add(game_phrase)
            selected_game = games_scene.get_selected_game()
            if selected_game:
                selector_box.vertices = s.get_polygon_vertices(4, 6, (0, 10 + games_scene.selected_index * 15))
                canvas.add(selector_box)
        
        canvas.draw()
