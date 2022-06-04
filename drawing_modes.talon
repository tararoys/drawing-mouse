not mode: sleep

-

drawing mode:
	mode.disable("sleep")
    mode.disable("command")
    mode.disable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
    mode.enable("user.drawing")
    user.racer_start()
    user.compass_mouse_guide_enable()


drawing mode off:
	mode.enable("command")
	mode.disable("user.drawing")
	user.racer_stop()
	user.compass_mouse_guide_disable()

