import requests
from pyquery import PyQuery as pq
from lxml import etree
import constants


def get_rank(name):
    r = requests.get(
        "http://maplestory.nexon.net/rankings/overall-ranking/legendary?pageIndex=1&character_name={}&search=true".format(name))
    response = r.text
    d = pq(response, parser="html")
    table = d("div.ranking-container > table tbody").find("tr")

    for c in table.items():
        char_name = c("td").eq(2).text()
        if char_name.lower() != name.lower():
            continue

        dict = c("td.level-move").text().split(" ", 3)
        exp = int(dict[1][1:-1])
        level = int(dict[0])
        tnl = int(constants.TO_NEXT_LEVEL[level])
        move = 0 if dict[2] is "-" else int(dict[2])

        # Negative if rank down is level-move (an image is used with the
        # rank-down; not a negative symbol)
        if "rank-down" in c("td.level-move").html():
            move = (int(move) * (-1))

        # Beginner detection (no job advancement yet)
        if c("td > img.job").attr("src") == "http://nxcache.nexon.net/maplestory/img/icons/icon-job-.gif":
            job = "None"
        else:
            job = c("td > img.job").attr("title")

        obj = {
            "name": char_name,
            "rank": int(c("td").eq(0).text()),
            "job": job,
            "world": c("td a.world").attr("href").replace("/rankings/world-ranking/", "").title(),
            "avatar": {
                "character": c("td img.avatar").eq(0).attr("src"),
            },
            "level": level,
            "move": move,
            "current_exp": exp,
            "exp_to_level": tnl - exp,
            "exp_percent": 0 if level is 250 else ((float(exp) / float(tnl)) * 100),
        }

        if char_name.lower() == name.lower():
            return obj
        else:
            return None

    return None

if __name__ == "__main__":
    print("This one should return none; off rankings: ", get_rank("Barter"))
    print(get_rank("catboy"))
    print(get_rank("catgiri"))
    print(get_rank("divinemyth"))
    print(get_rank("zerobydivide"))
    print(get_rank("zanyzany23"))
