from PIL import ImageFont, ImageDraw, Image


def createImageWithText(imgLength, txt: str):
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

    trashImage = Image.new("RGB", (1, 1))
    trashDraw = ImageDraw.Draw(trashImage)

    bbox = trashDraw.multiline_textbbox((0, 0), text=txt, font=font)

    print(bbox)

    image = Image.new(mode="RGBA", size=(bbox[2], bbox[3]), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), txt, (255, 255, 255), font=font)  # put the text on the image

    image.save(txt + "_" + str(imgLength) + "*" + str(image.size[1]) + ".png")
    image.show()


if __name__ == "__main__":
    txt = "beegText"
    createImageWithText(1000, txt)
    createImageWithText(100, txt)
    txt = "Very Very \n beeg Text"
    createImageWithText(1000, txt)
