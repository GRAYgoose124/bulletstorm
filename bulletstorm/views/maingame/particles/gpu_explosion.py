"""
From https://api.arcade.academy/en/stable/tutorials/gpu_particle_burst/index.html
GPU Particle Burst
"""
from pathlib import Path
import random
import time
import math
from array import array
from dataclasses import dataclass
import arcade
import arcade.gl

from .shaders.base import ShaderProgram

PARTICLE_COUNT = 300

MIN_FADE_TIME = 0.25
MAX_FADE_TIME = 1.5


@dataclass
class Burst:
    """Track for each burst."""

    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class GpuBurst(ShaderProgram):
    VERT = Path(__file__).parent / "shaders" / "gpu_explosion_vert.glsl"
    FRAG = Path(__file__).parent / "shaders" / "gpu_explosion_frag.glsl"

    def __init__(self, window):
        self.window = window
        self.burst_list = []

        # Program to visualize the points
        self.program = None
        self.hotload()

        self.window.ctx.enable_only(self.window.ctx.BLEND)

    def draw(self):
        # Set the particle size
        self.window.ctx.point_size = 2 * self.window.get_pixel_ratio()

        # Loop through each burst
        for burst in self.burst_list:
            # Set the uniform data
            self.program["time"] = time.time() - burst.start_time

            # Render the burst
            burst.vao.render(self.program, mode=self.window.ctx.POINTS)

    def update(self, dt):
        """Update game"""

        # Create a copy of our list, as we can't modify a list while iterating
        # it. Then see if any of the items have completely faded out and need
        # to be removed.
        temp_list = self.burst_list.copy()
        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
                self.burst_list.remove(burst)

    def make_explosion(self, x: float, y: float, count=PARTICLE_COUNT):
        """User clicks mouse"""

        def _gen_initial_data(initial_x, initial_y):
            """Generate data for each particle"""
            for i in range(count):
                angle = random.uniform(0, 2 * math.pi)
                speed = abs(random.gauss(0, 1)) * 0.5
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.5, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)

                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # Recalculate the coordinates from pixels to the OpenGL system with
        # 0, 0 at the center.
        x2 = x / self.window.width * 2.0 - 1.0
        y2 = y / self.window.height * 2.0 - 1.0

        # Get initial particle data
        initial_data = _gen_initial_data(x2, y2)

        # Create a buffer with that data
        buffer = self.window.ctx.buffer(data=array("f", initial_data))

        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(
            buffer, "2f 2f 3f f", ["in_pos", "in_vel", "in_color", "in_fade_rate"]
        )
        # Create our Vertex Attribute Object
        vao = self.window.ctx.geometry([buffer_description])

        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)


def make_explosion(target, count=PARTICLE_COUNT, screen_origin=(0, 0)):
    """Create a new explosion"""
    target.manager.parent.shaders["GpuBurst"].make_explosion(
        target.position[0] + screen_origin[0],
        target.position[1] + screen_origin[1],
        count,
    )
