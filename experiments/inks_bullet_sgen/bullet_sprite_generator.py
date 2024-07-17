import inkex
import random


class BulletSpriteGenerator(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--damage", type=int, default=10, help="Damage")
        pars.add_argument("--speed", type=float, default=1.0, help="Speed")
        pars.add_argument("--effects", type=str, default="", help="Effects")
        pars.add_argument(
            "--movement_types", type=str, default="", help="Movement Types"
        )

    def effect(self):
        layer = self.svg.get_current_layer()

        bullet_group = self.create_bullet_group()
        layer.add(bullet_group)

    def create_bullet_group(self):
        group = inkex.elements.Group()

        # Base bullet shape
        circle = inkex.elements.Circle(
            cx="50", cy="50", r="20", style="fill:#00f;stroke:#000;stroke-width:2"
        )
        group.add(circle)

        effects = self.options.effects.split(",")
        for effect in effects:
            effect_element = self.create_effect_element(effect)
            if effect_element:
                group.add(effect_element)

        metadata = {
            "damage": self.options.damage,
            "speed": self.options.speed,
            "effects": effects,
            "movement_types": self.options.movement_types.split(","),
        }
        group.set("metadata", str(metadata))
        return group

    def create_effect_element(self, effect):
        if effect == "sick":
            sick_effect = inkex.elements.Path(
                d="M 30,50 Q 50,10 70,50 Q 50,90 30,50",
                style="fill:none;stroke:#0f0;stroke-width:4",
            )
            return sick_effect
        elif effect == "weak":
            weak_effect = inkex.elements.Path(
                d="M 40,50 L 60,50 L 50,70 Z", style="fill:#f00;stroke:none"
            )
            return weak_effect
        else:
            return None


if __name__ == "__main__":
    BulletSpriteGenerator().run()
