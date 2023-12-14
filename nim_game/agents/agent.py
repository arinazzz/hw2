from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        self._level = AgentLevels(level)

    def _hard_step(state_curr: list[int]) -> NimStateChange:
        sm = 0
        for i in state_curr:
            sm = sm ^ i

        if (sm == 0):
            return Agent._easy_step(state_curr)
        else:
            for i, j in enumerate(state_curr):
                if j > (sm ^ j):
                    return NimStateChange(i, j - (sm ^ j))

    def _easy_step(state_curr: list[int]) -> NimStateChange:
        id = choice([i for i, j in enumerate(state_curr) if j != 0])
        step = randint(1, state_curr[id])
        return NimStateChange(id, step)

    def _normal_step(state_curr: list[int]) -> NimStateChange:
        if randint(0, 1):
            return Agent._easy_step(state_curr)
        else:
            return Agent._hard_step(state_curr)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.HARD:
            return Agent._hard_step(state_curr)
        if self._level == AgentLevels.EASY:
            return Agent._easy_step(state_curr)
        if self._level == AgentLevels.NORMAL:
            return Agent._normal_step(state_curr)
