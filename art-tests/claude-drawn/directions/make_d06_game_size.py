# Direction 6 at the size it would have in the game: the 352x240 room on the 640x360 canvas, shown at 2x.
# Seen at full width on a phone, this is how large the detail would be. Run make_d06_lived_in_clutter.py first.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d06_game_size.py
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
for name in ('d06-lived-in-clutter', 'd06-lived-in-clutter-evening'):
    room = Image.open(os.path.join(HERE, name + '-native.png')).convert('RGB')
    frame = Image.new('RGB', (640, 360), room.getpixel((0, 0)))
    frame.paste(room, ((640 - room.width) // 2, (360 - room.height) // 2))
    frame.resize((1280, 720), Image.NEAREST).save(os.path.join(HERE, name + '-game-size.png'))
