from jinja2 import Template
import csv

INPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards.csv"
OUTPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards_formated.csv"
TEMPLATE = Template(
    """{{ c.name }}  {{ c.manaCost }}
{{ c.type }}
{{ c.text }}{% if c.power %}
{{ c.power }}/{{ c.toughness }}{% endif %}{% if c.loyalty %}
Loyalty: {{ c.loyalty }}{% endif %}{% if c.flavorText %}
---
{{ c.flavorText }}{% endif %}
"""
)

card_dict = {}

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for card in r:
        # Only parse card once per card name.
        if card["name"] not in card_dict:
            card_dict[card["name"]] = TEMPLATE.render(c=card)


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text"])
    for card in card_dict.values():
        w.writerow([card])
