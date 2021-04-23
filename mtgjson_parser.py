from jinja2 import Template
import csv

INPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards.csv"
OUTPUT_PATH = "/Users/maxwoolf/Downloads/AllPrintingsCSVFiles/cards_formatted.csv"
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

with open(INPUT_PATH, "r", encoding="utf-8") as f1:
    r = csv.DictReader(f1)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f2:
        w = csv.writer(f2)
        w.writerow(["text"])
        for row in r:
            w.writerow([TEMPLATE.render(c=row)])
