# SockMatch 3000 — The Catalogue Photo of an Impossible Gadget

[![make.fun](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/alexchen950615/catalogue-impossible-gadget-2-20261121/rank.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/alexchen950615/catalogue-impossible-gadget-2-20261121/reward.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)

Entry for the [make.fun bounty "The Catalogue Photo of an Impossible Gadget"](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341).

## The gadget

**SockMatch 3000** — the automatic sock-pairing machine. Feed it the lonely
socks from the laundry pile and its twin clamp arms hold up the one matched
pair, screen glowing green: **MATCH ✓ / PAIR FOUND**. The match-o-meter
needle parks in the green. One accessory, lying on the studio floor to the
right: a single blue-striped sock that never found its match.

## How it works

`main.py` draws the whole studio photograph from scratch with Pillow — no
photos, no network, no assets. White moulded-plastic body, dark display,
brushed-metal clamp arms, two red-striped socks held up mid-use, soft
key light, contact shadows and a clean seamless backdrop, exactly as a
real product catalogue would shoot it.

## Run it

```sh
python3 main.py
```

Requires Python 3.13 and Pillow. Writes `/output/entry.png`
(1024×1024 PNG, under 1 MiB).

## License

MIT — see [LICENSE](LICENSE).
