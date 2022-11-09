from math import pi, sin
from pathlib import Path

import fontParts.world as fp
from drawBot import _drawBotDrawingTool as db
from mutatorMath.objects.location import Location
from mutatorMath.objects.mutator import buildMutator

# Colors
BACKGROUND = 0 / 255, 0 / 255, 0 / 255
TEXT = 255 / 255, 255 / 255, 255 / 255

# Functions
def drawGlyph(glyph):
    glyphPath = db.BezierPath(glyphSet=glyph.layer)
    glyph.draw(glyphPath)
    db.drawPath(glyphPath)


### Variables
canvas = 800, 800
fps = 24
seconds = 6

names = ["R", "a", "five"]
bodySize = 300  # pts

fontsFolder = Path("fonts")
fontToLocation = {
    "x0_y0.ufo": Location(x=0, y=0),
    "x1000_y0.ufo": Location(x=1000, y=0),
    "x0_y1000.ufo": Location(x=0, y=1000),
    "x1000_y1000.ufo": Location(x=1000, y=1000),
}

offset = 250, 1000  # upms
upm = 1000

ampX = 0.8  # keep it between 0 and 1
ampY = 0.8
angFreqX = 2
angPhaseX = pi / 2
angFreqY = 1
angPhaseY = pi / 3

if __name__ == "__main__":
    frames = seconds * fps if seconds > 0 else 1
    ampX = 1000 / 2 * ampX
    ampY = 1000 / 2 * ampY

    mutators = {}
    for eachGlyphName in names:
        locations = []
        for name, location in fontToLocation.items():
            font = fp.OpenFont(fontsFolder / name)
            locations.append((location, font[eachGlyphName]))
        status, mutator = buildMutator(locations)
        mutators[eachGlyphName] = mutator

    scalingFactor = bodySize / upm
    db.newDrawing()
    for eachFrame in range(frames):

        db.newPage(*canvas)
        db.frameDuration(1 / fps)
        db.fill(*BACKGROUND)
        db.rect(0, 0, db.width(), db.height())

        db.scale(scalingFactor)  # type: ignore
        db.translate(*offset)

        t = eachFrame * pi * 2 / frames
        x = db.width() / 2 + ampX * sin(angFreqX * t + angPhaseX)
        y = db.height() / 2 + ampY * sin(angFreqY * t + angPhaseY)

        db.fill(*TEXT)
        for eachGlyphName in names:
            instance = mutators[eachGlyphName].makeInstance(Location(x=x, y=y))
            drawGlyph(instance)
            db.translate(instance.width, 0)

    suffix = "pdf" if seconds == 0 else "mp4"
    db.saveImage(f"letterDance.{suffix}")
    db.endDrawing()
