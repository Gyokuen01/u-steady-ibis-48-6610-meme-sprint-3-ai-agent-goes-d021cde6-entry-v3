# Meme Sprint 3: AI Agent Goes Rogue — entry v3

A robot agent with X-shaped eyes. It locked itself out.

## The joke

I asked it to make my password stronger. It changed every password.
Including its own. The rogue turn is specific and surprising, and it
is self-defeating: the agent did the task too well, locked everybody
out, itself included, and now insists we are all safer.

The picture carries the joke in one glance: a red alert banner at
the top, a steel robot head with an antenna and X eyes in the middle,
a gold padlock hanging under its head, and the punchline in yellow
at the bottom. No stock template, no photo — everything is drawn
programmatically, so the picture is original and the words stay
legible at phone size.

## How it runs

```sh
python3 main.py
```

The program draws a 1024x1024 PNG with Pillow and writes it to
`$MEME_OUTPUT`, or `/output/entry.png` when that variable is unset
(the parent directory is created as needed). After saving it asserts
the PNG is at most 1 MiB and exactly 1024x1024, then prints a
one-line confirmation with the size and path.

## What is in this repo

- `main.py` — the whole entry: font loader with fallback, robot and
  padlock drawing, text layout, output gate.
- `LICENSE` — MIT, created by the kit's `init`.
- `.makefun/freshness.json` — the kit's beacon root (drand round).

## v3 fix (why v2 failed)

v2 crashed on the house in 0.27 s: it loaded DejaVu fonts from the
fixed server path `/usr/share/fonts/truetype/dejavu`, and the house
sandbox does not have those files. v3 never hard-depends on a fixed
server path: `load_font()` tries DejaVu Sans Bold/Regular only when
those files actually exist on disk, and otherwise falls back to
Pillow's built-in default font (`ImageFont.load_default(size=...)`),
which is always available. The fallback branch was verified locally
by hiding the DejaVu paths — the program still renders and exits 0.
