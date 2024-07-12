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
facility = {
    "mondstadt": [],
    "dragonspine": [],
    "liyue": [],
    "inazuma": [],
    "sumeru": [],
    "fontaine": [],
    "natlan": [],
    "snezhnaya": [],
    "khaenriah": []
}
facility_other = []
area = {
    "mondstadt": [],
    "dragonspine": [],
    "liyue": [],
    "inazuma": [],
    "sumeru": [],
    "fontaine": [],
    "natlan": [],
    "snezhnaya": [],
    "khaenriah": []
}
area_other = []
element = []
artifact_set = []
artifact_piece = []
character_main = []
living_being = []
enemy = []
boss = []

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
        elif "facility" in tags:
            for region in facility.keys():
                if region in tags:
                    facility[region].append(data)
                    break
            else:
                facility_other.append(data)
        elif "location" in tags:
            for region in area.keys():
                if region in tags:
                    area[region].append(data)
                    break
            else:
                area_other.append(data)
        elif "element" in tags:
            element.append(data)
        elif "artifact" in tags:
            artifact_set.append(data)
        elif "artifact-piece" in tags:
            artifact_piece.append(data)
        elif "character-main" in tags:
            character_main.append(data)
        elif "living-being" in tags:
            living_being.append(data)
        elif "enemy" in tags:
            enemy.append(data)
        elif "enemy-boss" in tags:
            boss.append(data)

write(weapon["sword"], "weapon/sword.csv", "名詞", "原神/武器/片手剣")
write(weapon["claymore"], "weapon/claymore.csv", "名詞", "原神/武器/両手剣")
write(weapon["polearm"], "weapon/polearm.csv", "名詞", "原神/武器/長柄武器")
write(weapon["bow"], "weapon/bow.csv", "名詞", "原神/武器/弓")
write(weapon["catalyst"], "weapon/catalyst.csv", "名詞", "原神/武器/法器")
write(weapon_other, "weapon/other.csv", "名詞")
write(facility["mondstadt"], "facility/mondstadt.csv", "名詞", "原神/施設/モンド")
write(facility["dragonspine"], "facility/dragonspine.csv", "名詞", "原神/施設/ドラゴンスパイン")
write(facility["liyue"], "facility/liyue.csv", "名詞", "原神/施設/璃月")
write(facility["inazuma"], "facility/inazuma.csv", "名詞", "原神/施設/稲妻")
write(facility["sumeru"], "facility/sumeru.csv", "名詞", "原神/施設/スメール")
write(facility["fontaine"], "facility/fontaine.csv", "名詞", "原神/施設/フォンテーヌ")
write(facility["natlan"], "facility/natlan.csv", "名詞", "原神/施設/ナタ")
write(facility["snezhnaya"], "facility/snezhnaya.csv", "名詞", "原神/施設/スネージナヤ")
write(facility["khaenriah"], "facility/khaenriah.csv", "名詞", "原神/施設/カーンルイア")
write(facility_other, "facility/other.csv", "名詞")
write(area["mondstadt"], "area/mondstadt.csv", "地名その他", "原神/地名/モンド")
write(area["dragonspine"], "area/dragonspine.csv", "地名その他", "原神/地名/ドラゴンスパイン")
write(area["liyue"], "area/liyue.csv", "地名その他", "原神/地名/璃月")
write(area["inazuma"], "area/inazuma.csv", "地名その他", "原神/地名/稲妻")
write(area["sumeru"], "area/sumeru.csv", "地名その他", "原神/地名/スメール")
write(area["fontaine"], "area/fontaine.csv", "地名その他", "原神/地名/フォンテーヌ")
write(area["natlan"], "area/natlan.csv", "地名その他", "原神/地名/ナタ")
write(area["snezhnaya"], "area/snezhnaya.csv", "地名その他", "原神/地名/スネージナヤ")
write(area["khaenriah"], "area/khaenriah.csv", "地名その他", "原神/地名/カーンルイア")
write(area_other, "area/other.csv", "地名その他")
write(element, "element.csv", "名詞")
write(artifact_set, "artifact/set.csv", "名詞", "原神/聖遺物")
write(artifact_piece, "artifact/piece.csv", "名詞")
write(character_main, "character/playable.csv", "人名", "原神/キャラクター")
write(living_being, "living-being.csv", "名詞", "原神/生物")
write(enemy, "enemy/enemy.csv", "名詞", "原神/敵")
write(boss, "enemy/boss.csv", "名詞", "原神/ボス")
