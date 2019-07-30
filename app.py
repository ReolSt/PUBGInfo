from pubg_python import PUBG, Shard, exceptions, domain
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

boostrap = Bootstrap(app)


api_key = ""
with open("emacser.api_key", "r") as api_key_file:
    api_key = api_key_file.readline().rstrip()
api = PUBG(api_key, Shard.PC_KAKAO)


@app.route('/')
def route_index():
    return render_template("home.html")


def search_roster(rosters, player_name):
    for roster in rosters:
        for (i, player) in enumerate(roster.participants):
            if player.name == player_name:
                return (i, roster.participants)
    return None


def make_dummy_player():
    player = domain.base.Player
    player.name = "NULL"
    player.patch_version = "0.0"
    player.shard_id = "0"
    player.stats = []
    player.title_id = "0"
    return player


@app.route('/user/<username>')
def search_user(username):
    try:
        players = api.players().filter(player_names=[username.rstrip()])
        player = list(players)[0]
        matches = [api.matches().get(m.id) for m in player.matches[:50]]
        player_index = []
        rosters = []
        for m in matches:
            (i, r) = search_roster(m.rosters, username)
            player_index.append(i)
            rosters.append(r)
    except exceptions.NotFoundError:
        player = make_dummy_player()
        matches = []
        rosters = []
        player_index = []
    return render_template("user.html",
                           jplayer=player,
                           jmatches=matches,
                           jrosters=rosters,
                           jplayer_index=player_index)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
