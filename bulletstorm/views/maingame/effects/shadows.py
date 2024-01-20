from pathlib import Path

from ....core.utils import setup_logging
from ....core.shader.toy import ShadertoyDef
from arcade.experimental import Shadertoy

log = setup_logging(__name__)


class ShadowsShadertoy(ShadertoyDef):
    def __init__(self, window):
        path = Path(__file__).parent / "shaders/raycasted_shadow_frag.glsl"
        shadertoy = Shadertoy.create_from_file(window.get_size(), path)
        super().__init__(shadertoy, path, n_channels=2)

        self.shadertoy.channel_0 = self.channels[0].color_attachments[0]
        self.shadertoy.channel_1 = self.channels[1].color_attachments[0]

    def draw(self, view):
        # Select the channel 0 frame buffer to draw on
        self.channels[0].use()
        self.channels[0].clear()
        # Draw the asteroids to occur in the channel 0 frame buffer
        view.level.manager.entities.draw()

        view.window.use()
        # Run the shader and render to the window
        p = (
            view.player.position[0] - view.camera_sprites.position[0],
            view.player.position[1] - view.camera_sprites.position[1],
        )

        self.shadertoy.program["lightPosition"] = p
        self.shadertoy.program["lightSize"] = view.window.get_size()[0] / 2
        self.shadertoy.render()
