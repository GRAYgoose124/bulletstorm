from pathlib import Path
import arcade
import numpy as np

from ....core.shader.program import ShaderProgram


class LineShaderProgram(ShaderProgram):
    VERT = Path(__file__).parent / "shaders" / "line_vert.glsl"
    FRAG = Path(__file__).parent / "shaders" / "line_frag.glsl"

    def __init__(self, window):
        self.window = window
        self.program = window.ctx.load_program(
            vertex_shader=str(self.VERT), fragment_shader=str(self.FRAG)
        )
        self.vao = None

    def update_lines(self, edges, max_lines):
        # Prepare the line data
        line_data = []
        for edge in edges:
            entity_a, entity_b = edge
            x1, y1, x2, y2 = (
                entity_a.center_x,
                entity_a.center_y,
                entity_b.center_x,
                entity_b.center_y,
            )

            # Calculate the color and other logic as in your existing code
            # Append data to line_data list
            # ...

            if (
                len(line_data) // 5 >= max_lines
            ):  # 5 elements per line (2 for position, 3 for color)
                break

        # Create a buffer with line data
        buffer = self.window.ctx.buffer(data=np.array("f", line_data))

        # Describe the buffer layout
        buffer_description = arcade.gl.BufferDescription(
            buffer, "2f 3f", ["in_pos", "in_color"]
        )
        self.vao = self.window.ctx.geometry([buffer_description])

    def draw(self):
        if self.vao:
            self.vao.render(self.program, mode=self.window.ctx.LINES)
