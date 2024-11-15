import sys
from matrix_library import shapes as s, canvas as c
import time
from evdev import InputDevice, categorize, ecodes
import os

# Initialize canvas
bt1device = "/dev/input/event1"
print(f"Checking for Bluetooth adapter at {bt1device}")
while os.path.exists(bt1device) == False:
    time.sleep(1)
gamepad = InputDevice(bt1device)

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

# Initialize selectors
selector = s.Polygon(s.get_polygon_vertices(4, 12, (20, 120)), (0, 255, 0))

# Games scene to manage game folders
class GamesScene:
    def __init__(self):
        self.game_folders = self.load_game_folders()
        self.selected_index = 0
        self.page_index = 0
        self.items_per_page = 7

    def load_game_folders(self):
        current_dir = os.path.dirname(__file__)
        games_dir = os.path.join(current_dir, "games")
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
    global canvas
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
    global canvas
    print("shutdown")
    canvas.clear()
    canvas.draw()
    del canvas
    sys.exit(0)

# Keyboard event handlers
def on_key_w():
    global selected_index, countdown_value, countdown_expired, canvas
    if main_scene:
        selected_index = (selected_index - 1) % len(options)
    else:
        games_scene.select_previous()
    countdown_value = 16
    countdown_expired = False

def on_key_s():
    global selected_index, countdown_value, countdown_expired, canvas
    if main_scene:
        selected_index = (selected_index + 1) % len(options)
    else:
        games_scene.select_next()
    countdown_value = 16
    countdown_expired = False

def on_key_j():
    global countdown_value, countdown_expired, canvas
    if main_scene:
        actions[selected_index]()
    else:
        selected_game = games_scene.get_selected_game()
        if selected_game:
            print(f"game/{selected_game}")
            canvas.clear()
            canvas.draw()
            del canvas
            sys.exit(0)
    countdown_value = 16
    countdown_expired = False

def on_key_a():
    if not main_scene:
        games_scene.previous_page()

def on_key_d():
    if not main_scene:
        games_scene.next_page()

def on_key_l():
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
    # current_time = time.time()
    # elapsed_time = current_time - last_frame_time

    # if elapsed_time >= frame_time:
    #     last_frame_time = current_time
    #     canvas.clear()
    
    canvas.clear()
    time.sleep(0.15)
    if main_scene:

        if gamepad.active_keys() == [46]:
            on_key_w()
        if gamepad.active_keys() == [32]:
            on_key_s()
        if gamepad.active_keys() == [23]:
            on_key_j()
        if gamepad.active_keys() == [49]:
            shutdown()

        selected_option = options[selected_index]
        
        # Calculate desired selector position for the main menu based on selected_index
        selector_x = 132  # Adjust X position as needed for the main menu
        selector_y = 46 + selected_index * 27  # Update Y based on selected_index
        
        # Get current selector position and calculate translation
        current_center = selector.get_center()
        dx = selector_x - current_center[0]
        dy = selector_y - current_center[1]
        
        # Move selector to new position
        selector.translate(dx, dy)

        # Update scrolling creator names
        creatornames.translate(-2, 0)
        if creatornames.get_width() + creatornames.position[0] < 0:
            creatornames.set_position([128, 100])

        # Countdown Timer Logic
        if countdown_value > 0:
            countdown_value -= 2 / fps
        else:
            if not countdown_expired:
                demo_action()
                countdown_expired = True

        # Update countdown display text and position
        countdown_display.set_text(str(int(countdown_value)))
        if countdown_value < 10:
            countdown_display.set_position((114, 119))
        else:
            countdown_display.set_position((110, 119))

        # Draw everything
        canvas.add(square)
        canvas.add(headerline)
        canvas.add(menuheader)
        canvas.add(demoheader)
        canvas.add(gamesheader)
        canvas.add(creatornames)
        canvas.add(countdown_display)
        canvas.add(selector)
    
    else:
        
        if gamepad.active_keys() == [46]:
            on_key_w()
        if gamepad.active_keys() == [18]:
            on_key_a()
        if gamepad.active_keys() == [32]:
            on_key_s()
        if gamepad.active_keys() == [33]:
            on_key_d()
        if gamepad.active_keys() == [23]:
            on_key_j()
        if gamepad.active_keys() == [34]:
            on_key_l()
        if gamepad.active_keys() == [49]:
            shutdown()

        game_names = games_scene.get_current_page()
        for i, game in enumerate(game_names):
            game_phrase = s.Phrase(game, (9, 7 + i * 15), (255, 255, 255), size=1)
            canvas.add(game_phrase)
        
        selected_game = games_scene.get_selected_game()
        if selected_game:
            # Calculate desired selector position for games menu
            selector_x = -6
            selector_y = 10 + games_scene.selected_index * 15
            
            # Get current selector position and calculate translation
            current_center = selector.get_center()
            dx = selector_x - current_center[0]
            dy = selector_y - current_center[1]
            
            # Move selector to new position
            selector.translate(dx, dy)
            canvas.add(selector)
        
    canvas.draw()