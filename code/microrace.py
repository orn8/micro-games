from microbit import *

# Set up the initial variables
total_clicks = 48
a_clicks = 0
b_clicks = 0
current_y = 4
start_time = 0
game_state = 'select'

clicks_list = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100]
clicks_index = -1

def display_total_clicks():
    display.scroll(str(clicks_list[clicks_index]), delay=50)

display.scroll("CLICKS: ", delay=75)

# Main game loop
while True:
    if game_state == 'select':
        if button_a.was_pressed():
            clicks_index = (clicks_index + 1) % len(clicks_list)
            display_total_clicks()

        if button_b.was_pressed():
            total_clicks = clicks_list[clicks_index]
            game_state = 'play'
            display.clear()
            
    clicks_per_step = total_clicks // 4
    
    if game_state == 'play':
        if button_a.was_pressed() and a_clicks < total_clicks // 2:
            a_clicks += 1
            if a_clicks % clicks_per_step == 0:
                display.set_pixel(2, current_y, 0)
                current_y -= 1
                if current_y < 0:
                    current_y = 0
            display.set_pixel(2, current_y, 9)

        if button_b.was_pressed() and b_clicks < total_clicks // 2:
            b_clicks += 1
            if b_clicks % clicks_per_step == 0:
                display.set_pixel(2, current_y, 0)
                current_y -= 1
                if current_y < 0:
                    current_y = 0
            display.set_pixel(2, current_y, 5)

    
        if a_clicks == 1 and b_clicks == 1:  # Start the timer when the first click is made
            start_time = running_time()
    
        if a_clicks >= total_clicks // 2 and b_clicks >= total_clicks // 2:
            end_time = running_time()
            score = int((end_time - start_time) / 1000)  # Convert to seconds
            display.scroll("SCORE: " + str(score))
            break