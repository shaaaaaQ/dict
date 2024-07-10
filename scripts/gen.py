# 仮
import os
import csv
import math

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

    data = list(filter(lambda item: item[1], data))

    # SKK
    with open(
        os.path.join(dirname, "../out", f"{game} SKK.txt"), "w", encoding="utf-8"
    ) as f:
        result = [";; okuri-ari entries.", ";; okuri-nasi entries."]
        for item in data:
            result.append(f"{item[1]} /{item[0]}/")
        f.write("\n".join(result))

    # Wnn
    for i in range(1, math.floor(len(data) / 500) + 2):
        with open(
            os.path.join(dirname, "../out", f"{game} Wnn_{i}.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            result = [f"{game} {i}"]
            for item in data:
                result.append(f"{item[1]}\t{item[0]}")
            f.write("\n".join(result))

    # MS
    with open(
        os.path.join(dirname, "../out", f"{game} MS-IME.txt"), "w", encoding="utf-16"
    ) as f:
        result = []
        for item in data:
            s = f"{item[1]}\t{item[0]}\t{item[2]}"
            if len(item) == 4 and item[3]:
                s += f"\t{item[3]}"
            result.append(s)
        f.write("\n".join(result))
