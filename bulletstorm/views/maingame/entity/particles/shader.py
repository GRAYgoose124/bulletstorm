from pathlib import Path


class ShaderProgram:
    VERT = Path(__file__).parent / "shaders" / "default_vert.glsl"
    FRAG = Path(__file__).parent / "shaders" / "default_frag.glsl"

    def __init__(self, window):
        self.window = window
        self.program = None
        self.hotload()

    def hotload(self):
        self.program = self.window.ctx.load_program(
            vertex_shader=self.VERT, fragment_shader=self.FRAG
        )

    def draw(self):
        pass

    def update(self, dt):
        pass
