# 仮
import os
import csv

dirname = os.path.dirname(__file__)

game_list = os.listdir(os.path.join(dirname, "../data"))

for game in game_list:
    csv_list = os.listdir(os.path.join(dirname, "../data", game))

    data = []

    for filename in csv_list:
        with open(
            os.path.join(dirname, "../data", game, filename), encoding="utf-8"
        ) as f:
            data.extend(csv.reader(f))

    with open(
        os.path.join(dirname, "../out", f"{game} SKK.txt"), "w", encoding="utf-8"
    ) as f:
        result = [";; okuri-ari entries.", ";; okuri-nasi entries."]
        for item in data:
            result.append(f"{item[1]} /{item[0]}/")
        f.write("\n".join(result))
