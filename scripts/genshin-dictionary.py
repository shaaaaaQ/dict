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
            if row:
                excludes.append(row[0])
with open(os.path.join(data_dir, "excludes.txt"), encoding="utf-8") as f:
    excludes.extend(f.read().splitlines())


q = {
    "weapon": {
        "sword": ["weapon/sword.csv", "名詞", "原神/武器/片手剣"],
        "claymore": ["weapon/claymore.csv", "名詞", "原神/武器/両手剣"],
        "polearm": ["weapon/polearm.csv", "名詞", "原神/武器/長柄武器"],
        "bow": ["weapon/bow.csv", "名詞", "原神/武器/弓"],
        "catalyst": ["weapon/catalyst.csv", "名詞", "原神/武器/法器"],
        "weapon": ["weapon/other.csv", "名詞"],
    },
    "facility": {
        "mondstadt": ["facility/mondstadt.csv", "名詞", "原神/施設/モンド"],
        "dragonspine": [
            "facility/dragonspine.csv",
            "名詞",
            "原神/施設/ドラゴンスパイン",
        ],
        "liyue": ["facility/liyue.csv", "名詞", "原神/施設/璃月"],
        "inazuma": ["facility/inazuma.csv", "名詞", "原神/施設/稲妻"],
        "sumeru": ["facility/sumeru.csv", "名詞", "原神/施設/スメール"],
        "fontaine": ["facility/fontaine.csv", "名詞", "原神/施設/フォンテーヌ"],
        "natlan": ["facility/natlan.csv", "名詞", "原神/施設/ナタ"],
        "snezhnaya": ["facility/snezhnaya.csv", "名詞", "原神/施設/スネージナヤ"],
        "khaenriah": ["facility/khaenriah.csv", "名詞", "原神/施設/カーンルイア"],
        "facility": ["facility/other.csv", "名詞"],
    },
    "location": {
        "mondstadt": ["area/mondstadt.csv", "地名その他", "原神/地名/モンド"],
        "dragonspine": [
            "area/dragonspine.csv",
            "地名その他",
            "原神/地名/ドラゴンスパイン",
        ],
        "liyue": ["area/liyue.csv", "地名その他", "原神/地名/璃月"],
        "inazuma": ["area/inazuma.csv", "地名その他", "原神/地名/稲妻"],
        "sumeru": ["area/sumeru.csv", "地名その他", "原神/地名/スメール"],
        "fontaine": ["area/fontaine.csv", "地名その他", "原神/地名/フォンテーヌ"],
        "natlan": ["area/natlan.csv", "地名その他", "原神/地名/ナタ"],
        "snezhnaya": ["area/snezhnaya.csv", "地名その他", "原神/地名/スネージナヤ"],
        "khaenriah": ["area/khaenriah.csv", "地名その他", "原神/地名/カーンルイア"],
        "location": ["area/other.csv", "地名その他"],
    },
    "drop": ["item/drop.csv", "名詞", "原神/アイテム/ドロップ"],
    "drop-boss": ["item/drop-boss.csv", "名詞", "原神/アイテム/ボスドロップ"],
    "talent-material": ["item/talent-material.csv", "名詞", "原神/アイテム/天賦素材"],
    "weapon-material": ["item/weapon-material.csv", "名詞", "原神/アイテム/武器素材"],
    "element": ["element.csv", "名詞"],
    "artifact-set": ["artifact/set.csv", "名詞", "原神/聖遺物"],
    "artifact-piece": ["artifact/piece.csv", "名詞"],
    "character-main": ["character/playable.csv", "人名", "原神/キャラクター"],
    "living-being": ["living-being.csv", "名詞", "原神/生物"],
    "enemy": ["enemy/enemy.csv", "名詞", "原神/敵"],
    "boss": ["enemy/boss.csv", "名詞", "原神/ボス"],
}

extracted = {}


def find(q, tags):
    result = []
    for k, v in q.items():
        if k in tags:
            result.append(k)
            if isinstance(v, list):
                return result, v
            elif isinstance(v, dict):
                res = find(v, tags)
                result.extend(res[0])
                return result, res[1]


for data in dataset:
    if "ja" not in data:
        continue
    if data["ja"] in excludes:
        continue
    if "tags" in data:
        tags = data["tags"]
        res = find(q, tags)
        if res:
            k = "+".join(res[0])
            if k in extracted:
                extracted[k]["data"].append(data)
            else:
                extracted[k] = {"data": [data], "args": res[1]}


def write(data_list, filepath, hinshi, comment=""):
    if data_list:
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


for v in extracted.values():
    write(v["data"], *v["args"])
