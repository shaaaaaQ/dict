import requests
import os
import csv
import glob
import jaconv

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "../data/Genshin Impact")
dataset = requests.get("https://dataset.genshin-dictionary.com/words.json").json()


def write(data_list, filepath, hinshi, comment=""):
    with open(os.path.join(data_dir, filepath), "a", encoding="utf-8") as f:
        print(f"新規追加 ({filepath}): ", len(data_list))
        writer = csv.writer(f)
        for data in data_list:
            word = data["ja"]
            hiragana = (
                jaconv.kata2hira(data["pronunciationJa"])
                if "pronunciationJa" in data
                else ""
            )
            _comment = ""
            if comment:
                _comment = comment
            elif "notes" in data:
                _comment = data["notes"]

            writer.writerow([word, hiragana, hinshi, _comment])


excludes = []
files = glob.glob(os.path.join(data_dir, "**/*.csv"), recursive=True)
for csv_path in files:
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if row:
                excludes.append(row[0])
with open(os.path.join(data_dir, "excludes.txt"), encoding="utf-8") as f:
    excludes.extend(f.read().splitlines())

weapon = {"sword": [], "claymore": [], "polearm": [], "bow": [], "catalyst": []}
weapon_other = []
element = []
artifact_set = []
artifact_piece = []

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
        elif "element" in tags:
            element.append(data)
        elif "artifact" in tags:
            artifact_set.append(data)
        elif "artifact-piece" in tags:
            artifact_piece.append(data)

write(weapon["sword"], "weapon/sword.csv", "名詞", "原神/武器/片手剣")
write(weapon["claymore"], "weapon/claymore.csv", "名詞", "原神/武器/両手剣")
write(weapon["polearm"], "weapon/polearm.csv", "名詞", "原神/武器/長柄武器")
write(weapon["bow"], "weapon/bow.csv", "名詞", "原神/武器/弓")
write(weapon["catalyst"], "weapon/catalyst.csv", "名詞", "原神/武器/法器")
write(weapon_other, "weapon/other.csv", "名詞")
write(element, "element.csv", "名詞")
write(artifact_set, "artifact/set.csv", "名詞", "原神/聖遺物")
write(artifact_piece, "artifact/piece.csv", "名詞")
