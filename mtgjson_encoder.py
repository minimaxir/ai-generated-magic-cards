import csv
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


def not_invalid(card):
    return card["type"] != "Vanguard"


card_dict = {}

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for card in r:
        # Only parse card once per card name.
        if card["name"] not in card_dict and not_invalid(card):
            card_dict[card["name"]] = {k: v for k, v in card.items() if k in FIELDS}

enc_card_list = []

for card in card_dict.values():
    card["text"] = card["text"].replace(card["name"], "~")
    for _ in range(REPETITIONS):
        shuffle(FIELDS)
        card_enc = "".join([f"<|{k}|>{card[k]}" for k in FIELDS])
        enc_card_list.append(card_enc.replace("[", "").replace("]", ""))

shuffle(enc_card_list)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text"])
    for card in enc_card_list:
        w.writerow([card])
