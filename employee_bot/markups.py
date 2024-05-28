from telebot import types


def regions_markup(regions):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(regions)):
        markup.add(types.KeyboardButton(regions[i]))
    return markup


def cities_markup(cities):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(cities)):
        markup.add(types.KeyboardButton(cities[i]))
    return markup


def workplaces_markup(workplaces):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(workplaces)):
        markup.add(types.KeyboardButton(workplaces[i]))
    return markup


def yesno_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Так")
    item2 = types.KeyboardButton("Ні")
    markup.add(item1, item2)
    return markup


def services_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Покупка")
    item2 = types.KeyboardButton("Покупка(франшиза)")
    item3 = types.KeyboardButton("Повернення")
    item4 = types.KeyboardButton("Ремонт")
    markup.add(item1, item2, item3, item4)
    return markup


def payment_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Готівкою")
    item2 = types.KeyboardButton("Карткою")
    markup.add(item1, item2)
    return markup


def nomeclature_markup(nomenclatures):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for nomenclature in nomenclatures:
        markup.add(types.KeyboardButton(f"{nomenclature['id']}. {nomenclature['name']}"))
    return markup
