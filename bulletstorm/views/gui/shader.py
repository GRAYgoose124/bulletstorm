class ShaderViewMixin:
    def __init__(self, *args, **kwargs):
        self.shaders = {}

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
