from array import array
from operator import truediv
from talon import Module, Context, canvas, ctrl, cron, ui, actions, app
from talon.types import Point2d

from math import atan2, sin, cos, pi
import time
from random import randrange, normalvariate, choice
from talon import skia

import numpy as np

racer = Module()

racer_direction = "straight"
racer_turns_cw = True
racer_current_speed = 0.0
racer_turning = False
racer_speed = 25
frame_rate = 25

racer_turn_start_time = 0

racer_position = Point2d(0, 0)
racer_angle    = 0.0

racer_tick_job = None

racer_random_mode = False

last_input_time = 0
end_time = 0

turning_radius = 50

turning_radius_curve_array = []
racer_precision_turn_mode = False
fraction = 0
precision_curve_array =[]
starting_point = None
starting_angle = 0

is_dragging = False

def had_input():
    global last_input_time
    last_input_time = time.time() 


racer.list("point_of_compass", desc="point of compass for race car")


ctx = Context()

direction_name_steps = [
        "east", "east south east", "south east", "south south east",
        "south", "south south west", "south west", "west south west",
        "west", "west north west", "north west", "north north west",
        "north", "north north east", "north east", "east north east" ] 

ctx.lists["self.point_of_compass"] = {
            word: str(idx * pi * 2 / len(direction_name_steps)) for (idx, word) in enumerate(direction_name_steps)
        } 


def racer_tick_cb():
    global racer_position
    global racer_angle

    global racer_turning
    global racer_turns_cw
    global is_dragging
    global turning_radius

    #racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)

    # if racer_random_mode:
    #     if racer_turning == False and randrange(0, 1000) < 10:
    #         racer_turning = max(0, normalvariate(1, 0.3))
    #         racer_turns_cw = choice([True, False])
    #     if racer_turning != False and randrange(0, 1000) < 15:
    #         racer_turns_cw = normalvariate(5, 2) * choice([-1, 1])

    if isinstance(racer_turning, float): 
        racer_turning -= 1 / 40
        if racer_turning <= 0:
            racer_turning = False

    if isinstance(racer_turns_cw, float): 
        if racer_turns_cw < 0:
            racer_turns_cw += 1 / 40
            if racer_turns_cw >= 0:
                racer_turns_cw = False
        else:
            racer_turns_cw -= 1 / 40
            if racer_turns_cw >= 0:
                racer_turns_cw = True

    if racer_current_speed > 0.0 and racer_turning is False:
        racer_position += Point2d(cos(racer_angle), sin(racer_angle)) * racer_current_speed 
        racer_canvas.move(racer_position.x, racer_position.y)
        ctrl.mouse_move(racer_position.x + 2500, racer_position.y + 2500)
    
    if racer_turning and racer_turn_start_time < time.time() - 0.1:
        x = turning_radius*cos(pi/2 + racer_angle) + turning_radius*cos(racer_current_speed/turning_radius-pi/2+racer_angle)
        y = turning_radius*sin(pi/2 + racer_angle) + turning_radius*sin(racer_current_speed/turning_radius-pi/2+racer_angle)
        print(x)
        print(y)
        racer_position = Point2d(racer_position.x + x, racer_position.y + y)
        racer_canvas.move(racer_position.x, racer_position.y)
        ctrl.mouse_move(racer_position.x + 2500, racer_position.y + 2500)
        if racer_turns_cw:
            racer_angle -=  racer_current_speed / turning_radius
            #racer_angle -= .1 # This is in radians.
        else:
            racer_angle +=  racer_current_speed / turning_radius
            #racer_angle += .1 # This is in radians. 
        
    racer_canvas.show()

    if racer_position.x + 2500 < 0:
        racer_angle = vertical_edge_change_angle(racer_angle, True)
        racer_position.x = -2500 # avoid geting stuck at edge
    if racer_position.x + 2500 >= ui.screens()[0].rect.width:
        racer_angle = vertical_edge_change_angle(racer_angle, False)
        racer_position.x = ui.screens()[0].rect.width - 1 - 2500
    if racer_position.y + 2500 < 0:
        racer_angle = horizontal_edge_change_angle(racer_angle, True)
        racer_position.y =  -2500 #avoid getting stuck at the edge
    if racer_position.y + 2500  >= ui.screens()[0].rect.height: 
        racer_angle = horizontal_edge_change_angle(racer_angle, False)
        racer_position.y = ui.screens()[0].rect.height - 1 - 2500 
    if is_dragging:
        actions.mouse_drag(0) 

    if last_input_time + 245 < time.time():
        if racer_random_mode:
            if choice([True, False, False, False, False, False, False]):
                actions.user.racer_stop()
        else:
            actions.user.racer_stop()
            app.notify("car stopped after 245s of inactivity")
    
    # code for curve command
    global fraction
    global end_time
    global starting_angle
    global precision_curve_array
    global starting_point
    global starting_angle

    if racer_precision_turn_mode:
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)

        end_time = last_input_time + 2000 # hardcoded one second from the beginning of the command
        now_time = time.time()


        current_index_percent = int((now_time - last_input_time)/4*100) 
        counter_clockwise_turn = list(reversed(precision_curve_array[ len(precision_curve_array)-fraction: len(precision_curve_array)-1]))
        clockwise_turn = list(precision_curve_array[0:fraction-1])
        current_index = 0

        if racer_turns_cw is True:
            current_index = int((len(counter_clockwise_turn) * current_index_percent)/100)      
            racer_angle = starting_angle - pi/180 * current_index

            ctrl.mouse_move(starting_point.x + 2500 + int(counter_clockwise_turn[current_index].x), starting_point.y + 2500 +  int(counter_clockwise_turn[current_index].y))
            racer_canvas.move(starting_point.x + counter_clockwise_turn[current_index].x,  starting_point.y +  counter_clockwise_turn[current_index].y)
        else:
            #racer_angle += pi/100
            current_index = int((len(counter_clockwise_turn) * current_index_percent)/100)
            #current_index = int((len(clockwise_turn) * current_index_percent)/100)     
            racer_angle = starting_angle + pi/180 * current_index
            ctrl.mouse_move(starting_point.x + 2500 + int(clockwise_turn[current_index].x), starting_point.y + 2500 +  int(clockwise_turn[current_index].y))
            racer_canvas.move(starting_point.x + clockwise_turn[current_index].x,  starting_point.y +  clockwise_turn[current_index].y)
        if is_dragging:
            actions.mouse_drag(0)
    
     
  

