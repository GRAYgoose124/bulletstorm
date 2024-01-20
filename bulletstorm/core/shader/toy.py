from dataclasses import field, dataclass
from arcade.experimental import Shadertoy
from arcade.gl import Framebuffer

from ...core.utils import setup_logging

log = setup_logging(__name__)


@dataclass
class ShadertoyDef:
    shadertoy: Shadertoy
    path: str
    n_channels: int = 1
    channels: list[Framebuffer] = field(default_factory=list)
    channel_draw_cmds: list[callable] = field(default_factory=list)

    def __post_init__(self):
        for _ in range(self.n_channels):
            c = self.shadertoy.ctx.framebuffer(
                color_attachments=[
                    self.shadertoy.ctx.texture(
                        self.shadertoy.ctx.window.get_size(), components=4
                    )
                ]
            )
            self.channels.append(c)

        log.debug("Loaded {} channels for {}".format(self.n_channels, self))

    def draw(self, view):
        raise NotImplementedError
