import logging
from .battle import Battle
from .utils import input_selection

log = logging.getLogger(__name__)


class TurnInfo:
    def __init__(self, actor):
        self.actor = actor
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def __repr__(self):
        return f"<TurnInfo: {self.actor}>"


class BattleStats:
    def __init__(self):
        self.turns = []

    def add_turn(self, turn: TurnInfo):
        self.turns.append(turn)

    def __repr__(self):
        return f"<BattleStats: {self.turns}>"

    def pretty_stats(self):
        return "\n".join(
            [
                f"{turn.actor.name} did {len(turn.actions)} actions."
                for turn in self.turns
            ]
        )


class BattleEngine:
    def __init__(self, battle: Battle = None):
        self.battle = battle
        self.active_actor = None
        self.battle_stats = None

    @property
    def is_player_turn(self):
        return self.active_actor in self.battle.parties["Player"]

    def set_battle(self, battle: Battle):
        self.battle = battle
        self.active_actor = None

    # action related
    def _get_possible_action_targets(self, action):
        """Get the targets for an action."""
        targets = []
        if action.can_target_self:
            targets.append(self.active_actor)
        if action.can_target_allies:
            targets.extend(self.active_actor.party.actors)
        if action.can_target_enemies:
            for party in self.battle.parties.values():
                if self.active_actor.party is not party:
                    targets.extend(party.actors)
        return targets

    def _do_action(self, action, target):
        # apply action effects, temporary stats are per battle and not involved in live/death calculations
        for stat, value in action.temporary_effects_on_target:
            target.temporary_statistics[stat] += value

        # usually applied to hp, mana, stamina values usually. but can be used for things like growth or long term poison
        for stat, value in action.permanent_effects_on_target:
            target.statistics[stat] += value

        # apply action costs
        for stat, value in action.cost:
            self.active_actor.statistics[stat] -= value

        self._process_action_taken(action, target)

    def _process_action_taken(self, action, target):
        if action.category == "Attack":
            print(
                f"\t{self.active_actor.name} attacks {target.name} for {action.permanent_effects_on_target.health} damage."
            )
            print(f"\t{target.name}'s health is now {target.total_stats.health}.")

    def _perform_player_choice(self):
        while True:
            menu_choice = input_selection(
                "Select an action: ", ["Action", "Stats", "Items", "Options", "Run"]
            )
            if menu_choice == "Action":
                self._perform_player_action()
                break
            elif menu_choice == "Stats":
                print(self.active_actor.pretty_stats())
                print(self.battle.pretty_print_battle())
            elif menu_choice == "Items":
                print("Items not implemented.")
            elif menu_choice == "Options":
                print("Options not implemented.")
            elif menu_choice == "Run":
                print("Run not implemented.")

    def _perform_player_action(self, end_turn=False):
        possible_actions = self.active_actor.possible_actions
        action = input_selection("Select an action: ", possible_actions)

        targets = self._get_possible_action_targets(action)
        target = input_selection("Select a target: ", targets)

        print(f"\t{self.active_actor.name} targets {target.name} with {action.name}.")

        self._do_action(action, target)
        if end_turn:
            self._next_turn()

    def _calculate_bot_action(self):
        """Calculate the bot's action."""
        if self.active_actor.possible_actions:
            return self.active_actor.possible_actions[0]

    def _calculate_bot_target(self, action):
        """Calculate the bot's target."""
        return self._get_possible_action_targets(action)[0]

    def _perform_bot_action(self, end_turn=False):
        """Perform the bot's action."""
        action = self._calculate_bot_action()
        if not action:
            return
        target = self._calculate_bot_target(action)

        self._do_action(action, target)
        if end_turn:
            self._next_turn()

        return f"{self.active_actor.name} targets {target.name} with {action.name}."

    def _next_turn(self):
        self.active_actor = self.battle._next_turn()
        self.active_turn_info = TurnInfo(self.active_actor)

    def start(self):
        print("Battle starting.")
        self.battle.initialize()
        self.battle_stats = BattleStats()

        while not self.battle.is_over:
            print(f"Turn {self.battle.turn}:")
            self._next_turn()

            print(f"\t{self.active_actor.name} is active.")

            if self.is_player_turn:
                print("\tPlayer's turn. What will you do?")
                # options are actions, items, or run
                self._perform_player_choice()
            else:
                print("\tEnemy's turn.")
                self._perform_bot_action()

            self.battle_stats.add_turn(self.active_turn_info)

        log.info("Battle over.")

        return self.battle
