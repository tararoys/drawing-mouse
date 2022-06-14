
mode: user.drawing 

-

tag(): user.drawing_mouse_buttons

start your engine: 
	# start your engine is the command to make the racecar mouse cursor appear
	user.racer_start()
park the car : 
	# [in order to turn off the mouse cursor]
	user.racer_stop()



car reverse  :
	# [in order to make the car go in the opposite direction] 
	user.racer_reverse()

skip <number_small> [point <digits>]:
	number = "{number_small}.{digits}" or "{number_small}"
	user.skip_forward_x_inches(number)

back <number_small> [point <digits>]:
	number = "{number_small}.{digits}" or "{number_small}"
	user.skip_backward_x_inches(number)

left | counter clockwise | counter  | port: 
	user.racer_turns_clockwise()

right | clockwise | clock | starboard: 
	user.racer_turns_counterclockwise()

straight | ahead :
	user.racer_goes_straight()

turn <number> [degrees]: 
	user.drive_along_curve(number)


drive <number_small> [point <digits>]:
	number = "{number_small}.{digits}" or "{number_small}"
	user.drive_forward_x_seconds(number)




radius up <number_small>: 
	user.increase_turning_radius(number_small)
 
radius down <number_small>: 
	user.decrease_turning_radius(number_small)
	
<number> : user.racer_set_direction_in_compass_degrees("{number}")

left <number> : user.racer_left_x_degrees("{number}")

right <number> : user.racer_right_x_degrees("{number}")



compass {user.point_of_compass}: 
	# [ to make the car point in one or the cardinal or ordinal directions north northeast east southeast south southwest west northwest]
	user.racer_set_compass_direction(point_of_compass)




drawing mode off:
	mode.enable("command")
	mode.disable("user.drawing")
	user.racer_stop()
	user.compass_mouse_guide_disable()



