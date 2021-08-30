from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
import numpy as np
import telebot
import os


bot = telebot.TeleBot("8805553535:AQGpsQeeLLZ-uyO1f-Jh_rTUsixkKgcy8Lw",)

try:
    os.mkdir("./images")
except Exception as e:
    pass

@bot.message_handler(commands=['start', 'help']) # Если нажали /start
def start(message):
    bot.send_message(message.chat.id, "Color picker:\n1. Send me original image\n2. Edit image using built-in telegram draw tool. Make a little circle. Color must be different than background.")
    os.mkdir(str("./images/" + str(message.chat.id)))




@bot.message_handler(content_types=['photo',])
def get_file1(message,):

        if os.path.isdir("./images/" + str(message.chat.id)) == False:
            os.mkdir(str("./images/" + str(message.chat.id)))
        file_info = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)

        with open(f"./images/{message.chat.id}/1.jpg", 'wb') as new_file:
            new_file.write(file)

        msg = bot.send_message(message.chat.id, "Now pick the color")
        bot.register_next_step_handler(msg, get_file2)

def get_file2(message,):

    if os.path.isdir("./images/" + str(message.chat.id)) == False:
        os.mkdir(str("./images/" + str(message.chat.id)))
    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)

    with open(f"./images/{message.chat.id}/2.jpg", 'wb') as new_file:
        new_file.write(file)
    bot.send_message(message.chat.id, "Doing magic...")


    img_a = Image.open(f"./images/{message.chat.id}/1.jpg")
    img_b = Image.open(f"./images/{message.chat.id}/2.jpg")
    img_diff = Image.new("RGBA", img_a.size)

    try:
        pixelmatch(img_a, img_b, img_diff,)
    except ValueError:
        bot.send_message(message.chat.id, "Error:\nDifferent images sizes. Don't resize image.")

    grayscale = img_diff.convert('L')
    pixels = np.asarray(grayscale)
    coords = np.column_stack(np.where(pixels < 90))

    try:
        x = coords[len(coords)//2][0]
        y = coords[len(coords) // 2][-1]
        pixels = img_a.load()

        preview = Image.new("RGB", (250, 250), (pixels[y,x][0], pixels[y,x][1], pixels[y,x][2]))


        bot.send_photo(message.chat.id, preview, f"Color detected:\nRGB:  `{pixels[y,x][0]} {pixels[y,x][1]} {pixels[y,x][2]}`", parse_mode="Markdown")
    except IndexError:
        bot.send_message(message.chat.id, 'Error!\nThere is no difference between images. Try to draw a bigger circle and remember that it must be different than background.')

    os.remove(f"./images/{message.chat.id}/1.jpg")
    os.remove(f"./images/{message.chat.id}/2.jpg")


bot.polling()
