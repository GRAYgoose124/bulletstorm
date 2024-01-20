from ...core.utils import setup_logging
from .toy import ShadertoyDef

log = setup_logging(__name__)


def channel_factory(size):
    """dataclass factory for creating channels based on dataclass defaults"""


class ShaderViewMixin:
    def __init__(self, *args, **kwargs):
        self.shaders = {}
        self.shadertoys = {}

    # shaders
    def add_shader(self, shader_cls):
        name = shader_cls.__name__
        if name not in self.shaders:
            self.shaders[name] = shader_cls(self.window)

    def reload_shader(self, shader_cls):
        name = shader_cls.__name__
        if name in self.shaders:
            self.shaders[name].hotload()

    def update(self, delta_time):
        for shader in self.shaders.values():
            shader.update(delta_time)

    def on_resize(self, width: int, height: int):
        for shader in self.shaders.values():
            shader.hotload()

        for st in self.shadertoys.values():
            st.shadertoy.resize((width, height))

    # todo generalize/unify with ShaderPrograms
    # https://api.arcade.academy/en/development/tutorials/raycasting/index.html
    def load_shadertoy(self, st_def: ShadertoyDef):
        st = st_def(self.window)
        self.shadertoys[st.__class__.__name__] = st

        log.debug("Loaded shadertoy: %s", st)

    def draw_shaders(self):
        for shader in self.shaders.values():
            shader.draw()

    def draw_shadertoys(self):
        for st in self.shadertoys.values():
            st.draw(self)
