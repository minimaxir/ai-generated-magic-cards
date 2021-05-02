# ai-generated-magic-cards

Tools for encoding Magic: The Gathering cards into a form suitable for AI text generation with tools such as [aitextgen](https://github.com/minimaxir/aitextgen).

In contrast to [mtgencode](https://github.com/billzorn/mtgencode), which encodes Magic cards intended for a character-based RNN training method, this form of encoding is much lighter since byte-pair encoding and Transformers can learn a model so well such that mtgencode is overkill. Additionally, this level of encoding can extend to future Magic sets, while many new mechanics introduced since mtgencode stopped development in 2017 make it dated.

This was used to create the dataset to train the GPT-2 model for [Create Your Own AI-Generated Magic: The Gathering Cards](https://colab.research.google.com/drive/1VOt090UzvltoBgMdUZmU5vwhi4X-6E_a?usp=sharing).

## Preparation

These scripts use the [AllPrintingsCSVFiles download](https://mtgjson.com/downloads/all-files/#allprintingscsvfiles) from [MTGJSON](https://mtgjson.com/). Download and unzip, then point the `INPUT_FILE` in the scripts to the contained `cards.csv`.

Additionally, you'll need to install `jinja2` to run the scripts:

```sh
pip3 install jinja2
```

## mtgjson_parser.py

`mtgjson_encoder.py` is a lighter-templating that renders the cards in a style similar to that of [Scryfall](https://scryfall.com/). Although you can train AI on it and the output will be more interpretable without decoding, it's less flexible.

Examples of cards with this encoding:

```
Ballista Squad {3}{W}
Creature — Human Rebel
{X}{W}, {T}: Ballista Squad deals X damage to target attacking or blocking creature.
2/2
---
The perfect antidote for a tightly packed formation.
```

```
Agonizing Memories {2}{B}{B}
Sorcery
Look at target player's hand and choose two cards from it. Put them on top of that player's library in any order.
---
In the aftermath of war, when the slaying is long done, the greatest miseries come home to roost.
```

```
Karn Liberated {7}
Legendary Planeswalker — Karn
+4: Target player exiles a card from their hand.
−3: Exile target permanent.
−14: Restart the game, leaving in exile all non-Aura permanent cards exiled with Karn Liberated. Then put those cards onto the battlefield under your control.
Loyalty: 6
```

## mtgencoder.py

`mtgjson_encoder.py` encodes Magic cards into a similar format as mtgencode, although only in two major ways:

1. Cards are encoded with the following sections/keys: `<|name|>`, `<|manaCost|>`, `<|type|>`, `<|text|>`, `<|power|>`, `<|toughness|>`, `<|loyalty|>`. These keys are randomized, allowing the cards to be generated in any order. All the encoded cards are repeated in a different order for `REPETITION` times (10 in the script); all repetitions are shuffled again to mitigate data leakage.
2. If the card name is present in the text; it is replaced with a `~`; this is mostly to prevent data leakage where the `<|text|>` appears before the `<|name|>`

Examples of encoded cards:

```
<|toughness|><|text|>Counter target spell unless its controller pays {X}.<|power|><|type|>Instant<|loyalty|><|manaCost|>{X}{U}<|name|>Clash of Wills
```

```
<|loyalty|><|text|>~ enters the battlefield tapped.
{T}: Add {C}.
{T}: Add {U} or {R}. ~ deals 1 damage to you.<|toughness|><|name|>Caldera Lake<|power|><|manaCost|><|type|>Land
```

```
<|loyalty|>5<|text|>+1: Scry 1, then draw a card.
−2: Return target creature to its owner's hand.
−8: You get an emblem with "Whenever an opponent casts their first spell each turn, counter that spell."<|name|>Jace, Unraveler of Secrets<|toughness|><|type|>Legendary Planeswalker — Jace<|manaCost|>{3}{U}{U}<|power|>
```

## The AI Model

The model itself takes advantage of efficient tokenization and `aitextgen`'s schema capabilities. The keys such as `<|name|>` are explicitly added tokens to the tokeniziation; therefore they get their own token_id and are faster to explicitly detect/generate without confounding. These added tokens are also `schema_tokens`, which when used with `generate(schema=True)`, returns a dictionary with each field as its own key, allowing it to be passed to a `jinja2` template for decoding without additional decoding.

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

## License

MIT
