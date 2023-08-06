# libbisca
> A Python bisca library

[![Build Status](https://www.travis-ci.org/NunoMCSilva/libbisca.svg)](https://www.travis-ci.org/NunoMCSilva/libbisca)
[![Coverage Status](https://img.shields.io/codecov/c/github/NunoMCSilva/libbisca)](https://codecov.io/gh/NunoMCSilva/libbisca)
![Version](https://img.shields.io/github/pipenv/locked/python-version/NunoMCSilva/libbisca)
[![PyPi](https://img.shields.io/pypi/v/libbisca)](https://test.pypi.org/project/libbisca1/)

[![License](https://img.shields.io/github/license/NunoMCSilva/libbisca)](https://github.com/NunoMCSilva/libbisca/blob/master/LICENSE.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

libbisca is a Python bisca library. Bisca is a Portuguese trick-taking card game.

State: Alpha (still needs a lot of work)

This is a small hobby project.
In the future I may write a BiscaAI (game engines) and a Bisca GUI (probably using tkinter) on top of this. 
Keeping them separate should allow anyone else to use libbisca (the game rules) without the rest. 

## Usage example (non-exhaustive)

```
>>> import libbisca as bisca

>>> state = bisca.get_state()

>>> state
State(hand_size=3, turn=South, stock=[5D, 6H, 5C, QD, AH, QH, KS, 6S, QS, 4C, 4S, 7H, 5H, 3C, AC, 2C, JD, KC, AD, 2D, 4H, KH, AS, KD, QC, 3D, 4D, 3S, JS, JC, 3H, 2S, 5S, 7S], trump=5D, players={North: PlayerState(hand=[7C, 2H, 7D], pile=[], score=0), South: PlayerState(hand=[6C, JH, 6D], pile=[], score=0)}, table=[])

>>> state.play(bisca.get_card("4D"))

>>> state
State(hand_size=3, turn=North, stock=[2C, 7D, QC, JC, 5S, 3H, 7S, JH, AH, 2H, 5C, 5D, QD, 7H, 5H, JS, 3S, 6H, JD, KH, KD, 6S, QS, KS, 3C, AD, 6D, KC, 4S, AC, 6C, AS, 4H, 4C], trump=2C, players={North: PlayerState(hand=[2S, QH, 3D], pile=[], score=0), South: PlayerState(hand=[2D, 7C], pile=[], score=0)}, table=[4D])

>>> state.do_random_move()
(QH, (South, 2, [4D, QH], [4C, 4H]))

>>> state
State(hand_size=3, turn=South, stock=[2C, 7D, QC, JC, 5S, 3H, 7S, JH, AH, 2H, 5C, 5D, QD, 7H, 5H, JS, 3S, 6H, JD, KH, KD, 6S, QS, KS, 3C, AD, 6D, KC, 4S, AC, 6C, AS], trump=2C, players={North: PlayerState(hand=[2S, 3D, 4H], pile=[], score=0), South: PlayerState(hand=[2D, 7C, 4C], pile=[[4D, QH]], score=2)}, table=[])

>>> state.do_random_rollout()

>>> state
State(hand_size=3, turn=North, stock=[], trump=2C, players={North: PlayerState(hand=[], pile=[[7H, 5C], [3C, 5D], [7D, 2C], [5S, 3H]], score=20), South: PlayerState(hand=[], pile=[[4D, QH], [2D, 2S], [7C, 3D], [AC, 4S], [AS, 6D], [KC, 6C], [KS, 4H], [AD, KD], [6S, JD], [4C, QS], [KH, 3S], [JS, QD], [5H, AH], [7S, JH], [JC, QC], [6H, 2H]], score=100)}, table=[])

>>> state.is_endgame()
True

>>> state.legal_moves
[]

>>> state.get_winner()
South

>>> state.players[bisca.Player.SOUTH].score
100
```

## Development setup

Assuming you are working on linux and have pipenv installed, do:

```
make install
make unit
```

# Release History
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), so all information is in ```CHANGELOG.md```.

## License and author info

Nuno Miguel Casteloa da Silva -- NunoMCSilva@gmail.com

Distributed under the GPL 3.0 license. See ```LICENSE.md```  for more information.

[https://github.com/NunoMCSilva/libbisca](https://github.com/NunoMCSilva/)

## Thanks

My thanks to all the projects, articles and code that inspired/helped me. There are too many to list here independently.
