from telebot import types
from dictionary import dictionary

def mainmenu():
    '''
    Returns a keyboard with menu navigation buttons
    '''

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item1 = types.KeyboardButton(dictionary["pass_gen"])
    item2 = types.KeyboardButton(dictionary["url_short"])
    item3 = types.KeyboardButton(dictionary["dice"])
    item4 = types.KeyboardButton(dictionary["qrcode_gen"])
    item5 = types.KeyboardButton(dictionary["qrcode_read"])
    item6 = types.KeyboardButton(dictionary["help"])

    markup.add(item1, item2, item3, item4, item5, item6)

    return markup


def back_button():
    '''
    Returns the keyboard with a back button to the menu
    '''

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item1 = types.KeyboardButton(dictionary["back_button"])

    markup.add(item1)

    return markup


def yes_no_buttnons():
    '''
    Returns a keyboard with buttons to select between Yes, No or Back
    '''

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item1 = types.KeyboardButton(dictionary["yes_button"])
    item2 = types.KeyboardButton(dictionary["no_button"])
    item3 = types.KeyboardButton(dictionary["back_button"])

    markup.add(item1, item2, item3)

    return markup
