#!/bin/env python3

from copy import copy

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from numpy import matrix as mat
from transform import rotate_transform as rot, scale_transform as sca, translate_transform as tra
from camera import viewing_transform as cam

import obj_read

class Props(object):
    pass

class Screen(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()

        self.connect('draw', self.on_expose)
        self.tick_timeout = GObject.timeout_add(17, self.tick, None)
    
    def tick(self, e):
        self.queue_draw_area(0, 0, self.get_allocation().width, self.get_allocation().height)
        
        # Will redo tick in 50 ms
        return True

    def on_expose(self, wid, cr):
        self.cr = cr
        self.draw(*self.window.get_size())

class MyCube(Screen):
    def __init__(self):
        super().__init__()
        self.props = Props()
        self.props.angle = 0
        self.props.model = obj_read.ObjReader(sys.argv[1])

    def draw(self, w, h):
        angle = self.props.angle
        cr = self.cr
        
        cr.set_source_rgb(0.0, 0.5, 0.8)
        cr.translate(w/2, h/2)
        cr.set_line_width(2.5)

        # Vertices
        points = copy(self.props.model.vertices)
        edges = copy(self.props.model.edges)

        # Rotate and push back
        for i in range(len(points)):
            points[i] = points[i] * tra(0, 0, -10) * tra(-self.props.model.origin[0], -self.props.model.origin[1], -self.props.model.origin[2]) * rot(0, angle, 0)    
        # Perspective projection
        dpts = []
        for point in points:
            proj = point * cam(30, w/h, 1.0, 10.0)
            dpts.append([proj[0,0]/proj[0,3], proj[0,1]/proj[0,3]])
        
        
        for edge in edges:
            try:
                cr.move_to(dpts[edge[0]][0], dpts[edge[0]][1])
                cr.line_to(dpts[edge[1]][0], dpts[edge[1]][1])
            except:
                print("BLARGH: edge[0]: %d  edge[1]: %d  len(dpts): %d" % (edge[0], edge[1], len(dpts)))
                raise

        cr.stroke()

        self.props.angle += 1

def run(Widget):
    print('Running %s' % Widget.__name__)

    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit )
    window.set_size_request(400, 400)
    widget = Widget()
    widget.window = window
    widget.show()
    window.add(widget)
    window.present()
    Gtk.main()

run(MyCube)
