import time, math, random, logging
import arcade
import arcade.gl
from pathlib import Path
from array import array

from ....core.shader.program import ShaderProgram


log = logging.getLogger(__name__)


class VectorFieldShader(ShaderProgram):
    VERT = Path(__file__).parent / "shaders" / "vector_field_vert.glsl"
    FRAG = Path(__file__).parent / "shaders" / "vector_field_frag.glsl"

    def __init__(self, window):
        super().__init__(window)
        self.window.ctx.enable_only(self.window.ctx.BLEND)
        self.vector_field = None
        self.entity_list = None

        # self.program["resolution"] = self.window.get_size()
        self.program["time"] = time.time()
        # self.program["mouse"] = self.window.mouse_position

        self.hotload()

    def set_entity_list(self, entity_list):
        self.entity_list = entity_list

    def update(self, dt):
        self.program["time"] += dt
        # self.program["mouse"] = self.window.mouse_position
        # self.program["resolution"] = self.window.get_size()

        self.vao = self.make_visual_vectors(self.entity_list)

    def draw(self):
        if self.vao:
            log.debug("Drawing vector field")
            self.vao.render(self.program, mode=self.window.ctx.LINES)

    def make_visual_vectors(self, entity_list):
        """Create a list of velocity vectors for each entity in the entity list."""

        def _gen_vectors():
            for entity in entity_list:
                yield entity.velocity[0]
                yield entity.velocity[1]
                yield entity.center_x
                yield entity.center_y

        buffer = self.window.ctx.buffer(data=array("f", _gen_vectors()))
        buffer_description = arcade.gl.BufferDescription(
            buffer,
            "2f 2f",
            ["in_vel", "in_pos"],
        )
        vao = self.window.ctx.geometry([buffer_description])

        return vao
