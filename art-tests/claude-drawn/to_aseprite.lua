-- Turns a Pixelfolio character sheet (4 rows x 3 columns of 64 px frames) into an .aseprite file:
-- 12 frames, tags down/left/right/up, indexed in ENDESGA 32.
-- aseprite -b --script-param in=visitor.png --script-param pal=../pixellab/e32.hex \
--   --script-param out=visitor.aseprite --script to_aseprite.lua
local p = app.params
local sheet = Image{ fromFile = p["in"] }
local spr = Sprite(64, 64)
local i = 0
for row, name in ipairs{ "down", "left", "right", "up" } do
  for col = 0, 2 do
    i = i + 1
    if i > 1 then spr:newEmptyFrame() end
    spr:newCel(spr.layers[1], i, Image(sheet, Rectangle(col * 64, (row - 1) * 64, 64, 64)))
    spr.frames[i].duration = 0.15
  end
  spr:newTag(i - 2, i).name = name
end
spr:setPalette(Palette{ fromFile = p["pal"] })
app.command.ChangePixelFormat{ format = "indexed", dithering = "none" }
spr:saveAs(p["out"])
