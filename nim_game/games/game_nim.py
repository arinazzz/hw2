import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent
from nim_game.common.enumerations import Players


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config) as file:
            templates = json.load(file)
        self._environment = EnvironmentNim(templates['heaps_amount'])
        self._agent = Agent(templates['opponent_level'])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(winner=Players.USER)

        opponent_step = self._agent.make_step(self.heaps_state)
        opponent_step.heap_id += 1
        self._environment.change_state(opponent_step)
        if self.is_game_finished():
            return GameState(winner=Players.BOT)

        return GameState(None, opponent_step, self.heaps_state)

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        if all([i == 0 for i in self.heaps_state]):
            return True
        else:
            return False

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
