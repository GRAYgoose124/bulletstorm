from ...core import Action, ActorStats

slash_attack = Action(
    name="Slash",
    category="Attack",
    description="A basic melee attack which barely stings.",
    cost=[("stamina", 1)],
    permanent_effects_on_target=ActorStats.zero(health=-1),
    can_target_enemies=True,
)
