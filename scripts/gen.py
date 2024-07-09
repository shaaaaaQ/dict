# 仮
import os
import csv

dirname = os.path.dirname(__file__)

with open(
    os.path.join(dirname, "../data/Genshin Impact/character.csv"), encoding="utf-8"
) as f:
    result = [";; okuri-ari entries.", ";; okuri-nasi entries."]
    reader = csv.reader(f)
    for row in reader:
        result.append(f"{row[1]} /{row[0]}/")

    with open(
        os.path.join(dirname, "../out/genshin_impact_skk.txt"), "w", encoding="utf-8"
    ) as f:
        f.write("\n".join(result))
