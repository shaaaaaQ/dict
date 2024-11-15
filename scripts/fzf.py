from pyfzf.pyfzf import FzfPrompt
import glob
import os
import csv

fzf = FzfPrompt()
li = []
for csv_path in glob.glob(
    os.path.join(os.path.dirname(__file__), "../data/**/*.csv"), recursive=True
):
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if row:
                li.append(f"{row[0]}     {row[1]}")
fzf.prompt(li)
