import requests
import os
import csv
import glob
import jaconv

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "../data/Genshin Impact")
dataset = requests.get("https://dataset.genshin-dictionary.com/words.json").json()

excludes = []
files = glob.glob(os.path.join(data_dir, "**/*.csv"), recursive=True)
for csv_path in files:
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row:
                continue
            excludes.append(row[0])

weapon = {
    "sword": [],
    "claymore": [],
    "polearm": [],
    "bow": [],
    "catalyst": []
}
weapon_other = []

for data in dataset:
    if "ja" not in data:
        continue
    if data["ja"] in excludes:
        continue
    if "tags" in data:
        tags = data["tags"]
        if "weapon" in tags:
            for weapon_type in weapon.keys():
                if weapon_type in tags:
                    weapon[weapon_type].append(data)
                    break
            else:
                weapon_other.append(data)

with open(os.path.join(data_dir, "weapon/sword.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/片手剣): ", len(weapon["sword"]))
    writer = csv.writer(f)
    for data in weapon["sword"]:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = "原神/武器/片手剣"

        writer.writerow([word, hiragana, hinshi, comment])

with open(os.path.join(data_dir, "weapon/claymore.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/両手剣): ", len(weapon["claymore"]))
    writer = csv.writer(f)
    for data in weapon["claymore"]:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = "原神/武器/両手剣"

        writer.writerow([word, hiragana, hinshi, comment])

with open(os.path.join(data_dir, "weapon/polearm.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/長柄武器): ", len(weapon["polearm"]))
    writer = csv.writer(f)
    for data in weapon["polearm"]:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = "原神/武器/長柄武器"

        writer.writerow([word, hiragana, hinshi, comment])

with open(os.path.join(data_dir, "weapon/bow.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/弓): ", len(weapon["bow"]))
    writer = csv.writer(f)
    for data in weapon["bow"]:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = "原神/武器/弓"

        writer.writerow([word, hiragana, hinshi, comment])

with open(os.path.join(data_dir, "weapon/catalyst.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/法器): ", len(weapon["catalyst"]))
    writer = csv.writer(f)
    for data in weapon["catalyst"]:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = "原神/武器/法器"

        writer.writerow([word, hiragana, hinshi, comment])

with open(os.path.join(data_dir, "weapon/other.csv"), "a", encoding="utf-8") as f:
    print("新規追加 (武器/その他): ", len(weapon_other))
    writer = csv.writer(f)
    for data in weapon_other:
        word = data["ja"]
        hiragana = (
            jaconv.kata2hira(data["pronunciationJa"])
            if "pronunciationJa" in data
            else ""
        )
        hinshi = "名詞"
        comment = data["notes"] if "notes" in data else ""

        writer.writerow([word, hiragana, hinshi, comment])