racer_canvas = None 
def on_mouse():
    racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500) 
    racer_canvas.move(racer_position.x, racer_position.y)


def racer_canvas_draw(canvas):
    global turning_radius
    global turning_radius_curve_array
    paint = canvas.paint
    global racer_speed
    global frame_rate
    global racer_direction

    paint.color = "00000000"

    canvas.translate(2500, 2500)
    canvas.translate(canvas.x, canvas.y)

    xpx = cos(-racer_angle + pi/2)
    ypx = -sin(-racer_angle + pi/2)

    xpy = sin(-racer_angle + pi/2)
    ypy = cos(-racer_angle + pi/2)

    paint.color = "ff0000ff"
    paint.stroke_width = 4
    canvas.draw_points(canvas.PointMode.POLYGON,
            [Point2d(0, 0),
                Point2d(-16 * xpx + -32 * xpy, -16 * ypx + -32 * ypy),
                Point2d(-20 * xpy, -20 * ypy),
                Point2d(16 * xpx - 32 * xpy, 16 * ypx - 32 * ypy),
                Point2d(0, 0)])
    rect = canvas.rect
    cx, cy = rect.center

    turning_radius_curve_array=[]

    if racer_turns_cw is True: 
        if racer_direction == "clockwise":
            paint.color = "00ff00ff"
        else: 
            paint.color = "ff0000ff"
        for x in np.arange( pi , 5*pi/2 , pi/180):
            turning_radius_curve_array.append(Point2d(( (turning_radius * cos(x)) * cos(racer_angle) - (turning_radius * sin(x) - turning_radius) * sin(racer_angle)), turning_radius * cos(x) * sin(racer_angle) + (turning_radius*sin(x) - turning_radius) * cos(racer_angle)))
    else:
        if racer_direction == "counterclockwise":
            paint.color = "00ff00ff"
        else: 
            paint.color = "ff0000ff"
        for x in np.arange( 3*pi/2, 6*pi/2 , pi/180):
            turning_radius_curve_array.append(Point2d(( (turning_radius * cos(x)) * cos(racer_angle) - (turning_radius * sin(x) + turning_radius) * sin(racer_angle)), turning_radius * cos(x) * sin(racer_angle) + (turning_radius*sin(x) + turning_radius) * cos(racer_angle)))


    canvas.draw_points(canvas.PointMode.POLYGON,
            turning_radius_curve_array)

    if racer_direction =="straight":
        paint.color = "00ff00ff"
    else:
        paint.color = "ff0000ff"
    canvas.draw_line(0,0, 5000*cos(racer_angle), 5000*sin(racer_angle))
    canvas.paint.textsize=20
    canvas.paint.text_align = 'center'
    for x in range(50):
        canvas.draw_line(racer_speed*frame_rate*x*cos(racer_angle), racer_speed*frame_rate*x*sin(racer_angle), racer_speed*frame_rate*x*cos(racer_angle)-50*sin(racer_angle), racer_speed*frame_rate*x*sin(racer_angle) + 50*cos(racer_angle))
        canvas.draw_text(str(x), racer_speed*frame_rate*x*cos(racer_angle)-60*sin(racer_angle), racer_speed*frame_rate*x*sin(racer_angle) + 60*cos(racer_angle))

    

    #paint.color = "ffff00ff"
    #canvas.draw_line(0,0, -5000*cos(racer_angle), -5000*sin(racer_angle))
 
    #canvas.paint.textsize=20
    #canvas.paint.text_align = 'center'
    #for x in range(50):
    #    canvas.draw_line(100*-x*cos(racer_angle), 100*-x*sin(racer_angle), 100*-x*cos(racer_angle)-50*sin(racer_angle), 100*-x*sin(racer_angle)+50*cos(racer_angle))
    #    canvas.draw_text(str(-x), 100*-x*cos(racer_angle)-60*sin(racer_angle), 100*-x*sin(racer_angle)+60*cos(racer_angle))



    #canvas.draw_points(canvas.PointMode.POLYGON, precision_curve_array)

    direction = 1 if racer_turns_cw else -1

    canvas.draw_line(-4 * xpy, -4 * ypy, 16 * xpx * direction - 8 * xpy, 16 * ypx * direction - 8 * ypy)

