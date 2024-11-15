import os
import csv
import glob
import re
import requests
import jaconv


def load_excludes(data_dir, ex_data_dir):
    excludes = []

    # CSV ファイルのデータを除外リストに追加
    csv_files = glob.glob(os.path.join(data_dir, "**/*.csv"), recursive=True)
    csv_files.extend(glob.glob(os.path.join(ex_data_dir, "**/*.csv"), recursive=True))
    for csv_path in csv_files:
        with open(csv_path, encoding="utf-8") as f:
            excludes.extend(row[0] for row in csv.reader(f) if row)

    # テキストファイルから除外リストを追加
    excludes_path = os.path.join(data_dir, "excludes.txt")
    if os.path.exists(excludes_path):
        with open(excludes_path, encoding="utf-8") as f:
            excludes.extend(f.read().splitlines())

    return set(excludes)


def find_tags_mapping(query, tags):
    for key, value in query.items():
        if key in tags:
            if isinstance(value, list):
                return [key], value
            elif isinstance(value, dict):
                sub_keys, sub_value = find_tags_mapping(value, tags)
                return [key] + sub_keys, sub_value
    return [], None


def process_dataset(dataset, excludes, query):
    extracted = {}

    for data in dataset:
        if "ja" not in data or data["ja"] in excludes:
            continue

        if "tags" in data:
            tags = data["tags"]
            keys, args = find_tags_mapping(query, tags)
            if keys and args:
                key_str = "+".join(keys)
                if key_str not in extracted:
                    extracted[key_str] = {"data": [], "args": args}
                extracted[key_str]["data"].append(data)

    return extracted


def write_to_csv(data_list, filepath, hinshi, comment="", data_dir=""):
    if not data_list:
        return

    os.makedirs(os.path.join(data_dir, os.path.dirname(filepath)), exist_ok=True)
    full_path = os.path.join(data_dir, filepath)

    print(f"新規追加 ({filepath}): {len(data_list)}")
    with open(full_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for data in data_list:
            word = data["ja"]
            hiragana = jaconv.kata2hira(data.get("pronunciationJa", "")) or (
                jaconv.kata2hira(word) if re.fullmatch("[\u30A0-\u30FF]+", word) else ""
            )
            row_comment = comment or data.get("notes", "")
            writer.writerow([word, hiragana, hinshi, row_comment])


def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../data/Genshin Impact")
    ex_data_dir = os.path.join(base_dir, "../data/Genshin Impact Extra")

    dataset = requests.get("https://dataset.genshin-dictionary.com/words.json").json()
    excludes = load_excludes(data_dir, ex_data_dir)

    query = {
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
        "domain": ["domain.csv", "名詞", "原神/秘境"],
        "item.csv": ["item/item.csv", "名詞", "原神/アイテム"],
        "drop": ["item/drop.csv", "名詞", "原神/アイテム/ドロップ"],
        "drop-boss": ["item/drop-boss.csv", "名詞", "原神/アイテム/ボスドロップ"],
        "gemstone": ["item/gemstone.csv", "名詞", "原神/アイテム/宝石"],
        "talent-material": [
            "item/talent-material.csv",
            "名詞",
            "原神/アイテム/天賦素材",
        ],
        "weapon-material": [
            "item/weapon-material.csv",
            "名詞",
            "原神/アイテム/武器素材",
        ],
        "food": ["food.csv", "名詞", "原神/食べ物"],
        "character-main": ["character/playable.csv", "人名", "原神/キャラクター"],
        "character-sub": ["character/npc.csv", "人名", "原神/キャラクター"],
        "sereniteapot": ["sereniteapot.csv", "名詞", "原神/塵歌壺"],
        "element": ["element.csv", "名詞"],
        "artifact-set": ["artifact/set.csv", "名詞", "原神/聖遺物"],
        "artifact-piece": ["artifact/piece.csv", "名詞"],
        "living-being": ["living-being.csv", "名詞", "原神/生物"],
        "enemy": ["enemy/enemy.csv", "名詞", "原神/敵"],
        "boss": ["enemy/boss.csv", "名詞", "原神/ボス"],
    }

    extracted_data = process_dataset(dataset, excludes, query)

    for key, value in extracted_data.items():
        write_to_csv(value["data"], *value["args"], data_dir=data_dir)


if __name__ == "__main__":
    main()
