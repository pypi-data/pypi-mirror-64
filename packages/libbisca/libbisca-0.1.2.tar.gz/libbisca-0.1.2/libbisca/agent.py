# -*- coding: utf-8 -*-

"""Bisca Agent

This module exports the following classes:
    * Agent - abstract Agent class
    * RandomAgent - concrete Agent subclass that randomly choose a move
"""
# TODO: improve docstring

from abc import ABC, abstractmethod

# import random

from libbisca.card import Card
from libbisca.state import State


class Agent(ABC):
    # abstract base class

    @abstractmethod
    def get_move(self, state) -> Card:  # TODO: see ObservedState option, typing "State"
        raise NotImplementedError


class RandomAgent(Agent):
    def get_move(self, state: State) -> Card:  # TODO: typing "State"
        move, _ = state.do_random_move()  # random.choice(state.legal_moves)
        return move


"""
# TODO: experimental
from dataclasses import dataclass
from typing import List
from libbisca.state import Player


@dataclass
class ObservedState:    # TODO: should other agents recieve this info at start + start_new_game, end_game?
    hand_size: int
    turn: Player
    is_stock_empty: bool
    trump: Card
    # hand, pile, score
    legal_moves: List[Card]
    table: List[Card]

# TODO: hmmm, a end_round would also be useful -- winner and added_score, rest unnecessary -- it all depends on Agent keeping
# own version of state or just getting the most outside of it -- for that Agent would need a specialized State where play for
# opponent would always work... hmmm
# TODO: make decision




# TODO: should do_random_move and do_rollout be part of a "decorator" state applied to normal state only if Agent requires it?


# TODO: To test
# TODO: put elsewhere? -- it's now in agent
# TODO: not sure about variant="StandardRules", hand_size: int = 3, eldest: Player = Player.SOUTH -- give factory function?
# TODO: add Agent
def run_games(num_games: int = 100, players: List = None, state_factory_func=get_state) -> Dict[Player, int]:
    results = {player: 0 for player in list(Player) + [None]}   # TODO: check PyCharm warning

    for _ in range(num_games // 2):  # TODO: this needs to be well documented
        for eldest in Player:
            state = state_factory_func(eldest=eldest)

            # TODO: decision here? correct that
            if players is None:
                state.do_random_rollout()
            else:
                # TODO: could use rollout with agents...
                while not state.is_endgame():
                    move = players[0 if state.turn == Player.NORTH else 1].get_move(state)     # TODO: doesn't need full state -- dataclass ObservedState?
                    state.play(move)
                    #raise NotImplementedError   # def wturn, stateplayers[state.turn].get_move(state_obs)

            results[state.get_winner()] += 1

    return results


# TODO: history and undo?

if __name__ == "__main__":
    print(run_games())

    import libbisca.agent as ag
    r = ag.RandomAgent()
    re = run_games(players=[r, r])
    print(re)

"""
