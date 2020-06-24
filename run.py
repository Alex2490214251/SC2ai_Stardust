# Imports have to be in this order, leave this comment here to fall back to it if they get messed up
# import sc2, sys
# from __init__ import run_ladder_game
# from sc2 import Race, Difficulty
# from sc2.player import Bot, Computer
# import random
import sc2, sys
from __init__ import run_ladder_game
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer
import random

import datetime

# Load bot
from bot_main import Bot_IV
bot = Bot(Race.Protoss, Bot_IV())

# Start game
if __name__ == "__main__":

    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(bot)
        print(f"{result} against opponent {opponentid}")
    else:
        # Local game
        print("Starting local game...")
        map_name = random.choice(
            [
                'AcropolisLE',
                'AutomatonLE',
                'EphemeronLE',
                'ThunderbirdLE',
                'TritonLE',
                'WintersGateLE',
                'WorldofSleepersLE',
                'EternalEmpireLE',
                'StasisLE',
                'SimulacrumLE',
                'GoldenWallLE',
                'EverDreamLE'
            ]
        )

        date = str(datetime.datetime.now().time()).replace(':', ' ')

        replay_name = map_name + date + '.SC2Replay'

        sc2.run_game(
            sc2.maps.get(map_name),
            [
                # Human(Race.Terran),
                bot,
                Computer(Race.Random, Difficulty.VeryHard),  # CheatInsane VeryHard
            ],
            realtime=False,
            save_replay_as=replay_name
        )
