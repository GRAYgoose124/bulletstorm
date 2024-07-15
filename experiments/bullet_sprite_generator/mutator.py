import inkex
import random

class Mutator(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--selected_ids', type=str, help='Comma-separated list of selected object IDs')
        pars.add_argument('--mutation_chance', type=float, default=0.1, help='Chance of mutation')

    def effect(self):
        selected_ids = self.options.selected_ids.split(',')
        for selected_id in selected_ids:
            selected_object = self.svg.getElementById(selected_id)

            if selected_object is None:
                inkex.utils.debug(f'Object with ID {selected_id} not found')
                continue

            metadata = eval(selected_object.get('metadata', '{}'))

            if random.random() < self.options.mutation_chance:
                metadata = self.apply_mutation(metadata)
                selected_object.set('metadata', str(metadata))
                inkex.utils.debug(f'Mutated metadata for {selected_id}: {metadata}')

    def apply_mutation(self, metadata):
        if 'damage' in metadata:
            metadata['damage'] += random.randint(-5, 5)
        if 'speed' in metadata:
            metadata['speed'] *= random.uniform(0.9, 1.1)
        if 'effects' in metadata:
            effects = ['weak', 'paralysis', 'silent', 'slow', 'confused']
            if random.random() < 0.5:
                new_effect = random.choice(effects)
                if new_effect not in metadata['effects']:
                    metadata['effects'].append(new_effect)
            else:
                if metadata['effects']:
                    metadata['effects'].pop(random.randint(0, len(metadata['effects']) - 1))
        return metadata

if __name__ == '__main__':
    Mutator().run()