def vertical_edge_change_angle(angle : float, left : bool) -> float:
    """Change the angle after colliding with vertical edge"""
    dx = cos(angle)
    dy = sin(angle)
    if left and dx < 0 or not left and dx > 0:
        dx = - dx
        angle = atan2(dy, dx)
    return angle

def horizontal_edge_change_angle(angle : float, top : bool) -> float:
    """Change the angle after colliding with horizontal edge"""
    dx = cos(angle)
    dy = sin(angle)
    if top and dy < 0 or not top and dy > 0:
        dy = - dy
        angle = atan2(dy, dx)


    return angle

@racer.action_class
class RacerActions:
    def racer_start():
        """Starts the "racing" mouse mode"""
        global racer_canvas
        global racer_position
        global racer_tick_job
        global job
        global racer_current_speed
        global frame_rate

        had_input()

        if racer_canvas is None:
            racer_canvas = canvas.Canvas(0, 0, 5000,5000)
            racer_canvas.move(racer_position.x, racer_position.y)
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        #^racer_position = Point2d(ui.screens()[0].rect.width / 2, ui.screens()[0].rect.height / 2)
        # racer_position = Point2d(5, 5)
        racer_canvas.move(racer_position.x, racer_position.y)
        racer_canvas.register("draw", racer_canvas_draw)
        racer_canvas.register("mousemove", on_mouse)  
        if racer_tick_job:
            cron.cancel(racer_tick_job)
        timing = str(int(1000/frame_rate))+"ms"
        racer_tick_job = cron.interval(timing, racer_tick_cb)
        racer_canvas.show() 
        # racer_canvas.freeze()
        job = cron.interval('16ms', on_mouse)

    def racer_stop():
        """Stops the "racing" mouse mode"""
        cron.cancel(racer_tick_job)
        cron.cancel(job)
        actions.mouse_release()
        racer_canvas.unregister("draw", racer_canvas_draw)
        racer_canvas.unregister("mousemove", on_mouse)
        racer_canvas.hide()

    def racer_random(activate: int = -1):
        """Activate or deactivate or toggle the random turn mode"""
        global racer_random_mode
        had_input()
        if activate == -1:
            racer_random_mode = not racer_random_mode
        else:
            racer_random_mode = activate != 0
        if racer_random_mode:
            actions.user.racer_gas_toggle()

    def racer_set_direction_in_compass_degrees(direction: str):
        """Set the direction to a value in compass degrees"""
        global racer_angle
        had_input()

        racer_angle = (float(direction)*(2*pi/360)) - pi/2

    def racer_left_x_degrees(direction: str):
        """Rotate left/counterclockwise x degrees"""
        global racer_angle
        had_input()
 
        racer_angle = racer_angle - (float(direction)*(2*pi/360)) 

    def racer_right_x_degrees(direction: str):
        """Rotate right/lockwise x degrees"""
        global racer_angle
        had_input()
        racer_angle = racer_angle +  (float(direction)*(2*pi/360))

    def racer_set_compass_direction(direction: str):
        """Set the direction to a value in radians"""
        global racer_angle
        had_input()
        racer_angle = (float(direction))
    
    def racer_turn_true():
        """Starts turning the "car" As opposed to going straight."""
        global racer_turns_cw
        global racer_direction
        if racer_turns_cw is True:
            racer_direction = "clockwise"
        else:
            racer_direction = "counterclockwise"

    def racer_turn_start():
        """Starts turning the "car"."""
        global racer_turning
        global racer_turn_start_time
        racer_turn_start_time = time.time()
        had_input()
        racer_turning = True

    def racer_turn_stop():
        """Stops turning the "car"."""
        global racer_turning
        had_input()
        #if racer_turn_start_time >= time.time() - 0.1: This code allowed you to use a short hiss to switch directions, but it was beng activated when I said 'radius up' so it is commented out
            #actions.user.racer_flip_turn_direction()
        #else:
        #    print("hmm")
        racer_turning = False

    def racer_flip_turn_direction():
        """Changes rotation from CW to CCW and back"""
        global racer_turns_cw
        global racer_direction
        had_input()
        racer_turns_cw = not racer_turns_cw
        if racer_direction is "clockwise":
            racer_direction = "counterclockwise"
        elif racer_direction is "counterclockwise":
            racer_direction = "clockwise"
        else:
            racer_direction = "straight"


    def racer_turns_clockwise():
        """Set turning direction to clockwise"""
        global racer_turns_cw
        global racer_direction 
        racer_direction = 'clockwise'
        had_input
        racer_turns_cw = True
        

    def racer_turns_counterclockwise():
        """Set turning direction to counterclockwise"""
        global racer_turns_cw
        global racer_direction 
        racer_direction = "counterclockwise"
        had_input()
        racer_turns_cw = False

    def racer_goes_straight():
        """set racer to go straight ahead"""
        global racer_direction 
        racer_direction = "straight"

    def get_racer_direction():
        """get the current racer direction.  options are  a choice between the strings 'clockwise, 'counterclockwise', and 'straight'"""
        global racer_direction
        return racer_direction
 

    def racer_nudge():
        """Drives the car forward a tiny bit"""
        global racer_current_speed
        had_input()
        racer_current_speed = 0.1
        def reset():
            global racer_current_speed
            racer_current_speed = 0.0
        cron.after("500ms", reset)

    def racer_gas():
        """Start driving forward"""
        global racer_current_speed
        global racer_position
        global racer_speed
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        racer_current_speed = racer_speed


    def racer_brakes():
        """stop driving"""
        global racer_current_speed
        global racer_position
        racer_current_speed = 0
        

    def racer_gas_toggle():
        """Switch between driving and stopped"""
        global racer_current_speed
        global racer_position
        global racer_speed
        had_input()
        if racer_current_speed == 0.0:
            racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
            racer_current_speed = racer_speed
        else:
            racer_current_speed = 0.0

    def racer_turbo_toggle():
        """Switch between driving TURBO DRIVING"""
        global racer_current_speed
        global racer_speed
        global racer_position
        had_input()
        if racer_current_speed == racer_speed:
            racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
            racer_current_speed = racer_speed*racer_speed
        else:
            racer_current_speed = racer_speed

    def racer_reverse():
        """Turn the racer around 180 degrees"""
        global racer_angle
        global racer_position
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        racer_angle += pi
        had_input()

    def int_to_float(seconds:int):
        """turn an int to a float"""
        return float(seconds)

    def set_turning_radius(number:int):
        """set turning radius"""
        global turning_radius
        turning_radius = number*10

    def increase_turning_radius(number:int):
        """increase turning radius"""
        global turning_radius
        turning_radius = turning_radius + number * 10

    def decrease_turning_radius(number:int):
        """decrease turning radius"""
        global turning_radius
        turning_radius = turning_radius - number*10

    def drive_forward_x_seconds(seconds:str):
        """drive the mouse forward a certain number of inches"""
        global racer_current_speed
        global racer_position
        global racer_speed
        time = str(int(float(seconds)*1000)) + "ms"


        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        had_input()
        #time = str(seconds*1000)+"ms"
        racer_current_speed = racer_speed
        def reset():
            global racer_current_speed
            racer_current_speed = 0.0
        cron.after(time, reset)

    def skip_forward_x_inches(seconds:int):
        """drive the mouse forward a certain number of inches"""
        global racer_current_speed
        global racer_position
        global racer_canvas
        seconds = float(seconds)
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        racer_position += Point2d(cos(racer_angle)*seconds*racer_speed*frame_rate, sin(racer_angle)*seconds*racer_speed*frame_rate)
        racer_canvas.move(racer_position.x, racer_position.y)
        ctrl.mouse_move(racer_position.x +2500, racer_position.y +2500)

    def skip_backward_x_inches(seconds:str):
        """drive the mouse forward a certain number of inches"""
        global racer_current_speed
        global racer_position
        global racer_canvas
        seconds = float(seconds)
        racer_position = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        racer_position += Point2d(cos(racer_angle)*-seconds*racer_speed*frame_rate, sin(racer_angle)*-seconds*racer_speed*frame_rate)
        racer_canvas.move(racer_position.x, racer_position.y)
        ctrl.mouse_move(racer_position.x +2500, racer_position.y +2500)

    def drive_along_curve(degrees:int):
        """drive the mouse along a curve"""
        global turning_radius_curve_array
        global racer_position 
        global racer_angle
        global racer_turns_cw
        global precision_curve_array
        global fraction
        global racer_precision_turn_mode 
        global starting_point
        global starting_angle

        starting_point = Point2d(actions.mouse_x() - 2500, actions.mouse_y() - 2500)
        starting_angle = racer_angle
        precision_curve_array = turning_radius_curve_array
        racer_precision_turn_mode = True
        fraction = int(degrees)
        if is_dragging:
            actions.mouse_drag(0)
        def reset():
            global racer_precision_turn_mode
            racer_precision_turn_mode = False

        had_input()
        end_time =  "4000ms"
        cron.after(end_time, reset)

    def drive_forward_x_deciseconds(deciseconds:int):
        """drive the mouse forward a certain number of inches"""
        global racer_current_speed
        global racer_position
        global racer_speed
        had_input() #starting time 
        time = str(deciseconds*100)+"ms" #stopping time
        racer_current_speed = racer_speed
        def reset():
            global racer_current_speed
            racer_current_speed = 0.0
        cron.after(time, reset)

    def pen_down():
        """puts the pencil down"""
        global is_dragging
        is_dragging = True

    def pen_up():
        """picks the pencil up"""
        global is_dragging
        is_dragging = False

    def set_racer_speed(speed: int): 
        """sets the speed of the mouse as it drives forward."""
        global racer_speed
        racer_speed = speed

    def increase_racer_speed(speed: int): 
        """increases the speed of the mouse as it drives forward."""
        global racer_speed
        racer_speed += speed
    
    def decrease_racer_speed(speed: int): 
        """decreases the speed of the mouse as it drives forward."""
        global racer_speed
        if (racer_speed - speed) >= 0:  
            racer_speed -= speed
        else:
            racer_speed = 0
    
# inkscape stuff: 
racer.tag("inkscape", desc="tag for enabling inkscape commands in drawing mode") 