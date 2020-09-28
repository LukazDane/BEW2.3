"""
[Day 7] Assignment: Steganography
    - Turn in on Gradescope (https://make.sc/bew2.3-gradescope)
    - Lesson Plan: https://make-school-courses.github.io/BEW-2.3-Web-Security/#/Lessons/Steganography

Deliverables:
    1. All TODOs in this file.
    2. Decoded sample image with secret text revealed
    3. Your own image encoded with hidden secret text!
"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(path_to_png, decoded_name):
    """
    TODO: Add docstring and complete implementation.
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    for i in range(x_size):
        for j in range(y_size):
            r = red_channel.getpixel((i, j))
            if r | 1 == r:
                decoded_image.putpixel((i, j), (0, 0, 0))
            else:
                decoded_image.putpixel((i, j), (255, 255, 255))

    decoded_image.save("images/{}.png".format(decoded_name))


def write_text(text, img_size):
    font_path = "~/Library/Fonts/Roboto-Regular.ttf"

    image = Image.new("RGB", img_size)
    draw = ImageDraw.Draw(image)
    txt = text
    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.85

    font = ImageFont.truetype(font_path, fontsize)
    while font.getsize(txt)[0] < img_fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font_path, fontsize)

    draw.text((25, 25), txt, font=font)  # put the text on the image

    return image


def encode_image(file_location, text, encoded_name):
    image = Image.open(file_location)
    image = image.convert('RGB')

    red_channel, green_channel, blue_channel = image.split()

    x_size = image.size[0]
    y_size = image.size[1]

    img_txt = write_text(text, image.size)
    bw_encode = img_txt.convert('1')

    encoded_image = Image.new("RGB", image.size)
    pixels = encoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            pass
            red_channel_pix = bin(red_channel.getpixel((i, j)))
            tencode_pix = bin(bw_encode.getpixel((i, j)))

            if tencode_pix[-1] == '1':
                red_channel_pix = red_channel_pix[:-1] + '1'
            else:
                red_channel_pix = red_channel_pix[:-1] + '0'
            pixels[i, j] = (int(red_channel_pix, 2), green_channel.getpixel(
                (i, j)), blue_channel.getpixel((i, j)))

    encoded_image.save("images/{}.png".format(encoded_name))


if __name__ == "__main__":
    encode_image("images/snail.png",
                 "Talkin to strangers online was the best decision I ever made. Reality is lemons, and this internet's my lemonade!", "yungGemmy")

    decode_image("images/yungGemmy.png", "decoded_yungGemmy")
