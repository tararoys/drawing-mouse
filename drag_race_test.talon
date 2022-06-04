test this thing:
    x = mouse_x()
    y = mouse_y()
    mouse_drag(0)
    
    
    new_x = x + 100
    new_y = y + 0
    mouse_move(new_x,new_y)
    mouse_drag(0)
    
    sleep(1000ms)
    new_x = new_x + 100
    new_y = new_y + 100
    mouse_move(new_x,new_y)
    mouse_drag(0)
    
    sleep(1000ms)
    new_x = new_x + 0
    new_y = new_y + 100
    mouse_move(new_x,new_y)
    mouse_drag(0)
    
    sleep(1000ms)
    new_x = new_x - 200
    new_y = new_y - 200
    mouse_move(new_x,new_y)
    mouse_drag(0)
    mouse_release(0)




