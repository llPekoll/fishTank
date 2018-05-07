import pyglet.gl import *
import pyglet


window = pyglet.window.Window(fullscren=True)
target_resolution = 320, 200
class Aquarium():
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.texture = pyglet.image.Texture.create(width, height)




def draw_scene():
    glClearColor(0.7, 0.6, 0.5)
    glClear(GL_COLOR_BUFFER_BIT)


pyglet.clock.schedule_interval(update,1/60.)


@window.event
def on_draw():
    viewport.begin()
    window.clear()
    draw_scene()
    viewport.end()

pyglet.app.run()


