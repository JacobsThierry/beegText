#!/usr/bin/python3
from PIL import ImageFont, ImageDraw, Image
import argparse


## Up margin is wrong : I fix it by checking the first row that hase a non-transparent pixel in it
def fixUpMargin(img: Image, draw: ImageDraw):
    upMargin = 0

    ok = False

    while not ok:
        for i in range(img.size[0]):
            print(img.getpixel((i, upMargin)))
            if (img.getpixel((i, upMargin))[3]) > 0:
                ok = True
        upMargin += 1

    return img.crop((0, upMargin, img.size[0], img.size[1]))


def createImageWithText(imgLength, txt: str, save):
    txt = txt.strip()
    fontsize = 1  # starting font size

    fontname = "whitney-semibold.otf"

    font = ImageFont.truetype(fontname, fontsize)

    while font.getlength(txt) < imgLength:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(fontname, fontsize)

    # de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(fontname, fontsize)

    print("final font size", fontsize)

    trashImage = Image.new("RGB", (imgLength, imgLength))
    trashDraw = ImageDraw.Draw(trashImage)

    bbox = trashDraw.multiline_textbbox((0, 0), text=txt, font=font)

    print(bbox)

    image = Image.new(mode="RGBA", size=(bbox[2], bbox[3]), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.text(
        (0, 0), txt, (255, 255, 255), font=font, spacing=0
    )  # put the text on the image

    image = fixUpMargin(image, draw)

    if save:
        image.save(txt + "_" + str(imgLength) + "*" + str(image.size[1]) + ".png")
    image.show(txt)


def test():
    txt = "beegText"
    createImageWithText(1000, txt)
    createImageWithText(100, txt)
    txt = "Very Very \n beeg Text"
    createImageWithText(1000, txt)


parser = argparse.ArgumentParser(prog="beegText")
parser.add_argument("txt", type=str)
parser.add_argument("--size", type=int)
parser.add_argument("--save", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    size = 1000

    if args.size:
        size = args.size

    createImageWithText(size, args.txt, args.save)
