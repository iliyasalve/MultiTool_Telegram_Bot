import telebot
from config import token

import re
import io 
import os 

from dictionary import dictionary
from keyboards import mainmenu, back_button, yes_no_buttnons

from functions.password_generation import generate_password
from functions.url_shortener import url_shortener
from functions.dice_roll import dice_roll
from functions.qrcode_generation import qrcode_generation
from functions.qrcode_reader import read_qr_code

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Welcome, {message.from_user.first_name}!\n" +
                     "Use the buttons below to select the function you are interested in.", 
                     reply_markup = mainmenu())


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':

        if message.text == dictionary["pass_gen"]:
            msg = bot.send_message(message.chat.id, "Enter the desired password length: ", reply_markup = back_button())
            bot.register_next_step_handler(msg, password_length)

        if message.text == dictionary["url_short"]:
            msg = bot.send_message(message.chat.id, "Enter the link you want to shorten: ", reply_markup = back_button())
            bot.register_next_step_handler(msg, url_short)

        if message.text == dictionary["dice"]:
            msg = bot.send_message(message.chat.id, "Specify the number of dice you want to roll: ", reply_markup = back_button())
            bot.register_next_step_handler(msg, dice_game)
        
        if message.text == dictionary["qrcode_gen"]:
            msg = bot.send_message(message.chat.id, "Enter text or link to generate QR code: ", reply_markup = back_button())
            bot.register_next_step_handler(msg, qrcode_gen)
        
        if message.text == dictionary["qrcode_read"]:
            msg = bot.send_message(message.chat.id, "Send an image to decrypt the QR code: ", reply_markup = back_button())
            bot.register_next_step_handler(msg, qrcode_read)

        if message.text == dictionary["back_button"]:
            bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())

        if  message.text == dictionary["help"]:
            msg = bot.send_message(message.chat.id, f"Here's what this bot can do:\n\n" +
                                   f"-> {dictionary["pass_gen"]}: Generates a password of user-specified length\n" +
                                   f"-> {dictionary["url_short"]}: Shortens a link\n" +
                                   f"-> {dictionary["dice"]}: Toss the dice (the number of dice is determined by the user)\n" +
                                   f"-> {dictionary["qrcode_gen"]}: Generate QR code using user-entered text\n" +
                                   f"-> {dictionary["qrcode_read"]}: Decipher the QR code using a picture sent by the user\n", 
                                   reply_markup = back_button())


def password_length(message):
    length = message.text

    if length.isdigit():
        length = int(length)

        msg = bot.send_message(message.chat.id, "Should you use punctuation characters in your password? (Yes/No) : ", reply_markup = yes_no_buttnons())
        bot.register_next_step_handler(msg, password, length)

    elif length == dictionary["back_button"]:
        bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())

    else:
        msg = bot.send_message(message.chat.id, "You must enter numbers only. Try again", reply_markup = back_button())
        bot.register_next_step_handler(msg, password_length)

def password(message, length):
    is_punctuation = message.text

    if is_punctuation == "Yes" or is_punctuation == "No":
        generated_password = generate_password(length, is_punctuation)
        bot.send_message(message.chat.id, "Your new password:")
        bot.send_message(message.chat.id, generated_password, reply_markup = back_button())
    
    elif is_punctuation == dictionary["back_button"]:
        bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())

    else:
        msg = bot.send_message(message.chat.id, f"You entered an incorrect value, you must enter either Yes or No. Try again", reply_markup = yes_no_buttnons())
        bot.register_next_step_handler(msg, password, length)


def url_short(message):
    url = message.text

    if url != dictionary["back_button"]:
        
        is_url = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)

        if is_url:
            new_url = url_shortener(url)
            bot.send_message(message.chat.id, "Your short link:")
            bot.send_message(message.chat.id, new_url, reply_markup = back_button())

        else:
            bot.send_message(message.chat.id, "You didn't send a link. Make sure the link starts with http:// or https://", reply_markup = back_button())

    else:
        bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())


def dice_game(message):
    dice_number = message.text

    if dice_number.isdigit():
        diсe_result = dice_roll(int(dice_number))

        bot.send_message(message.chat.id, f"Result of rolled dice: {diсe_result}", reply_markup = back_button())

    elif dice_number == dictionary["back_button"]:
        bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())

    else:
        msg = bot.send_message(message.chat.id, "You must enter numbers only. Try again", reply_markup = back_button())
        bot.register_next_step_handler(msg, dice_game)


def qrcode_gen(message):
    input = message.text

    if input != dictionary["back_button"]:

        qr_code = qrcode_generation(input)

        # Save an image to the clipboard
        img_bytes = io.BytesIO()
        img_bytes.name = "QRCode.png"
        qr_code.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        bot.send_message(message.chat.id, "Your QR code:")
        bot.send_photo(message.chat.id,img_bytes, reply_markup = back_button())
    
    else:
        bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())


def qrcode_read(message):
    
    if message.content_type != "photo":

        if message.text == dictionary["back_button"]:
            bot.send_message(message.chat.id, dictionary["back_message"], reply_markup = mainmenu())
        
        else:
            msg = bot.send_message(message.chat.id, "You must send a photo only. Try again", reply_markup = back_button())
            bot.register_next_step_handler(msg, qrcode_read)

    else:
        photo = bot.get_file(message.photo[-1].file_id )
        downloaded_photo = bot.download_file(photo.file_path)

        path_name = "./source/tmp/"+str(message.from_user.id)+".png"

        with open(path_name, 'wb') as tmp_file:
            tmp_file.write(downloaded_photo)

        result = read_qr_code(path_name)
        
        if result == "-1":
            msg = bot.send_message(message.chat.id, "There is no QR code on the image. Try again", reply_markup = back_button())
            bot.register_next_step_handler(msg, qrcode_read)
        else:
            bot.send_message(message.chat.id, "Result from QR code:")
            bot.send_message(message.chat.id, result, reply_markup = back_button())

        os.remove(path_name)


bot.polling()