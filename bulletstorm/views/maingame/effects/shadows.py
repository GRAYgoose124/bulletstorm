import math
from pathlib import Path

from ....core.utils import setup_logging
from ....core.shader.toy import ShadertoyDef
from arcade.experimental import Shadertoy
import numpy as np

log = setup_logging(__name__)


def rotate_point(x, y, angle):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return R.dot(np.array((x, y)))


class ShadowsShadertoy(ShadertoyDef):
    def __init__(self, window):
        # path = Path(__file__).parent / "shaders/debug_shapelist_frag.glsl"
        path = Path(__file__).parent / "shaders/shadows_frag.glsl"
        shadertoy = Shadertoy.create_from_file(window.get_size(), path)
        super().__init__(shadertoy, path, n_channels=2)

        self.shadertoy.channel_0 = self.channels[0].color_attachments[0]
        self.shadertoy.channel_1 = self.channels[1].color_attachments[0]
        self.do_not_retry = False

    def draw(self, view):
        # fill occlusion channel
        self.channels[0].use()
        self.channels[0].clear()
        view.level.manager.entities.draw()

        # draw Shadertoy to main window
        view.window.use()
        p = (
            view.player.position[0] - view.camera_sprites.position[0],
            view.player.position[1] - view.camera_sprites.position[1],
        )

        # place the light in front of the player
        direction = rotate_point(0, 1, view.player.angle)
        p = p[0] + direction[0] * 200, p[1] + direction[1] * 200

        # for debugging without proper uniforms
        # if not self.do_not_retry:
        #    try:
        self.shadertoy.program["lightPosition"] = p
        self.shadertoy.program["lightSize"] = view.window.width * 0.6
        #        self.do_not_retry = True
        self.shadertoy.render()
