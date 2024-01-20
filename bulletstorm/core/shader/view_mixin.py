from arcade.experimental import Shadertoy
from ...core.utils import setup_logging

log = setup_logging(__name__)


class ShaderViewMixin:
    def __init__(self, *args, **kwargs):
        self.shaders = {}

        self.shadertoy = None
        self.channel0 = None
        self.channel1 = None
        self.channel2 = None

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

        # if self.shadertoy is not None:
        #     self.shadertoy.resize(width, height)
        #     self.channel0.resize(width, height)
        #     self.channel1.resize(width, height)
        if self.shadertoy_path is not None:
            self.shadertoy.resize((width, height))

    # todo generalize/unify with ShaderPrograms
    # https://api.arcade.academy/en/development/tutorials/raycasting/index.html
    def load_shadertoy(self, path):
        # Size of the window
        window_size = self.window.get_size()

        # Create the shader toy, passing in a path for the shader source
        self.shadertoy = Shadertoy.create_from_file(window_size, path)
        self.shadertoy_path = path
        # Create the channels 0 and 1 frame buffers.
        # Make the buffer the size of the window, with 4 channels (RGBA)
        self.channel0 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )
        self.channel1 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )
        self.channel2 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )

        # Assign the frame buffers to the channels
        self.shadertoy.channel_0 = self.channel0.color_attachments[0]
        self.shadertoy.channel_1 = self.channel1.color_attachments[0]
        self.shadertoy.channel_2 = self.channel2.color_attachments[0]

        log.debug("Loaded shadertoy: %s", path)

    def draw_shadertoy(self):
        # Select the channel 0 frame buffer to draw on
        self.channel0.use()
        self.channel0.clear()
        # Draw the asteroids to occur in the channel 0 frame buffer
        self.level.manager.entities.draw()

        self.channel1.use()
        self.channel1.clear()
        self.level.manager.entities.draw()

        # Select this window to draw on
        self.window.use()
        # Run the shader and render to the window
        p = (
            self.player.position[0] - self.camera_sprites.position[0],
            self.player.position[1] - self.camera_sprites.position[1],
        )

        self.shadertoy.program["lightPosition"] = p
        self.shadertoy.program["lightSize"] = 300
        self.shadertoy.render()
