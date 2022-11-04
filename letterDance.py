from math import pi, sin
from pathlib import Path

import fontParts.world as fp
from drawBot import _drawBotDrawingTool as db
from mutatorMath.objects.location import Location
from mutatorMath.objects.mutator import buildMutator

# Constants
BLACK = 0, 0, 0
WHITE = 1, 1, 1

# Functions
def drawGlyph(glyph):
    glyphPath = db.BezierPath(glyphSet=glyph.layer)
    glyph.draw(glyphPath)
    db.drawPath(glyphPath)


### Variables
canvas = 800, 800
fps = 24
seconds = 6
frames = seconds * fps if seconds > 0 else 1

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

ampX = 1000 * 0.6
ampY = 1000 * 0.6
angFreqX = 2
angPhaseX = pi / 2
angFreqY = 1
angPhaseY = pi / 3

if __name__ == "__main__":

    mutators = {}
    for eachGlyphName in names:
        locations = []
        for name, location in fontToLocation.items():
            font = fp.OpenFont(fontsFolder / name)
            locations.append((location, font[eachGlyphName]))
        status, mutator = buildMutator(locations)
        mutators[eachGlyphName] = mutator

    scalingFactor = bodySize / fp.OpenFont(fontsFolder / "x0_y0.ufo").info.unitsPerEm  # type: ignore
    db.newDrawing()
    for eachFrame in range(frames):

        db.newPage(800, 800)
        db.frameDuration(1 / fps)
        db.fill(*BLACK)
        db.rect(0, 0, db.width(), db.height())

        db.scale(scalingFactor)
        db.translate(*offset)

        t = eachFrame * pi * 2 / frames
        x = db.width() / 2 + ampX * sin(angFreqX * t + angPhaseX)
        y = db.height() / 2 + ampY * sin(angFreqY * t + angPhaseY)

        db.fill(*WHITE)
        for eachGlyphName in names:
            instance = mutators[eachGlyphName].makeInstance(Location(x=x, y=y))
            drawGlyph(instance)
            db.translate(instance.width, 0)

    suffix = "pdf" if seconds == 0 else "mp4"
    db.saveImage(f"letterDance_2.{suffix}")
    db.endDrawing()
