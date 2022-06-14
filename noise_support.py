from talon import Module, actions, noise

noise_module = Module()

@noise_module.action_class
class NoiseActions:
    def noise_pop():
        """Invoked when the user does the pop noise."""
        pass

    def noise_hiss_start():
        """Invoked when the user starts hissing (potentially while speaking)"""
        pass

    def noise_hiss_stop():
        """Invoked when the user finishes hissing (potentially while speaking)"""
        pass

def  pop_handler(blah):
    actions.user.racer_gas_toggle()
    
def hiss_handler(active):
    if active: 
        print('s')
        #actions.key('shift')
        if actions.user.get_racer_direction() == 'clockwise' or actions.user.get_racer_direction() == 'counterclockwise':
            actions.user.racer_turn_start()
            actions.user.racer_gas()
        elif actions.user.get_racer_direction() == 'straight':
            actions.user.racer_gas()

    else:
        print('done')
        actions.user.racer_turn_stop()
        actions.user.racer_brakes()



#def hiss_handler(active):
#    if active:
#        actions.user.noise_hiss_start()
#    else:
#        actions.user.noise_hiss_stop()

#noise.register("pop", pop_handler)
noise.register("hiss", hiss_handler)


def on_pop(active):
    print('pop')


noise.register("pop", on_pop)





