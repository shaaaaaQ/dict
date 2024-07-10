import requests
import os
import csv

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "../data/Genshin Impact")
dataset = requests.get("https://dataset.genshin-dictionary.com/words.json").json()

# weapon
with open(os.path.join(data_dir, "weapon.csv"), "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    csv_data = list(reader)
    print(csv_data)
    for data in dataset:
        if "tags" in data and "weapon" in data["tags"]:
            word = data["ja"]
            kana = data["pronunciationJa"] if "pronunciationJa" in data else ""
            hinshi = "名詞"
            comment = "原神/武器"

            if not list(filter(lambda row: row[0] == word, csv_data)):
                print(word, " nai")
                csv_data.append([word, kana, hinshi, comment])
    with open(os.path.join(data_dir, "weapon.csv"), "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
