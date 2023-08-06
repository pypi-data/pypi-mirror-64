import sys

snail = "\U0001F40C"
koala = "\U0001F428"
turtle = "\U0001F422"
crocodile = "\U0001F40A"
octopus = "\U0001F419"
fox = "\U0001F98A"
shark = "\U0001F988"
horse = "\U0001F984"
trex = "\U0001F996"
eagle = "\U0001F985"

keyboard = "\U00002328"


def speedmoji(speed):
    if (sys.version_info < (3, 0)):
        return ""
    if speed <= 10:
        return snail
    if speed <= 20:
        return koala
    if speed <= 30:
        return turtle
    if speed <= 40:
        return crocodile
    if speed <= 50:
        return octopus
    if speed <= 60:
        return fox
    if speed <= 70:
        return shark
    if speed <= 80:
        return horse
    if speed <= 90:
        return trex
    if speed > 90:
        return eagle


def keymoji():
    if (sys.version_info > (3, 0)):
        return keyboard
    return ""
