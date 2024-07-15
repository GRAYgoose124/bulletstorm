import inkex

class MetadataEditor(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--selected_id', type=str, help='ID of the selected object')
        pars.add_argument('--damage', type=int, default=10, help='Damage')
        pars.add_argument('--speed', type=float, default=1.0, help='Speed')
        pars.add_argument('--effects', type=str, default='', help='Effects')
        pars.add_argument('--movement_types', type=str, default='', help='Movement Types')

    def effect(self):
        selected_id = self.options.selected_id
        selected_object = self.svg.getElementById(selected_id)

        if selected_object is None:
            inkex.utils.debug('Selected object not found')
            return

        metadata = {
            'damage': self.options.damage,
            'speed': self.options.speed,
            'effects': self.options.effects.split(','),
            'movement_types': self.options.movement_types.split(',')
        }
        selected_object.set('metadata', str(metadata))
        inkex.utils.debug(f'Metadata updated: {metadata}')

if __name__ == '__main__':
    MetadataEditor().run()
