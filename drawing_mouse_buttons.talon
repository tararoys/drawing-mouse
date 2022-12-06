tag: user.drawing_mouse_buttons
mode: user.drawing

-

touch:
	mouse_click(0)
	# close the mouse grid if open
	user.grid_close()
    	# End any open drags
	# Touch automatically ends left drags so this is for right drags specifically
	user.mouse_drag_end()

righty:
	mouse_click(1)
	# close the mouse grid if open
	user.grid_close()

midclick:
	mouse_click(2)
	# close the mouse grid
	user.grid_close()

#see keys.py for modifiers.
#defaults
#command
#control
#option = alt
#shift
#super = windows key
<user.modifiers> touch:
	key("{modifiers}:down")
	mouse_click(0)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
<user.modifiers> righty:
	key("{modifiers}:down")
	mouse_click(1)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
(dubclick | duke):
	mouse_click()
	mouse_click()
	# close the mouse grid
	#user.grid_close()
(tripclick | triplick):
	mouse_click()
	mouse_click()
	mouse_click()
	# close the mouse grid
	user.grid_close()
left drag | drag:
	user.mouse_drag(0)
	# close the mouse grid
	user.grid_close()
right drag | righty drag:
	user.mouse_drag(1)
	# close the mouse grid
	user.grid_close()
end drag | drag end:
    user.mouse_drag_end()
copy mouse position: user.copy_mouse_position()
curse no:
    # Command added 2021-12-13, can remove after 2022-06-01
    app.notify("Please activate the user.mouse_cursor_commands_enable tag to enable this command")
^press <user.keys>$: key(keys)