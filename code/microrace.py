from microbit import *
import random

# Player starting position
player_x = 2
player_y = 4

# Score and game status
score = 0
game_over = False

# List to track obstacles
obstacles = []

# Obstacle speed and spawn interval
obstacle_speed = 1000  # Initial speed is set to 1 second
spawn_interval = 1000  # Initial spawn interval is set to 1 second

# Time variables for obstacle dropping and speed adjustments
last_drop_time = running_time()
last_adjustment_time = running_time()
drop_interval = obstacle_speed
adjustment_interval = 10000  # Adjust speed every 10 seconds

# Function to create a new obstacle
def create_obstacle():
    obstacles.append([random.randint(0, 4), 0])

def remove_obstacle(obstacle):
    obstacles.remove(obstacle)

# Function to handle player movement
def handle_player_movement():
    global player_x

    if button_a.is_pressed() and player_x > 0:
        player_x -= 1

    if button_b.is_pressed() and player_x < 4:
        player_x += 1

# Function to update game status
def update_game():
    global player_x, player_y, score, game_over, obstacle_speed, drop_interval, spawn_interval, last_drop_time, last_adjustment_time

    # Clear display
    display.clear()

    # Draw player
    display.set_pixel(player_x, player_y, 9)

    # Draw obstacles
    for obstacle in obstacles:
        display.set_pixel(obstacle[0], obstacle[1], 5)

        # Check if obstacle hit the player
        if obstacle[0] == player_x and obstacle[1] == player_y:
            game_over = True

        # Move obstacle down and check if it reaches the bottom
        obstacle[1] += 1

        if obstacle[1] > 4:
            remove_obstacle(obstacle)

    # Increase score
    score += 1

    # Decrease obstacle speed and spawn interval every 10 seconds
    if (running_time() - last_adjustment_time) >= adjustment_interval:
        last_adjustment_time = running_time()
        if obstacle_speed > 50:
            obstacle_speed -= 50
        if spawn_interval > 50:
            spawn_interval -= 50

# Main game loop
while True:
    # Check if game over
    if game_over:
        break

    # Check for button presses
    handle_player_movement()

    # Update game
    update_game()

    # Calculate time intervals for obstacle dropping
    current_time = running_time()
    time_elapsed = current_time - last_drop_time

    # Create new obstacle randomly
    if time_elapsed >= drop_interval:
        create_obstacle()
        last_drop_time = current_time

    sleep(100)  # Small delay to prevent constant looping

# Game over, display score
display.scroll("SCORE: " + str(score))