import csv
import re
from random import shuffle

REPETITIONS = 10
FIELDS = [
    "name",
    "manaCost",
    "type",
    "text",
    "power",
    "toughness",
    "loyalty",
]
INPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards.csv"
OUTPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards_encoded.csv"


# https://docs.python.org/3/library/re.html#re.sub
def integer_to_carets(matchobj):
    return "^" * int(matchobj.group(0))


def not_invalid(card):
    return card["type"] != "Vanguard" and card["name"] != "Gleemax"


card_dict = {}

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for card in r:
        # Only parse card once per card name.
        if card["name"] not in card_dict and not_invalid(card):
            card_dict[card["name"]] = {k: v for k, v in card.items() if k in FIELDS}


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text"])
    for card in card_dict.values():
        card["text"] = card["text"].replace(card["name"], "~")
        for _ in range(REPETITIONS):
            shuffle(FIELDS)
            card_enc = "".join([f"<|{k}|>{card[k]}" for k in FIELDS])
            card_enc = re.sub(r"\d+", integer_to_carets, card_enc)
            w.writerow([card_enc.replace("[", "").replace("]", "")])
