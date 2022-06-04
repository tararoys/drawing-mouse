from typing import Tuple


from talon import Context, Module, canvas, cron, ctrl, cron
from talon.skia import Shader, Color, Paint, Rect
from math import atan2, sin, cos, pi
from talon.types import Point2d

import numpy as np


class CompassMouseGuide:
    def __init__(self, width: float, height: float):
        self.enabled = False
        self.canvas = None
        self.job = None
        self.last_pos = None
        self.width = width
        self.height = height

    def enable(self):
        if self.enabled:
            return
        self.enabled = True
        self.last_pos = None
        self.canvas = canvas.Canvas(0, 0, self.width + 2, self.height + 2)
        self.check_mouse()
        self.canvas.register('mousemove', self.on_mouse)
        self.canvas.register('draw', self.draw_canvas)
        self.canvas.freeze()
        # uncomment this if the mouse movement event isn't working
        self.job = cron.interval('16ms', self.check_mouse)

    def disable(self):
        if not self.enabled:
            return
        cron.cancel(self.job)
        self.enabled = False
        self.canvas.close()
        self.canvas = None

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()



    def draw_canvas(self, canvas):
        paint = canvas.paint
        paint.color = 'fff'
        rect = canvas.rect

        SMALL_DIST   = 5
        SMALL_LENGTH = 10
        LARGE_DIST   = 25
        LARGE_LENGTH = 30
        irange = lambda start, stop, step: range(int(start), int(stop), int(step))
        paint.antialias = False
        #for off, color in ((0, 'ffffffff'), (1, '000000ff')):
        paint.color = 'ffffffff'

        # draw axis lines
        cx, cy = rect.center
        #cxo = cx + off
        #cyo = cy + off

        # draw circle 

        paint.color="ff0000ff"
        canvas.paint.style = Paint.Style.STROKE
        canvas.paint.stroke_width = 2
        #canvas.draw_path(canvas.rect,[Point2d(0,0)] )


        for x in np.arange(0.0,2*pi,pi/12):
            canvas.draw_line(cx+250*cos(x), cy + 250*sin(x), cx + 200 * cos(x), cy + 200*sin(x))

        canvas.paint.textsize=20
        canvas.paint.text_align = 'center'
        for x in irange(0, 360, 15):
            canvas.draw_text(str(x), cx + 200 * cos(x *pi/180-pi/2), cy + 200*sin(x*pi/180-pi/2))

        #N
        canvas.draw_line(cx-250* cos(pi/2), cy - sin(pi/2) * 250, cx - 200*cos(pi/2), cy - 200 * sin(pi/2))


        #NE
        canvas.draw_line(cx + 250*.7071067, cy - .7071067 * 250, cx + 200*.707106, cy - 200 * .707106)

        #E
        canvas.draw_line(cx + 250*1, cy + 0 * 250, cx + 200*1, cy + 200 * 0)

        #SE

        canvas.draw_line(cx + 250*.7071067, cy + .7071067 * 250, cx + 200*.707106, cy + 200 * .707106)

        #S

        canvas.draw_line(cx-250*0, cy + 1 * 250, cx - 200*0, cy + 200 * 1)

        #SW

        canvas.draw_line(cx - 250*.7071067, cy + .7071067 * 250, cx - 200*.707106, cy + 200 * .707106)

        #W
        canvas.draw_line(cx-250*1, cy - 0 * 250, cx - 200*1, cy - 200 * 0)

        #Nw
        canvas.draw_line(cx-250*.7071067, cy - .7071067 * 250, cx - 200*.707106, cy - 200 * .707106)

        canvas.draw_circle( cx, cy, 250)

        canvas.paint.textsize = 60
        canvas.paint.text_align = 'center'

        canvas.draw_text('N', cx, cy - 260)
        canvas.draw_text('E', cx + 270, cy + 20)
        canvas.draw_text('S', cx , cy + 300)
        canvas.draw_text('W', cx - 280, cy + 20)

        canvas.paint.textsize = 30

        canvas.draw_text('NE', cx + 270 * .7071067, cy - 270 * .7071067)
        canvas.draw_text('SE', cx + 280 * .7071067, cy + 280 * .7071067)
        canvas.draw_text('SW', cx - 280 * .7071067, cy + 280 * .7071067)
        canvas.draw_text('NW', cx - 270 * .7071067, cy - 270 * .7071067)


        canvas.paint.textsize = 20
        #draw hashmarks
        #for x in irange(0, 45, 1):

            #draw ticks
           # for tick_dist, tick_length in ((SMALL_DIST, SMALL_LENGTH),
           #                                (LARGE_DIST, LARGE_LENGTH)):
           #     half = tick_length // 2
                # ticks to the left
           #     for x in irange(rect.left + off, cx - tick_dist + 1, tick_dist):
           #         canvas.draw_line(x, cy - half, x, cy + half)
                # ticks to the right
           #     for x in irange(cxo + tick_dist - 1, rect.right + 1, tick_dist):
           #         canvas.draw_line(x, cy - half, x, cy + half)
               # ticks above
           #     for y in irange(rect.top + off + 1, cy - tick_dist + 1, tick_dist):
           #         canvas.draw_line(cx - half, y, cx + half, y)
               # ticks below
           #     for y in irange(cyo + tick_dist, rect.bot + 1, tick_dist):
           #         canvas.draw_line(cx - half, y, cx + half, y)
            

    def on_mouse(self, event):
        self.check_mouse()

    def check_mouse(self):
        pos = ctrl.mouse_pos()
        if pos != self.last_pos:
            x, y = pos
            self.canvas.move(x - self.width // 2, y - self.height // 2)
            self.last_pos = pos

compass_mouse_guide = CompassMouseGuide(620, 620)

mod = Module()

@mod.action_class
class Actions:
    def compass_mouse_guide_enable():
        """Enable relative compass mouse guide"""
        compass_mouse_guide.enable()

    def compass_mouse_guide_disable():
        """Disable relative compass mouse guide"""
        compass_mouse_guide.disable()

    def compass_mouse_guide_toggle():
        """Toggle relative compass mouse guide"""
        compass_mouse_guide.toggle()


ctx = Context()

