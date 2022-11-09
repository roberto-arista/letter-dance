from math import pi, sin
from pathlib import Path

import fontParts.world as fp
from drawBot import _drawBotDrawingTool as db
from mutatorMath.objects.location import Location
from mutatorMath.objects.mutator import buildMutator

# Colors
BACKGROUND = 0 / 255, 0 / 255, 0 / 255
DESIGN_SPACE_LENGTH = 1000

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
colorToLocation = {
    (114 / 255, 196 / 255, 212 / 255): Location(x=0, y=0),
    (194 / 255, 101 / 255, 165 / 255): Location(x=1000, y=0),
    (234 / 255, 158 / 255, 66 / 255): Location(x=0, y=1000),
    (235 / 255, 219 / 255, 91 / 255): Location(x=1000, y=1000),
}

offset = 250, 1000  # upms
upm = 1000
lag = 20
is3D = False

ampX = 0.8  # keep it between 0 and 1
ampY = 0.8
if is3D:
    ampZ = 0.8

angFreqX = 2
angPhaseX = pi / 2
angFreqY = 1
angPhaseY = pi / 3
if is3D:
    angFreqZ = 2
    angPhaseZ = pi / 4

if __name__ == "__main__":
    frames = seconds * fps if seconds > 0 else 1
    ampX = DESIGN_SPACE_LENGTH / 2 * ampX
    ampY = DESIGN_SPACE_LENGTH / 2 * ampY
    if is3D:
        ampZ = DESIGN_SPACE_LENGTH / 2 * ampZ

    glyphMutators = {}
    for eachGlyphName in names:
        locations = []
        for name, location in fontToLocation.items():
            font = fp.OpenFont(fontsFolder / name)
            locations.append((location, font[eachGlyphName]))
        status, mutator = buildMutator(locations)
        glyphMutators[eachGlyphName] = mutator

    channelMutators = {}
    for index, channel in enumerate("rgb"):
        locations = []
        for color, location in colorToLocation.items():
            locations.append((location, color[index]))
        status, mutator = buildMutator(locations)
        channelMutators[channel] = mutator

    scalingFactor = bodySize / upm
    db.newDrawing()
    for eachFrame in range(frames):

        db.newPage(*canvas)
        db.frameDuration(1 / fps)
        db.fill(*BACKGROUND)
        db.rect(0, 0, db.width(), db.height())

        db.scale(scalingFactor)  # type: ignore
        db.translate(*offset)

        for indexName, eachGlyphName in enumerate(names):
            t = (eachFrame + indexName * lag) % frames * pi * 2 / frames
            x = DESIGN_SPACE_LENGTH / 2 + ampX * sin(angFreqX * t + angPhaseX)
            y = DESIGN_SPACE_LENGTH / 2 + ampY * sin(angFreqY * t + angPhaseY)
            loc = Location(x=x, y=y)

            clr = [channelMutators[c].makeInstance(loc) for c in "rgb"]
            db.fill(*clr)

            if is3D:
                z = DESIGN_SPACE_LENGTH / 2 + ampZ * sin(angFreqZ * t + angPhaseZ)
                loc = Location(x=x, y=y, z=z)

            instance = glyphMutators[eachGlyphName].makeInstance(loc)
            drawGlyph(instance)
            db.translate(instance.width, 0)

    suffix = "pdf" if seconds == 0 else "mp4"
    db.saveImage(f"letterDance.{suffix}")
    db.endDrawing()
