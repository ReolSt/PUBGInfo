# -*- coding: utf-8 -*-
from pubg_python import PUBG, Shard

with open("emacser.api_key", "r") as api_key_file:
    api_key = api_key_file.readline().rstrip()
api = PUBG(api_key, Shard.PC_KAKAO)

players = api.players().filter(player_names=['GNUemacs'])
player = players[0]

print(player.matches)
